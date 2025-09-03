using OrderAPI.Models.DTOs;
using OrderAPI.Models.Entities;

namespace OrderAPI.Services.Interfaces
{
    public interface IOrderService
    {
        public IEnumerable<Order> GetAllOrders();
        public Order? GetOrderById(Guid id);
        public Order CreateOrder(OrderDTO dto);
        public bool DeleteOrder(Guid id);
        public bool UpdatedOrder(OrderDTO dto);
    }
}