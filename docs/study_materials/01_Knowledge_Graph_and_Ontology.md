# Bài 1: Từ Dữ Liệu Thô Đến Mạng Lưới Tri Thức - Hiểu Sâu Về Ontology và Knowledge Graph

Thay vì chỉ liệt kê các khái niệm khô khan, tài liệu này sẽ kể cho bạn nghe "câu chuyện" về cách dữ liệu được tổ chức trong dự án của chúng ta, giúp bạn hiểu được **tại sao chúng ta lại cần Đồ thị tri thức (Knowledge Graph)** và **cách nó kết nối với các thuật toán phía sau**.

---

## 1. Bức tranh toàn cảnh: Tại sao lại là Đồ Thị (Graph) mà không phải Bảng (Table)?
Hãy tưởng tượng bạn đang xây dựng một hệ thống Hỏi Đáp (QA) cho sinh viên ngành Khoa học Máy tính. Nếu bạn lưu trữ kiến thức dưới dạng "Bảng Excel" truyền thống, bạn sẽ có các cột như: `Tên khái niệm`, `Lĩnh vực`, `Định nghĩa`. 

Cách lưu trữ này rất tốt để tra cứu từ điển, nhưng nó **bất lực** trước những câu hỏi đòi hỏi sự suy luận logic như: 
> *"Thuật toán Random Forest liên quan như thế nào đến Data Mining?"*

Để trả lời được câu hỏi đó, máy tính cần hiểu được **mối quan hệ đan chéo** giữa các khái niệm. Đó chính là lúc **Knowledge Graph (Đồ thị tri thức)** ra đời. Thay vì lưu dữ liệu vào các ô tính cô lập, nó vẽ ra một "Bản đồ tư duy" khổng lồ, nơi mỗi khái niệm là một trạm dừng (Node), và mối liên hệ giữa chúng là những con đường (Edge).

## 2. Bản Thể Học (Ontology) - "Bản thiết kế kiến trúc" của tri thức
Nếu Knowledge Graph là một ngôi nhà, thì Ontology chính là **Bản thiết kế kiến trúc** của ngôi nhà đó.

Ontology không chứa dữ liệu thực tế (nó không biết "Random Forest" là gì), nhưng nó đặt ra các **quy tắc tối cao**:
1. Có những loại "vật liệu" (Khái niệm) nào được phép tồn tại?
2. Có những "cách kết nối" (Mối quan hệ) nào được phép sử dụng?
Trong dự án này, chúng ta sử dụng **Computer Science Ontology (CSO)**. Đây là một Ontology đã được các nhà khoa học trên thế giới xây dựng sẵn bằng cách cho AI quét qua hàng triệu bài báo nghiên cứu. Nhờ có CSO, hệ thống của chúng ta biết được những quy tắc ngầm định của thế giới Khoa học Máy tính.

## 3. Kiến trúc hạt nhân: Triples (Bộ Ba Suy Luận)
Làm sao để dạy cho máy tính hiểu một mạng lưới khổng lồ? Cách đơn giản nhất là chia nhỏ toàn bộ thế giới thành các câu đơn giản mang cấu trúc **Chủ ngữ - Vị ngữ - Vị ngữ (Subject - Predicate - Object)**. Trong chuyên ngành, người ta gọi đây là cấu trúc **Triple**.

Hãy lấy một ví dụ thực tế từ file code `data_loader.py`:
- `(Machine Learning)` ---> `(superTopicOf)` ---> `(Deep Learning)`
- Lời dịch: *"Học máy là chủ đề cha bao trùm lên Học sâu."*

Mỗi Triple chính là một viên gạch. Bằng cách chắp vá hàng trăm ngàn viên gạch (Triples) này lại với nhau, máy tính sẽ tự động dệt nên một mạng lưới Đồ thị tri thức khổng lồ.

## 4. Các "chất kết dính" (Relations) và Tầm nhìn xa về Thuật toán
Bây giờ, hãy liên kết cấu trúc dữ liệu với **Phase 3 (Các thuật toán)** mà chúng ta vừa code. Trong đồ thị CSO có vô số loại quan hệ, nhưng chúng ta chỉ chọn lọc ra 3 "chất kết dính" quan trọng nhất, vì mỗi chất kết dính lại phục vụ một mục đích suy luận riêng cho thuật toán:

### A. `superTopicOf` (Quan hệ Cha - Con)
- **Ý nghĩa tự nhiên:** Khái niệm này đẻ ra khái niệm kia.
- **Sự liên kết với thuật toán:** Nhờ có quan hệ này, thuật toán mới biết đường đi "từ trên xuống dưới" (Từ Data Science lặn sâu xuống Decision Tree). Nó là cột sống tạo nên hàm `depth_heuristic` cho thuật toán A* Search, giúp A* biết được ai ở tầng cao, ai ở tầng thấp để mò đường nhanh hơn.

### B. `contributesTo` (Quan hệ Đóng góp ngang hàng)
- **Ý nghĩa tự nhiên:** Hai lĩnh vực không phải cha con, nhưng kỹ thuật của ngành này giúp ích cho ngành kia.
- **Sự liên kết với thuật toán:** Đây là con đường đi tắt. Nhờ gán trọng số (Weight) là 1.5 (xa hơn một chút so với cha-con là 1.0), thuật toán Dijkstra có thể đánh giá xem liệu "đi vòng qua các ngành liên quan" có nhanh hơn là "đi thẳng theo cây gia phả" hay không.

### C. `relatedEquivalent` (Xử lý sự hỗn loạn của ngôn từ)
- **Ý nghĩa tự nhiên:** "Neural Networks" hay "Artificial Neural Networks" thực chất chỉ là một.
- **Sự liên kết với thuật toán:** Nếu không có quan hệ này, thuật toán BFS/DFS sẽ bị kẹt trong một mớ bòng bong các từ đồng nghĩa, đi lòng vòng không lối thoát. Trong `graph_builder.py`, chúng ta đã dùng kỹ thuật **Alias Mapping** để gom tất cả các từ đồng nghĩa này lại thành 1 node duy nhất (Canonical Node). Điều này giúp đồ thị "sạch sẽ" và đường đi mượt mà hơn.

## 5. Cầu nối đến việc Cắt tỉa (Pruning)
Đến đây, bạn đã hình dung được sự vĩ đại của CSO với hơn 103,000 Triples tạo ra 15,000 trạm dừng (Nodes). Nhưng sự vĩ đại đó lại là "cơn ác mộng" cho RAM máy tính và thời gian chờ đợi của người dùng khi hệ thống QA chạy thực tế.

Đó là lý do bức tranh tri thức này dẫn chúng ta đến hành động tiếp theo: **Cắt tỉa đồ thị (Graph Pruning)**. Thay vì mang cả bản đồ thế giới để hỏi đường từ nhà ra chợ, chúng ta dùng thuật toán BFS khoanh vùng một khu vực "Data Science" với độ sâu 5 tầng, chỉ lấy 554 nodes. Vừa đủ tinh gọn để thuật toán Dijkstra và A* tỏa sáng, vừa đủ phong phú để trả lời các câu hỏi QA!
