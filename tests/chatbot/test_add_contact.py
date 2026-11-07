import unittest

from hw05.chatbot.commands.add_contact import add_contact


class TestAddContact(unittest.TestCase):
    def setUp(self):
        self.contacts = {}

    def test_adds_a_new_contact(self):
        self.assertEqual(add_contact(["Jime", "0501234356"], self.contacts), "Contact added.")
        self.assertEqual(self.contacts, {"Jime": "0501234356"})

    def test_duplicate_is_rejected(self):
        add_contact(["Jime", "0501234356"], self.contacts)
        self.assertEqual(
            add_contact(["Jime", "0999999999"], self.contacts), "Contact already exists."
        )
        self.assertEqual(self.contacts["Jime"], "0501234356")

    def test_no_arguments(self):
        self.assertEqual(add_contact([], self.contacts), "Give me name and phone please.")
        self.assertEqual(self.contacts, {})

    def test_only_a_name(self):
        self.assertEqual(add_contact(["Bob"], self.contacts), "Give me name and phone please.")
        self.assertEqual(self.contacts, {})

    def test_too_many_arguments(self):
        self.assertEqual(
            add_contact(["Bob", "123", "extra"], self.contacts),
            "Give me name and phone please.",
        )
        self.assertEqual(self.contacts, {})


if __name__ == "__main__":
    unittest.main()
