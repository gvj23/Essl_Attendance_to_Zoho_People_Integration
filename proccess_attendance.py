import mysql.connector
from collections import defaultdict
from datetime import date, timedelta

# MYSQL CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="essl_user",
    password="Admin@123",
    database="essl_zohopeople"
)

cursor = conn.cursor(dictionary=True)

print("✅ MYSQL CONNECTED")

# -----------------------------
# FETCH RAW LOGS
# -----------------------------
cursor.execute("""
SELECT employee_code,
       log_datetime,
       direction
FROM raw_logs
ORDER BY employee_code, log_datetime
""")

rows = cursor.fetchall()

print(f"✅ FETCHED {len(rows)} RAW LOGS")

# -----------------------------
# GROUP BY EMPLOYEE + DATE
# -----------------------------
attendance = defaultdict(list)

for row in rows:

    emp = str(row["employee_code"]).strip()

    dt = row["log_datetime"]

    direction = str(row["direction"]).lower().strip()

    # Skip machine duplicate
    if direction == "255":
        continue

    attendance[(emp, dt.date())].append({
        "time": dt,
        "direction": direction
    })

print(f"✅ EMPLOYEE DAYS : {len(attendance)}")

# -----------------------------
# INSERT QUERY
# -----------------------------
insert_query = """
INSERT INTO zoho_ready_logs
(
employee_code,
attendance_date,
check_in,
check_out
)
VALUES
(
%s,%s,%s,%s
)
ON DUPLICATE KEY UPDATE
check_in=VALUES(check_in),
check_out=VALUES(check_out),
sync_status='pending'
"""

inserted = 0

# -----------------------------
# PROCESS
# -----------------------------
for (emp, att_date), logs in attendance.items():

    # Skip today
    if att_date == date.today():
        continue

    logs.sort(key=lambda x: x["time"])

    cleaned = []

    previous = None

    # Remove duplicate punches within 30 seconds
    for log in logs:

        if previous:

            diff = (
                log["time"] -
                previous["time"]
            ).total_seconds()

            if (
                diff <= 30 and
                log["direction"] == previous["direction"]
            ):
                continue

        cleaned.append(log)
        previous = log

    if len(cleaned) == 0:
        continue

    # -----------------------------
    # FIND FIRST IN
    # -----------------------------
    check_in = None

    for log in cleaned:

        if log["direction"] == "in":
            check_in = log["time"]
            break

    if check_in is None:
        check_in = cleaned[0]["time"]

    # -----------------------------
    # FIND LAST OUT
    # -----------------------------
    check_out = None

    for log in reversed(cleaned):

        if log["direction"] == "out":
            check_out = log["time"]
            break

    if check_out is None:
        check_out = cleaned[-1]["time"]

    # Ignore if checkout before checkin
    if check_out < check_in:
        check_out = check_in

    cursor.execute(
        insert_query,
        (
            emp,
            att_date,
            check_in,
            check_out
        )
    )

    inserted += 1

conn.commit()

print(f"✅ INSERTED {inserted} RECORDS")

cursor.close()
conn.close()

print("✅ PROCESSING COMPLETED")
