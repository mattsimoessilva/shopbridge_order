using Xunit;
using Moq;
using System;
using System.Collections.Generic;
using OrderAPI.Models.DTOs;
using OrderAPI.Models.Entities;
using OrderAPI.Repositories.Interfaces;
using OrderAPI.Services;

public class OrderServiceTests
{
    private readonly Mock<IOrderRepository> _mockRepo;
    private readonly OrderService _service;

    public OrderServiceTests()
    {
        _mockRepo = new Mock<IOrderRepository>();
        _service = new OrderService(_mockRepo.Object);
    }

    [Fact]
    public void GetAllOrders_ReturnsOrders()
    {
        var orders = new List<Order> { new Order { Id = Guid.NewGuid() } };
        _mockRepo.Setup(r => r.GetAll()).Returns(orders);

        var result = _service.GetAllOrders();

        Assert.Equal(orders, result);
    }

    [Fact]
    public void GetOrderById_ExistingId_ReturnsOrder()
    {
        var orderId = Guid.NewGuid();
        var order = new Order { Id = orderId };
        _mockRepo.Setup(r => r.GetById(orderId)).Returns(order);

        var result = _service.GetOrderById(orderId);

        Assert.Equal(order, result);
    }

    [Fact]
    public void GetOrderById_NonExistingId_ReturnsNull()
    {
        _mockRepo.Setup(r => r.GetById(It.IsAny<Guid>())).Returns((Order)null);

        var result = _service.GetOrderById(Guid.NewGuid());

        Assert.Null(result);
    }

    [Fact]
    public void CreateOrder_ValidDTO_CreatesOrderAndCallsAdd()
    {
        var dto = new OrderDTO
        {
            CustomerId = Guid.NewGuid(),
            PaymentMethod = PaymentMethod.CreditCard,
            Items = new List<OrderItemDTO>
            {
                new OrderItemDTO { ProductId = Guid.NewGuid(), Name = "Test", Quantity = 2, UnitPrice = 10.0m }
            }
        };

        Order? capturedOrder = null;
        _mockRepo.Setup(r => r.Add(It.IsAny<Order>()))
                 .Callback<Order>(o => capturedOrder = o);

        var result = _service.CreateOrder(dto);

        Assert.NotNull(result);
        Assert.Equal(dto.CustomerId, result.CustomerId);
        Assert.Equal(OrderStatus.Pending, result.Status);
        Assert.Equal(20.0m, result.Payment.Amount);
        Assert.Single(result.Items);
        Assert.Equal("Test", result.Items[0].ProductName);
        Assert.Equal(capturedOrder, result);
    }

    [Fact]
    public void DeleteOrder_ValidId_ReturnsTrue()
    {
        _mockRepo.Setup(r => r.Remove(It.IsAny<Guid>())).Returns(true);

        var result = _service.DeleteOrder(Guid.NewGuid());

        Assert.True(result);
    }

    [Fact]
    public void DeleteOrder_InvalidId_ReturnsFalse()
    {
        _mockRepo.Setup(r => r.Remove(It.IsAny<Guid>())).Returns(false);

        var result = _service.DeleteOrder(Guid.NewGuid());

        Assert.False(result);
    }

    [Fact]
    public void UpdatedOrder_ExistingOrder_UpdatesAndReturnsTrue()
    {
        var orderId = Guid.NewGuid();
        var existingOrder = new Order { Id = orderId };
        var dto = new OrderDTO
        {
            Id = orderId,
            CustomerId = Guid.NewGuid(),
            PaymentMethod = PaymentMethod.Pix,
            Items = new List<OrderItemDTO>
            {
                new OrderItemDTO { ProductId = Guid.NewGuid(), Name = "Updated", Quantity = 1, UnitPrice = 5.0m }
            }
        };

        _mockRepo.Setup(r => r.GetById(orderId)).Returns(existingOrder);
        _mockRepo.Setup(r => r.Update(It.IsAny<Order>())).Returns(true);

        var result = _service.UpdatedOrder(dto);

        Assert.True(result);
        Assert.Equal(OrderStatus.Processing, existingOrder.Status);
        Assert.Equal("Updated", existingOrder.Items[0].ProductName);
        Assert.Equal(5.0m, existingOrder.Payment.Amount);
    }

    [Fact]
    public void UpdatedOrder_NonExistingOrder_ReturnsFalse()
    {
        _mockRepo.Setup(r => r.GetById(It.IsAny<Guid>())).Returns((Order)null);

        var dto = new OrderDTO { Id = Guid.NewGuid() };

        var result = _service.UpdatedOrder(dto);

        Assert.False(result);
    }
}
