import unittest
import json
import requests
from testconfig import config
from bitcasa import BitcasaClient
from StringIO import StringIO

class TestFiles(unittest.TestCase):
    def setUp(self):
        if 'client' not in config:
            raise ValueError('No client section found in config')
        if 'client_id' not in config['client']:
            raise ValueError('client_id not found in client config')
        if 'secret' not in config['client']:
            raise ValueError('secret not found in client config')
        self.client_id = config['client']['client_id']
        self.secret = config['client']['secret']

        if 'user' not in config:
            raise ValueError('No user section found in config')
        if 'access_token' not in config['user']:
            raise ValueError('No access_token found in user config')
        self.access_token = config['user']['access_token']

    def test_read(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        contents = 'this is a test'
        f = StringIO(contents)
        filename = 'test_file.txt'
        unittest_folder.add_file(f, len(contents), filename)
        self.assertEqual(len(unittest_folder.items), 1)
        read_iter = unittest_folder.items[0].read()
        read_contents = ''
        for chunk in read_iter:
            read_contents += chunk
        self.assertEqual(contents, read_contents)

    def test_delete(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        contents = 'this is a test'
        f = StringIO(contents)
        filename = 'test_file.txt'
        unittest_folder.add_file(f, len(contents), filename)
        uploaded_file = unittest_folder['test_file.txt']
        uploaded_file.delete()
        unittest_folder.refresh()
        self.assertEqual(len(unittest_folder.items), 0)

    def test_rename(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        contents = 'this is a test'
        f = StringIO(contents)
        filename = 'test_file.txt'
        unittest_folder.add_file(f, len(contents), filename)
        uploaded_file = unittest_folder['test_file.txt']
        uploaded_file.rename('something new.txt')
        unittest_folder.refresh()
        self.assertEqual(unittest_folder.items[0].name, 'something new.txt')

    def test_copy(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        sub_folder = client.create_folder(unittest_folder.path, 'sub_folder')
        contents = 'this is a test'
        f = StringIO(contents)
        filename = 'test_file.txt'
        unittest_folder.add_file(f, len(contents), filename)
        uploaded_file = unittest_folder['test_file.txt']
        new_file = uploaded_file.copy_to(sub_folder, 'something new')
        self.assertIn(sub_folder.path, new_file.path)

    def test_move(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        sub_folder = client.create_folder(unittest_folder.path, 'sub_folder')
        contents = 'this is a test'
        f = StringIO(contents)
        filename = 'test_file.txt'
        unittest_folder.add_file(f, len(contents), filename)
        uploaded_file = unittest_folder['test_file.txt']
        new_file = uploaded_file.move_to(sub_folder, 'something new')
        self.assertIn(sub_folder.path, new_file.path)
