using Swashbuckle.AspNetCore.Annotations;

namespace OrderAPI.Models.DTOs
{
    public class OrderResponseDTO
    {
        [SwaggerSchema("Order's unique identifier", ReadOnly = true)]
        public Guid Id { get; set; }

        [SwaggerSchema("Timestamp when the order was created", ReadOnly = true)]
        public DateTime CreatedAt { get; set; }

        [SwaggerSchema("Customer's unique identifier", ReadOnly = true)]
        public Guid CustomerId { get; set; }

        [SwaggerSchema("Current status of the order", ReadOnly = true)]
        public OrderStatus Status { get; set; }

        [SwaggerSchema("List of items in the order", ReadOnly = true)]
        public List<OrderItemDTO> Items { get; set; } = new();

        [SwaggerSchema("Total amount for the order", ReadOnly = true)]
        public decimal TotalAmount { get; set; }
    }

}