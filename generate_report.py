import mysql.connector
import pandas as pd
from datetime import date, timedelta

# REPORT DATE (Yesterday)
report_date = date.today() - timedelta(days=1)

# MYSQL CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="essl_user",
    password="Admin@123",
    database="essl_zohopeople"
)

print("✅ GENERATING HR REPORT")

# FETCH SUMMARY DATA
employee_code = ('S016','S027','S038','S039')

query = f"""
SELECT
    employee_code,
    attendance_date,
    first_in,
    last_out,
    total_work_hours,
    total_break_hours,
    total_punches
FROM hr_attendance_report
WHERE employee_code IN ('S016','S027','S038','Temp 7', '1')
AND attendance_date BETWEEN '2026-07-26' AND '2026-08-27'
ORDER BY attendance_date, employee_code
"""

df = pd.read_sql(query, conn)

print(f"✅ Rows Fetched: {len(df)}")

# ----------------------------------
# CONVERT DECIMAL HOURS → HH:MM
# ----------------------------------

def decimal_hours_to_hhmm(hours):

    if pd.isna(hours):
        return ""

    total_minutes = round(float(hours) * 60)

    hrs = total_minutes // 60
    mins = total_minutes % 60

    return f"{hrs:02d}:{mins:02d}"

if not df.empty:

    df["total_work_hours"] = (
        df["total_work_hours"]
        .apply(decimal_hours_to_hhmm)
    )

    df["total_break_hours"] = (
        df["total_break_hours"]
        .apply(decimal_hours_to_hhmm)
    )

# ----------------------------------
# EXPORT TO EXCEL
# ----------------------------------

file_path = f"/root/reports/hr_report_{employee_code}.xlsx"

with pd.ExcelWriter(
    file_path,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Attendance Summary",
        index=False
    )

print(f"✅ HR REPORT GENERATED: {file_path}")

conn.close()
