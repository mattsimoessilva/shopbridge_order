using System.ComponentModel.DataAnnotations;

namespace OrderAPI.Models.Entities
{
    public class Payment
    {
        [Key]
        public Guid Id { get; set; }

        [Required]
        public Guid OrderId;

        public Order? Order { get; set; }

        [Required]
        public PaymentMethod Method { get; set; }

        [Range(0.01, double.MaxValue)]
        public decimal Amount { get; set; }

        public DateTime PaidAt { get; set; }

        public bool IsConfirmed { get; set; }
    }
}