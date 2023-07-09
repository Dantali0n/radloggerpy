# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from radloggerpy.hacking import checks

from tests import base


class TestHacking(base.TestCase):
    """Hacking allows to define additional flake8 linting rules

    The hacking library is maintained by OpenStack and allows to define
    additional flake8 rules for code linting. These test cases assert that
    these additional flake8 rules work as intended.
    """

    def setUp(self):
        super(TestHacking, self).setUp()

    def test_no_redundant_import_alias_offending(self):
        """Settings an alias to the name of the import is not allowed"""

        offending_line = "from X import Y as Y"
        generator = checks.no_redundant_import_alias(offending_line)

        self.assertEqual(0, next(generator)[0])

    def test_no_redundant_import_alias_allowed(self):
        """Any alias name that is not the exact of the import is allowed"""

        allowed_line = "from X import Y as Z"
        generator = checks.no_redundant_import_alias(allowed_line)

        self.assertRaises(StopIteration, next, generator)

    def test_check_builtins_gettext_offending(self):
        """Not allowed as it uses native gettext function"""

        filename = "radloggerpy/radlogger.py"
        lines = [
            "from X import Y as Y",
            "def function():",
            "    print(_('builtin gettext'))",
        ]

        generator = checks.check_builtins_gettext(
            "logical_line", [" _"], filename, lines, False
        )

        self.assertEqual(0, next(generator)[0])

    def test_check_builtins_gettext_allowed(self):
        """Allowed as _i18n import ensure native gettext is overridden"""

        filename = "radloggerpy/radlogger.py"
        lines = [
            "from radloggerpy._i18n import _",
            "def function():",
            "    print(_('builtin gettext'))",
        ]

        generator = checks.check_builtins_gettext(
            "logical_line", [" _"], filename, lines, False
        )

        self.assertRaises(StopIteration, next, generator)

    def test_check_log_warn_deprecated_offending(self):
        logical_line = "LOG.warn('example')"
        filename = "radloggerpy/foo/bar.py"

        generator = checks.check_log_warn_deprecated(logical_line, filename)

        self.assertEqual(0, next(generator)[0])

    def test_check_log_warn_deprecated_allowed(self):
        logical_line = "LOG.warning('example')"
        filename = "radloggerpy/foo/bar.py"

        generator = checks.check_log_warn_deprecated(logical_line, filename)

        self.assertRaises(StopIteration, next, generator)

    def test_check_assert_is_instance_offending(self):
        logical_line = "self.assertTrue(isinstance(observed, Type))"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.check_assert_is_instance(logical_line, filename)

        self.assertEqual(0, next(generator)[0])

    def test_check_assert_is_instance_allowed(self):
        logical_line = "assertIsInstance(observed, type)"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.check_assert_is_instance(logical_line, filename)

        self.assertRaises(StopIteration, next, generator)

    def test_check_assert_empty_offending(self):
        logical_line = "self.assertEqual(measured, [])"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.check_assert_empty(logical_line, filename)

        self.assertEqual(0, next(generator)[0])

    def test_check_assert_empty_allowed(self):
        logical_line = "self.assertEqual([], measured)"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.check_assert_empty(logical_line, filename)

        self.assertRaises(StopIteration, next, generator)

    def test_check_assert_false_offending(self):
        logical_line = "assertEqual(False, observed)"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.check_assert_false(logical_line, filename)

        self.assertEqual(0, next(generator)[0])

    def test_check_assert_false_allowed(self):
        logical_line = "assertFalse(observed)"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.check_assert_false(logical_line, filename)

        self.assertRaises(StopIteration, next, generator)

    def test_check_assert_true_offending(self):
        logical_line = "assertEqual(True, observed)"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.check_assert_true(logical_line, filename)

        self.assertEqual(0, next(generator)[0])

    def test_check_assert_true_allowed(self):
        logical_line = "assertTrue(observed)"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.check_assert_false(logical_line, filename)

        self.assertRaises(StopIteration, next, generator)

    def test_check_python3_no_iteritems_offending(self):
        logical_line = "input.iteritems()"

        generator = checks.check_python3_no_iteritems(logical_line)

        self.assertEqual(0, next(generator)[0])

    def test_check_python3_no_iteritems_allowed(self):
        logical_line = "six.iteritems(input)"

        generator = checks.check_python3_no_iteritems(logical_line)

        self.assertRaises(StopIteration, next, generator)

    def test_check_no_basestring_offending(self):
        logical_line = "self.assertIsInstance(basestring, object)"

        generator = checks.check_no_basestring(logical_line)

        self.assertEqual(0, next(generator)[0])

    def test_check_no_basestring_allowed(self):
        logical_line = "self.assertIsInstance(six.string_types, object)"

        generator = checks.check_no_basestring(logical_line)

        self.assertRaises(StopIteration, next, generator)

    def test_check_python3_xrange_offending(self):
        logical_line = "xrange(1, 2, 3)"

        generator = checks.check_python3_xrange(logical_line)

        self.assertEqual(0, next(generator)[0])

    def test_check_python3_xrange_allowed(self):
        logical_line = "range.range(1, 2)"

        generator = checks.check_python3_xrange(logical_line)

        self.assertRaises(StopIteration, next, generator)

    def test_check_assert_called_once_with_offending(self):
        logical_line = "m_mocked.asserthascalled(1, 2)"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.check_assert_called_once_with(logical_line, filename)

        self.assertEqual(0, next(generator)[0])

    def test_check_assert_called_once_with_offending_two(self):
        logical_line = "m_mocked.calledoncewith(1, 2)"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.check_assert_called_once_with(logical_line, filename)

        self.assertEqual(0, next(generator)[0])

    def test_check_assert_called_once_with_allowed(self):
        logical_line = "m_mocked.assert_called_once_with(1, 2)"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.check_assert_called_once_with(logical_line, filename)

        self.assertRaises(StopIteration, next, generator)

    def test_no_translate_debug_logs_offending(self):
        logical_line = "LOG.debug(_('Shikato ga nai~'))"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.no_translate_debug_logs(logical_line, filename)

        self.assertEqual(0, next(generator)[0])

    def test_no_translate_debug_logs_allowed(self):
        logical_line = "LOG.warning(_('Shikato ga nai~'))"
        filename = "radloggerpy/tests/bar.py"

        generator = checks.no_translate_debug_logs(logical_line, filename)

        self.assertRaises(StopIteration, next, generator)
