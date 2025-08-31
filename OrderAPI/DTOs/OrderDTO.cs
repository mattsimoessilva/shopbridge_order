namespace OrderAPI.DTOs
{
    public class OrderDTO
    {
        public Guid Id { get; set; }
        public string CustomerName { get; set; } = string.Empty;
        public List<ProductSnapshotDTO> Items { get; set; } = new();
    }
}