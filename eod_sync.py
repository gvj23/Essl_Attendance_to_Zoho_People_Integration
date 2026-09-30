import os

BASE = "/opt/essl/app/src"
PYTHON = "/opt/essl/venv/bin/python"

print("=== STEP 1 : PROCESS ATTENDANCE ===")
os.system(f"{PYTHON} {BASE}/proccess_attendance.py")

print("=== STEP 2 : SMART ATTENDANCE ENGINE ===")
os.system(f"{PYTHON} {BASE}/smart_attendance_engine.py")

print("=== STEP 3 : ZOHO SYNC ===")
os.system(f"{PYTHON} {BASE}/sync_attendance.py")

print("=== STEP 4 : ZOHO LEAVE SYNC ===")
os.system(f"{PYTHON} {BASE}/sync_leave.py")
