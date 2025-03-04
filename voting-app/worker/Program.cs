using System;
using System.Collections.Generic;
using System.Data.Common;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Newtonsoft.Json;
using Npgsql;
using OpenTelemetry;
using OpenTelemetry.Context.Propagation;
using OpenTelemetry.Trace;
using OpenTelemetry.Resources;
using OpenTelemetry.Exporter;
using StackExchange.Redis;
using OpenTelemetry.Extensions.Propagators;


namespace Worker
{
    public class Program
    {
        private static readonly string OtlpEndpoint =
            Environment.GetEnvironmentVariable("OTLP_ENDPOINT") ?? "http://otel-collector.default.svc.cluster.local:4317";

        public static int Main(string[] args)
        {
            // *** ADDED: Composite Propagator ***
            var propagator = new CompositeTextMapPropagator(new TextMapPropagator[]
            {
                new TraceContextPropagator(),
                new OpenTelemetry.Context.Propagation.B3Propagator()
            });

            Sdk.SetDefaultTextMapPropagator(propagator);


            using var tracerProvider = Sdk.CreateTracerProviderBuilder()
                .SetResourceBuilder(ResourceBuilder.CreateDefault().AddService("voting-app-worker")) // *** CHANGED: Unique service name
                .AddSource("WorkerService")
                .AddOtlpExporter(otlpOptions =>
                {
                    otlpOptions.Endpoint = new Uri(OtlpEndpoint);
                    otlpOptions.Protocol = OtlpExportProtocol.Grpc;
                })
                .Build();

            var activitySource = new ActivitySource("WorkerService");

            try
            {
                var pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                var redisConn = OpenRedisConnection("redis");
                var redis = redisConn.GetDatabase();

                var keepAliveCommand = pgsql.CreateCommand();
                keepAliveCommand.CommandText = "SELECT 1";

                // *** CHANGED: Include traceparent in anonymous type ***
                var definition = new { vote = "", voter_id = "", traceparent = "" };
                while (true)
                {
                    Thread.Sleep(100);
                    if (redisConn == null || !redisConn.IsConnected)
                    {
                        Console.WriteLine("Reconnecting Redis");
                        redisConn = OpenRedisConnection("redis");
                        redis = redisConn.GetDatabase();
                    }

                    string json = redis.ListLeftPopAsync("votes").Result;
                    if (json != null)
                    {
                        // *** CHANGED: Deserialize to include traceparent ***
                        var voteData = JsonConvert.DeserializeAnonymousType(json, definition);

                        // *** CHANGED: Correct context extraction ***
                        ActivityContext parentContext = ExtractActivityContext(voteData.traceparent);

                        // Start a new activity with the extracted trace context
                        using (var activity = activitySource.StartActivity("ProcessingVote", ActivityKind.Consumer, parentContext))
                        {
                            Console.WriteLine($"Processing vote for '{voteData.vote}' by '{voteData.voter_id}'");

                            if (!pgsql.State.Equals(System.Data.ConnectionState.Open))
                            {
                                Console.WriteLine("Reconnecting DB");
                                pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                            }
                            else
                            {
                                UpdateVote(pgsql, voteData.voter_id, voteData.vote);
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
                Console.Error.WriteLine(ex.ToString());
                return 1;
            }
        }

        // *** CHANGED: Correct context extraction ***
        private static ActivityContext ExtractActivityContext(string traceparent)
        {
            if (string.IsNullOrEmpty(traceparent))
            {
                return default;
            }

            var carrier = new Dictionary<string, string> { { "traceparent", traceparent } };
            var propagator = Propagators.DefaultTextMapPropagator; // Use the default
            PropagationContext parentContext = propagator.Extract(default, carrier, (c, key) =>
            {
                return c.TryGetValue(key, out var value) ? new[] { value } : Enumerable.Empty<string>();
            });

            return parentContext.ActivityContext;
        }


        private static NpgsqlConnection OpenDbConnection(string connectionString)
        {
            NpgsqlConnection connection;
            while (true)
            {
                try
                {
                    connection = new NpgsqlConnection(connectionString);
                    connection.Open();
                    break;
                }
                catch (SocketException)
                {
                    Console.Error.WriteLine("Waiting for db");
                    Thread.Sleep(1000);
                }
                catch (DbException)
                {
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

        private static ConnectionMultiplexer OpenRedisConnection(string hostname)
        {
            var ipAddress = GetIp(hostname);
            Console.WriteLine($"Found redis at {ipAddress}");

            while (true)
            {
                try
                {
                    Console.WriteLine("Connecting to redis");
                    return ConnectionMultiplexer.Connect(ipAddress);
                }
                catch (RedisConnectionException)
                {
                    Console.Error.WriteLine("Waiting for redis");
                    Thread.Sleep(1000);
                }
            }
        }

        private static string GetIp(string hostname)
            => Dns.GetHostEntryAsync(hostname)
                .Result
                .AddressList
                .First(a => a.AddressFamily == AddressFamily.InterNetwork)
                .ToString();

        private static void UpdateVote(NpgsqlConnection connection, string voterId, string vote)
        {
            using var activity = new ActivitySource("WorkerService").StartActivity("UpdateVote");
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