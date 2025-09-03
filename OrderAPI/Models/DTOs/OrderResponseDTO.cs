namespace OrderAPI.Models.DTOs
{
    public class OrderResponseDTO
    {
        public Guid Id { get; set; }
        public DateTime CreatedAt { get; set; }
        public Guid CustomerId { get; set; }
        public OrderStatus Status { get; set; }
        public List<OrderItemDTO> Items { get; set; } = new();
    }

}