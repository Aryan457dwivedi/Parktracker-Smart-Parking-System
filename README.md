An Automated Parking Allocation System developed using Python, OpenCV, Haar Cascade, Tesseract OCR, Flask, and MySQL that detects license plates, allocates parking slots automatically, and computes parking charges.



##  Features

- **Number Plate Detection** using OpenCV & Tesseract
- **Automatic Parking Slot Allocation** (Hexadecimal from 1 to 50)
- **Entry & Exit Management**
- **Parking Fee Calculation** (₹10 per hour)
- **MySQL Database Integration**
- **Bill Generation upon Exit**

##  Demo 
<img width="2879" height="1224" alt="Screenshot 2026-01-22 050001" src="https://github.com/user-attachments/assets/0004c449-4445-4554-b0a7-78d5e36df82a" />
<img width="2879" height="1768" alt="Screenshot 2026-01-22 045657" src="https://github.com/user-attachments/assets/180c9f10-0754-4b19-a186-3bd471532483" />
<img width="2879" height="1799" alt="Screenshot 2026-01-22 045644" src="https://github.com/user-attachments/assets/baf522f3-702b-45fa-b0f1-70edf1b4cc46" />


##  Tech Stack

- **Backend:** Python, Flask  
- **Computer Vision:** OpenCV, Tesseract OCR  
- **Database:** MySQL  
- **Frontend:** HTML, CSS, JavaScript  
- **Tools:** Git, GitHub  



##  Setup & Installation

### 1️ Install Dependencies

```bash
pip install opencv-python pytesseract mysql-connector-python flask flask-socketio
```
2️ Configure Tesseract OCR
Download from:
https://github.com/UB-Mannheim/tesseract/wiki

Update path in up.py:
```bash
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```
3️ MySQL Database Setup
```bash
CREATE DATABASE parking_db;
USE parking_db;

CREATE TABLE parking_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plate_number VARCHAR(20) NOT NULL,
    parking_slot VARCHAR(5) NOT NULL,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME DEFAULT NULL,
    fee DECIMAL(10,2) DEFAULT NULL
);
```
4️ Update Database Credentials
Edit app.py, entry.py, exit.py

```bash
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="parking_db"
)
```

## Usage
Start Web Dashboard
```bash
python app.py
```
Open browser:

```bash
http://127.0.0.1:5000
```
## Vehicle Entry
```bash

python entry.py
```
- Detects plate number

- Assigns parking slot

- Stores entry time

## Vehicle Exit
```bash

python exit.py
```
- Detects plate number

- Calculates bill

- Updates database

- Displays receipt

## Sample Bill Output
```bash
========= PARKING BILL =========
Plate Number: KA01AB1234
Parking Slot: A
Entry Time  : 2025-02-11 10:00:00
Exit Time   : 2025-02-11 12:30:00
Duration    : 2.5 hours
Total Fee   : ₹25.00
================================
```
## Author

Aryan Dwivedi

Final Year CSE Student

Python | AI | Full Stack

