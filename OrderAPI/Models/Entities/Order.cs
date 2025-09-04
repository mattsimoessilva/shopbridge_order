using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;
using Swashbuckle.AspNetCore.Annotations;

namespace OrderAPI.Models.Entities
{
    public class Order
    {
        [Key]
        public Guid Id { get; set; }

        [Required]
        [JsonIgnore]
        public DateTime CreatedAt { get; set; }

        [JsonIgnore]
        public DateTime? UpdatedAt { get; set; }

        [JsonIgnore]
        public DateTime? DeletedAt { get; set; }

        [Required]
        public Guid CustomerId { get; set; }

        [Required]
        public ICollection<OrderItem> Items { get; set; } = new List<OrderItem>();

        [Required]
        public decimal TotalAmount { get; set; }

        [Required]
        public OrderStatus Status { get; set; }
    }
}