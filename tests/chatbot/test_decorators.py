import unittest

from hw05.chatbot.decorators import input_error


class TestInputError(unittest.TestCase):
    def test_passes_through_the_return_value(self):
        @input_error
        def handler(value):
            return f"got {value}"

        self.assertEqual(handler("x"), "got x")

    def test_value_error_message(self):
        @input_error
        def handler():
            raise ValueError

        self.assertEqual(handler(), "Give me name and phone please.")

    def test_key_error_message(self):
        @input_error
        def handler():
            raise KeyError("Bob")

        self.assertEqual(handler(), "Contact not found.")

    def test_index_error_message(self):
        @input_error
        def handler():
            raise IndexError

        self.assertEqual(handler(), "Enter the argument for the command.")

    def test_unpacking_failure_is_a_value_error(self):
        @input_error
        def handler(args):
            name, phone = args
            return f"{name} {phone}"

        self.assertEqual(handler([]), "Give me name and phone please.")

    def test_other_exceptions_are_not_swallowed(self):
        @input_error
        def handler():
            raise RuntimeError("boom")

        with self.assertRaises(RuntimeError):
            handler()

    def test_preserves_function_metadata(self):
        @input_error
        def handler():
            """Original docstring."""

        self.assertEqual(handler.__name__, "handler")
        self.assertEqual(handler.__doc__, "Original docstring.")

    def test_forwards_args_and_kwargs(self):
        @input_error
        def handler(a, b, c=None):
            return (a, b, c)

        self.assertEqual(handler(1, 2, c=3), (1, 2, 3))


if __name__ == "__main__":
    unittest.main()
