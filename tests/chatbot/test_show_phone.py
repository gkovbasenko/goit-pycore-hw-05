import unittest

from hw05.chatbot.commands.show_phone import show_phone


class TestShowPhone(unittest.TestCase):
    def setUp(self):
        self.contacts = {"Jime": "0501234356"}

    def test_returns_the_phone_number(self):
        self.assertEqual(show_phone(["Jime"], self.contacts), "0501234356")

    def test_unknown_contact(self):
        self.assertEqual(show_phone(["Bob"], self.contacts), "Contact not found.")

    def test_no_arguments(self):
        self.assertEqual(show_phone([], self.contacts), "Enter the argument for the command.")

    def test_extra_arguments_are_ignored(self):
        self.assertEqual(show_phone(["Jime", "extra"], self.contacts), "0501234356")


if __name__ == "__main__":
    unittest.main()
