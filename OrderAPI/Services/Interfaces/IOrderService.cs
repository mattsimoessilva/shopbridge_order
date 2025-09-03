using OrderAPI.Models.DTOs;
using OrderAPI.Models.Entities;

namespace OrderAPI.Services.Interfaces
{
    public interface IOrderService
    {
        public Task<IEnumerable<OrderResponseDTO>> GetAllOrdersAsync();
        public Task<OrderResponseDTO?> GetOrderByIdAsync(Guid id);
        public Task<OrderResponseDTO> CreateOrderAsync(OrderDTO dto);
        public Task<bool> DeleteOrderAsync(Guid id);
        public Task<bool> UpdateOrderAsync(OrderDTO dto);
    }
}