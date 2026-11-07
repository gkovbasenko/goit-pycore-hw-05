import unittest
from collections.abc import Iterator

from hw05.task2.generator_numbers import generator_numbers, sum_profit

SAMPLE = (
    "Загальний дохід працівника складається з декількох частин: 1000.01 "
    "як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
)


class TestGeneratorNumbers(unittest.TestCase):
    def test_returns_an_iterator(self):
        self.assertIsInstance(generator_numbers(SAMPLE), Iterator)

    def test_yields_sample_numbers_in_order(self):
        self.assertEqual(list(generator_numbers(SAMPLE)), [1000.01, 27.45, 324.00])

    def test_yields_floats(self):
        self.assertTrue(all(isinstance(n, float) for n in generator_numbers(SAMPLE)))

    def test_text_without_numbers(self):
        self.assertEqual(list(generator_numbers("no numbers here")), [])

    def test_empty_text(self):
        self.assertEqual(list(generator_numbers("")), [])

    def test_number_at_start_and_end(self):
        self.assertEqual(list(generator_numbers("5.5 middle 7.25")), [5.5, 7.25])

    def test_ignores_numbers_glued_to_other_characters(self):
        self.assertEqual(list(generator_numbers("price12.50 and v1.2.3")), [])

    def test_includes_integers(self):
        self.assertEqual(list(generator_numbers("100 and 2.50")), [100.0, 2.50])

    def test_integers_are_yielded_as_floats(self):
        self.assertTrue(all(isinstance(n, float) for n in generator_numbers("1 2 3")))

    def test_consecutive_numbers(self):
        self.assertEqual(list(generator_numbers("1.5 2.5 3.5")), [1.5, 2.5, 3.5])

    def test_newlines_and_tabs_delimit_numbers(self):
        self.assertEqual(list(generator_numbers("1.5\n2.5\t3.5")), [1.5, 2.5, 3.5])

    def test_zero_and_leading_zero_values(self):
        self.assertEqual(list(generator_numbers("0.0 and 0.75")), [0.0, 0.75])

    def test_is_lazy(self):
        numbers = generator_numbers(SAMPLE)
        self.assertEqual(next(numbers), 1000.01)
        self.assertEqual(next(numbers), 27.45)


class TestSumProfit(unittest.TestCase):
    def test_sums_sample_text(self):
        self.assertAlmostEqual(sum_profit(SAMPLE, generator_numbers), 1351.46)

    def test_uses_the_supplied_callable(self):
        calls = []

        def spy(text):
            calls.append(text)
            yield 1.5
            yield 2.5

        self.assertEqual(sum_profit(SAMPLE, spy), 4.0)
        self.assertEqual(calls, [SAMPLE])

    def test_text_without_numbers_sums_to_zero(self):
        self.assertEqual(sum_profit("no numbers here", generator_numbers), 0)

    def test_accepts_any_iterator_producing_callable(self):
        self.assertEqual(sum_profit("ignored", lambda _: iter([1.25, 2.75])), 4.0)

    def test_consumes_the_iterator_only_once(self):
        numbers = generator_numbers(SAMPLE)
        self.assertAlmostEqual(sum_profit(SAMPLE, lambda _: numbers), 1351.46)
        self.assertEqual(list(numbers), [])


if __name__ == "__main__":
    unittest.main()
