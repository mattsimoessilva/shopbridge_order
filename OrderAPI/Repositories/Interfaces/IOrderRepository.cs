using OrderAPI.Models;

namespace OrderAPI.Repositories.Interfaces
{
    public interface IOrderRepository
    {
        IEnumerable<Order> GetAll();
        Order? GetById(Guid id);
        void Add(Order order);
        bool Remove(Guid id);
        bool Update(Order order);
    }
}