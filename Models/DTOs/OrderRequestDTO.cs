using Swashbuckle.AspNetCore.Annotations;

namespace OrderAPI.Models.DTOs
{
    public class OrderRequestDTO
    {
        [SwaggerSchema("Order's unique identifier", ReadOnly = true)]
        public Guid Id { get; set; }

        [SwaggerSchema("Timestamp when the order was created", ReadOnly = true)]
        public DateTime CreatedAt { get; set; }

        [SwaggerSchema("Timestamp when the order was last updated", ReadOnly = true)]
        public DateTime? UpdatedAt { get; set; }

        [SwaggerSchema("Timestamp when the order was deleted", ReadOnly = false)]
        public Guid CustomerId { get; set; }

        [SwaggerSchema("Current status of the order")]
        public OrderStatus Status { get; set; }

        [SwaggerSchema("List of items in the order")]
        public required List<OrderItemDTO> Items { get; set; }
    }
}