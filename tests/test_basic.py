# -*- coding: utf-8 -*-
import unittest
import falconry

gitlog = '''
999fc0687d6b27309e3604602cf996c71b229537 Added a few tests for smtp EmailBackend.
24  2   tests/mail/tests.py
59b1aaa5a5136702f5b7b2ab718d91128473b9c3 Added a couple tests for collectstatic.
12  1   tests/staticfiles_tests/test_management.py
4fcd28d442c2fec56f544f99cb658f33f847824c Fixed #28881 -- Doc'd that CommonPasswordValidator's password list must be lowercase.
6   5   docs/topics/auth/passwords.txt
02365d3f38a64a5c2f3e932f23925a381d5bb151 Fixed #28542 -- Fixed deletion of primary key constraint if the new field is unique.
4   5   django/db/backends/base/schema.py
30  14  tests/schema/tests.py
56e590cc0be4d8c8b6fe0967583a6e02d18ee03e Fixed #28761 -- Documented how an inline formset's prefix works.
1   0   AUTHORS
31  0   docs/topics/forms/formsets.txt
4   0   docs/topics/forms/modelforms.txt
9a621edf624a4eb1f1645fca628a9e432f0de776 Fixed #29016 -- Fixed incorrect foreign key nullification on related instance deletion.
1   1   django/db/models/deletion.py
2   1   docs/releases/1.11.10.txt
3   0   docs/releases/2.0.2.txt
2   0   tests/delete_regress/models.py
26  2   tests/delete_regress/tests.py
'''

split_gitlog = gitlog.strip().split('\n')


class BasicTestSuite(unittest.TestCase):

    def test_line_has_sha1(self):
        expected = True
        line = '9a621edf624a4eb1f1645fca628a9e432f0de776 Fixed #29016 -- Fixed incorrect foreign key nullification on related instance deletion.'
        result = falconry.gitutils.line_has_sha(line)
        self.assertEqual(expected, result)

    def test_line_has_she(self):
        expected = [True, False, True, False, True, False, True, False, False,
                    True, False, False, False,
                    True, False, False, False, False, False]
        result = [falconry.gitutils.line_has_sha(line) for line in split_gitlog]
        # print("{} - {} - {}".format(len(split_gitlog), len(expected), len(result)))
        self.assertEqual(expected, result)

    def test_explode_path(self):
        given = "/home/git/project/library/file.txt"
        expected = [
            '/home/git/project/library/file.txt',
            '/home/git/project/library',
            '/home/git/project',
            '/home/git',
            '/home',
            '/']

        result = falconry.gitutils.explode_path(given)
        self.assertEqual(expected, result)

    def test_path_from_line(self):
        expected = 'tests/delete_regress/models.py'
        line = "2   0   tests/delete_regress/models.py"
        result = falconry.gitutils.path_from_line(line)
        self.assertEqual(expected, result)

    def test_parse(self):
        expected = [('999fc0687d6b27309e3604602cf996c71b229537', 'tests/mail/tests.py', 'tests/mail', 'tests'), ('59b1aaa5a5136702f5b7b2ab718d91128473b9c3', 'tests/staticfiles_tests/test_management.py', 'tests/staticfiles_tests', 'tests'), ('4fcd28d442c2fec56f544f99cb658f33f847824c', 'docs/topics/auth/passwords.txt', 'docs/topics/auth', 'docs/topics', 'docs'), ('02365d3f38a64a5c2f3e932f23925a381d5bb151', 'django/db/backends/base/schema.py', 'django/db/backends/base', 'django/db/backends', 'django/db', 'django', 'tests/schema/tests.py', 'tests/schema', 'tests'), ('56e590cc0be4d8c8b6fe0967583a6e02d18ee03e', 'AUTHORS', 'docs/topics/forms/formsets.txt', 'docs/topics/forms', 'docs/topics', 'docs', 'docs/topics/forms/modelforms.txt', 'docs/topics/forms', 'docs/topics', 'docs')]
        result = [r for r in falconry.gitutils.parse(gitlog)]
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
