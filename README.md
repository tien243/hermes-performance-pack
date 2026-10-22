# Hermes Performance Pack 🚀

Plugin tối ưu hiệu năng tốc độ cao cho **Hermes Agent** (`nousresearch/hermes-agent`).

Gói plugin này mang các công cụ xử lý tìm kiếm native và đọc file đa luồng vào Hermes, giúp rút ngắn thời gian phản hồi và giảm số vòng lặp I/O trong các tác vụ kiểm tra mã nguồn.

---

## 🌟 Công cụ cung cấp (Toolset: `performance`)

1. **`ripgrep_search` (Native Fast Search)**:
   - Sử dụng trực tiếp binary `ripgrep` (`rg`) trên hệ thống để tìm kiếm regex trong code và văn bản.
   - Tránh việc phải spawn shell gián tiếp (`grep` / `find`).
   - Tự động kiểm soát giới hạn dòng kết quả (`head_limit`), lọc theo file glob, và ngăn chặn path traversal.

2. **`batch_read_files` (Concurrent File Reader)**:
   - Đọc đồng thời nhiều file trong 1 turn duy nhất thông qua `ThreadPoolExecutor` có giới hạn (tối đa 10 file/lần, 5 luồng đồng thời).
   - Giúp agent kiểm tra nhiều file liên quan cùng lúc thay vì phải gọi lệnh đọc file tuần tự từng lượt.
   - Có cơ chế chặn đọc file vượt quá 10MB và giới hạn số dòng tối đa trên mỗi file để bảo vệ bộ nhớ.

*(Lưu ý về Context Pruning: Theo kiến trúc của Hermes, việc cắt tỉa/nén context phải được triển khai riêng qua `ContextEngine` plugin kế thừa `agent.context_engine.ContextEngine`, không thể thực hiện qua tool thông thường).*

---

## 📦 Hướng dẫn cài đặt vào Hermes Agent

### Cách 1: Cài đặt vào thư mục User Plugins của Hermes
Copy thư mục `hermes-performance-pack` vào:

- **Linux / macOS**: `~/.hermes/plugins/hermes-performance-pack`
- **Windows**: `%LOCALAPPDATA%\hermes\plugins\hermes-performance-pack` hoặc `~/.hermes/plugins/hermes-performance-pack`

### Cách 2: Kích hoạt cho một Project cụ thể
Đặt thư mục plugin vào `.hermes/plugins/hermes-performance-pack` ngay tại thư mục gốc của project bạn đang làm việc với Hermes.

---

## ⚙️ Kích hoạt & Sử dụng

Kiểm tra plugin đã được nhận diện:
```bash
hermes plugins list
```

Bật toolset trong `config.yaml` của Hermes:
```yaml
tools:
  enabled:
    - performance
```

---

## 🧪 Chạy Unit Tests

Trong thư mục plugin, chạy:
```bash
python test_tools.py
```

---
*Phát triển bởi Đặng Tiến (Solo2OS Ecosystem)*
