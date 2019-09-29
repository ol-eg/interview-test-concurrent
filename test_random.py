import unittest

from random_wrapper import Random


class TestRandom(unittest.TestCase):
    def setUp(self):
        self.random = Random()

    def test_random_string(self):
        random_strings = list()
        for _ in range(100):
            random_strings.append(self.random.string)
        unique_strings = set(random_strings)

        self.assertEqual(len(random_strings),
                         len(unique_strings))

    def _test_ints(self, p, n):
        random_ints = [getattr(self.random, p) for _ in range(n)]
        unique_ints = set(random_ints)
        self.assertTrue(len(unique_ints) >= n // 3, f'{random_ints}')

    def test_one_to_ten(self):
        self._test_ints('one_to_ten', 10)

    def test_one_to_hundred(self):
        self._test_ints('one_to_hundred', 100)


if __name__ == '__main__':
    unittest.main()
