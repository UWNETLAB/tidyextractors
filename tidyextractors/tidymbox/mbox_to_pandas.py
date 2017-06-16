import os
import re
import tqdm
import mailbox
import pandas as pd

# Adapted from Phil Deutsch's "mbox-analysis" https://github.com/phildeutsch/mbox-analysis

def clean_addresses(addresses):
    """
    Cleans email address.
    :param addresses: List of strings (email addresses)
    :return: List of strings (cleaned email addresses)
    """
    if addresses is None:
        return []
    addresses = addresses.replace("\'", "")
    address_list = re.split('[,;]', addresses)
    clean_list = []
    for address in address_list:
        temp_clean_address = clean_address(address)
        clean_list.append(temp_clean_address)
    return clean_list


def clean_address(address):
    """
    Cleans a single email address.
    :param address: String (email address)
    :return: String (clean email address)
    """
    address = address.replace("<", "")
    address = address.replace(">", "")
    address = address.replace("\"", "")
    address = address.replace("\n", " ")
    address = address.replace("MAILER-DAEMON", "")
    address = address.lower().strip()

    email = None
    for word in address.split(' '):
        email_regex = re.compile(
            "^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$"
            )
        email = re.match(email_regex, word)
        if email is not None:
            clean_email = email.group(0)
    if email is None:
        if address.split(' ')[-1].find('@') > -1:
            clean_email = address.split(' ')[-1].strip()
        elif address.split(' ')[-1].find('?') > -1:
            clean_email = 'n/a'
        else:
            clean_email = address

    return clean_email


def get_body(message):
    """
    Extracts body text from an mbox message.
    :param message: Mbox message
    :return: String
    """
    try:
        sm = str(message)
        body_start = sm.find('iamunique', sm.find('iamunique')+1)
        body_start = sm.find('Content-Transfer-Encoding', body_start+1)
        body_start = sm.find('\n', body_start+1)+1

        body_end = sm.find('From: ', body_start + 1)
        if body_end == -1:
            body_end = sm.find('iamunique', body_start + 1)
            body_end = sm.find('\n', body_end - 25)
        body = sm[body_start:body_end]

        body = body.replace("=20\n", "")
        body = body.replace("=FC", "ü")
        body = body.replace("=F6", "ö")
        body = body.replace("=84", "\"")
        body = body.replace("=94", "\"")
        body = body.replace("=96", "-")
        body = body.replace("=92", "\'")
        body = body.replace("=93", "\"")
        body = body.replace("=E4", "ä")
        body = body.replace("=DF", "ss")
        body = body.replace("=", "")
        body = body.replace("\"", "")
        body = body.replace("\'", "")
    except:
        body = "N/A"

    return body


def write_table(mboxfile, mailTable):
    """
    Takes a list and extends it with lists of data, which is
    extracted from mbox messages.
    :param mboxfile: Mbox file name/path
    :param mailTable: A list (of lists)
    :return: An extended list of lists
    """
    for message in mailbox.mbox(mboxfile):
        clean_from = clean_address(message['From'])
        clean_to = clean_addresses(message['To'])
        clean_cc = clean_addresses(message['Cc'])
        mailTable.append([
            clean_from,
            clean_to,
            clean_cc,
            message['Date'],
            message['Subject'],
            get_body(message)
            ])



def mbox_to_pandas(mbox_path):
    """
    Extracts all mbox messages from mbox files in mbox_path.
    :param mbox_path: Path to an mbox file OR a directory containing mbox files.
    :return: A Pandas DataFrame with messages as rows/observations.
    """
    if os.path.isfile(mbox_path):
        mbox_files = [mbox_path]
    else:
        mbox_files = [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(mbox_path) for f in files if f.endswith('mbox')]

    mail_table = []

    f_pbar = tqdm.tqdm(range(0,len(mbox_files)))
    f_pbar.set_description('Extracting mbox files...')

    for mbox_file in mbox_files:
        write_table(mbox_file, mail_table)
        f_pbar.update(1)

    df_out = pd.DataFrame(mail_table)
    df_out.columns = ['From', 'To', 'Cc', 'Date', 'Subject', 'Body']
    df_out['NumTo'] = df_out['To'].map(lambda i: len(i))
    return df_out