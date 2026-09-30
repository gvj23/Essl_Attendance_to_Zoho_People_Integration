import mysql.connector
from collections import defaultdict
from datetime import timedelta, date

# MYSQL CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="essl_user",
    password="Admin@123",
    database="essl_zohopeople"
)

cursor = conn.cursor(dictionary=True)

print("✅ SESSION-BASED SMART ENGINE STARTED")

# CLEAR OLD REPORT
cursor.execute("DELETE FROM hr_attendance_report")
conn.commit()

# FETCH RAW LOGS
query = """
SELECT employee_code, log_datetime
FROM raw_logs
ORDER BY employee_code, log_datetime
"""

cursor.execute(query)
rows = cursor.fetchall()

print(f"✅ FETCHED {len(rows)} LOGS")

# GROUP EMPLOYEE + DATE
attendance = defaultdict(list)

for row in rows:

    emp = row["employee_code"]
    dt = row["log_datetime"]

    attendance_date = dt.date()

    # SKIP TODAY
    if attendance_date == date.today():
        continue

    key = (emp, attendance_date)

    attendance[key].append(dt)

# PROCESS EACH DAY
for (emp, att_date), logs in attendance.items():

    cleaned_logs = []

    previous = None

    # REMOVE DUPLICATE MACHINE TRIGGERS
    for log in logs:

        if previous:

            time_diff = log - previous

            # Ignore duplicate punch within 30 sec
            if time_diff <= timedelta(seconds=30):
                continue

        cleaned_logs.append(log)
        previous = log

    # SKIP IF LESS THAN 2 PUNCHES
    if len(cleaned_logs) < 2:
        continue

    # SORT LOGS
    cleaned_logs.sort()

    # FIRST & LAST
    first_in = cleaned_logs[0]
    last_out = cleaned_logs[-1]

    # CALCULATIONS
    total_work_seconds = 0
    total_break_seconds = 0

    # SESSION LOGIC
    for i in range(len(cleaned_logs) - 1):

        current_punch = cleaned_logs[i]
        next_punch = cleaned_logs[i + 1]

        duration = (
            next_punch - current_punch
        ).total_seconds()

        # EVEN INDEX = WORK SESSION
        if i % 2 == 0:
            total_work_seconds += duration

        # ODD INDEX = BREAK SESSION
        else:
            total_break_seconds += duration

    # CONVERT TO HOURS
    total_work_hours = round(
        total_work_seconds / 3600,
        2
    )

    total_break_hours = round(
        total_break_seconds / 3600,
        2
    )

    # INSERT REPORT
    insert_query = """
    INSERT INTO hr_attendance_report
    (
        employee_code,
        attendance_date,
        first_in,
        last_out,
        total_work_hours,
        total_break_hours,
        total_punches
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(insert_query, (
        emp,
        att_date,
        first_in,
        last_out,
        total_work_hours,
        total_break_hours,
        len(cleaned_logs)
    ))

conn.commit()

print("✅ SESSION REPORT GENERATED")

cursor.close()
conn.close()

print("✅ DONE")
