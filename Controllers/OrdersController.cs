using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using OrderAPI.Models.DTOs;
using OrderAPI.Models.Entities;
using OrderAPI.Services.Interfaces;
using Swashbuckle.AspNetCore.Annotations;

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

        [HttpPost]
        [SwaggerOperation(Summary = "Creates a new order.")]
        [ProducesResponseType(typeof(OrderResponseDTO), StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<IActionResult> Create([FromBody] OrderRequestDTO orderRequest)
        {
            var createdOrder = await _orderService.CreateOrderAsync(orderRequest);
            return CreatedAtAction(nameof(GetById), new { id = createdOrder.Id }, createdOrder);
        }

        [HttpGet]
        [SwaggerOperation(Summary = "Retrieves all orders.")]
        [ProducesResponseType(typeof(IEnumerable<OrderResponseDTO>), StatusCodes.Status200OK)]
        public async Task<IActionResult> GetAll()
        {
            var orders = await _orderService.GetAllOrdersAsync();
            return Ok(orders);
        }

        [HttpGet("{id}")]
        [SwaggerOperation(Summary = "Retrieves a specific order by ID.")]
        [ProducesResponseType(typeof(OrderResponseDTO), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult> GetById(Guid id)
        {
            var order = await _orderService.GetOrderByIdAsync(id);
            if (order == null) return NotFound();
            return Ok(order);
        }

        [HttpPut]
        [SwaggerOperation(Summary = "Updates an existing order.")]
        [ProducesResponseType(typeof(OrderResponseDTO), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<IActionResult> Update([FromBody] OrderRequestDTO orderRequest)
        {
            var updatedOrder = await _orderService.UpdateOrderAsync(orderRequest);

            return Ok(updatedOrder);
        }

        [HttpDelete("{id}")]
        [SwaggerOperation(Summary = "Deletes an order by ID.")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<IActionResult> Delete(Guid id)
        {
            var success = await _orderService.DeleteOrderAsync(id);
            if (!success) return NotFound();
            return NoContent();
        }
    }
}