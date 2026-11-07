import unittest

from hw05.chatbot.commands.show_all import show_all


class TestShowAll(unittest.TestCase):
    def test_empty_contacts(self):
        self.assertEqual(show_all({}), "No contacts found.")

    def test_single_contact(self):
        self.assertEqual(show_all({"Jime": "0501234356"}), "Jime: 0501234356")

    def test_contacts_are_sorted_by_name(self):
        contacts = {"Zoe": "3", "Alice": "1", "Bob": "2"}
        self.assertEqual(show_all(contacts), "Alice: 1\nBob: 2\nZoe: 3")


if __name__ == "__main__":
    unittest.main()
