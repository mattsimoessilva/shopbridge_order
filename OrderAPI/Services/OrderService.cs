using OrderAPI.Models.DTOs;
using OrderAPI.Models.Entities;
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
            var orderItems = dto.Items.Select(item => new OrderItem
            {
                Id = Guid.NewGuid(),
                ProductId = item.ProductId,
                ProductName = item.Name,
                Quantity = item.Quantity,
                UnitPrice = item.UnitPrice
            }).ToList();

            var totalAmount = orderItems.Sum(p => p.UnitPrice * p.Quantity);

            var order = new Order
            {
                Id = Guid.NewGuid(),
                CustomerId = dto.CustomerId,
                CreatedAt = DateTime.UtcNow,
                Items = orderItems,
                Status = OrderStatus.Pending,
                Payment = new Payment
                {
                    Id = Guid.NewGuid(),
                    Method = dto.PaymentMethod,
                    Amount = totalAmount,
                    PaidAt = DateTime.UtcNow,
                    IsConfirmed = false
                }
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

            var updatedItems = dto.Items.Select(item => new OrderItem
            {
                Id = Guid.NewGuid(),
                ProductId = item.ProductId,
                ProductName = item.Name,
                Quantity = item.Quantity,
                UnitPrice = item.UnitPrice
            }).ToList();

            var updatedTotal = updatedItems.Sum(i => i.UnitPrice * i.Quantity);

            existingOrder.CustomerId = dto.CustomerId;
            existingOrder.CreatedAt = DateTime.UtcNow;
            existingOrder.Items = updatedItems;
            existingOrder.Status = OrderStatus.Processing;

            existingOrder.Payment = new Payment
            {
                Id = Guid.NewGuid(),
                Method = dto.PaymentMethod,
                Amount = updatedTotal,
                PaidAt = DateTime.UtcNow,
                IsConfirmed = false
            };

            return _repository.Update(existingOrder);
        }
    }
}