Install
========
   .. code-block:: bash

        pip install mailgun3_python

Mailgun Examples
================

.. code-block:: python

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