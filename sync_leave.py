import requests
import mysql.connector
from datetime import datetime

# =====================================================
# ZOHO CONFIG
# =====================================================

CLIENT_ID = "1000.22RMIEUJD3GZVEVDIUVPWQPV4Q52DN"
CLIENT_SECRET = "9fccf7b52e3f9ae3303a47c11cdf6f930ac1bcd55d"
REFRESH_TOKEN = "1000.7c4f65209f5e80e34ed5380f24558979.93f69d5716b40c3097790a05e2f6858c"
# =====================================================
# ACCESS TOKEN
# =====================================================

def get_access_token():

    response = requests.post(
        "https://accounts.zoho.in/oauth/v2/token",
        data={
            "refresh_token": REFRESH_TOKEN,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token"
        },
        timeout=30
    )

    response.raise_for_status()

    token_data = response.json()

    if "access_token" not in token_data:
        raise Exception(
            f"Unable to generate access token : {token_data}"
        )

    return token_data["access_token"]

# =====================================================
# EPOCH CONVERTER
# =====================================================

def convert_epoch(epoch_value):

    try:

        if not epoch_value:
            return None

        return datetime.fromtimestamp(
            int(epoch_value) / 1000
        )

    except:
        return None

# =====================================================
# MYSQL
# =====================================================

conn = mysql.connector.connect(
    host="localhost",
    user="essl_user",
    password="Admin@123",
    database="essl_zohopeople"
)

cursor = conn.cursor()

# =====================================================
# TOKEN
# =====================================================

ACCESS_TOKEN = get_access_token()

HEADERS = {
    "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"
}

# =====================================================
# FETCH LEAVES
# =====================================================

URL = "https://people.zoho.in/people/api/forms/leave/getRecords"

print("=" * 80)
print("FETCHING LEAVE DATA FROM ZOHO")
print("=" * 80)

response = requests.get(
    URL,
    headers=HEADERS,
    timeout=60
)

response.raise_for_status()

data = response.json()

if "response" not in data:
    raise Exception("Invalid Zoho response")

if "result" not in data["response"]:
    raise Exception("No leave records found")

records = data["response"]["result"]

print(f"Total Leave Groups : {len(records)}")

# =====================================================
# PROCESS RECORDS
# =====================================================

processed = 0

for item in records:

    for leave_group_id, leave_rows in item.items():

        for leave in leave_rows:

            try:

                employee_text = leave.get(
                    "Employee_ID",
                    ""
                )

                employee_code = ""

                parts = employee_text.split()

                if parts:
                    employee_code = parts[-1]

                leave_type = leave.get(
                    "Leavetype",
                    ""
                )

                from_date = datetime.strptime(
                    leave.get("From"),
                    "%d-%b-%Y"
                ).date()

                to_date = datetime.strptime(
                    leave.get("To"),
                    "%d-%b-%Y"
                ).date()

                days_taken = float(
                    leave.get("Daystaken", 0)
                )

                approval_status = leave.get(
                    "ApprovalStatus",
                    ""
                )

                zoho_leave_id = str(
                    leave.get("Zoho_ID")
                )

                created_time = convert_epoch(
                    leave.get("CreatedTime")
                )

                modified_time = convert_epoch(
                    leave.get("ModifiedTime")
                )

                cursor.execute("""
                INSERT INTO employee_leave
                (
                    employee_code,
                    leave_type,
                    from_date,
                    to_date,
                    days_taken,
                    approval_status,
                    zoho_leave_id,
                    created_time,
                    modified_time
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s
                )
                ON DUPLICATE KEY UPDATE
                    leave_type=VALUES(leave_type),
                    days_taken=VALUES(days_taken),
                    approval_status=VALUES(approval_status),
                    modified_time=VALUES(modified_time)
                """,
                (
                    employee_code,
                    leave_type,
                    from_date,
                    to_date,
                    days_taken,
                    approval_status,
                    zoho_leave_id,
                    created_time,
                    modified_time
                ))

                processed += 1

                print(
                    f"[OK] {employee_code} | "
                    f"{leave_type} | "
                    f"{from_date}"
                )

            except Exception as e:

                print(
                    f"[ERROR] Leave ID {leave_group_id}"
                )

                print(e)

# =====================================================
# COMMIT
# =====================================================

conn.commit()

print("\n" + "=" * 80)
print(f"TOTAL LEAVES PROCESSED : {processed}")
print("=" * 80)

cursor.close()
conn.close()

print("LEAVE SYNC COMPLETED")
