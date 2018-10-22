"""
Copyright 2018
Author: Elke Schaechtele

Module for automated sending of emails using python.
"""
import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


class MailServer(object):

    def __init__(self, from_mail_address, smtp_server, port, password):
        """ Initialise the mail server and logger.
        
        :param from_mail_address: Adress that sends mail :type str
        :param smtp_server: The smtp server :type str
        :param port: The port :type int
        :param password: Password of sending mail account :type str
        """
        self.from_mail_address = from_mail_address
        self.smtp_server = smtp_server
        self.port = port
        self.password = password
        self.server = None
        self.logger = logging.getLogger(__name__)
        self.logger.info('Hi there')

    def _initialise_server_connection(self):
        """ Login to mail account with password.
        
        :return: None 
        """
        self.server = smtplib.SMTP(self.smtp_server, self.port)
        self.server.starttls()
        self.server.login(self.from_mail_address, self.password)

    def send(self, to_mail_address, subject, text, attachment_files):
        msg = self._prepare_msg(to_mail_address, subject, text,
                                attachment_files)
        self._initialise_server_connection()
        try:
            result = self.server.sendmail(self.from_mail_address,
                                          to_mail_address, msg.as_string())
            self.logger.info('Mail sent from %s to %s (attachments: %s)' %
                             (self.from_mail_address, to_mail_address,
                              attachment_files))
        except:
            self.logger.info('An error occured. Recieved result: %s' % result)
            raise
        self.server.quit()

    def _prepare_msg(self, to_mail_address, subject, text, attachment_files):
        msg = MIMEMultipart()
        msg['From'] = self.from_mail_address
        msg['To'] = to_mail_address
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text))  # add the e-mail text
        # add all attached files as base64 encoded strings
        for attachment_file in attachment_files:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attachment_file, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' %
                            os.path.basename(attachment_file))
            msg.attach(part)
        return msg