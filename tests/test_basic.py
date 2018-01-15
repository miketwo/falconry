# -*- coding: utf-8 -*-

import unittest
import falconry


class BasicTestSuite(unittest.TestCase):
    """Docs here."""

    def test_clone(self):
        expected = True
        result = falconry.gitutils.clone("reponame")
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
