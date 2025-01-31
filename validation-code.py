import smtplib
import dns.resolver
from fpdf import FPDF

# Allowed email domains
ALLOWED_DOMAINS = {"gmail.com", "icloud.com", "hotmail.com", "outlook.com", "yahoo.com"}

# Function to get the MX record for a domain
def get_mx_record(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = records[0].exchange.to_text()
        return mx_record
    except Exception as e:
        print(f"Failed to get MX record for domain {domain}: {e}")
        return None

# Function to verify if the email exists using SMTP
def verify_email(email):
    try:
        domain = email.split('@')[-1]
        
        # Check if domain is allowed
        if domain not in ALLOWED_DOMAINS:
            print(f"Domain {domain} is not allowed.")
            return False
        
        mx_record = get_mx_record(domain)
        if not mx_record:
            print(f"Domain {domain} has no MX records.")
            return False

        # Connect to the mail server
        server = smtplib.SMTP(mx_record)
        server.set_debuglevel(0)

        # SMTP Handshake
        server.helo('gmail.com')
        server.mail('dukascopy.bank1@gmail.com')

        # Check if the recipient email exists
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return True
        else:
            print(f"Failed to verify email {email}")
            return False

    except Exception as e:
        print(f"Error verifying email {email}: {e}")
        return False

# Function to read the email list from a file
def read_email_list(file_path):
    try:
        with open(file_path, 'r') as file:
            email_list = [line.strip() for line in file.readlines() if line.strip()]
        return email_list
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

# Main function to validate and verify emails from the list
def validate_emails_from_file(file_path):
    email_list = read_email_list(file_path)
    valid_emails = []
    invalid_emails = []

    for email in email_list:
        if verify_email(email):
            valid_emails.append(email)
        else:
            invalid_emails.append(email)
            print(f"Email {email} is invalid or does not exist.")

    return valid_emails, invalid_emails

# Path to the email list file
file_path = 'list.txt'

# Validate the emails from the file
valid, invalid = validate_emails_from_file(file_path)

# Generate PDF report
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

for item in valid:
    pdf.cell(200, 10, txt=item, ln=True, align='L')
pdf.output("valid_emails1.pdf")
