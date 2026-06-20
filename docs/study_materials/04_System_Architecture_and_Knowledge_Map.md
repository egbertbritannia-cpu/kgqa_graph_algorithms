# Bài 4: System Architecture & Knowledge Map

Sơ đồ Mermaid khi gộp lại quá lớn sẽ bị thu nhỏ chữ khiến bạn khó đọc. Vì vậy, tôi đã chia nhỏ bức tranh tổng thể thành một **Bản trình chiếu (Carousel)** gồm 4 phần riêng biệt. 

Hãy bấm mũi tên qua lại để xem từng module của hệ thống nhé:

````carousel
### 1. Data Acquisition & Construction
Sơ đồ mô tả cách lấy dữ liệu từ CSO, lọc các quan hệ cần thiết và xây dựng đồ thị NetworkX ban đầu.

```mermaid
graph LR
    A[CSO Portal] -->|Download| B(CSO.3.5.csv)
    B -->|Parse| C{Triples}
    
    C -->|Filter| E1("superTopicOf (Weight: 1.0)")
    C -->|Filter| E2("contributesTo (Weight: 1.5)")
    C -->|Filter| E3("relatedEquivalent")
    
    E3 -->|Alias Mapping| M[Merge Synonyms]
    E1 & E2 & M --> I[NetworkX DiGraph]
```
<!-- slide -->
### 2. Graph Pruning (Cắt tỉa đồ thị)
Sơ đồ mô tả cách dùng BFS để trích xuất một nhánh nhỏ (subgraph) đủ sức tính toán từ đồ thị khổng lồ ban đầu.

```mermaid
graph LR
    I[Full NetworkX DiGraph<br>~15K nodes] --> M{BFS Search}
    M -->|Root| N["data_mining"]
    M -->|Limit| O["max_depth = 5"]
    
    M --> P["Extracted Subgraph<br>~554 Nodes"]
    P --> Q["Add 'depth' attribute to nodes"]
```
<!-- slide -->
### 3. Algorithm Layer (Thuật toán duyệt đồ thị)
Sơ đồ mô tả 4 thuật toán cốt lõi và mục đích của chúng khi áp dụng vào Question Answering.

```mermaid
graph TD
    P[Extracted Subgraph] --> R1[BFS]
    P --> R2[DFS]
    P --> R3[Dijkstra]
    P --> R4[A* Search]

    R1 --> S1["Find shortest path by HOPS<br>(Unweighted)"]
    R2 --> S2["Explore & Enumerate sub-topics<br>(Unweighted)"]
    R3 --> S3["Find shortest SEMANTIC path<br>(Weighted)"]
    
    R4 --> S4["Optimized Dijkstra<br>f(n) = g(n) + h(n)"]
    
    H["depth_heuristic"] -.-> S4
```
<!-- slide -->
### 4. Explainable QA (Đích đến cuối cùng)
Sơ đồ mô tả cách hệ thống lấy kết quả từ thuật toán để tạo ra câu trả lời giải thích được.

```mermaid
graph LR
    User[User Question] --> Parser[Query Parser]
    Parser -->|Extracts Concepts| Algo[Graph Algorithms]
    
    Algo --> Path["Found Path:<br>Deep Learning -> Machine Learning"]
    
    Path --> Verb[Path Verbalizer]
    Verb --> QA["Explainable Answer:<br>'Deep Learning is a sub-topic of Machine Learning'"]
```
````

### Tóm tắt các phân hệ (Layers):
1. **Data Acquisition:** Lấy dữ liệu từ CSO và cấu trúc Triples.
2. **Graph Construction:** Lọc nhiễu, gộp node đồng nghĩa (Alias Mapping), và tiêm trọng số (Semantic Weights).
3. **Graph Pruning:** Cắt tỉa đồ thị bằng BFS để lấy ra một mảnh nhỏ (subgraph) đủ sức tính toán.
4. **Algorithm Layer:** 4 thuật toán đồ thị và cách chọn thuật toán cho từng loại câu hỏi.
5. **Explainable QA:** Biến đường đi (path) thành câu trả lời tự nhiên.
