using Swashbuckle.AspNetCore.Annotations;

[SwaggerSchema("Enumeration representing the status of an order")]
public enum OrderStatus
{
    Pending,    // Order has been created but not yet processed
    Processing, // Order is currently being processed
    Shipped,    // Order has been shipped to the customer
    Delivered,  // Order has been delivered to the customer
    Cancelled   // Order has been cancelled
}