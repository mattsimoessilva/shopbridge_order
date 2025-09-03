using System.ComponentModel.DataAnnotations;

namespace OrderAPI.Models.Entities
{
    public class Customer
    {
        [Key]
        public Guid Id { get; set; }

        [Required]
        [MaxLength(100)]
        public required string FullName { get; set; }

        [Required]
        [EmailAddress]
        public required string Email { get; set; }

        [MaxLength(200)]
        public required string Address { get; set; }

        public ICollection<Order> Orders { get; set; } = new List<Order>();
    }
}
    