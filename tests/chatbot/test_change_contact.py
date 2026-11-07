import unittest

from hw05.chatbot.commands.change_contact import change_contact


class TestChangeContact(unittest.TestCase):
    def setUp(self):
        self.contacts = {"Jime": "0501234356"}

    def test_updates_an_existing_contact(self):
        self.assertEqual(
            change_contact(["Jime", "0999999999"], self.contacts), "Contact updated."
        )
        self.assertEqual(self.contacts["Jime"], "0999999999")

    def test_unknown_contact(self):
        self.assertEqual(change_contact(["Bob", "0999999999"], self.contacts), "Contact not found.")
        self.assertEqual(self.contacts, {"Jime": "0501234356"})

    def test_no_arguments(self):
        self.assertEqual(change_contact([], self.contacts), "Give me name and phone please.")

    def test_only_a_name(self):
        self.assertEqual(change_contact(["Jime"], self.contacts), "Give me name and phone please.")
        self.assertEqual(self.contacts["Jime"], "0501234356")

    def test_too_many_arguments(self):
        self.assertEqual(
            change_contact(["Jime", "123", "extra"], self.contacts),
            "Give me name and phone please.",
        )


if __name__ == "__main__":
    unittest.main()
