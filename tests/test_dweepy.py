"""A port of dweetio-client's (the official javascript one, to python)
"""
# stdlib imports
import os
import subprocess
import unittest
import uuid

# local imports
import dweepy


test_data = {
    'hello': "world",
    'somenum': 6816513845,
}

test_lock = os.environ.get('DWEET_LOCK')
test_key = os.environ.get('DWEET_KEY')
test_alert_condition = "if(dweet.alertValue > 10) return 'TEST: Greater than 10'; if(dweet.alertValue < 10) return 'TEST: Less than 10';"


def check_valid_dweet_response(testcase, dweet, skip_content=False):
    testcase.assertIn('thing', dweet)
    testcase.assertIn('content', dweet)
    testcase.assertIn('created', dweet)
    if not skip_content:
        testcase.assertDictEqual(test_data, dweet['content'])


def check_valid_get_response(testcase, dweets):
    testcase.assertIsInstance(dweets, list)
    testcase.assertGreater(len(dweets), 0)
    # Only check the first one
    check_valid_dweet_response(testcase, dweets[0])


class BaseTestCase(unittest.TestCase):

    def assertDictEqual(self, a, b, *args, **kwargs):
        """Python < v2.7 compatibility. Assert 'a' > 'b'"""
        try:
            f = super(BaseTestCase, self).assertDictEqual
        except AttributeError:
            self.assertTrue(a == b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def assertGreater(self, a, b, *args, **kwargs):
        """Python < v2.7 compatibility. Assert 'a' > 'b'"""
        try:
            f = super(BaseTestCase, self).assertGreater
        except AttributeError:
            self.assertTrue(a > b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def assertIn(self, a, b, *args, **kwargs):
        """Python < v2.7 compatibility. Assert 'a' in 'b'"""
        try:
            f = super(BaseTestCase, self).assertIn
        except AttributeError:
            self.assertTrue(a in b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def assertIsInstance(self, a, b, *args, **kwargs):
        """Python < v2.7 compatibility. Assert isinstance(a, b)"""
        try:
            f = super(BaseTestCase, self).assertIsInstance
        except AttributeError:
            self.assertTrue(isinstance(a, b), *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)


class LockingTests(BaseTestCase):

    def setUp(self):
        try:
            dweepy.remove_lock(test_lock, test_key)
        except dweepy.DweepyError:
            pass

    def tearDown(self):
        try:
            dweepy.remove_lock(test_lock, test_key)
        except dweepy.DweepyError:
            pass

    def test_remove_lock_locked(self):
        """`remove_lock` should return a valid response when in use.
        """
        my_thing_id = str(uuid.uuid4())
        dweepy.lock(my_thing_id, test_lock, test_key)
        self.assertEqual(dweepy.remove_lock(test_lock, test_key), test_lock)

    def test_remove_lock_unlocked(self):
        """`remove_lock` should raise exception when lock not in use.
        """
        try:
            dweepy.remove_lock(test_lock, test_key)
        except dweepy.DweepyError as e:
            self.assertEqual(e.args[0], 'this lock is not in use')

    def test_lock_unlock(self):
        """Test that locking/unlocking doesn't raise an error.
        """
        my_thing_id = str(uuid.uuid4())
        dweepy.lock(my_thing_id, test_lock, test_key)
        dweepy.unlock(my_thing_id, test_key)


class LockedTests(BaseTestCase):

    def setUp(self):
        try:
            dweepy.remove_lock(test_lock, test_key)
        except dweepy.DweepyError:
            pass
        self.my_thing_id = str(uuid.uuid4())
        dweepy.lock(self.my_thing_id, test_lock, test_key)

    def tearDown(self):
        dweepy.unlock(self.my_thing_id, test_key)
        try:
            dweepy.remove_lock(test_lock, test_key)
        except dweepy.DweepyError:
            pass

    def test_dweet_for_without_a_key(self):
        """`dweet_for` without a key should raise an exception.
        """
        try:
            dweepy.dweet_for(self.my_thing_id, test_data)
        except dweepy.DweepyError as e:
            self.assertEqual(e.args[0], 'this thing is locked and requires a key')
        else:
            self.fail("shouldn't ever get called")

    def test_get_latest_dweet_for_without_a_key(self):
        """`get_latest_dweet_for` without a key should raise an exception.
        """
        try:
            dweepy.get_latest_dweet_for(self.my_thing_id)
        except dweepy.DweepyError as e:
            self.assertEqual(e.args[0], 'this thing is locked and requires a key')
        else:
            self.fail("shouldn't ever get called")

    def test_dweet_for_with_an_invalid_key(self):
        """`dweet_for` with an invalid key should raise an exception.
        """
        try:
            dweepy.dweet_for(self.my_thing_id, test_data, key='badkey')
        except dweepy.DweepyError as e:
            self.assertEqual(e.args[0], 'the key you provided doesn\'t work with this thing')
        else:
            self.fail("shouldn't ever get called")

    def test_get_latest_dweet_for_with_an_invalid_key(self):
        """`get_latest_dweet_for` with an invalid key should raise an exception.
        """
        try:
            dweepy.get_latest_dweet_for(self.my_thing_id, key='badkey')
        except dweepy.DweepyError as e:
            self.assertEqual(e.args[0], 'the key you provided doesn\'t work with this thing')
        else:
            self.fail("shouldn't ever get called")

    def test_dweet_for_with_a_valid_key(self):
        """`dweet_for` with a valid key should return a valid response.
        """
        dweet = dweepy.dweet_for(self.my_thing_id, test_data, key=test_key)
        check_valid_dweet_response(self, dweet)
        self.assertEqual(dweet['thing'], self.my_thing_id)

    def test_get_latest_dweet_for_with_a_valid_key(self):
        """`get_latest_dweet_for` with a valid key should return a valid response.
        """
        dweepy.dweet_for(self.my_thing_id, test_data, key=test_key)
        dweets = dweepy.get_latest_dweet_for(self.my_thing_id, key=test_key)
        check_valid_get_response(self, dweets)


class LockedStreamingDweetsTests(BaseTestCase):

    def setUp(self):
        try:
            dweepy.remove_lock(test_lock, test_key)
        except dweepy.DweepyError:
            pass
        self.my_thing_id = str(uuid.uuid4())
        dweepy.lock(self.my_thing_id, test_lock, test_key)
        self.process = subprocess.Popen('./tests/streamer.sh {0} {1}'.format(self.my_thing_id, test_key), shell=True, stderr=subprocess.STDOUT)

    def tearDown(self):
        self.process.terminate()
        dweepy.unlock(self.my_thing_id, test_key)
        try:
            dweepy.remove_lock(test_lock, test_key)
        except dweepy.DweepyError:
            pass

    def test_listen_for_dweets_from_with_key(self):
        """`listen_for_dweets_from` with a key should hear dweets.
        """
        dweets_heard = 0
        for dweet in dweepy.listen_for_dweets_from(self.my_thing_id, timeout=5, key=test_key):
            dweets_heard += 1
            check_valid_dweet_response(self, dweet)
        self.assertGreater(dweets_heard, 0)


class AlertTests(BaseTestCase):

    def setUp(self):
        try:
            dweepy.remove_lock(test_lock, test_key)
        except dweepy.DweepyError:
            pass
        self.my_thing_id = str(uuid.uuid4())
        dweepy.lock(self.my_thing_id, test_lock, test_key)

    def tearDown(self):
        dweepy.unlock(self.my_thing_id, test_key)
        try:
            dweepy.remove_lock(test_lock, test_key)
        except dweepy.DweepyError:
            pass

    def test_set_alert(self):
        """`set_alert` should return a valid response
        """
        alert = dweepy.set_alert(
            self.my_thing_id,
            ['test@example.com', 'anothertest@example.com'],
            test_alert_condition,
            test_key,
        )
        self.assertEqual(alert['condition'], test_alert_condition)

    def test_get_alert(self):
        """`get_alert` should return a valid response
        """
        dweepy.set_alert(
            self.my_thing_id,
            ['test@example.com', 'anothertest@example.com'],
            test_alert_condition,
            test_key,
        )
        alert = dweepy.get_alert(self.my_thing_id, test_key)
        self.assertEqual(alert['condition'], test_alert_condition)

    def test_dweet_for_alert(self):
        """`dweet_for` should not raise an exception no matter what alert condition is used
        """
        dweepy.set_alert(
            self.my_thing_id,
            ['test@example.com', 'anothertest@example.com'],
            test_alert_condition,
            test_key,
        )
        dweet = dweepy.dweet_for(self.my_thing_id, {'alertValue': 11}, key=test_key)
        check_valid_dweet_response(self, dweet, skip_content=True)
        dweet = dweepy.dweet_for(self.my_thing_id, {'alertValue': 5}, key=test_key)
        check_valid_dweet_response(self, dweet, skip_content=True)
        dweet = dweepy.dweet_for(self.my_thing_id, {'alertValue': 10}, key=test_key)
        check_valid_dweet_response(self, dweet, skip_content=True)

    def test_remove_alert(self):
        """`remove_alert` should return a valid response
        """
        dweepy.set_alert(
            self.my_thing_id,
            ['test@example.com', 'anothertest@example.com'],
            test_alert_condition,
            test_key,
        )
        dweepy.remove_alert(self.my_thing_id, test_key)

    def test_404_after_remove_alert(self):
        """`get_alert` should raise an exception if alert does not exist
        """
        dweepy.set_alert(
            self.my_thing_id,
            ['test@example.com', 'anothertest@example.com'],
            test_alert_condition,
            test_key,
        )
        dweepy.remove_alert(self.my_thing_id, test_key)
        try:
            dweepy.get_alert(self.my_thing_id, test_key)
        except dweepy.DweepyError as e:
            self.assertEqual(e.args[0], 'we couldn\'t find this')
        else:
            self.fail("shouldn't ever get called")


class UnlockedDweetingTests(BaseTestCase):

    def test_valid_dweet(self):
        """`dweet` should return a valid response.
        """
        dweet = dweepy.dweet(test_data)
        check_valid_dweet_response(self, dweet)

    def test_valid_dweet_for(self):
        """`dweet_for` should return a valid response.
        """
        my_thing_id = str(uuid.uuid4())
        dweet = dweepy.dweet_for(my_thing_id, test_data)
        check_valid_dweet_response(self, dweet)
        self.assertEqual(dweet['thing'], my_thing_id)


class UnlockedReadingDweetsTests(BaseTestCase):

    def setUp(self):
        self.my_thing_id = str(uuid.uuid4())

    def test_get_latest_dweet_for(self):
        """`get_latest_dweet_for` should return a valid response.
        """
        dweepy.dweet_for(self.my_thing_id, test_data)

        dweets = dweepy.get_latest_dweet_for(self.my_thing_id)
        check_valid_get_response(self, dweets)

    def test_get_dweets_for(self):
        """`get_all_dweets_for` should return a valid response.
        """
        dweepy.dweet_for(self.my_thing_id, test_data)
        dweepy.dweet_for(self.my_thing_id, test_data)

        dweets = dweepy.get_dweets_for(self.my_thing_id)
        check_valid_get_response(self, dweets)


class UnlockedStreamingDweetsTests(BaseTestCase):

    def setUp(self):
        self.my_thing_id = str(uuid.uuid4())
        self.process = subprocess.Popen('./tests/streamer.sh {0}'.format(self.my_thing_id), shell=True, stderr=subprocess.STDOUT)

    def tearDown(self):
        self.process.terminate()

    def test_listen_for_dweets_from(self):
        """`listen_for_dweets_from` should hear dweets.
        """
        dweets_heard = 0
        for dweet in dweepy.listen_for_dweets_from(self.my_thing_id, timeout=5):
            dweets_heard += 1
            check_valid_dweet_response(self, dweet)
        self.assertGreater(dweets_heard, 0)
