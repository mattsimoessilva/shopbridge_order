using OrderAPI.Data;
using Microsoft.OpenApi.Models;
using Microsoft.AspNetCore.Builder;
using OrderAPI.Repositories;
using Microsoft.EntityFrameworkCore;
using OrderAPI.Repositories.Interfaces;
using OrderAPI.Services.Interfaces;
using OrderAPI.Services;

var builder = WebApplication.CreateBuilder(args);

// Adds EF Core with SQlite
builder.Services.AddDbContext<OrderDbContext>(options =>
    options.UseSqlite("Data Source=orders.db"));

// Registers services
builder.Services.AddScoped<IOrderRepository, OrderRepository>();
builder.Services.AddScoped<IOrderService, OrderService>();

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "ShopBridge Order Service API",
        Version = "v1"
    });
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();
app.Run();

