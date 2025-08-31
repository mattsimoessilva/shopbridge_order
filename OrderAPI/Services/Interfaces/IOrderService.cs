using OrderAPI.DTOs;
using OrderAPI.Models;

namespace OrderAPI.Services.Interfaces
{
    public interface IOrderService
    {
        IEnumerable<Order> GetAllOrders();
        Order? GetOrderById(Guid id);
        Order CreateOrder(OrderDTO dto);
        bool DeleteOrder(Guid id);
        bool UpdatedOrder(OrderDTO dto);
    }
}