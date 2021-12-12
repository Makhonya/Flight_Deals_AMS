from twilio.rest import Client
import os
import smtplib

auth_id = os.getenv('auth_id')
auth_token = os.getenv('auth_token')

MY_EMAIL = os.getenv('my_email')
MY_PASSWORD = os.getenv('my_password')

class NotificationManager:
    # def __init__(self):
    #     self.client = Client(auth_id, auth_token)

    # def send_message(self, message):
    #     # Send SMS
    #     sms = self.client.messages.create(
    #         from_='+12184604394',
    #         to='+31636061086',
    #         body=message
    #     )
    #     print(sms.status)

    def send_email(self, names, emails, link, message):
        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            for name, email in zip(names, emails):
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Dear {name},\n\n {message}\n\n{link}"
                )