import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email details
sender_email = "harshsapla03@gmail.com"
receiver_email = "harshhyadav2606@gmail.com"
subject = "Test Email"
body = "This is a test email sent from Python!"

# Create MIMEText object
msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = receiver_email

try:
    # Connect to the SMTP server
    print("Connecting to SMTP server...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        # Use your app-specific password here
        server.login(sender_email, "zpry ayup joxf eleg")  # Replace with app-specific password
        print("Login successful.")
        server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
        print("Email sent successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
