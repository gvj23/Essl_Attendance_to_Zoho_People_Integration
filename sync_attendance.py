import mysql.connector
import requests
import time
import sys

# =====================================================
# ZOHO CONFIG
# =====================================================

CLIENT_ID = "1000.22RMIEUJD3GZVEVDIUVPWQPV4Q52DN"
CLIENT_SECRET = "9fccf7b52e3f9ae3303a47c11cdf6f930ac1bcd55d"
REFRESH_TOKEN = "1000.7c4f65209f5e80e34ed5380f24558979.93f69d5716b40c3097790a05e2f6858c"


ZOHO_URL = "https://people.zoho.in/people/api/attendance"

# =====================================================
# GET ACCESS TOKEN
# =====================================================

def get_access_token():
    url = "https://accounts.zoho.in/oauth/v2/token"

    payload = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=payload)
    response.raise_for_status()
    token = response.json()

    if "access_token" not in token:
        raise Exception(f"Unable to generate access token: {token}")

    return token["access_token"]


ACCESS_TOKEN = get_access_token()

HEADERS = {
    "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# =====================================================
# MYSQL
# =====================================================

conn = mysql.connector.connect(
    host="localhost",
    user="essl_user",
    password="Admin@123",
    database="essl_zohopeople"
)

cursor = conn.cursor(dictionary=True)

# =====================================================
# FETCH PENDING RECORDS
# =====================================================

from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

cursor.execute("""
SELECT *
FROM zoho_ready_logs
WHERE sync_status = 'pending'
AND DATE(attendance_date) = %s
ORDER BY attendance_date ASC, id ASC
""", (yesterday,))

rows = cursor.fetchall()

print("=" * 80)
print(f"Total Records Found : {len(rows)}")
print("=" * 80)



if not rows:
    print("No pending attendance records found for today.")
    cursor.close()
    conn.close()
    sys.exit()

# =====================================================
# START SYNC
# =====================================================

for row in rows:

    try:

        payload = {
            "dateFormat": "yyyy-MM-dd HH:mm:ss",
            "empId": row["employee_code"],
            "checkIn": str(row["check_in"]),
            "checkOut": str(row["check_out"])
        }

        print("\n" + "=" * 80)
        print("Employee Code   :", row["employee_code"])
        print("Attendance Date :", row["attendance_date"])
        print("Check In        :", row["check_in"])
        print("Check Out       :", row["check_out"])
        print("\nPayload")
        print(payload)
        print("=" * 80)

        response = requests.post(
            ZOHO_URL,
            headers=HEADERS,
            data=payload,
            timeout=30
        )

        response_text = response.text.lower()

        print("\nZoho Response")
        print("HTTP Status :", response.status_code)
        print("Response    :", response.text)

        # Threshold
        if '"code":7209' in response_text:
            print("\nAPI Threshold Exceeded. Stopping sync.")
            break

        # Decide status
        if (
            "duplicate check-in" in response_text
            or "duplicate check-out" in response_text
        ):
            status = "success"
            print("Result : Duplicate -> SUCCESS")

        elif (
            response.status_code == 200
            and "success" in response_text
            and "failure" not in response_text
        ):
            status = "success"
            print("Result : SUCCESS")

        elif "invalid user" in response_text:
            status = "failed"
            print("Result : INVALID USER")

        else:
            status = "failed"
            print("Result : FAILED")

        cursor.execute("""
        UPDATE zoho_ready_logs
        SET sync_status=%s,
            zoho_response=%s
        WHERE id=%s
        """, (
            status,
            response.text,
            row["id"]
        ))

        conn.commit()

        print(f"Database Updated : {status}")
        print("=" * 80)

        time.sleep(2)

    except Exception as e:
        print("ERROR :", e)

        cursor.execute("""
        UPDATE zoho_ready_logs
        SET sync_status='failed',
            zoho_response=%s
        WHERE id=%s
        """, (
            str(e),
            row["id"]
        ))

        conn.commit()
        time.sleep(2)

cursor.close()
conn.close()

print("\n===================================")
print("Zoho Attendance Sync Completed")
print("===================================")
