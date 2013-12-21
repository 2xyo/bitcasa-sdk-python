import unittest
import json
import requests
from testconfig import config
from bitcasa import BitcasaClient
from StringIO import StringIO

class TestFolders(unittest.TestCase):
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

    def test_refresh(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        self.assertEqual(len(unittest_folder.items), 0)
        client.create_folder(unittest_folder.path, 'new folder')
        unittest_folder.refresh()
        self.assertEqual(len(unittest_folder.items), 1)
        self.assertEqual(unittest_folder.items[0].name, 'new folder')

    def test_items(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        f = StringIO('this is a test')
        filename = 'test_file.txt'
        result = client.upload_file(f, filename, unittest_folder.path, 'overwrite')
        self.assertIn(unittest_folder.path, result.path)
        self.assertEqual(result.name, filename)
        paths = [i.path for i in unittest_folder.items]
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0], result.path)

    def test_getitem(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        f = StringIO('this is a test')
        filename = 'test_file.txt'
        result = client.upload_file(f, filename, unittest_folder.path, 'overwrite')
        path = unittest_folder['test_file.txt'].path
        self.assertEqual(path, result.path)

    def test_iter(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        f = StringIO('this is a test')
        filename = 'test_file.txt'
        result = client.upload_file(f, filename, unittest_folder.path, 'overwrite')
        items = [i for i in unittest_folder]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].path, result.path)

    def test_add_file(self):
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

    def test_add_folder(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        unittest_folder.add_folder('new folder')
        self.assertEqual(len(unittest_folder.items), 1)
        self.assertEqual(unittest_folder.items[0].name, 'new folder')

    def test_copy(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        sub_folder = client.create_folder(unittest_folder.path, 'sub_folder')
        copy_folder = sub_folder.copy_to(unittest_folder, 'sub_folder_copy')
        unittest_folder.refresh()
        self.assertIn(unittest_folder.path, copy_folder.path)

    def test_move(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        sub_folder = client.create_folder(unittest_folder.path, 'sub_folder')
        move_folder = sub_folder.move_to(unittest_folder, 'sub_folder_move')
        unittest_folder.refresh()
        self.assertIn(unittest_folder.path, move_folder.path)

    def test_delete(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        sub_folder = client.create_folder(unittest_folder.path, 'sub folder')
        unittest_folder.refresh()
        self.assertEqual(len(unittest_folder.items), 1)
        self.assertEqual(unittest_folder.items[0].name, 'sub folder')
        sub_folder.delete()
        unittest_folder.refresh()
        self.assertEqual(len(unittest_folder.items), 0)

    def test_rename(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        unittest_folder_renamed = client.create_folder('/', 'renamed unittest')
        client.delete_folder(unittest_folder.path)
        client.delete_folder(unittest_folder_renamed.path)
        unittest_folder = client.create_folder('/', 'unittest')
        new_name = 'renamed unittest'
        unittest_folder.rename(new_name)
        self.assertEqual(unittest_folder.name, new_name)
