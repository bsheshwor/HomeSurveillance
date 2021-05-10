import smtplib
from email.message import EmailMessage
from playsound import playsound

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = 'gaurabstha001@gmail.com'
    msg['from'] = user
    password = 'pgvrykietyiugmxf'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    for i in range(5):
        i = playsound('ALert.wav')


    server.quit()


email_alert("Security Alert!!", "Someone just trespassed your property!! ", "shresthanaruto97@gmail.com")
 