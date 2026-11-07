import unittest

from hw05.task1.fibonacci import caching_fibonacci


def cache_of(fib):
    """Reach into the closure to inspect the memoization dict."""
    return next(
        cell.cell_contents
        for cell in fib.__closure__
        if isinstance(cell.cell_contents, dict)
    )


class TestCachingFibonacci(unittest.TestCase):
    def setUp(self):
        self.fib = caching_fibonacci()

    def test_factory_takes_no_arguments(self):
        self.assertTrue(callable(self.fib))

    def test_base_cases(self):
        self.assertEqual(self.fib(0), 0)
        self.assertEqual(self.fib(1), 1)

    def test_negative_input_returns_zero(self):
        self.assertEqual(self.fib(-1), 0)
        self.assertEqual(self.fib(-10), 0)

    def test_known_sequence(self):
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        self.assertEqual([self.fib(n) for n in range(11)], expected)

    def test_larger_values(self):
        self.assertEqual(self.fib(15), 610)
        self.assertEqual(self.fib(35), 9227465)

    def test_repeated_calls_are_consistent(self):
        self.assertEqual(self.fib(20), self.fib(20))


class TestCacheBehaviour(unittest.TestCase):
    def setUp(self):
        self.fib = caching_fibonacci()

    def test_cache_starts_empty(self):
        self.assertEqual(cache_of(self.fib), {})

    def test_call_populates_the_cache(self):
        self.fib(10)
        self.assertEqual(cache_of(self.fib)[10], 55)

    def test_cache_survives_between_calls(self):
        self.fib(10)
        self.fib(12)
        cache = cache_of(self.fib)
        self.assertEqual(cache[10], 55)
        self.assertEqual(cache[12], 144)

    def test_base_cases_are_not_cached(self):
        self.fib(1)
        self.assertEqual(cache_of(self.fib), {})

    def test_each_factory_call_gets_its_own_cache(self):
        other = caching_fibonacci()
        self.fib(10)
        self.assertIsNot(other, self.fib)
        self.assertEqual(cache_of(other), {})
        self.assertEqual(other(10), 55)

    def test_warm_cache_avoids_deep_recursion(self):
        for n in range(2, 300):
            self.fib(n)
        self.assertEqual(self.fib(100), 354224848179261915075)


if __name__ == "__main__":
    unittest.main()
