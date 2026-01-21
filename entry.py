import mysql.connector
import datetime
import requests
from up import prg  # Import the function from your existing code

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Enter_Your_Password",   # temporary
    database="parking_db"
)

cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS parking_records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        plate_number VARCHAR(20) NOT NULL,
        parking_slot VARCHAR(10) NOT NULL,
        entry_time DATETIME NOT NULL,
        exit_time DATETIME NULL,
        fee DECIMAL(10,2) NULL
    )
""")

def get_available_slot():
    """ Assigns the first available slot in hexadecimal format from 1 to 50 """
    cursor.execute("SELECT parking_slot FROM parking_records WHERE exit_time IS NULL")
    occupied_slots = {slot[0] for slot in cursor.fetchall()}

    for i in range(1, 51):
        hex_slot = hex(i)[2:].upper()
        if hex_slot not in occupied_slots:
            return hex_slot
    return None

def store_parking_record():
    """ Detect plate and store entry """
    plate_number = prg()

    if plate_number:
        parking_slot = get_available_slot()
        if parking_slot:
            entry_time = datetime.datetime.now()

            cursor.execute(
                "INSERT INTO parking_records (plate_number, parking_slot, entry_time) VALUES (%s, %s, %s)",
                (plate_number, parking_slot, entry_time)
            )
            conn.commit()

            #  Notify dashboard
            try:
                requests.get("http://127.0.0.1:5000/notify")
            except:
                pass

            print(f"Stored: {plate_number} | Slot: {parking_slot} | Time: {entry_time}")
        else:
            print("No available parking slots!")
    else:
        print("No plate detected!")

store_parking_record()

cursor.close()
conn.close()
