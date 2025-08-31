using OrderAPI.DTOs;
using OrderAPI.Models;
using OrderAPI.Repositories.Interfaces;
using OrderAPI.Services.Interfaces;

namespace OrderAPI.Services
{
    public class OrderService : IOrderService
    {
        private readonly IOrderRepository _repository;

        public OrderService(IOrderRepository repository)
        {
            _repository = repository;
        }

        public IEnumerable<Order> GetAllOrders() => _repository.GetAll();

        public Order? GetOrderById(Guid id) => _repository.GetById(id);

        public Order CreateOrder(OrderDTO dto)
        {
            var productSnapshots = dto.Items.Select(item => new ProductSnapshotDTO
            {
                ProductId = item.ProductId,
                Name = item.Name,
                UnitPrice = item.UnitPrice,
                Quantity = item.Quantity
            }).ToList();

            var totalAmount = productSnapshots.Sum(p => p.UnitPrice * p.Quantity);

            var order = new Order
            {
                Id = Guid.NewGuid(),
                CustomerName = dto.CustomerName,
                OrderDate = DateTime.UtcNow,
                Products = productSnapshots,
                TotalAmount = totalAmount
            };

            _repository.Add(order);
            return order;
        }

        public bool DeleteOrder(Guid id) => _repository.Remove(id);

        public bool UpdatedOrder(OrderDTO dto)
        {
            var existingOrder = _repository.GetById(dto.Id);
            if (existingOrder == null)
                return false;

            var updatedSnapshots = dto.Items.Select(item => new ProductSnapshotDTO
            {
                ProductId = item.ProductId,
                Name = item.Name,
                UnitPrice = item.UnitPrice,
                Quantity = item.Quantity
            }).ToList();

            var updatedTotal = updatedSnapshots.Sum(p => p.UnitPrice * p.Quantity);

            existingOrder.CustomerName = dto.CustomerName;
            existingOrder.OrderDate = DateTime.UtcNow;
            existingOrder.Products = updatedSnapshots;
            existingOrder.TotalAmount = updatedTotal;

            return _repository.Update(existingOrder);
        }
    }
}