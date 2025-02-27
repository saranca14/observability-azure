using System;
using System.Data.Common;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Newtonsoft.Json;
using Npgsql;
using StackExchange.Redis;
using OpenTelemetry;
using OpenTelemetry.Trace;
using OpenTelemetry.Resources;

namespace Worker
{
    public class Program
    {
        private static TracerProvider tracerProvider;

        public static int Main(string[] args)
        {
            // Define OpenTelemetry Resource (similar to Python Voting App)
            var resource = ResourceBuilder.CreateDefault()
                .AddService(serviceName: "voting-app")  // Shared application name
                .AddAttributes(new[]
                {
                    new KeyValuePair<string, object>("service.instance.id", "worker-service"), // Unique per microservice
                    new KeyValuePair<string, object>("service.namespace", "voting-app"),
                    new KeyValuePair<string, object>("service.version", "1.0.0")
                });

            // Initialize OpenTelemetry
            tracerProvider = Sdk.CreateTracerProviderBuilder()
                .SetResourceBuilder(resource)
                .AddSource("WorkerApp")
                .AddOtlpExporter()  // Exports traces to OpenTelemetry Collector
                .AddConsoleExporter() // Debugging in console
                .Build();

            var tracer = TracerProvider.Default.GetTracer("WorkerApp");

            using (var activity = tracer.StartActiveSpan("WorkerStartup"))
            {
                try
                {
                    var pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;", tracer);
                    var redisConn = OpenRedisConnection("redis", tracer);
                    var redis = redisConn.GetDatabase();

                    var keepAliveCommand = pgsql.CreateCommand();
                    keepAliveCommand.CommandText = "SELECT 1";

                    var definition = new { vote = "", voter_id = "" };
                    while (true)
                    {
                        Thread.Sleep(100);

                        // Reconnect redis if down
                        if (redisConn == null || !redisConn.IsConnected)
                        {
                            activity.SetStatus(ActivityStatusCode.Error, "Redis connection lost");
                            Console.WriteLine("Reconnecting Redis");
                            redisConn = OpenRedisConnection("redis", tracer);
                            redis = redisConn.GetDatabase();
                        }

                        string json = redis.ListLeftPopAsync("votes").Result;
                        if (json != null)
                        {
                            using (var processVoteActivity = tracer.StartActiveSpan("ProcessingVote"))
                            {
                                var vote = JsonConvert.DeserializeAnonymousType(json, definition);
                                Console.WriteLine($"Processing vote for '{vote.vote}' by '{vote.voter_id}'");

                                // Reconnect DB if down
                                if (!pgsql.State.Equals(System.Data.ConnectionState.Open))
                                {
                                    Console.WriteLine("Reconnecting DB");
                                    pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;", tracer);
                                }
                                else
                                {
                                    UpdateVote(pgsql, vote.voter_id, vote.vote, tracer);
                                }
                            }
                        }
                        else
                        {
                            keepAliveCommand.ExecuteNonQuery();
                        }
                    }
                }
                catch (Exception ex)
                {
                    activity.SetStatus(ActivityStatusCode.Error, ex.Message);
                    Console.Error.WriteLine(ex.ToString());
                    return 1;
                }
            }
        }

        private static NpgsqlConnection OpenDbConnection(string connectionString, Tracer tracer)
        {
            NpgsqlConnection connection;

            using (var activity = tracer.StartActiveSpan("DBConnection"))
            {
                while (true)
                {
                    try
                    {
                        connection = new NpgsqlConnection(connectionString);
                        connection.Open();
                        break;
                    }
                    catch (Exception ex)
                    {
                        activity.SetStatus(ActivityStatusCode.Error, ex.Message);
                        Console.Error.WriteLine("Waiting for db");
                        Thread.Sleep(1000);
                    }
                }

                Console.Error.WriteLine("Connected to db");

                var command = connection.CreateCommand();
                command.CommandText = @"CREATE TABLE IF NOT EXISTS votes (
                                            id VARCHAR(255) NOT NULL UNIQUE,
                                            vote VARCHAR(255) NOT NULL
                                        )";
                command.ExecuteNonQuery();

                return connection;
            }
        }

        private static ConnectionMultiplexer OpenRedisConnection(string hostname, Tracer tracer)
        {
            var ipAddress = GetIp(hostname);
            Console.WriteLine($"Found redis at {ipAddress}");

            using (var activity = tracer.StartActiveSpan("RedisConnection"))
            {
                while (true)
                {
                    try
                    {
                        Console.Error.WriteLine("Connecting to redis");
                        return ConnectionMultiplexer.Connect(ipAddress);
                    }
                    catch (RedisConnectionException ex)
                    {
                        activity.SetStatus(ActivityStatusCode.Error, ex.Message);
                        Console.Error.WriteLine("Waiting for redis");
                        Thread.Sleep(1000);
                    }
                }
            }
        }

        private static string GetIp(string hostname)
            => Dns.GetHostEntryAsync(hostname)
                .Result
                .AddressList
                .First(a => a.AddressFamily == AddressFamily.InterNetwork)
                .ToString();

        private static void UpdateVote(NpgsqlConnection connection, string voterId, string vote, Tracer tracer)
        {
            using (var activity = tracer.StartActiveSpan("UpdateVote"))
            {
                var command = connection.CreateCommand();
                try
                {
                    command.CommandText = "INSERT INTO votes (id, vote) VALUES (@id, @vote)";
                    command.Parameters.AddWithValue("@id", voterId);
                    command.Parameters.AddWithValue("@vote", vote);
                    command.ExecuteNonQuery();
                }
                catch (DbException)
                {
                    command.CommandText = "UPDATE votes SET vote = @vote WHERE id = @id";
                    command.ExecuteNonQuery();
                }
                finally
                {
                    command.Dispose();
                }
            }
        }
    }
}
