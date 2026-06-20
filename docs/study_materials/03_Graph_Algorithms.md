# Bài 3: Các Thuật Toán Đồ Thị Áp Dụng Cho Question Answering (QA)
Tài liệu này hệ thống hóa 4 thuật toán được xây dựng trong thư mục `src/algorithms/`. 
Mục tiêu cốt lõi của các thuật toán này là tìm đường đi (Pathfinding) giữa các khái niệm, từ đó lấy chính **Đường đi này làm lời giải thích cho câu trả lời QA** (Explainable QA).

## 1. BFS (Breadth-First Search - Tìm kiếm theo chiều rộng)
- **Cách hoạt động:** Duyệt loang dần ra xung quanh như vết dầu loang (level-by-level). Dùng cấu trúc Queue (hàng đợi FIFO).
- **Đặc điểm:** Không quan tâm đến trọng số cạnh (Unweighted).
- **Mục đích QA:** Dùng để trả lời câu hỏi *"Khoảng cách ngắn nhất (ít bước nhất) giữa khái niệm A và B là bao nhiêu?"*. Đường đi đầu tiên nó chạm đến đích chắc chắn là đường đi ít bước (hops) nhất.

## 2. DFS (Depth-First Search - Tìm kiếm theo chiều sâu)
- **Cách hoạt động:** Đâm thẳng xuống một nhánh cho đến khi hết đường hoặc chạm giới hạn (depth limit) rồi mới quay lui (Backtracking). Dùng cấu trúc Stack (ngăn xếp LIFO).
- **Đặc điểm:** Tìm được đường đi nhưng KHÔNG đảm bảo ngắn nhất.
- **Mục đích QA:** Không dùng để tìm đường đi tối ưu, mà dùng để **Khám phá và Liệt kê**. Câu hỏi QA: *"Kể tên tất cả các lĩnh vực con thuộc nhánh AI với độ sâu 3 cấp"*.

## 3. Dijkstra (Tìm đường đi ngắn nhất có trọng số)
- **Cách hoạt động:** Mở rộng Node có tổng chi phí (cost) tích lũy nhỏ nhất tính từ điểm bắt đầu. Dùng Priority Queue (Hàng đợi ưu tiên / Min-Heap).
- **Đặc điểm:** Luôn tìm được đường đi có tổng trọng số (weight) nhỏ nhất.
- **Mục đích QA:** Đây là thuật toán cốt lõi cho Semantic QA. Khi người dùng hỏi *"Mối liên hệ ngữ nghĩa chặt chẽ nhất giữa A và B là gì?"*, Dijkstra sẽ tìm ra con đường tối ưu về mặt ngữ nghĩa, thay vì chỉ đếm số bước nhảy như BFS.

## 4. A* Search (A-Star) và Hàm Heuristic
- **Vấn đề của Dijkstra:** Dijkstra tìm đường theo mọi hướng (như sóng âm), dẫn đến lãng phí tài nguyên khi duyệt qua quá nhiều nodes không cần thiết (đặc biệt khi đồ thị lớn).
- **Cách hoạt động của A*:** Sử dụng công thức `f(n) = g(n) + h(n)`.
  - `g(n)`: Chi phí thực tế đi từ A đến n (giống Dijkstra).
  - `h(n)`: **Heuristic** - Lời tiên tri ước lượng khoảng cách từ n đến đích.
- **Hàm Heuristic trong dự án (`depth_heuristic`):** Chúng ta lợi dụng đặc tính phân cấp (Hierarchy) của CSO. Nếu node n và node đích có cùng độ sâu (depth), chúng có khả năng gần nhau. Nếu lệch độ sâu quá nhiều, chúng rất xa nhau. A* sẽ ưu tiên duyệt những node có Heuristic nhỏ.
- **Mục đích QA:** Thay thế Dijkstra khi cần trả lời trên toàn bộ đồ thị CSO 15,000 nodes với tốc độ nhanh nhất có thể.
