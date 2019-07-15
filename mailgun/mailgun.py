"""Mailgun class to send email and get extracted data"""
import os
import json

import requests
from loguru import logger


from .email_parsing import parse_mail
from .error import NoAPIKey, NoDomain


class Mailgun:
    """
    Initializes an object of Mailgun class.

    Args:
        apiKey:``str``
            API key provided to user.
        domain:``str``
            Your domain for mailgun
        version:``str``
            API version.
    Returns:
        Mailgun class object.            
    """

    def __init__(self, apikey: str = None, domain: str = None, version: str = "v3"):

        if apikey:
            self.apikey = apikey
        else:
            self.apikey = os.getenv("MAILGUN_API_KEY", None)
            if not self.apikey:
                raise NoAPIKey("Either pass apikey or set env `MAILGUN_API_KEY`")

        if domain:
            self.domain = domain
        else:
            self.domain = os.getenv("MAILGUN_DOMAIN", None)
            if not self.domain:
                raise NoDomain("Either pass domain or set env `MAILGUN_DOMAIN`")

        self.version = version
        self.base_url = "https://api.mailgun.net/{}/".format(self.version)

        self.auth = ("api", self.apikey)

    def send_message(
        self,
        from_: str,
        to: str,
        subject: str,
        html_body: str = None,
        text_body: str = None,
        files: list = None,
    ):

        """
        Send email

        Args:
            from_: ``str``
                example "Test email <test@docsumo.com>"
            to: ``str``
                user email id
            subject: ``str``
            html_body: ``str``
            text_body: ``str``
            files: ``list``
                list of files

        Return:
            Response from API: ``json``

                .. code-block:: json

                    {'id': '<20190714191959.1.D7B53FD6D5077D03@mg.docsumo.com>',
                    'message': 'Queued. Thank you.'}


        Example:

            .. code-block:: python

                send_message(None, "bkrm.dahal@gmail.com", 
                "Docsumo: Automate invoice data capture at Docsumo", 'welcome_email', 
                files=['/Users/bikramdahal/Downloads/backup_image/savage and palmer/Behariji Enterprises - BE 32 19-20 DONE.pdf'])

        """
        if text_body:
            body = {"text": text_body}
        else:
            body = {}

        if html_body:
            body.update({"html": html_body})

        data = {
            "from": from_ or "Rushabh Sheth, Docsumo <rushabh.sheth@docsumo.com>",
            "to": to,
            "subject": subject,
        }
        data.update(body)

        # add files
        if files:
            attachment = []
            for f in files:
                filename = os.path.basename(f)
                with open(f, "rb") as f:
                    object_buffer = f.read()
                attachment.append(("attachment", (filename, object_buffer)))
            url = self.base_url + "{}/messages".format(self.domain)
            response = requests.post(url, auth=self.auth, data=data, files=attachment)

        else:
            url = self.base_url + "{}/messages".format(self.domain)
            response = requests.post(url, auth=self.auth, data=data)
        return response.json()

    def send_message_template(
        self, from_: str, to: str, subject: str, template_name: str, data: dict
    ):
        """
        Send email using template

        Args:
            from_: ``str``
                example "Test email <test@docsumo.com>"
            to: ``str``
                user email id
            subject: ``str``
            template_name: ``str``
            data: ``str``
                data for template make string from dict using ``json.dumps``

        Return:
            Response from API: ``json``

                .. code-block:: json

                    {'id': '<20190714191959.1.D7B53FD6D5077D03@mg.docsumo.com>',
                    'message': 'Queued. Thank you.'}


        Example:

            .. code-block:: python

                send_message_template(None, "bkrm.dahal@gmail.com", 
                "Docsumo: Automate invoice data capture at Docsumo", 'welcome_email', 
                {"company_name": "docsumo", "first_name": "bikram"})

        """
        payload = {
            "from": from_ or "Rushabh Sheth, Docsumo <rushabh.sheth@docsumo.com>",
            "to": to,
            "subject": subject,
            "template": template_name,
            "h:X-Mailgun-Variables": json.dumps(data),
        }
        url = self.base_url + "{}/messages".format(self.domain)
        response = requests.post(url, auth=self.auth, data=payload)
        return response.json()

    def get_logs(self, params={"event": "stored"}):
        """
        Logs

        Args:
            Params: ``dict``
                filter for logs. 
        
        Return:
            logs dicts: ``dict``

        """
        url = self.base_url + "{}/events".format(self.domain)
        response = requests.get(url, auth=self.auth, params=params)
        return response.json()

    def create_mailing_list(self, list_name: str, description: str):
        """
        Create new mailing list

        Args:
            list_name: ``str``
            description: ``str``
        
        Return:
            Response dict: ``dict``

        """
        url = self.base_url + "{}/lists".format(self.domain)
        response = requests.post(
            url,
            auth=self.auth,
            data={
                "address": "{}@{}".format(list_name, self.domain),
                "description": description,
            },
        )
        return response.json()

    def add_to_mailing_list(self, list_name, data):

        """add user to list 
        Args:
            list_name: ``str``
            data: ``dict``
                data of user

                    .. code-block:: json
                    
                        {'subscribed': True,
                        'address': 'bar@example.com',
                        'name': 'Bob Bar',
                        'description': 'Developer',
                        'vars': '{"age": 26}'}

        Return:
            Rsponses from API: ``dict``
        """
        url = self.base_url + "lists/{}@{}/members".format(list_name, self.domain)
        response = requests.post(url, auth=self.auth, data=data)
        return response.json()

    def validated_email(self, email: str):
        """
        Validate the Email

        Args:
            email: ``str``
        
        Return:
            valid True or false: ``bool``

        """

        response = requests.get(
            "https://api.mailgun.net/v4/address/validate",
            auth=self.apikey,
            params={"address": email},
        )

        # if validate
        data = response.json()
        risk = data.get("risk", "empty")

        if risk in ["empty", "low", "medium"]:
            return True
        else:
            return False

    def get_message_mime(self, url):
        """
        get email mime to parse email

        Args:
            url: ``str``
                image storage url
        
        Return:
            json with body-mime: ``dict``
        """
        headers = {"Accept": "message/rfc2822"}

        # let's make a request to the API
        r = requests.get(url, auth=self.auth, headers=headers)
        return r.json()

    def parse_email_mime(self, body_mime, email_id: str = None):
        """
        parse email-mime

        Args:
            body-mime: ``str``
        
        Return:
            Metadata and file saved in tmp dir: ``dict``
        """
        metadata = parse_mail(body_mime, email_id, "tmp")
        return metadata

    def __str__(self):
        return "Mailgun API"

    def __repr__(self):
        return "Mailgun API"