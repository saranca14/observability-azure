# Base stage: Uses the official .NET SDK image
FROM --platform=${BUILDPLATFORM} mcr.microsoft.com/dotnet/sdk:7.0 AS base

# Add curl for healthcheck and debugging (similar to Python image)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/local/app

# Copy the project file and restore dependencies
COPY *.csproj .
RUN dotnet restore

# Development stage
FROM base AS dev
RUN apt-get install -y nano
ENV DOTNET_ENV=Development
CMD ["dotnet", "watch", "run"]

# Production build stage
FROM base AS build
COPY . .
RUN dotnet publish -c Release -o /app --self-contained false --no-restore

# Final production stage
FROM mcr.microsoft.com/dotnet/runtime:7.0 AS final

# Set the working directory
WORKDIR /app

# Copy the built application
COPY --from=build /app .

# Expose port 80
EXPOSE 80

# Set OpenTelemetry environment variables
ENV OTEL_SERVICE_NAME=voting-app \
    OTEL_SERVICE_INSTANCE_ID=worker-service \
    OTEL_EXPORTER_OTLP_ENDPOINT=otel-collector.default.svc.cluster.local:4318 \
    OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
    OTEL_EXPORTER_OTLP_INSECURE=true \
    OTEL_LOG_LEVEL=debug

# Run the application
ENTRYPOINT ["dotnet", "Worker.dll"]
