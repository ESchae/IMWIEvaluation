import mail
import unittest
import os
import shutil
import re

# TODO: add more tests


class MailTest(unittest.TestCase):

    maxDiff = None  # enable output of long string

    def setUp(self):
        self.mail_server = mail.MailServer('from@domain.com',
                                           'smtp.server.com', 123, 'password')
        # generate folder containing attachment files
        os.mkdir('attachments')
        self.attachment_files = ['attachments/a1.csv', 'attachments/a2.csv']
        for attachment_file in self.attachment_files:
            with open(attachment_file, 'w') as f:
                f.write('namet\taddress')

    def tearDown(self):
        shutil.rmtree('attachments')

    def test_prepare_msg(self):
        to_mail_address = 'to@domain.com'
        subject = 'a subject'
        text = 'hello there'
        msg = self.mail_server._prepare_msg(to_mail_address, subject, text,
                                            self.attachment_files)
        self.assertEqual(msg['Subject'], 'a subject')


if __name__ == '__main__':
    unittest.main()


