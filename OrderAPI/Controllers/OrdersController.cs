using Microsoft.AspNetCore.Mvc;
using OrderAPI.DTOs;
using OrderAPI.Models;
using OrderAPI.Services.Interfaces;

namespace OrderAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class OrdersController : ControllerBase
    {
        private readonly IOrderService _orderService;

        public OrdersController(IOrderService orderService)
        {
            _orderService = orderService;
        }

        /// <summary>
        /// Retrieves all orders.
        /// </summary>
        [HttpGet]
        [ProducesResponseType(typeof(IEnumerable<Order>), StatusCodes.Status200OK)]
        public IActionResult GetAll()
        {
            var orders = _orderService.GetAllOrders();
            return Ok(orders);
        }

        /// <summary>
        /// Retrieves a specific order by ID.
        /// </summary.
        [HttpGet("{id}")]
        [ProducesResponseType(typeof(Order), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public IActionResult GetById(Guid id)
        {
            var order = _orderService.GetOrderById(id);
            if (order == null) return NotFound();
            return Ok(order);
        }

        /// <summary>
        /// Creates a new order.
        /// </summary>
        [HttpPost]
        [ProducesResponseType(typeof(Order), StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public IActionResult Create([FromBody] OrderDTO order)
        {
            if (!ModelState.IsValid) return BadRequest(ModelState);

            var createdOrder = _orderService.CreateOrder(order);
            return CreatedAtAction(nameof(GetById), new { id = createdOrder.Id }, createdOrder);
        }

        /// <summary>
        /// Deletes an order by ID.
        /// </summary>
        [HttpDelete("{id}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public IActionResult Delete(Guid id)
        {
            var success = _orderService.DeleteOrder(id);
            if (!success) return NotFound();
            return NoContent();
        }
    }
}