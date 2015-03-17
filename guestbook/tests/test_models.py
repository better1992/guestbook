from unittest import TestCase
import mock
from mock import patch, MagicMock
from google.appengine.api import users
from guestbookapp.models import Greeting, GuestBook, get_guestbook_key


class TestBassClass(TestCase):
    testbed = testbed.Testbed()

    def generate_user(self, user_email='', user_id='', is_admin=False):
        self.testbed.setup_env(
            user_email=user_email,
            user_id=user_id,
            user_is_admin='1' if is_admin else '0',
            overwrite=True)

    def setUp(self):
        # Activate the testbed, which prepares the service stubs for use.

        self.testbed.activate()

        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        self.testbed.init_user_stub()
        self.generate_user('test@example.com', '123456', True)
        for i in range(1, 21):
            dict_parameter = {
            'guestbook_name': 'demo',
            'greeting_message': 'message %d' % i
            }
            Greeting.put_from_dict(dict_parameter)

    def tearDown(self):
        self.testbed.deactivate()


class TestGreeting(TestBassClass):
    def test_put_from_dict(self):
        dict_parameter = {
        'guestbook_name': 'demo',
        'greeting_message': '123'
        }

        result = Greeting.put_from_dict(dict_parameter)
        greetings_test = mock.Mock(return_value=result)
        assert result is not None
        assert result.author.nickname() == 'test@example.com'
        assert result.content == '123'

    def test_get_greeting(self):
        dict_parameter = {
        'guestbook_name': 'demo',
        'greeting_message': '123'
        }

        newGreeting = Greeting.put_from_dict(dict_parameter)
        result = Greeting.get_greeting('demo', newGreeting.key.id())
        assert result.key.id() == newGreeting.key.id()

    def test_get_latest(self):
        greetings, next_cursor, more = Greeting.get_latest('demo', 10, None)
        assert greetings is not None
        assert len(greetings) == 10
        assert next_cursor is not None
        assert more is True

    def test_delete_greeting(self):
        greetings, next_cursor, more = Greeting.get_latest('demo', 20, None)
        id_1 = greetings[0].key.id()
        dict_parameter = {
            'id': greetings[0].key.id(),
            'guestbook_name': 'demo'
        }
        Greeting.delete_greeting(dict_parameter)
        greetings, next_cursor, more = Greeting.get_latest('demo', 20, None)
        id_2 = greetings[0].key.id()
        assert id_1 is not id_2

    @patch('google.appengine.api.users.get_current_user')
    def test_edit_greeting(self, get_current_user):
        user = mock.Mock(spec=users.User)
        user.email.return_value = 'update_by@example.com'
        user.federated_identity.return_value = '123456'
        get_current_user.return_value = user
        greetings, next_cursor, more = Greeting.get_latest('demo', 20, None)
        id_1 = greetings[0].key.id()
        dict_parameter = {
            'greeting_id': id_1,
            'greeting_message': 'update_message',
            'guestbook_name': 'demo'
        }
        result = Greeting.edit_greeting(dict_parameter)
        assert result.content == 'update_message'


class TestGuestBook(TestBassClass):

    @patch('google.appengine.ext.ndb.Key')
    def test_get_guestbook_key(self, get_key_method):
        guestbook = mock.Mock(spec=GuestBook)
        guestbook.name.return_value = 'demo'
        result = get_guestbook_key(guestbook.name)
        self.assertEqual(get_key_method('GuestBook', guestbook.name), result)


    def test_get_guestbook(self):
        assert GuestBook.get_guestbook('demo').name == 'demo'

    def test_add_guestbook(self):
        GuestBook.add_guestbook('new_guestbook')
        result = GuestBook.get_guestbook('new_guestbook')
        assert result.name == 'new_guestbook'













