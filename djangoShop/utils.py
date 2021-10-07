import threading
from django.core.mail import send_mail

class EmailThreading(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.message,
            'myshop@gmail.com',
            self.recipient_list,
            fail_silently=False
        )


def send_reset_password_mail(subject, message, recipient_list):
    EmailThreading(subject, message, recipient_list).start()