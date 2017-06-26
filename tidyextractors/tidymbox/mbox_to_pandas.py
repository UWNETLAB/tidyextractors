# *********************************************************************************************
# Copyright (C) 2017 Joel Becker,  Jillian Anderson, Steve McColl and Dr. John McLevey
#
# This file is part of the tidyextractors package developed for Dr John McLevey's Networks Lab
# at the University of Waterloo. For more information, see
# http://tidyextractors.readthedocs.io/en/latest/
#
# tidyextractors is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# tidyextractors is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with tidyextractors.
# If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************************************

import os
import re
import tqdm
import mailbox
import warnings
import pandas as pd
import email.utils as email
import email.header as header

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
    if isinstance(address, header.Header):
        return clean_address(address.encode('ascii'))

    elif isinstance(address, str):
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

    elif address is None:
        return None

    else:
        raise ValueError('An unexpected type was given to clean_address. Address was {}'.format(address))
        return None


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
        body = None

    return body


def write_table(mboxfile, mailTable):
    """
    Takes a list and extends it with lists of data, which is
    extracted from mbox messages.
    :param mboxfile: Mbox file name/path
    :param mailTable: A list (of lists)
    :return: An extended list of lists
    """
    mail_box_contents = mailbox.mbox(mboxfile)

    m_pbar = tqdm.tqdm(range(0,len(mail_box_contents)))
    m_pbar.set_description('Extracting mbox messages...')

    count = 0
    update_interval = min(50,len(mail_box_contents))

    for message in mail_box_contents:
        count += 1
        if count % update_interval == 0:
            m_pbar.update(update_interval)
        clean_from = clean_address(message['From'])
        clean_to = clean_addresses(message['To'])
        clean_cc = clean_addresses(message['Cc'])

        try:
            clean_date = email.parsedate_to_datetime(message['Date'])
        except:
            clean_date = None

        mailTable.append([
            clean_from,
            clean_to,
            clean_cc,
            clean_date,
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
    df_out['NumCC'] = df_out['Cc'].map(lambda i: len(i))
    return df_out