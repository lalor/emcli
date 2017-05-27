from __future__ import print_function

import os
import sys
import ConfigParser
import argparse
import StringIO
import fileinput

import yagmail

from storage import Storage
from logger import get_logger

logger = get_logger()

def _argparse():
    parser = argparse.ArgumentParser(description='A email client in terminal')
    parser.add_argument('-s', action='store', dest='subject', required=True, help='specify a subject (must be in quotes if it has spaces)')
    parser.add_argument('-a', action='store', nargs='*', dest='attaches', required=False, help='attach file(s) to the message')
    parser.add_argument('-f', action='store', dest='conf', required=False, help='specify an alternate .emcli.cnf file')
    parser.add_argument('-r', action='store', nargs='*', dest='recipients', required=True, help='recipient who you are sending the email to')
    parser.add_argument('-v', action='version', version='%(prog)s 0.1')
    return parser.parse_args()


def get_config_file(config_file):
    if config_file is None:
        config_file = os.path.expanduser('~/.emcli.cnf')
    return config_file


def exit_if_file_not_exist(filename):
    if not os.path.exists(filename):
        logger.error('{0} is not exists'.format(config_file))
        raise SystemExit()


def get_meta_from_config(config_file):
    config = ConfigParser.SafeConfigParser()

    with open(config_file) as fp:
        config.readfp(fp)

    meta = Storage()
    for key in ['smtp_server', 'smtp_port', 'username', 'password']:
        try:
            val = config.get('DEFAULT', key)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as err:
            logger.error(err)
            raise SystemExit(err)
        else:
            meta[key] = val

    return meta


def get_content():
    return sys.stdin.read()


def send_email(meta):
    content = get_content()
    body = [content]
    if meta.attaches:
        body.extend(meta.attaches)

    with yagmail.SMTP(user=meta.username, password=meta.password,
                      host=meta.smtp_server, port=int(meta.smtp_port)) as yag:
        logger.info('send email "{0}" to {1}'.format(meta.subject, meta.recipients))
        yag.send(meta.recipients, meta.subject, body)


def main():
    parser = _argparse()

    config_file = get_config_file(parser.conf)
    exit_if_file_not_exist(config_file)

    meta = get_meta_from_config(get_config_file(parser.conf))

    meta.attaches = parser.attaches
    meta.recipients = parser.recipients
    meta.subject = parser.subject

    send_email(meta)


if __name__ == '__main__':
    main()
