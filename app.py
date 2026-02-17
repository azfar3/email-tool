import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender_email, password, receiver_email, subject, body):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False


st.title("Bulk Email Automator")

with st.sidebar:
    st.header("Login Details")
    sender_mail = st.text_input("Sender Email (Gmail)")
    app_password = st.text_input(
        "App Password",
        type="password",
        help="Create 'App Password' from GMAIL Settigns.",
    )

st.subheader("Step 1: Template Design")
subject = st.text_input(
    "Email Subject", value="IMARAT - Legal Ops Agreement Ready for Collection"
)
template = st.text_area(
    "Email Body",
    value="Dear Concerned,\n\nPlease note that we have received the executed Agreement from the authorized signatories.\n\n{id}\t{name}\n\n\nAt this point in time the Agreement(s) are in legal Operation Department located at Mall of IMARAT (MOI), 11th Floor. Please confirm if the Client will collect the same or you require us to dispatch the same to our POCs in various offices.\n\nLooking forward to your kind confirmation enabling us to proceed accordingly.\n\nKind Regards,\nSyed Murtaza Abbas\nIMARAT Legal Operations",
    height=150,
)
st.info("Tip: Use {name} and {id} in the text above.")

st.subheader("Step 2: Recipient Details")
data_input = st.text_area(
    "Enter Data (Format: email,name,id - in one line for each recipient)",
    placeholder="ali@example.com,Ali,101\nsara@example.com,Sara,102",
)

if st.button("Send All Emails"):
    if not sender_mail or not app_password:
        st.warning("Fill login Details first.")
    else:
        lines = data_input.strip().split("\n")
        success_count = 0

        for line in lines:
            try:
                email, name, uid = line.split(",")
                personalized_body = template.replace("{name}", name.strip()).replace(
                    "{id}", uid.strip()
                )
                personalized_subject = subject.replace("{name}", name.strip())

                if send_email(
                    sender_mail,
                    app_password,
                    email.strip(),
                    personalized_subject,
                    personalized_body,
                ):
                    st.success(f"Sent to: {name} ({email})")
                    success_count += 1
            except:
                st.error(f"Wrong Format: {line}")

        st.balloons()
        st.write(f"Total {success_count} emails send successfully!")
