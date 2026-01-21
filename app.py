from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
import mysql.connector
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Enter_Your_Password",
        database="parking_db"
    )

@app.route("/")
def home():
    return render_template("dashboard.html")

# SLOT STATUS
@app.route("/api/status")
def status():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT parking_slot, exit_time FROM parking_records")
    rows = cur.fetchall()

    slots = {}
    for slot, exit_time in rows:
        slots[slot] = "available" if exit_time else "occupied"

    cur.close()
    conn.close()

    return jsonify(slots)

#  SOCKET NOTIFY
@app.route("/notify")
def notify():
    socketio.emit("update")
    return "OK"

# RUN ENTRY
@app.route("/run-entry")
def run_entry():
    subprocess.Popen(["python", "entry.py"])
    return "Entry started"

# RUN EXIT
@app.route("/run-exit")
def run_exit():
    subprocess.Popen(["python", "exit.py"])
    return "Exit started"

#  RECENT ACTIVITY LOGS
@app.route("/api/logs")
def logs():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT plate_number, parking_slot, entry_time, exit_time, fee
    FROM parking_records
    ORDER BY id DESC
    LIMIT 10
    """)

    rows = cur.fetchall()
    data = []

    for r in rows:
        data.append({
            "plate": r[0],
            "slot": r[1],
            "entry": str(r[2]),
            "exit": str(r[3]) if r[3] else "-",
            "fee": str(r[4]) if r[4] else "-"
        })

    cur.close()
    conn.close()

    return jsonify(data)

if __name__ == "__main__":
    socketio.run(app, debug=True)
