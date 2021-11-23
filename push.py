# Import smtplib for the actual sending function
import smtplib


def email_alert():
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("kommandoapp@gmail.com", "project!")
    server.sendmail("kommandoapp@gmail.com",
                 "it490proj2@gmail.com", 
                 "Your trade has been executed ")

    server.quit()


email_alert()