using System.ComponentModel.DataAnnotations;

namespace OrderAPI.Models.Entities
{
    public class OrderItem
    {
        [Key]
        public Guid Id { get; set; }

        [Required]
        public Guid OrderId { get; set; }

        public Order? Order { get; set; }

        [Required]
        public Guid ProductId { get; set; }

        [Required]
        public required string ProductName { get; set; }

        [Range(0.01, double.MaxValue)]
        public int Quantity { get; set; }

        [Range(0.01, double.MaxValue)]
        public decimal UnitPrice { get; set; }

        public decimal TotalPrice => Quantity * UnitPrice;
    }
}