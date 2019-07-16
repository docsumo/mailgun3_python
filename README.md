# mailgun3_python
Python client for mailgun.  

[![Documentation Status](https://readthedocs.org/projects/mailgun3-python/badge/?version=latest)](https://mailgun3-python.readthedocs.io/en/latest/?badge=latest)

For detail:
- [Here is Documentation](https://mailgun3-python.readthedocs.io/en/latest/index.html)  


# Install 
```bash
pip install mailgun3_python
```

# Set API KEY from docsumo setting page as env variable `MAILGUN_API_KEY` & ``MAILGUN_DOMAIN`` or pass apikey parameter in Mailgun class.

```bash
export MAILGUN_API_KEY="key-c-fgrt456" >>  ~/.bashrc
export MAILGUN_DOMAIN="example.com" >>  ~/.bashrc
source ~/.bashrc
```

# Example

```python

from mailgun import Mailgun

mailgun = Mailgun()

# send email with attachment 
mailgun.send_message("Text, <test@gmail.com>", 
                    "bkrm.dahal@gmail.com", 
                    "Docsumo: Automate invoice data capture at Docsumo", 
                    'Hi, welcome to docsumo.', 
                    files=['./invoice.pdf'])

# send message with saved template
mailgun.send_message_template("Text, <test@gmail.com>", 
                                "bkrm.dahal@gmail.com", 
                                "Docsumo: Automate invoice data capture at Docsumo", 
                                "welcome_email", 
                                {"company_name": "docsumo", "first_name": "bikram"})
```





