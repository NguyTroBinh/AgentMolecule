# Multi-Agent Molecule Discovery Platform

Dự án này là một hệ thống thiết kế phân tử tự động (agentic pipeline) phục vụ mục tiêu tìm kiếm thuốc cho các bệnh về Hệ Thần kinh Trung ương (CNS). Hệ thống chuyển đổi ý định khoa học thành các quy trình làm việc từ đầu đến cuối, bao gồm thiết kế, sàng lọc và ưu tiên phân tử. Nền tảng được xây dựng dựa trên kiến trúc Multi-Agent sử dụng LangGraph để điều phối các tác nhân thông minh, kết hợp với các công cụ hóa tin học (RDKit) tiêu chuẩn công nghiệp.
Các chứng năng chính:
- Hệ thống tác nhân tự trị: Bao gồm Planner, Generator, Validator và Ranker Agent làm việc phối hợp.
- Thực thi bất đồng bộ: Sử dụng Celery/Redis để xử lý các lượt chạy nặng mà không gây nghẽn API.
- Công cụ hóa học tiêu chuẩn: Tích hợp RDKit để tính toán các chỉ số MW, LogP, QED, v.v.

### 1. Kiến trúc hệ thống

**Hệ thống hoạt động theo mô hình vòng lặp với 4 tác nhân chuyên biệt:**
- **Planner Agent:** Phân tích mục tiêu khoa học, thiết lập số vòng chạy, số phân tử được sinh ra ở mỗi vòng và chiến lược đột biến phân tử.
- **Generator Agent:** Thực hiện "biến đổi" các phân tử mồi (seeds) để tạo ra các phân tử SMILES mới dựa trên yêu cầu của Planner.
- **Validator Agent:** Tính toán các chỉ số vật lý như MW, LogP, HBD, HBA, TPSA, QED và sử dụng "filter" để đưa ra đánh giá.
- **Ranker Agent:** Chấm điểm phân tử theo công thức **Score = QED - 0.1 * violations**, chọn ra top_k phân tử có score cao nhất kết hợp với nhận xét.

<img width="2816" height="1536" alt="WorkflowMultiAgent" src="https://github.com/user-attachments/assets/4d7009fe-0d81-4446-8504-21303c579a71" />


### 2. Công nghệ sử dụng

- **Framework:** FastAPI (Backend API), LangGraph (Agent Orchestration).
- **AI Models:** Groq Cloud (Llama 3.1 & 3.3).
- **Chemistry Engine:** RDKit (Tính toán hóa lý & valid SMILES).
- **Infrastructure:** Celery & Redis (Xử lý tác vụ bất đồng bộ), Docker & Docker Compose.
- **Database:** SQLModel (SQLite) lưu trữ audit trace và kết quả.

### 3. Khởi tạo và cài đặt

**Yêu cầu hệ thống**
- Lấy API Key từ [Groq Cloud](https://console.groq.com/keys).

**Các bước thực hiện**
- Clone dự án:

  ```
  git clone https://github.com/NguyTroBinh/AgentMolecule.git
  cd AgentMolecule
- Cài đặt các thư viện cần thiết từ file requirements.txt:

  ```
  pip install -r requirements.txt
- Cấu hình môi trường: Tạo file .env bao gồm các thông tin sau:
  
  ```
  GROQ_API_KEY=your_key_here
  
  REDIS_URL=redis://redis:6379/0
  
  DATABASE_URL=sqlite:///./database.db
- Khởi chạy với Docker:

  ```
  docker compose up --build
### 4. Hướng dẫn sử dụng

**Khởi tạo lượt tìm kiếm:** Truy cập Swagger UI tại: http://localhost:8000/docs và gửi yêu cầu POST /api/v1/runs

**Payload mẫu:**

```
{
  "objective": "Tối ưu hóa các phân tử giống thuốc; tối đa hóa chỉ số QED.",
  "seeds": [
    "c1ccccc1",
    "CCO" 
  ],
  "filters": {
    "mw": 500,
    "logp": 5,
    "hbd": 5,
    "hba": 10,
    "tpsa": 140,
    "max_violations": 2
  } 
}
```
<img width="1752" height="362" alt="ResponseRun" src="https://github.com/user-attachments/assets/803d4e87-4210-4d07-bf13-ab4670becf3f" />

**Theo dõi và Lấy kết quả**

- **Trạng thái & Trace**: GET /api/v1/runs/{id}/status - Xem trạng thái hoạt động.
<img width="1748" height="568" alt="ResponseStatus" src="https://github.com/user-attachments/assets/9790bb2f-7c05-48a6-9b26-c5781326336d" />

- **Kết quả Top-K**: GET /api/v1/runs/{id}/results - Danh sách các phân tử tốt nhất đã tìm được kèm chỉ số hóa học chi tiết.
<img width="1745" height="765" alt="ResponseResult" src="https://github.com/user-attachments/assets/07f8174f-e05f-4189-bed9-db555a5b08ad" />
