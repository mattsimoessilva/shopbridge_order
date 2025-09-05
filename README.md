# ShopBridge Order Service API

This repository implements the **Order Service** of the ShopBridge system, designed as part of the **MVP project for the Third Sprint of the Full Stack Development postgraduate program at CCEC - PUC-Rio**. The service provides a fully functional API for managing customer orders, enabling creation, retrieval, update, and deletion of order data in a microservices architecture.

Developed using **ASP.NET Core**, the service follows a layered architecture and adheres to industry best practices for RESTful APIs. It is designed to be integrated seamlessly into the system orchestration layer via Docker Compose.

---

## Repository Structure

```
orderapi/
│
├── Controllers/         # API controllers handling HTTP requests
├── Models/              # Domain models and DTOs
├── Services/            # Business logic and service layer
├── Repositories/        # Data persistence and database access
├── Migrations/          # EF Core database migrations
├── orderapi.csproj      # Project definition
└── README.md
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/mattsimoessilva/shopbridge_order.git
cd shopbridge_order
```

### 2. Configure environment variables
The service expects a `.env` file for database connection strings, ports, and other environment-specific settings. A template `.env.example` is provided.

### 3. Run the service
You can run the service locally via Docker Compose (from the orchestration repository) or directly using `dotnet run`:

```bash
dotnet run --project orderapi.csproj
```

The API will be available at **http://localhost:5001**.

---

## API Endpoints

### Orders

| Method | Endpoint           | Description                       |
|--------|------------------|-----------------------------------|
| POST   | `/api/Orders`     | Creates a new order               |
| GET    | `/api/Orders`     | Retrieves all orders              |
| GET    | `/api/Orders/{id}` | Retrieves a specific order by ID  |
| PUT    | `/api/Orders`     | Updates an existing order         |
| DELETE | `/api/Orders/{id}` | Deletes an order by ID            |

### Request & Response Schemas

- **OrderRequestDTO**: Used to create or update orders; includes `customerId`, `status`, and a list of `OrderItemDTO` items.  
- **OrderResponseDTO**: Returned for all queries; includes `id`, `createdAt`, `customerId`, `status`, `items`, and `totalAmount`.  
- **OrderItemDTO**: Represents an individual item in an order, including `productId`, `productName`, `quantity`, `unitPrice`, and `totalPrice`.  
- **OrderStatus**: Enumeration indicating order state (`0-4`).  
- **ProblemDetails**: Standardized error responses.

All endpoints follow REST conventions and return appropriate HTTP status codes (200, 201, 204, 400, 404, 500) with JSON payloads.

---

## Notes

- The service uses **SQLite** for local persistence and supports Docker volumes for data retention.  
- It is designed to operate as part of the **ShopBridge microservices system**, communicating with other services (ProductAPI, LogisticsAPI) via internal Docker networking.  
- All timestamps are in ISO 8601 format, and UUIDs are used for unique identification of orders, customers, and products.

---

## References

[1] S. Newman, *Building Microservices: Designing Fine-Grained Systems*. O’Reilly Media, 2015.  
[2] Microsoft, *ASP.NET Core Documentation*, 2025. Available: https://docs.microsoft.com/aspnet/core  
.