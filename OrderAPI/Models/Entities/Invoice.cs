using System.ComponentModel.DataAnnotations;

namespace OrderAPI.Models.Entities
{
    public class Invoice
    {
        [Key]
        public Guid Id { get; set; }

        [Required]
        public Guid OrderId { get; set; }

        public required Order Order { get; set; }

        [Required]
        [MaxLength(50)]
        public required string InvoiceNumber { get; set; }

        public DateTime IssuedAt { get; set; }

        [Range(0.01, double.MaxValue)]
        public decimal TotalAmount { get; set; }
    }
}