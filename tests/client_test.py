import unittest
from client import create_presence, translate_message


class TestClientCreatePresence(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_presence(self):
        # Проверка соотвествия типа сообщения, статусу "presence"
        self.assertEqual(create_presence()['action'], "presence")

    def test_create_presence_name(self):
        # Проверка соответствия введённого имени пользователя, имени пользователя
        self.assertEqual(create_presence('test_username')["user"]["account_name"], 'test_username')


class TestClientTranslateMessage(unittest.TestCase):
    def test_translate_message_type(self):
        # Проверка правильности типа внесённого сообщения
        with self.assertRaises(TypeError):
            translate_message(100)

    def test_translate_message_response_is_correct(self):
        # Проверка соответствия выведенного статуса, статусу о корректной работе
        self.assertEqual(translate_message({'response': 200}), 200)


if __name__ == "__main__":
    unittest.main()
