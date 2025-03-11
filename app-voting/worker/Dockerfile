# Base stage: Uses the official .NET SDK image
FROM --platform=${BUILDPLATFORM} mcr.microsoft.com/dotnet/sdk:7.0 AS base

# Add curl for healthcheck and debugging
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/local/app

# --- Development stage (Optional - comment out if not needed) ---
FROM base AS dev
RUN apt-get install -y nano
ENV DOTNET_ENV=Development
CMD ["dotnet", "watch", "run"]

# --- Production build stage ---
FROM base AS build
WORKDIR /usr/local/app

# 1. Copy ONLY the project file
COPY *.csproj .

# 2. Restore dependencies *WITHIN THE BUILD STAGE*
RUN dotnet restore -r linux-x64

# 3. NOW copy the rest of the source code
COPY . .

# 4. Clean (optional, but good practice)
RUN dotnet clean -c Release -r linux-x64

# 5. Publish (self-contained)
RUN dotnet publish -c Release -o /app --self-contained true -r linux-x64 --no-restore

# --- Final production stage ---
FROM mcr.microsoft.com/dotnet/runtime:7.0 AS final
WORKDIR /app
COPY --from=build /app .
ENV OTEL_SERVICE_NAME=voting-app-worker \
    OTEL_SERVICE_INSTANCE_ID=worker-service \
    OTEL_EXPORTER_OTLP_ENDPOINT=otel-collector.default.svc.cluster.local:4317 \
    OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
    OTEL_EXPORTER_OTLP_INSECURE=true \
    OTEL_LOG_LEVEL=debug
ENTRYPOINT ["./Worker"]