## NYC Taxi Data Pipeline (Submission 2)

## 📌 ข้อมูลที่ใช้ (Data Source)

โปรเจกต์นี้ใช้ข้อมูลบันทึกการเดินทางของแท็กซี่ในนครนิวยอร์ก (NYC Taxi & Limousine Commission - TLC) 
- **เว็บไซต์โครงการ (Official Website):** https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- **Storage Endpoint ที่ใช้ดึงไฟล์:** https://d37ci6vzurychx.cloudfront.net/trip-data

ประเภทรถที่วิเคราะห์: Yellow Taxi, Green Taxi, For-Hire Vehicle (FHV), และ High Volume FHV
ช่วงเวลาที่ดึงข้อมูล: มกราคม 2024 ถึง มิถุนายน 2024 (พารามิเตอร์กำหนดค่าเป็น Year = 2024, Months = 1-6)
รูปแบบไฟล์ต้นฉบับ: Parquet

## 📂 โครงสร้าง Pipeline (Pipeline Structure)

pipeline.py: โค้ดหลักที่ใช้รันกระบวนการ ETL (Extract, Validate, Transform)

requirements.txt: รายชื่อไลบรารีที่จำเป็นสำหรับการรันระบบ

data/: โฟลเดอร์สำหรับเก็บไฟล์ Parquet ต้นฉบับที่ดาวน์โหลดมา (ถูก ignore ไว้เพื่อไม่ให้อัปโหลดไฟล์ขนาดใหญ่ขึ้น GitHub)

output/: โฟลเดอร์จัดเก็บไฟล์ผลลัพธ์ที่ผ่านการจัดการแล้ว (curated_taxi_summary.csv และ curated_monthly_trips.csv)

pipeline_run.log: ไฟล์บันทึกหลักฐานการรันและสถานะการทำงานของระบบ

## 🚀 วิธีติดตั้งและวิธีรัน (Installation & Execution)

1.  **Clone repository และเข้าไปที่โฟลเดอร์โปรเจกต์:**
    ```bash
    git clone https://github.com/YokoYoko48/nyc-taxi-data-pipeline.git
    cd nyc-taxi-data-pipeline
    ```
2.  **ติดตั้งไลบรารีที่จำเป็น:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **รัน Data Pipeline:**
    ```bash
    python pipeline.py
    ```

*หมายเหตุ: เมื่อรันเสร็จสิ้น ระบบจะสร้างไฟล์ผลลัพธ์ในโฟลเดอร์ `output/` และบันทึกประวัติการทำงานใน `pipeline_run.log`*

### 📊 Pipeline / Data Flow Diagram

![Data Flow Diagram](pipeline_diagram.png)

## 🧠 การตัดสินใจสำคัญในการออกแบบ (Key Design Decisions)

1.  **การแยกโครงสร้างฟังก์ชันการทำงาน (Modular Design):** ตัดสินใจแยกกระบวนการทำงานออกเป็นฟังก์ชันย่อยอย่างชัดเจน ได้แก่ `extract_data()`, `validate_data()`, และ `transform_and_load()` แทนการเขียนโค้ดต่อกันยาวๆ เพื่อให้ง่ายต่อการดูแลรักษา และสามารถปรับแก้ตรรกะเฉพาะจุดได้โดยไม่กระทบส่วนอื่น
2.  **การใช้ระบบ Logging แทน Print:** ตัดสินใจใช้ไลบรารี `logging` เพื่อเขียนบันทึกการทำงานลงในไฟล์ `pipeline_run.log` ทำให้เรามีหลักฐานสถานะการทำงาน (Evidence of execution) และสามารถตรวจสอบข้อผิดพลาด (Data Quality Check) ย้อนหลังได้ว่าเกิดความผิดปกติในขั้นตอนใด ซึ่งเป็นมาตรฐานที่ดีกว่าการใช้ `print()` แสดงผลบนหน้าจอเพียงอย่างเดียว
3.  **การทำ Parameterization และ Quality Check:** ออกแบบฟังก์ชัน `extract_data(year, months)` ให้รับค่าพารามิเตอร์แทนการ Hardcode ทำให้ง่ายต่อการอัปเดตข้อมูลใหม่ (เช่น ครึ่งปีหลัง) พร้อมแทรกการตรวจสอบ Data Completeness, Null values และค่าติดลบ ให้อัตโนมัติระหว่างรัน

## 🔄 การพัฒนาจาก Submission 1 และข้อจำกัด

*   **การพัฒนา:** Pipeline นี้ถูกพัฒนาจาก Jupyter Notebook ใน Submission 1 ให้กลายเป็นระบบสคริปต์อัตโนมัติที่สามารถปรับเปลี่ยนพารามิเตอร์ (เช่น เปลี่ยนปีหรือเดือน) เพื่ออัปเดตข้อมูลใหม่ได้ทันที นอกจากนี้ยังมีการเพิ่มขั้นตอน Data Validation และการสร้างชุดข้อมูลพร้อมใช้ (Curated Output) สำหรับนำไปทำ Data Visualization ต่อ โดยมีไฟล์ `curated_monthly_trips.csv` เพื่อให้สามารถตรวจสอบย้อนกลับ (Traceability) ไปยังข้อมูลดิบรายเดือนได้
*   **ข้อจำกัด:** ปัจจุบันระบบยังคงต้องสั่งรันด้วยตัวเอง (Manual Trigger) บนเครื่อง Local ยังไม่ได้มีการนำไปตั้งเวลาทำงานอัตโนมัติ (เช่น ใช้ Cron Job, Apache Airflow หรือ AWS EventBridge) และยังทำงานแบบ Synchronous ซึ่งอาจใช้เวลาดาวน์โหลดข้อมูลนานหากอินเทอร์เน็ตไม่เสถียร นอกจากนี้หากสเกลข้อมูลใหญ่ขึ้นเป็นระดับหลายปี อาจต้องพิจารณาบูรณาการการจัดเก็บแบบ Data Lake ผ่านระบบ Cloud (เช่น AWS S3) เพื่อแก้ปัญหาคอขวดด้านพื้นที่เก็บข้อมูล

## 📝 Learning Reflection

การพัฒนาระบบจาก Notebook สู่ Data Pipeline ทำให้เห็นความสำคัญของการวางโครงสร้างโค้ดและการตรวจสอบสถานะการทำงาน การแยกฟังก์ชันเป็นสัดส่วน (Modularity) ช่วยให้โค้ดมีความเป็นระเบียบและดูแลรักษาง่ายขึ้นอย่างมาก นอกจากนี้ การส่งมอบข้อมูลสุดท้ายในรูปแบบ Curated Output ควบคู่กับการใช้ Logging ยังช่วยแยกส่วนการเตรียมข้อมูลออกจากการวิเคราะห์ ทำให้กระบวนการวิเคราะห์ผลลัพธ์มีความเสถียร ตรวจสอบย้อนกลับได้ และน่าเชื่อถือมากขึ้น
