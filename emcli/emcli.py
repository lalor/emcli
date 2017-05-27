from __future__ import print_function

import os
import sys
import logging
import ConfigParser
import argparse
import itertools
import StringIO
import fileinput

import yagmail

from storage import Storage


def _argparse():
    parser = argparse.ArgumentParser(description='A email client in terminal')
    parser.add_argument('-s', action='store', dest='subject', required=True, help='specify a subject (must be in quotes if it has spaces)')
    parser.add_argument('-a', action='append', nargs='*', dest='attaches', required=False, help='attach file(s) to the message')
    parser.add_argument('-f', action='store', dest='conf', required=False, help='specify an alternate .emcli.cnf file')
    parser.add_argument('-r', action='append', nargs='*', dest='recipients', required=True, help='recipients')
    parser.add_argument('-v', action='version', version='%(prog)s 0.1')
    return parser.parse_args()


def get_config_file(config_file):
    if config_file is None:
        config_file = os.path.expanduser('~/.emcli.cnf')

    if not os.path.exists(config_file):
        raise SystemExit('{0} is not exists'.format(config_file))

    return config_file


def parse_config(config_file):

    config = ConfigParser.SafeConfigParser()
    with open(config_file) as fp:
        config.readfp(fp)

    meta = Storage()
    for key in ['smtp_server', 'smtp_port', 'username', 'password']:
        try:
            val = config.get('DEFAULT', key)
        except ConfigParser.NoSectionError as err:
            logging.error(err)
            raise SystemExit(err)
        except ConfigParser.NoOptionError as err:
            logging.error(err)
            raise SystemExit(err)
        else:
            meta[key] = val

    return meta


def get_content():
    content = StringIO.StringIO()
    for line in sys.stdin:
        content.write(line)

    return content.getvalue()


def send_email(meta):
    content = get_content()
    body = [content]
    if meta.attaches:
        attaches = list(itertools.chain(*meta.attaches))
        body.extend(attaches)

    with yagmail.SMTP(user=meta.username, password=meta.password,
                      host=meta.smtp_server, port=int(meta.smtp_port)) as yag:
        for recipient in itertools.chain(meta.recipients):
            yag.send(recipient, meta.subject, body)


def main():
    parser = _argparse()
    meta = parse_config(get_config_file(parser.conf))
    meta.attaches = parser.attaches
    meta.recipients = parser.recipients
    meta.subject = parser.subject
    send_email(meta)


if __name__ == '__main__':
    main()
