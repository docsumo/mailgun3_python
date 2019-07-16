"""Parse body-mime"""
import email
import os
import glob
import zipfile

allowed_file = (".png", ".jpg", ".tiff", ".jpeg", ".pdf")


def parse_email(email_string: str, email_id: str, output_dir: str = "tmp"):
    """
    parse email and save the file

    Args:
        email_string: ``str``
            string of email body-mime
        email_id: ``str``
            unique id for email
        output_dir: ``str``
        
    Return:
        Email metadata dict: ``dict``

            .. code-block:: json

                {
                "from": bkrm.dahal@gmail.com,
                "to": bikram.dahal@docsumo.com,
                "date": "2019-01-01 22:00:00",
                "subject": "Testing email"
                }

    """

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
