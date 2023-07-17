import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("Email Sender")

# tab1, tab2 = st.tabs(['Accounts','Message'])
tab1, tab2 = st.columns(2)
with tab1:
    st.header("Sender")
    sender_email = st.text_input("Sending email address", key="sender_email_input")
    app_password = st.text_input('App Password', key="app_password_input")

with tab2:
    st.header("Receiver")
    receiver = st.text_input("Receiving email address", key="receiver_email_input")
    subject = st.text_input('Subject', key="subject_input")
    message = st.text_area('Message', key="message_input")

    # Send button
    if st.button("Send"):
        if not receiver or not subject or not message:
            st.error("Please enter the receiver's email, subject, and message.")
        else:
            try:
                # Create a MIME message
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver
                msg['Subject'] = subject

                # Attach the message to the MIME message
                msg.attach(MIMEText(message, 'plain'))

                # Establish a secure SMTP connection
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, app_password)
                    server.send_message(msg)

                st.write(f"Email sent to {receiver} from {sender_email}")
            except Exception as e:
                st.error(f"Error sending email: {str(e)}")


# def main():
#     # Use sidebar for page navigation
#     st.sidebar.title("Sidebar")

# if __name__ == "__main__":
#     main()