# Bài 2: Xử Lý Dữ Liệu và Thư Viện NetworkX
Tài liệu này giải thích cách dữ liệu thô biến thành cấu trúc đồ thị trong bộ nhớ máy tính.

## 1. Parse Dữ liệu (data_loader.py)
Dữ liệu gốc tải từ CSO Portal là một file CSV. 
Mỗi dòng trong file CSV có định dạng URL: `https://cso.kmi.open.ac.uk/topics/machine_learning`
- Thuật toán xử lý: Cắt chuỗi (split) và thay thế dấu gạch dưới (`_`) bằng dấu cách, loại bỏ URL để lấy ra tên thực thể thuần túy: `machine learning`.

## 2. Thư viện NetworkX
NetworkX là thư viện chuẩn mực (de-facto standard) trong Python để mô hình hóa, phân tích và nghiên cứu đồ thị.
Trong file `graph_builder.py`, chúng ta dùng `nx.DiGraph()` (Đồ thị có hướng - Directed Graph).
- Tại sao lại là đồ thị có hướng? Vì quan hệ cha con có tính một chiều (`A là cha của B` KHÔNG đồng nghĩa `B là cha của A`).

## 3. Khái niệm Trọng Số Cạnh (Edge Weights)
Đây là một phần cực kỳ quan trọng cho hệ thống Question Answering (QA). 
Đồ thị nguyên thủy của CSO là *Unweighted Graph* (Đồ thị không có trọng số). Tuy nhiên, để đo lường "khoảng cách ngữ nghĩa", chúng ta phải tự tiêm (inject) trọng số vào:
- `weight = 1.0` cho `superTopicOf`
- `weight = 1.5` cho `contributesTo`

**Tại sao?**
Thuật toán tìm đường sẽ luôn cố gắng đi theo con đường có tổng trọng số nhỏ nhất. 
Bằng cách gán weight 1.0 cho quan hệ cha-con và 1.5 cho quan hệ đóng góp ngang hàng, chúng ta nói với thuật toán rằng: *"Hai khái niệm cha-con có liên hệ chặt chẽ (gần) hơn hai khái niệm đóng góp chéo cho nhau"*.

## 4. Alias Mapping (Xử lý đồng nghĩa)
Trong `graph_builder.py` có hàm `get_canonical(node)`. 
Thuật toán này giải quyết quan hệ `relatedEquivalent` (đồng nghĩa). 
- Thay vì thêm 2 nodes riêng biệt vào đồ thị và nối chúng lại, thuật toán này Map (Ánh xạ) node bị trùng về chung 1 ID duy nhất. 
- Giúp giảm thiểu số lượng nodes dư thừa và tăng độ chính xác khi truy vấn.
