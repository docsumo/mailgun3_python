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


class TestSendEmail(unittest.TestCase):
    def test_email(self):
        r = mail.send_message(
            "Rushabh Sheth, Docsumo <rushabh.sheth@docsumo.com>",
            "bkrm.dahal@gmail.com",
            "Docsumo: Automate invoice data capture at",
            "welcome_email",
        )
        logger.info(r)
        self.assertEqual(r["message"], "Queued. Thank you.")

    def test_email_with_attachemnt(self):
        r = mail.send_message(
            "Rushabh Sheth, Docsumo <rushabh.sheth@docsumo.com>",
            "bkrm.dahal@gmail.com",
            "Docsumo: Automate invoice data capture at",
            "welcome_email",
            files=["/Users/bikramdahal/Arch/API/mailgun3_python/tests/files/data.pdf"],
        )
        logger.info(r)
        self.assertEqual(r["message"], "Queued. Thank you.")

    def test_email_with_template(self):
        r = mail.send_message_template(
            "Rushabh Sheth, Docsumo <rushabh.sheth@docsumo.com>",
            "bkrm.dahal@gmail.com",
            "Docsumo: Automate invoice data capture at",
            "welcome_email",
            {"company_name": "docsumo", "first_name": "Bikram"},
        )
        logger.info(r)
        self.assertEqual(r["message"], "Queued. Thank you.")


class TestStoreEmail(unittest.TestCase):
    def test_get_logs(self):
        stored_email = mail.get_logs()
        stored_email = stored_email["items"][0]
        url = stored_email["storage"]["url"]
        logger.info(url)
        self.assertEqual(isinstance(url, str), True)

    def test_get_metadata(self):
        stored_email = mail.get_logs()
        stored_email = stored_email["items"][0]
        url = stored_email["storage"]["url"]
        body_mime = mail.get_message_mime(url)["body-mime"]
        meta_data = mail.parse_email_mime(body_mime)
        logger.info(meta_data)
        self.assertEqual(isinstance(meta_data, dict), True)


# class TestValidateEmail(unittest.TestCase):
#     def test_validate_email(self):
#         validate = mail.validated_email("bkrm.dahal@gmail.com")
#         logger.info(validate)
#         self.assertEqual(validate, True)

#     def test_validate_email_not_valid(self):
#         validate = mail.validated_email("bkrmafghfgdhfgd@gmail.com")
#         logger.info(validate)
#         self.assertEqual(validate, False)

if __name__ == "__main__":
    unittest.main()
