# Hermes Performance Pack 🚀

Plugin tối ưu hiệu năng tốc độ cao cho **Hermes Agent** (`nousresearch/hermes-agent`).

Gói plugin này mang các công cụ xử lý I/O native và cơ chế quản lý ngữ cảnh tinh gọn vào Hermes, giải quyết các điểm nghẽn thường gặp khi chạy agent trên các dự án lớn.

---

## 🌟 Tính năng chính

1. **`ripgrep_search` (Native Fast Search)**:
   - Sử dụng binary `ripgrep` (`rg`) native để tìm kiếm regex trong code và tài liệu.
   - Nhanh hơn 5-10 lần so với việc chạy shell `grep` / `find` hoặc đọc duyệt tuần tự.
   - Tự động giới hạn số dòng kết quả (`head_limit`) và lọc glob file an toàn.

2. **`batch_read_files` (Parallel File Reader)**:
   - Đọc đồng thời nhiều file trong 1 turn duy nhất thông qua `ThreadPoolExecutor`.
   - Giảm thiểu số vòng lặp qua lại (round-trips) của agent khi cần inspect nhiều file liên quan.

3. **`prune_tool_context` (Context Pruning Marker)**:
   - Đánh dấu và cô đọng các kết quả tool đã hoàn thành (như log dài, code dump), giúp giữ cửa sổ ngữ cảnh tập trung vào các facts cốt lõi.

---

## 📦 Hướng dẫn cài đặt vào Hermes Agent

### Cách 1: Cài đặt vào thư mục User Plugins của Hermes
Copy thư mục `hermes-performance-pack` vào thư mục plugins của Hermes:

- **Linux / macOS**: `~/.hermes/plugins/hermes-performance-pack`
- **Windows**: `%LOCALAPPDATA%\hermes\plugins\hermes-performance-pack` hoặc `~/.hermes/plugins/hermes-performance-pack`

### Cách 2: Kích hoạt cho một Project cụ thể
Đặt thư mục plugin vào `.hermes/plugins/hermes-performance-pack` ngay tại thư mục gốc của project bạn đang mở trên Hermes.

---

## ⚙️ Cấu hình

Sau khi đặt plugin vào thư mục, kiểm tra danh sách plugin bằng CLI của Hermes:
```bash
hermes plugins list
```

Bật toolset trong cấu hình `config.yaml` của Hermes nếu cần:
```yaml
tools:
  enabled:
    - performance
```

Hoặc trong phiên chat với Hermes, agent sẽ tự động nhìn thấy các tool:
- `ripgrep_search`
- `batch_read_files`
- `prune_tool_context`

---

## 🛠️ Yêu cầu môi trường
- Binary `ripgrep` (`rg` hoặc `rg.exe`) có sẵn trên PATH (Hermes native installer trên Windows thường đã tích hợp sẵn `rg.exe` trong `%LOCALAPPDATA%\hermes\bin\`).

---
*Phát triển bởi Đặng Tiến (Solo2OS Ecosystem)*
