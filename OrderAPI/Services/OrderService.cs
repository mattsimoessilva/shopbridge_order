using OrderAPI.Models.DTOs;
using OrderAPI.Models.Entities;
using OrderAPI.Repositories.Interfaces;
using OrderAPI.Services.Interfaces;
using System; // Ensure System is included for Exception base class

namespace OrderAPI.Services
{
    public class OrderService : IOrderService
    {
        private readonly IOrderRepository _repository;

        public OrderService(IOrderRepository repository)
        {
            _repository = repository;
        }

        public async Task<IEnumerable<OrderResponseDTO>> GetAllOrdersAsync()
        {
            var orders = await _repository.GetAllAsync();

            return orders.Select(order => new OrderResponseDTO
            {
                Id = order.Id,
                CreatedAt = order.CreatedAt,
                CustomerId = order.CustomerId,
                Status = order.Status,
                Items = order.Items.Select(item => new OrderItemDTO
                {
                    ProductId = item.ProductId,
                    ProductName = item.ProductName,
                    Quantity = item.Quantity,
                    UnitPrice = item.UnitPrice
                }).ToList(),
                TotalAmount = order.TotalAmount
            });
        }


        public async Task<OrderResponseDTO?> GetOrderByIdAsync(Guid id)
        {
            var order = await _repository.GetByIdAsync(id);

            if (order is null)
                return null;

            return new OrderResponseDTO
            {
                Id = order.Id,
                CreatedAt = order.CreatedAt,
                Items = order.Items.Select(i => new OrderItemDTO
                {
                    ProductId = i.ProductId,
                    ProductName = i.ProductName,
                    Quantity = i.Quantity,
                    UnitPrice = i.UnitPrice
                }).ToList(),
                TotalAmount = order.TotalAmount
            };
        }


        public async Task<OrderResponseDTO> CreateOrderAsync(OrderRequestDTO dto)
        {
            var orderId = Guid.NewGuid();
            
            var orderItems = dto.Items.Select(item => new OrderItem
            {
                Id = Guid.NewGuid(),
                ProductId = item.ProductId,
                ProductName = item.ProductName,
                Quantity = item.Quantity,
                UnitPrice = item.UnitPrice,
            }).ToList();

            var totalAmount = orderItems.Sum(p => p.UnitPrice * p.Quantity);

            var order = new Order
            {
                Id = orderId,
                CustomerId = dto.CustomerId,
                CreatedAt = DateTime.UtcNow,
                Items = orderItems,
                TotalAmount = totalAmount,
                Status = OrderStatus.Pending
            };

            await _repository.AddAsync(order);

            return new OrderResponseDTO
            {
                Id = order.Id,
                CreatedAt = order.CreatedAt,
                CustomerId = order.CustomerId,
                Status = order.Status,
                Items = order.Items.Select(i => new OrderItemDTO
                {
                    ProductId = i.ProductId,
                    ProductName = i.ProductName,
                    Quantity = i.Quantity,
                    UnitPrice = i.UnitPrice
                }).ToList(),
                TotalAmount = order.TotalAmount
            };
 
        }


        public async Task<bool> DeleteOrderAsync(Guid id) => await _repository.RemoveAsync(id);

        public async Task<bool> UpdateOrderAsync(OrderRequestDTO dto)
        {
            var existingOrder = await _repository.GetByIdAsync(dto.Id);
            if (existingOrder == null)
                return false;

            var updatedItems = dto.Items.Select(item => new OrderItem
            {
                Id = Guid.NewGuid(),
                ProductId = item.ProductId,
                ProductName = item.ProductName,
                Quantity = item.Quantity,
                UnitPrice = item.UnitPrice
            }).ToList();

            var updatedTotal = updatedItems.Sum(i => i.UnitPrice * i.Quantity);

            existingOrder.CustomerId = dto.CustomerId;
            existingOrder.CreatedAt = DateTime.UtcNow;
            existingOrder.Items = updatedItems;
            existingOrder.Status = OrderStatus.Processing;

            await _repository.UpdateAsync(existingOrder);
            return true;
        }
    }
}