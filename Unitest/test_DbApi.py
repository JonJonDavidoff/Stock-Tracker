from unittest import TestCase
import os
import DbApi

email = 'sdfdfsdf@gmail.com'


class TestDBApi(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        DbApi.remove_user_by_email(email)

    def test_add_new_user(self):
        global email
        result = DbApi.add_user(first_name='dffds', last_name='fsdfsd', email=email, password='1234667')
        self.assertTrue(result)
