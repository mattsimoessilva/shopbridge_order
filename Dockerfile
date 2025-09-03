# Stage 1: Build the application
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src

# Copy project files and restore dependencies
COPY OrderAPI/*.csproj ./OrderAPI/
RUN dotnet restore ./OrderAPI/OrderAPI.csproj

# Copy the rest of the source code and build
COPY . .
WORKDIR /src/OrderAPI
RUN dotnet publish -c Release -o /app/publish

# Stage 2: Run the application using a minimal runtime image
FROM mcr.microsoft.com/dotnet/aspnet:6.0-alpine AS runtime
WORKDIR /app
COPY --from=build /app/publish .

# Expose the port your API listens on
EXPOSE 80

# Start the application
ENTRYPOINT ["dotnet", "OrderAPI.dll"]
