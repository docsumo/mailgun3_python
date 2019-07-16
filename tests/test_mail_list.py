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


class TestMailList(unittest.TestCase):
    def test_a_mailing_list_create(self):
        data = mail.mailing_list_create("test", "Welcome Email")
        logger.info(data)
        self.assertEqual(isinstance(data, dict), True)

    def test_b_mailing_list_add_email(self):
        data = mail.mailing_list_add_email(
            "test",
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

    def test_c_mailing_list_update_email(self):
        data = mail.mailing_list_update_email(
            "test", "bkrm.dahal@gmail.com", {"subscribed": False, "name": "Testing Bar"}
        )
        logger.info(data)
        self.assertEqual(isinstance(data, dict), True)

    def test_d_mailing_list_delete_email(self):

        data = mail.mailing_list_delete_email("test", "bkrm.dahal@gmail.com")
        logger.info(data)
        self.assertEqual(isinstance(data, dict), True)

    def test_e_mailing_list_delete(self):
        data = mail.mailing_list_delete("test")
        logger.info(data)
        self.assertEqual(isinstance(data, dict), True)


if __name__ == "__main__":
    unittest.main()
