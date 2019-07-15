"""Once data are store in s3, parse and upload to s3"""
import email
import os
import json
import glob
import zipfile
import urllib.parse
from io import BytesIO
import shutil
import uuid

import requests


# s3 = boto3.client("s3")
allowed_file = (".png", ".jpg", ".tiff", ".jpeg", ".pdf")


def parse_mail(email_string: str, email_id: str, output_dir: str = "tmp"):
    """parse email and save the file"""

    msg = email.message_from_string(email_string)

    # metdata
    metadata = {
        "from": msg["From"],
        "to": msg["To"],
        "date": msg["Date"],
        "subject": msg["Subject"],
    }

    # make output dir
    # if not os.path.exists(output_dir):
    # if exist remove folder and make new folder

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = glob.glob(os.path.join(output_dir, "*"))
    try:
        for f in files:
            os.remove(f)
    except:
        print(">>>> No files")

    # parse body and attachment
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))

            # skip any text/plain (txt) attachments
            if ctype == "text/plain" and "attachment" not in cdispo:
                metadata["body"] = part.get_payload(decode=True).decode(
                    "utf-8"
                )  # decode

            elif part.get_filename():
                filepath = os.path.join(output_dir, part.get_filename())
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
    else:
        metadata["body"] = str(msg.get_payload(decode=True))

    # unzip file
    file_paths = glob.glob(output_dir + "/*.zip")

    if file_paths:
        for f in file_paths:
            with zipfile.ZipFile(f, "r") as zip_ref:
                zip_ref.extractall(output_dir)

    # all files
    file_paths = glob.glob(output_dir + "/*")
    tmp_file_path = []
    for f in file_paths:
        _, ext = os.path.splitext(os.path.basename(f))
        if ext in allowed_file:
            tmp_file_path.append(f)

    metadata["files"] = tmp_file_path
    metadata["email_name"] = email_id
    return metadata


# def send_data(event, context):
#     # print("Received event: " + json.dumps(event, indent=2))

#     # Get the object from the event and show its content type
#     bucket = event["Records"][0]["s3"]["bucket"]["name"]
#     key = urllib.parse.unquote_plus(
#         event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
#     )

#     if "AMAZON_SES_SETUP_NOTIFICATION" in key:
#         return "AMAZON_SES_SETUP_NOTIFICATION, File no action"

#     try:
#         response = s3.get_object(Bucket=bucket, Key=key)
#         file_name_key = "/tmp/" + key.split("/")[-1]
#         s3.download_file(bucket, key, file_name_key)

#         # parse file
#         output_dir = "/tmp/{}/".format(uuid.uuid4().hex)
#         metadata = parse_mail(file_name_key, output_dir)

#         for filename in metadata["files"]:
#             multipart_form_data = {
#                 "files": (filename, open(filename, "rb")),
#                 "metadata": (None, json.dumps(metadata)),
#                 "type": (None, "invoice"),
#             }

#             # get url
#             email_to_meta = metadata["to"]
#             url_meta = "https://{}.docsumo.com/api/v1/pik/email/predict/"
#             if "testingdoc" in email_to_meta:
#                 url = url_meta.format("apptesting")
#                 token = os.environ.get("TOKEN_TESTING")
#             elif "stagingdoc" in email_to_meta:
#                 url = url_meta.format("appstaging")
#                 token = os.environ.get("TOKEN_STAGING")
#             else:
#                 url = url_meta.format("app")
#                 token = os.environ.get("TOKEN_PROD")

#             response = requests.post(
#                 url,
#                 files=multipart_form_data,
#                 headers={"token": token, "email": email_to_meta},
#             )
#             print(response.text)

#         return metadata

#     except Exception as e:
#         print(e)
#         print(
#             "Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.".format(
#                 key, bucket
#             )
#         )
#         raise e
