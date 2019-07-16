.. email documentation master file, created by
   sphinx-quickstart on Thu Aug  9 13:47:11 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Mailgun python client documentation!
===============================================

Install
========
   .. code-block:: bash

        pip install mailgun3_python

Examples
========

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

Examples
========

.. toctree::
   :maxdepth: 2

   examples

Mailgun Class
=============

.. toctree::
   :maxdepth: 2

   main_class

Mailgun Utils
=============

.. toctree::
   :maxdepth: 2

   utils


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
