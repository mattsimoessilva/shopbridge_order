using System.ComponentModel.DataAnnotations;

namespace OrderAPI.Models.DTOs
{
    public class OrderItemDTO
    {
        [Required]
        public Guid ProductId { get; set; }

        [Required]
        public required string Name { get; set; }

        [Range(1, int.MaxValue)]
        public int Quantity { get; set; }

        [Range(0.01, double.MaxValue)]
        public decimal UnitPrice { get; set; }
    }
}