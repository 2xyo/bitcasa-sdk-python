import json
import requests
import re
import unittest
from testconfig import config
from bitcasa import BitcasaClient
from bitcasa.client import BASEURL
from urllib import urlencode
import urlparse
from StringIO import StringIO

class TestClient(unittest.TestCase):
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
        if 'username' not in config['user']:
            raise ValueError('No username found in user config')
        if 'password' not in config['user']:
            raise ValueError('No password found in user config')
        if 'access_token' not in config['user']:
            raise ValueError('No access_token found in user config')
        self.username = config['user']['username']
        self.password = config['user']['password']
        self.access_token = config['user']['access_token']

    def test_login_url(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect)
        given_login_url = client.login_url
        query_string = urlencode({'client_id':self.client_id, 'redirect':redirect})
        expected_login_url = '{0}oauth2/authenticate?{1}'.format(BASEURL, query_string)

    def test_authentication(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect)
        response = requests.get(client.login_url)
        self.assertEqual(response.status_code, 200)
        pattern = re.compile(r'<input type="hidden" name="csrf_token" value="(.+?)"/>')
        matches = pattern.findall(response.content)
        self.assertEqual(len(matches), 1)
        csrf_token = matches[0]
        params = {
                'user': self.username,
                'password': self.password,
                'redirect': redirect,
                'csrf_token': csrf_token
            }
        response = requests.post(client.login_url, params=params)#, allow_redirects=False)
        self.assertEqual(response.status_code, 200)
        parsed_url = urlparse.urlparse(response.url)
        parsed_qs  = urlparse.parse_qs(parsed_url.query)
        self.assertIn('authorization_code', parsed_qs)
        code = parsed_qs['authorization_code']
        client.authenticate(code)

    def test_create_folder(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')

    def test_get_folder(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        unittest_folder_again = client.get_folder(unittest_folder.path, unittest_folder.name)

    def test_delete_folder(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)

    def test_copy_folder(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        sub_folder = client.create_folder(unittest_folder.path, 'sub_folder')
        copy_folder = client.copy_folder(sub_folder.path, unittest_folder.path, 'sub_folder_copy')
        self.assertIn(unittest_folder.path, copy_folder.path)

    def test_rename_folder(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        sub_folder = client.create_folder(unittest_folder.path, 'sub_folder')
        renamed_folder = client.rename_folder(sub_folder.path, 'renamed_sub_folder', 'overwrite')
        self.assertEqual(renamed_folder.name, 'renamed_sub_folder')
        self.assertEqual(sub_folder.path, renamed_folder.path)

    def test_rename_file(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        f = StringIO('this is a test')
        filename = 'test_file.txt'
        result = client.upload_file(f, filename, unittest_folder.path, 'overwrite')
        new_result = client.rename_file(result.path, 'renamed_file', 'overwrite')
        self.assertEqual(new_result.name, 'renamed_file')
        self.assertEqual(result.path, new_result.path)

    def test_copy_file(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        f = StringIO('this is a test')
        filename = 'test_file.txt'
        result = client.upload_file(f, filename, unittest_folder.path, 'overwrite')
        copied_result = client.copy_file(result.path, unittest_folder.path, 'test_file_copy.txt', 'overwrite')
        result_iter = result.read()
        contents = ''
        copied_contents = ''
        for chunk in result_iter:
            contents += chunk
        copied_iter = copied_result.read()
        for chunk in copied_iter:
            copied_contents += chunk
        self.assertEqual(contents, copied_contents)

    def test_move_file(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        f = StringIO('this is a test')
        filename = 'test_file.txt'
        result = client.upload_file(f, filename, unittest_folder.path, 'overwrite')
        moved_result = client.move_file(result.path, unittest_folder.path, 'test_file_copy.txt', 'overwrite')
        result_iter = result.read()
        contents = ''
        moved_contents = ''
        for chunk in result_iter:
            contents += chunk
        moved_iter = moved_result.read()
        for chunk in moved_iter:
            moved_contents += chunk
        self.assertEqual(contents, moved_contents)

    def test_move_folder(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        sub_folder = client.create_folder(unittest_folder.path, 'sub_folder')
        unittest_folder_two = client.create_folder('/', 'unittest_two')
        moved_folder = client.move_folder(unittest_folder_two.path, sub_folder.path, 'moved_sub_folder', 'rename')
        paths = [i.path for i in sub_folder.items]
        self.assertIn(moved_folder.path, paths)


    def test_add_file(self):
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

    def test_read_file(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        original_contents = 'this is a test'
        f = StringIO(original_contents)
        filename = 'test_file.txt'
        result = client.upload_file(f, filename, unittest_folder.path, 'overwrite')
        self.assertIn(unittest_folder.path, result.path)
        self.assertEqual(result.name, filename)
        returned_contents = ''
        for chunk in client.get_file_contents('test_download.txt', result.path):
            returned_contents += chunk
        self.assertEqual(original_contents, returned_contents)

    def test_delete_file(self):
        redirect = 'http://example.com'
        client = BitcasaClient(self.client_id, self.secret, redirect, self.access_token)
        unittest_folder = client.create_folder('/', 'unittest')
        client.delete_folder(unittest_folder.path)
        unittest_folder = client.create_folder('/', 'unittest')
        original_contents = 'this is a test'
        f = StringIO(original_contents)
        filename = 'test_file.txt'
        result = client.upload_file(f, filename, unittest_folder.path, 'overwrite')
        client.delete_file(result.path)
