using Microsoft.EntityFrameworkCore;
using OrderAPI.Models.Entities;
using OrderAPI.Models.DTOs;
using System.Text.Json;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

namespace OrderAPI.Data
{
    public class OrderDbContext : DbContext
    {
        public OrderDbContext(DbContextOptions<OrderDbContext> options) : base(options) { }

        public DbSet<Order> Orders => Set<Order>();

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            var converter = new ValueConverter<List<OrderItemDTO>, string>(
                v => JsonSerializer.Serialize(v, new JsonSerializerOptions()),
                v => JsonSerializer.Deserialize<List<OrderItemDTO>>(v, new JsonSerializerOptions()) ?? new()
            );

            modelBuilder.Entity<Order>()
                .Property(o => o.Products)
                .HasConversion(converter);
        }
    }
}