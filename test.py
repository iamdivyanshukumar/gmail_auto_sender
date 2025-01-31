import os

CSV_FILE = "participants.csv"

if not os.path.exists(CSV_FILE):
    print(f"Error: CSV file '{CSV_FILE}' not found!")
    exit(1)

# Configuration - Use correct SMTP details
SMTP_SERVER = "smtp.gmail.com"  # Correct Gmail SMTP server
SMTP_PORT = 587
YOUR_EMAIL = os.getenv("divyanshussa2@gmail.com")  # Store email in an environment variable
YOUR_PASSWORD = os.getenv("wpelxnaupguhlzwi")  # Store app password securely