#!/usr/bin/env python
"""
Test module for the bookman.py module
"""
from unittest import TestCase, main
from bookman.bookman import Interface
from os import environ

class TestInterface(TestCase):
    """
    """
    def setUp(self):
        """Patches Interface's parse method with a custom one that alters args
        so tests can execute correctly"""
        self.i = Interface()
        self.i.original_parse = self.i.parse
        self.i.parse = self.parse_overload

    def tearDown(self):
        pass

    def parse_overload(self, args):
        """Hacky overload function to deal with weird CLI problem with bookman
        where it has one more argument than necessary. Adds an argument that will
        get thrown out by the original parse method"""
        args = ['disposable-arg'] + args
        return self.i.original_parse(args)

        
    def test_parse_valid(self):
        """Test parse function with valid arguments"""
        args = '-c config -f json -d dir search'.split()
        parsed = self.i.parse(args)
        self.assertEqual(parsed.config, 'config')
        self.assertEqual(parsed.api_key, '')
        self.assertEqual(parsed.books_json, 'json')
        self.assertEqual(parsed.books_dir, 'dir')
        self.assertEqual(parsed.command, 'search')
        
    def test_parse_invalid(self):
        """Test parse function with invalid arguments"""
        args = '-c config invalid-command'.split()
        with self.assertRaises(SystemExit):
            parsed = self.i.parse(args)

    def test_config_from_env(self):
        """Test configurating bookman from environment variables"""
        environ['API_KEY'] = 'key'
        environ['BOOKS_JSON'] = 'json'
        environ['BOOKS_DIR'] = 'dir'
        self.i.load_env()
        self.assertEqual(self.i.lib_attrs['books_json'], 'json')
        self.assertEqual(self.i.lib_attrs['api_key'], 'key')
        self.assertEqual(self.i.lib_attrs['books_dir'], 'dir')
       

    def test_config_from_file(self):
        """Test bookman configuration from file"""
        args = '-c resources/config.ini search'.split()
        parsed = self.i.parse(args)
        self.i.load_ini(parsed)
        self.assertEqual(self.i.lib_attrs['books_json'], 'json')
        self.assertEqual(self.i.lib_attrs['api_key'], 'key')
        self.assertEqual(self.i.lib_attrs['books_dir'], 'directory')

    def test_config_from_arguments(self):
        """Test configurating bookman from the cli arguments"""
        args = '-c config -k key -d dir -f json search'.split()
        parsed = self.i.parse(args)
        self.i.config_from_args(parsed)
        self.assertEqual(self.i.lib_attrs['books_json'], parsed.books_json)
        self.assertEqual(self.i.lib_attrs['api_key'], parsed.api_key)
        self.assertEqual(self.i.lib_attrs['books_dir'], parsed.books_dir)

    def test_configuration_overwriting(self):
        """Test that configuration option overwriting priority is correct.
        eg. configurations from file are overwritten by environment"""
        args = '-c resources/config.ini -k key_args -d dir_args -f json_args search'.split()
        parsed = self.i.parse(args)
        self.i.config_from_args(parsed)
        self.i.config_from_args(parsed)
        self.assertEqual(self.i.lib_attrs['books_json'], 'json_args')
        self.assertEqual(self.i.lib_attrs['api_key'], 'key_args')
        self.assertEqual(self.i.lib_attrs['books_dir'], 'dir_args')

    def test_default_init(self):
        """Test that default configuration file is created when absent."""
        pass

if __name__ == '__main__':
    main()
