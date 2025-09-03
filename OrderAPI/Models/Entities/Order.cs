using System.ComponentModel.DataAnnotations;

namespace OrderAPI.Models.Entities
{
    public class Order
    {
        [Key]
        public Guid Id { get; set; }

        [Required]
        public DateTime CreatedAt { get; set; }

        public DateTime? UpdatedAt { get; set; }

        public DateTime? DeletedAt { get; set; }

        [Required]
        public Guid CustomerId { get; set; }

        public Customer? Customer { get; set; }

        [Required]
        public ICollection<OrderItem> Items { get; set; } = new List<OrderItem>();

        public Payment? Payment { get; set; }

        public Invoice? Invoice { get; set; }

        [Required]
        public OrderStatus Status { get; set; }
    }
}