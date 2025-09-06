using OrderAPI.Models.Entities;
using OrderAPI.Data;
using Microsoft.EntityFrameworkCore;
using OrderAPI.Repositories.Interfaces;

namespace OrderAPI.Repositories
{
    public class OrderRepository : IOrderRepository
    {
        private readonly OrderDbContext _context;

        public OrderRepository(OrderDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Order>> GetAllAsync()
        {
            return await _context.Orders
                .Where(o => o.DeletedAt == null)
                .AsNoTracking()
                .ToListAsync();
        }

        public Order? GetById(Guid id)
        {
            return _context.Orders
                .Where(o => o.DeletedAt == null)
                .AsNoTracking()
                .FirstOrDefault(o => o.Id == id);
        }

        public async Task<Order?> GetByIdAsync(Guid id)
        {
            return await _context.Orders
                .AsNoTracking()
                .Include(o => o.Items) 
                .FirstOrDefaultAsync(o => o.Id == id);
        }


        public void Add(Order order)
        {
            _context.Orders.Add(order);
            _context.SaveChanges();
        }

        public async Task AddAsync(Order order)
        {
            await _context.Orders.AddAsync(order);
            await _context.SaveChangesAsync();
        }

        public bool Remove(Guid id)
        {
            var order = _context.Orders.FirstOrDefault(o => o.Id == id);
            if (order == null) return false;

            order.DeletedAt = DateTime.UtcNow;
            _context.SaveChanges();
            return true;
        }

        public async Task<bool> RemoveAsync(Guid id)
        {
            var order = await _context.Orders.FirstOrDefaultAsync(o => o.Id == id);
            if (order == null) return false;

            _context.Orders.Remove(order);
            await _context.SaveChangesAsync();
            return true;
        }

        public bool Update(Order updatedOrder)
        {
            var existingOrder = _context.Orders.FirstOrDefault(o => o.Id == updatedOrder.Id);
            if (existingOrder == null) return false;

            existingOrder.CustomerId = updatedOrder.CustomerId;
            existingOrder.Items = updatedOrder.Items;

            _context.SaveChanges();
            return true;
        }

        public async Task<bool> UpdateAsync(Order updatedOrder)
        {
            var existingOrder = await _context.Orders.FirstOrDefaultAsync(o => o.Id == updatedOrder.Id);
            if (existingOrder == null) return false;

            existingOrder.CustomerId = updatedOrder.CustomerId;
            existingOrder.Items = updatedOrder.Items;

            await _context.SaveChangesAsync();
            return true;
        }
    }
}