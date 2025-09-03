using Xunit;
using Moq;
using Microsoft.AspNetCore.Mvc;
using OrderAPI.Controllers;
using OrderAPI.Models.DTOs;
using OrderAPI.Models.Entities;
using OrderAPI.Services.Interfaces;
using System;
using System.Collections.Generic;

public class OrdersControllerTests
{
    private readonly Mock<IOrderService> _mockService;
    private readonly OrdersController _controller;

    public OrdersControllerTests()
    {
        _mockService = new Mock<IOrderService>();
        _controller = new OrdersController(_mockService.Object);
    }

    [Fact]
    public void GetAll_ReturnsOkWithOrders()
    {
        var orders = new List<Order> { new Order { Id = Guid.NewGuid() } };
        _mockService.Setup(s => s.GetAllOrders()).Returns(orders);

        var result = _controller.GetAll();

        var okResult = Assert.IsType<OkObjectResult>(result);
        Assert.Equal(orders, okResult.Value);
    }

    [Fact]
    public void GetById_ExistingId_ReturnsOk()
    {
        var orderId = Guid.NewGuid();
        var order = new Order { Id = orderId };
        _mockService.Setup(s => s.GetOrderById(orderId)).Returns(order);

        var result = _controller.GetById(orderId);

        var okResult = Assert.IsType<OkObjectResult>(result);
        Assert.Equal(order, okResult.Value);
    }

    [Fact]
    public void GetById_NonExistingId_ReturnsNotFound()
    {
        _mockService.Setup(s => s.GetOrderById(It.IsAny<Guid>())).Returns((Order)null);

        var result = _controller.GetById(Guid.NewGuid());

        Assert.IsType<NotFoundResult>(result);
    }

    [Fact]
    public void Create_ValidOrder_ReturnsCreated()
    {
        var orderDto = new OrderDTO { CustomerId = Guid.NewGuid(), Items = new List<OrderItemDTO>() };
        var createdOrder = new Order { Id = Guid.NewGuid() };

        _mockService.Setup(s => s.CreateOrder(orderDto)).Returns(createdOrder);

        var result = _controller.Create(orderDto);

        var createdResult = Assert.IsType<CreatedAtActionResult>(result);
        Assert.Equal(createdOrder, createdResult.Value);
        Assert.Equal("GetById", createdResult.ActionName);
    }

    [Fact]
    public void Create_InvalidModel_ReturnsBadRequest()
    {
        _controller.ModelState.AddModelError("CustomerId", "Required");

        var result = _controller.Create(new OrderDTO());

        Assert.IsType<BadRequestObjectResult>(result);
    }

    [Fact]
    public void Delete_ExistingId_ReturnsNoContent()
    {
        _mockService.Setup(s => s.DeleteOrder(It.IsAny<Guid>())).Returns(true);

        var result = _controller.Delete(Guid.NewGuid());

        Assert.IsType<NoContentResult>(result);
    }

    [Fact]
    public void Delete_NonExistingId_ReturnsNotFound()
    {
        _mockService.Setup(s => s.DeleteOrder(It.IsAny<Guid>())).Returns(false);

        var result = _controller.Delete(Guid.NewGuid());

        Assert.IsType<NotFoundResult>(result);
    }

    [Fact]
    public void Update_ValidOrder_ReturnsOk()
    {
        var orderDto = new OrderDTO { CustomerId = Guid.NewGuid(), Items = new List<OrderItemDTO>() };
        var updatedOrder = new Order { Id = Guid.NewGuid() };

        _mockService.Setup(s => s.UpdatedOrder(orderDto)).Returns(updatedOrder);

        var result = _controller.Update(orderDto);

        var okResult = Assert.IsType<OkObjectResult>(result);
        Assert.Equal(updatedOrder, okResult.Value);
    }

    [Fact]
    public void Update_InvalidModel_ReturnsBadRequest()
    {
        _controller.ModelState.AddModelError("Items", "Required");

        var result = _controller.Update(new OrderDTO());

        Assert.IsType<BadRequestObjectResult>(result);
    }
}
