import os
import sys
import unittest
import time

sys.path.insert(0, os.path.abspath("../"))
from mailgun import Mailgun
from loguru import logger


#################
# config ########
#################
mail = Mailgun()


class TestMailgun(unittest.TestCase):
    def test_email(self):
        r = mail.send_message(
            "Rushabh Sheth, Docsumo <rushabh.sheth@docsumo.com>",
            "bkrm.dahal@gmail.com",
            "Docsumo: Automate invoice data capture at",
            "welcome_email",
        )
        self.assertEqual(r["message"], "Queued. Thank you.")

    def test_email_with_attachemnt(self):
        r = mail.send_message(
            "Rushabh Sheth, Docsumo <rushabh.sheth@docsumo.com>",
            "bkrm.dahal@gmail.com",
            "Docsumo: Automate invoice data capture at",
            "welcome_email",
            files=["/Users/bikramdahal/Arch/API/mailgun3_python/tests/files/data.pdf"],
        )
        self.assertEqual(r["message"], "Queued. Thank you.")

    def test_email_with_template(self):
        r = mail.send_message_template(
            "Rushabh Sheth, Docsumo <rushabh.sheth@docsumo.com>",
            "bkrm.dahal@gmail.com",
            "Docsumo: Automate invoice data capture at",
            "welcome_email",
            {"company_name": "docsumo", "first_name": "Bikram"},
        )
        self.assertEqual(r["message"], "Queued. Thank you.")

    def test_get_logs(self):
        stored_email = mail.get_logs()
        stored_email = stored_email["items"][0]
        url = stored_email["storage"]["url"]
        self.assertEqual(isinstance(url, str), True)

    def test_get_metadata(self):
        stored_email = mail.get_logs()
        stored_email = stored_email["items"][0]
        url = stored_email["storage"]["url"]
        body_mime = mail.get_message_mime(url)["body-mime"]
        meta_data = mail.parse_email_mime(body_mime)
        self.assertEqual(isinstance(meta_data, dict), True)


class TestMailList(unittest.TestCase):
    # def test_create_mail_list(self):
    #     data = mail.create_mailing_list('welcome', "Welcome Email")
    #     logger.info(data)
    #     self.assertEqual(isinstance(data, dict), True)

    def test_add_user_mail_List(self):
        data = mail.add_to_mailing_list(
            "welcome",
            {
                "subscribed": True,
                "address": "bkrm.dahal@gmail.com",
                "name": "Bob Bar",
                "description": "Developer",
                "vars": '{"age": 26}',
            },
        )
        logger.info(data)
        self.assertEqual(isinstance(data, dict), True)


if __name__ == "__main__":
    unittest.main()
