from twilio.rest import Client
import smtplib

def textMessage(cameraID, phoneNumbs):
    account_sid = 'ACdc90288e56ed2eaaa1c41e39366804ea'
    auth_token = '9a98bff27424f8ad5874abdc126497cf'
    client = Client(account_sid, auth_token)
    message = f"SICK Person Detected:\n{cameraID}"

    for phoneNumb in phoneNumbs:
        client.messages.create(
            body=message,
            from_='+1 347 673 0970',
            to=phoneNumb
        )
def emailMessage(cameraID, emails):
    gmail_user = 'tempcheck.check@gmail.com'
    gmail_password = 'assimo11!'

    sent_from = gmail_user
    subject = 'Sick Person Detected:'
    body = f"SICK Person Detected:\n{cameraID}"

    email_text = """\
    From: %s
    To: %s
    Subject: %s
    \n
    %s
    """ % (sent_from, ", ".join(emails), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, emails, email_text)
        server.close()
    except:
        pass



	
