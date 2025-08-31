using System.ComponentModel.DataAnnotations;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

namespace OrderAPI.Models
{
    public class Order
    {
        [Key]
        public Guid Id { get; set; }

        [Required]
        public string CustomerName { get; set; } = string.Empty;

        public DateTime OrderDate { get; set; }

        [Range(0.01, double.MaxValue)]
        public decimal TotalAmount { get; set; }

        public List<ProductSnapshotDTO> Products { get; set; } = new();
    }
}