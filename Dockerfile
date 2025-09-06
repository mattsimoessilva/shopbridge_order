# Stage 1: Build the application
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy project file and restore dependencies
COPY OrderAPI.csproj ./
RUN dotnet restore OrderAPI.csproj

# Copy the rest of the source code and build
COPY . .
RUN dotnet publish OrderAPI.csproj -c Release -o /app/publish

# Stage 2: Run the application using the runtime image
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /app

# Set ASP.NET Core to listen on port 80
ENV ASPNETCORE_URLS=http://+:80

# Copy published app from build stage
COPY --from=build /app/publish .

# Expose container port
EXPOSE 80

# Start the application
ENTRYPOINT ["dotnet", "OrderAPI.dll"]
