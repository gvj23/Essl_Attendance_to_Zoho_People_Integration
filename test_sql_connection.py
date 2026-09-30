import pyodbc
import mysql.connector

print("🚀 TESTING ESSL MSSQL + MYSQL CONNECTIONS\n")

# ==========================
# MSSQL CONNECTION (Windows)
# ==========================
try:
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

    print("✅ MSSQL CONNECTED SUCCESSFULLY")

    mssql_cursor = mssql_conn.cursor()

    # SQL Server Version
    mssql_cursor.execute("SELECT @@VERSION")
    print("\nSQL Server Version:")
    print(mssql_cursor.fetchone()[0])

    # Database Name
    mssql_cursor.execute("SELECT DB_NAME()")
    print("\nDatabase:")
    print(mssql_cursor.fetchone()[0])

    # List Tables
    print("\nAvailable Tables:")
    mssql_cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE='BASE TABLE'
        ORDER BY TABLE_NAME
    """)

    tables = mssql_cursor.fetchall()

    for table in tables:
        print(" -", table[0])

except Exception as e:
    print("\n❌ MSSQL CONNECTION FAILED")
    print(e)


# ==========================
# MYSQL CONNECTION
# ==========================
try:
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="essl_user",
        password="Admin@123",
        database="essl_zohopeople"
    )

    print("\n✅ MYSQL CONNECTED SUCCESSFULLY")

    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute("SELECT DATABASE();")

    print("Current MySQL Database:", mysql_cursor.fetchone()[0])

except Exception as e:
    print("\n❌ MYSQL CONNECTION FAILED")
    print(e)


# ==========================
# CLOSE CONNECTIONS
# ==========================
try:
    mssql_conn.close()
except:
    pass

try:
    mysql_conn.close()
except:
    pass

print("\n🎉 TEST COMPLETED")
