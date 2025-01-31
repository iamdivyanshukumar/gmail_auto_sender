import smtplib
import csv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Directly set the values for testing (you can also use os.environ if needed)
os.environ["EMAIL_USER"] = "your.divyanshussa2@gmail.com"
os.environ["EMAIL_PASS"] = "wpelxnaupguhlzwi"

# Load email and password from environment variables
YOUR_EMAIL = os.getenv("EMAIL_USER")
YOUR_PASSWORD = os.getenv("EMAIL_PASS")

# Debug: Print email and password to verify they are loaded correctly
print("YOUR_EMAIL:", YOUR_EMAIL)
print("YOUR_PASSWORD:", YOUR_PASSWORD)

# Configuration - Update these values
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
CSV_FILE = "participants.csv"
CERTIFICATES_DIR = "iee_certificates"

EMAIL_SUBJECT = "Your Participation Certificate"
EMAIL_BODY_TEMPLATE = """
Hello {name},

Thank you for participating in our event! Please find your participation certificate attached.

Best regards,
Event Team
"""

def send_certificate_emails():
    # Check if the CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file '{CSV_FILE}' not found!")
        return

    # Read the CSV file
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # Debug: Print headers
            print("CSV Headers:", csv_reader.fieldnames)

            # Connect to SMTP server
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(YOUR_EMAIL, YOUR_PASSWORD)
            
            for row in csv_reader:
                try:
                    name = row['name']
                    email = row['email']
                    cert_filename = row['certificate_filename']

                    print(f"Sending to {name} ({email}) with certificate: {cert_filename}")

                    # Create email message
                    msg = MIMEMultipart()
                    msg['From'] = YOUR_EMAIL
                    msg['To'] = email
                    msg['Subject'] = EMAIL_SUBJECT
                    
                    # Add email body
                    body = EMAIL_BODY_TEMPLATE.format(name=name)
                    msg.attach(MIMEText(body, 'plain'))
                    
                    # Attach certificate
                    cert_path = os.path.join(CERTIFICATES_DIR, cert_filename)
                    if not os.path.exists(cert_path):
                        print(f"Certificate file not found: {cert_path}")
                        continue
                    
                    with open(cert_path, "rb") as f:
                        attach = MIMEApplication(f.read(), _subtype="pdf")
                        attach.add_header('Content-Disposition', 'attachment', filename=cert_filename)
                        msg.attach(attach)
                    
                    # Send email
                    server.send_message(msg)
                    print(f"Sent certificate to {name} at {email}")
                
                except Exception as e:
                    print(f"Error sending to {email}: {str(e)}")

            server.quit()
    except Exception as e:
        print(f"Error opening CSV file: {str(e)}")

if __name__ == "__main__":
    send_certificate_emails()
