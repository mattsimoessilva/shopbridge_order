using OrderAPI.Models;
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

        public IEnumerable<Order> GetAll()
        {
            return _context.Orders
                .AsNoTracking()
                .ToList();
        }

        public Order? GetById(Guid id)
        {
            return _context.Orders
                .AsNoTracking()
                .FirstOrDefault(o => o.Id == id);
        }

        public void Add(Order order)
        {
            _context.Orders.Add(order);
            _context.SaveChanges();
        }

        public bool Remove(Guid id)
        {
            var order = _context.Orders.FirstOrDefault(o => o.Id == id);
            if (order == null) return false;

            _context.Orders.Remove(order);
            _context.SaveChanges();
            return true;
        }

        public bool Update(Order updatedOrder)
        {
            var existingOrder = _context.Orders.FirstOrDefault(o => o.Id == updatedOrder.Id);
            if (existingOrder == null) return false;

            existingOrder.CustomerName = updatedOrder.CustomerName;
            existingOrder.OrderDate = updatedOrder.OrderDate;
            existingOrder.Products = updatedOrder.Products;
            existingOrder.TotalAmount = updatedOrder.TotalAmount;

            _context.SaveChanges();
            return true;
        }
    }
}