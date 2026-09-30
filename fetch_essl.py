import pyodbc
import mysql.connector

print("🚀 FETCHING FROM ESSL (MSSQL)")

# MSSQL CONNECTION
mssql_conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=192.168.1.50,1433;"
    "DATABASE=etimetracklitenew;"
    "UID=essl;"
    "PWD=essl;"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=10;"
)

mssql_cursor = mssql_conn.cursor()

# MYSQL CONNECTION
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="essl_user",
    password="Admin@123",
    database="essl_zohopeople"
)

mysql_cursor = mysql_conn.cursor()
print("\n===== MSSQL CHECK =====")

mssql_cursor.execute("SELECT @@SERVERNAME")
print("SERVER :", mssql_cursor.fetchone())

mssql_cursor.execute("SELECT DB_NAME()")
print("DATABASE :", mssql_cursor.fetchone())

mssql_cursor.execute("SELECT MAX(LogDateTime) FROM Atten_Logs")
print("MAX DATE :", mssql_cursor.fetchone())

print("=======================\n")


# FETCH FROM MSSQL
query="""SELECT
    EmployeeCode,
    LogDateTime,
    Direction
FROM Atten_Logs
WHERE LogDateTime >= DATEADD(day,-2,GETDATE())
ORDER BY LogDateTime ASC;
"""

mssql_cursor.execute(query)
rows = mssql_cursor.fetchall()

print(f"✅ FETCHED {len(rows)} FROM ESSL")

# INSERT INTO MYSQL
insert_query = """
INSERT IGNORE INTO raw_logs (employee_code, log_datetime, direction)
VALUES (%s, %s, %s)
"""

count = 0

for row in rows:
    mysql_cursor.execute(insert_query, (
        row[0], row[1], row[2]
    ))
if mysql_cursor.rowcount > 0:
    count += 1

mysql_conn.commit()

print(f"✅ INSERTED {count} INTO MYSQL raw_logs")

# CLOSE
mssql_cursor.close()
mssql_conn.close()
mysql_cursor.close()
mysql_conn.close()

print("✅ ESSL → MYSQL DONE")
