# ESSL Attendance to Zoho People Integration

## Overview

This project automates attendance synchronization between the ESSL Biometric Attendance System and Zoho People.

The solution extracts raw attendance logs from ESSL, processes employee check-in/check-out records, stores intermediate data in MySQL, and automatically updates attendance records in Zoho People using OAuth-based API integration.

Additionally, this repository contains the HR Attendance Portal used for attendance monitoring, reporting, and synchronization management.

---

## Features

### Attendance Processing
- Fetch attendance logs from ESSL database
- Process IN/OUT punches
- Generate daily attendance records
- Handle missing punches
- Store processed attendance in MySQL

### Zoho People Integration
- OAuth 2.0 Authentication
- Automatic Access Token Refresh
- Attendance Sync to Zoho People
- Sync Status Tracking
- Error Logging and Retry Support

### HR Attendance Portal
- Employee Attendance Dashboard
- Attendance Reports
- Sync Monitoring
- Attendance Analytics
- User Management

---

## Project Structure

```text
src/
│
├── fetch_essl.py
├── process_attendance.py
├── smart_attendance_engine.py
├── sync_attendance.py
├── sync_leave.py
├── sync_zoho.py
├── generate_report.py
├── refresh_token.py
├── database.py
├── config.py
├── logger.py
├── utils.py
│
└── HR Portal
```

---

## Technology Stack

### Backend
- Python 3.x
- Flask
- MySQL
- MSSQL

### APIs
- Zoho People API
- OAuth 2.0 Authentication

### Database
- MySQL
- Microsoft SQL Server

### Infrastructure
- Ubuntu Server
- Apache
- Docker (Optional)

---

## Attendance Flow

```text
ESSL Device
      │
      ▼
MSSQL Attendance Logs
      │
      ▼
fetch_essl.py
      │
      ▼
process_attendance.py
      │
      ▼
zoho_ready_logs
      │
      ▼
sync_attendance.py
      │
      ▼
Zoho People
```

---

## Database Tables

### atten_logs
Stores raw attendance records from ESSL.

### daily_attendance
Stores processed daily attendance.

### zoho_ready_logs
Stores attendance records prepared for Zoho sync.

### sync_logs
Stores synchronization status and API responses.

---

## Configuration

Update the configuration values in:

```python
config.py
```

Example:

```python
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REFRESH_TOKEN = "YOUR_REFRESH_TOKEN"
```

---

## Installation

Clone Repository

```bash
git clone https://github.com/gvj23/Essl_Attendance_to_Zoho_People_Integration.git
cd Essl_Attendance_to_Zoho_People_Integration
```

Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Attendance Sync

Fetch Attendance

```bash
python fetch_essl.py
```

Process Attendance

```bash
python process_attendance.py
```

Sync to Zoho

```bash
python sync_attendance.py
```

Generate Reports

```bash
python generate_report.py
```

---

## Logging

Logs are maintained for:

- Attendance Processing
- API Requests
- API Responses
- Sync Failures
- Database Errors

---

## Security

Never commit:

```text
Client ID
Client Secret
Refresh Token
Access Token
Database Passwords
.env Files
```

Add them to:

```text
.gitignore
```

---

## Future Enhancements

- Real-time attendance synchronization
- Employee self-service portal
- Mobile application support
- Multi-branch attendance management
- Advanced analytics dashboard
- Leave synchronization automation

---

## Author

**K. Gunasekaran**

Software Engineer | Linux Administrator | DevOps Enthusiast

GitHub: https://github.com/gvj23

---

## License

This project is intended for internal organizational use.
