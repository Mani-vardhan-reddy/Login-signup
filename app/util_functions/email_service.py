import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from app.core.config import settings

class SMTPService():
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user_name = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        self.mail_from = settings.SMTP_FROM_EMAIL
        self.from_name = settings.SMTP_FROM_NAME
        self.use_tls = settings.SMTP_TLS
        self.use_ssl = settings.SMTP_SSL
        
    def _get_server(self):
        
        try:
            if self.use_ssl:
                server = smtplib.SMTP_SSL(self.host, self.port)
                
            else:
                server = smtplib.SMTP(self.host, self.port)
                if self.use_tls:
                    server.starttls()
                    
            server.login(self.user_name, self.password)
            return server
        except Exception as e:
            raise Exception(f"SMTP Connection error: {e}")
        
    def send_mail(self, to_email: str, subject: str, body: str, html=False):
        """
        send plain text or html email
        """
        message = MIMEMultipart("alternative")
        message['From'] = formataddr((self.from_name, self.mail_from))
        message['To'] = to_email
        message['Subject'] = subject
        
        if html:
            part = MIMEText(body, 'html')
            
        else:
            part = MIMEText(body, 'plain')
            
        message.attach(part)
        
        try:
            server = self._get_server()
            server.sendmail(self.mail_from, to_email, message.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"Error sending mail: {e}")
            return False