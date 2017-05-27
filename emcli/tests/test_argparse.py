import sys
import os
import tempfile
import unittest

__author__ = 'hzlaimingxing'

pardir = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir))
sys.path.append(pardir)

from emcli.emcli import get_argparse


class TestArgparse(unittest.TestCase):

    def setUp(self):
        sys.argv[1:] = []

    def test_normal_request(self):
        args = ['-s', 'subject', '-a', 'a.py', 'b.py', '-r', 'a@163.com', 'b@163.com', '-f', 'config.cnf']
        sys.argv.extend(args)
        parser = get_argparse()

        self.assertEqual(parser.subject, 'subject')
        self.assertEqual(parser.attaches, ['a.py', 'b.py'])
        self.assertEqual(parser.recipients, ['a@163.com', 'b@163.com'])
        self.assertEqual(parser.conf, 'config.cnf')

    def test_single_request(self):
        args = ['-s', 'subject', '-a', 'a.py', '-r', 'a@163.com']
        sys.argv.extend(args)
        parser = get_argparse()

        self.assertEqual(parser.subject, 'subject')
        self.assertEqual(parser.attaches, ['a.py'])
        self.assertEqual(parser.recipients, ['a@163.com'])

    def test_missing_subject(self):
        args = ['-a', 'a.py', 'b.py', '-r', 'a@163.com', 'b@163.com', '-f', 'config.cnf']
        sys.argv.extend(args)
        with self.assertRaises(SystemExit):
            parser = get_argparse()

    def test_missing_recipients(self):
        args = ['-s', 'subject', '-a', 'a.py', 'b.py', '-f', 'config.cnf']
        sys.argv.extend(args)
        with self.assertRaises(SystemExit):
            parser = get_argparse()

    def test_missing_attaches(self):
        args = ['-s', 'subject', '-r', 'a@163.com', 'b@163.com', '-f', 'config.cnf']
        sys.argv.extend(args)
        parser = get_argparse()
        self.assertEqual(parser.attaches, None)

    def test_missing_conf(self):
        args = ['-s', 'subject', '-a', 'a.py', 'b.py', '-r', 'a@163.com', 'b@163.com']
        sys.argv.extend(args)
        parser = get_argparse()
        self.assertEqual(parser.conf, None)


if __name__ == '__main__':
    unittest.main()
