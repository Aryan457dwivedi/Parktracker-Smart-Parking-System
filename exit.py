import mysql.connector
import datetime
import requests
from up import prg  # Import the function from your existing code

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Enter_Your_Password",
    database="parking_db"
)
cursor = conn.cursor(buffered=True)

def process_exit():
    """ Detect plate, update exit and bill """
    plate_number = prg()

    if not plate_number:
        print("Error: No plate detected!")
        return

    cursor.execute("""
        SELECT entry_time, parking_slot
        FROM parking_records
        WHERE plate_number = %s AND exit_time IS NULL
    """, (plate_number,))

    result = cursor.fetchone()

    if not result:
        print(f"Error: No active parking record found for {plate_number}.")
        return

    entry_time, parking_slot = result
    exit_time = datetime.datetime.now()

    cursor.fetchall()  # clear buffer

    duration_hours = (exit_time - entry_time).total_seconds() / 3600
    duration_hours = max(duration_hours, 1)

    fee = round(duration_hours * 10, 2)

    cursor.execute("""
        UPDATE parking_records
        SET exit_time = %s, fee = %s
        WHERE plate_number = %s AND exit_time IS NULL
    """, (exit_time, fee, plate_number))

    conn.commit()

    # Notify dashboard
    try:
        requests.get("http://127.0.0.1:5000/notify")
    except:
        pass

    print("\n========= PARKING BILL =========")
    print(f"Plate Number: {plate_number}")
    print(f"Parking Slot: {parking_slot}")
    print(f"Entry Time  : {entry_time}")
    print(f"Exit Time   : {exit_time}")
    print(f"Duration    : {round(duration_hours, 2)} hours")
    print(f"Total Fee   : ₹{fee}")
    print("================================\n")

process_exit()

cursor.close()
conn.close()
