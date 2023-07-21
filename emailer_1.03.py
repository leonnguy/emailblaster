import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send an email
def send_email(sender_email, app_password, recipient_email, subject, message):
    try:
        # SMTP server settings
        smtp_server = "smtp.gmail.com"
        port = 587

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the message to the email
        msg.attach(MIMEText(message, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Streamlit app
def main():
    st.title("Email Sender App")
    st.write("Upload a CSV or Excel file with columns 'sender_email' and 'app_password'.")

    # File uploader for CSV and Excel files
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Read the uploaded file into a DataFrame
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

        # Sidebar with the uploaded file's information
        st.sidebar.header("Uploaded File Details")
        st.sidebar.write(f"Number of Rows: {df.shape[0]}")
        st.sidebar.write(f"Number of Columns: {df.shape[1]}")

        # Create the UI for sending emails
        st.header("Send Emails")
        recipient_email = st.text_input("Recipient Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        send_button = st.button("Send Emails")

        if send_button:
            st.write("Sending emails...")
            for index, row in df.iterrows():
                sender_email = row['sender_email']
                app_password = row['app_password']

                # Send the email and check for success
                if send_email(sender_email, app_password, recipient_email, subject, message):
                    st.success(f"Email sent from {sender_email} successfully!")
                else:
                    st.error(f"Failed to send email from {sender_email}.")

if __name__ == "__main__":
    main()
