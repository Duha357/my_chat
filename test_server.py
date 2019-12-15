import time
import unittest
from server import presence_response


class TestServer(unittest.TestCase):
    def test_presence_response_action_is_true(self):
        # Проверка наличия ключа ACTION
        self.assertEqual(presence_response({'one': 'two', 'time': time.time()}),
                         {'response': 400, 'error': 'Не верный запрос'})

    def test_presence_response_action(self):
        # Проверка соответствия значения ключа ACTION, статусу "presence"
        self.assertEqual(presence_response({'action': 'test_action', 'time': 1000.10}),
                         {'response': 400, 'error': 'Не верный запрос'})

    def test_presence_response_time_is_true(self):
        # Проверка наличия ключа TIME
        self.assertEqual(presence_response({'action': 'presence'}), {'response': 400, 'error': 'Не верный запрос'})

    def test_presence_response_response_is_correct(self):
        # Проверка соответствия выведенного статуса, статусу о корректной работе
        self.assertEqual(presence_response({'action': 'presence', 'time': 1000.1000}), {'response': 200})


if __name__ == "__main__":
    unittest.main()
