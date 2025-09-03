using System.ComponentModel.DataAnnotations;
using OrderAPI.Models.Entities;

namespace OrderAPI.Models.DTOs
{
    public class OrderDTO
    {
        public Guid Id { get; set; }

        [Required]
        public Guid CustomerId { get; set; }

        [Required]
        public List<OrderItemDTO> Items { get; set; } = new();

        [Required]
        public PaymentMethod PaymentMethod { get; set; }
    }
}