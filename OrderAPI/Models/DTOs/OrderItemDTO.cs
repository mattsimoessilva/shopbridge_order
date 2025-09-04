using Swashbuckle.AspNetCore.Annotations;

namespace OrderAPI.Models.DTOs
{
    public class OrderItemDTO
    {
        [SwaggerSchema("Product's unique identifier")]
        public Guid ProductId { get; set; }

        [SwaggerSchema("Name of the product")]
        public string ProductName { get; set; } = string.Empty;

        [SwaggerSchema("Quantity of the product ordered")]
        public int Quantity { get; set; }

        [SwaggerSchema("Unit price of the product")]
        public decimal UnitPrice { get; set; }

        [SwaggerSchema("Total price for the item (Quantity * UnitPrice)", ReadOnly = true)]
        public decimal TotalPrice => Quantity * UnitPrice;
    }

}