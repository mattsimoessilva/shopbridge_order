using OrderAPI.Models.Entities;

namespace OrderAPI.Repositories.Interfaces
{
    public interface IOrderRepository
    {
        Task<IEnumerable<Order>> GetAllAsync();
        Task<Order?> GetByIdAsync(Guid id);
        Task AddAsync(Order order);
        Task<bool> RemoveAsync(Guid id);
        Task<bool> UpdateAsync(Order order);
        Order? GetById(Guid id);
        void Add(Order order);
        bool Remove(Guid id);
        bool Update(Order order);

    }
}