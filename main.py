import os

BASE = "/opt/essl/app/src"
PYTHON = "/opt/essl/venv/bin/python"

print("🚀 STARTING FULL ATTENDANCE PIPELINE\n")

print("📥 Step 1 - Fetching attendance from ESSL...")
os.system(f"{PYTHON} {BASE}/fetch_essl.py")

print("\n📊 Step 2 - Processing attendance...")
os.system(f"{PYTHON} {BASE}/proccess_attendance.py")

print("\n📤 Step 3 - Syncing to Zoho...")
os.system(f"{PYTHON} {BASE}/sync_attendance.py")

print("\n🧠 Step 4 - Running Smart Attendance Engine...")
os.system(f"{PYTHON} {BASE}/smart_attendance_engine.py")

print("\n✅ FULL ATTENDANCE PIPELINE COMPLETED")
