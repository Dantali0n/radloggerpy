# Copyright (c) 2014 OpenStack Foundation.
# SPDX-License-Identifier: Apache-2.0

import os
import re

from hacking import core

_all_log_levels = {
    "reserved": "_",  # this should never be used with a log unless
    # it is a variable used for a log message and
    # a exception
    "error": "_LE",
    "info": "_LI",
    "warning": "_LW",
    "critical": "_LC",
    "exception": "_LE",
}
_all_hints = set(_all_log_levels.values())


log_warn = re.compile(r"(.)*LOG\.(warn)\(\s*('|\"|_)")
re_redundant_import_alias = re.compile(r".*import (.+) as \1$")


@core.flake8ext
def no_translate_debug_logs(logical_line, filename):
    """Check for 'LOG.debug(_(' and 'LOG.debug(_Lx('

    * This check assumes that 'LOG' is a logger.
    """
    for hint in _all_hints:
        if logical_line.startswith("LOG.debug(%s(" % hint):
            yield (0, "N319 Don't translate debug level logs")


@core.flake8ext
def check_assert_called_once_with(logical_line, filename):
    # Try to detect nonexistent mock methods like:
    #    assertCalledOnceWith
    #    assert_has_called
    #    called_once_with
    if "radloggerpy/tests/" in filename:
        if ".assert_called_once_with(" in logical_line:
            return
        uncased_line = logical_line.lower().replace("_", "")

        check_calls = [".calledoncewith"]
        if any(x for x in check_calls if x in uncased_line):
            msg = (
                "N322: Possible use of no-op mock method. "
                "please use assert_called_once_with."
            )
            yield (0, msg)

        if ".asserthascalled" in uncased_line:
            msg = (
                "N322: Possible use of no-op mock method. "
                "please use assert_has_calls."
            )
            yield (0, msg)


@core.flake8ext
def check_python3_xrange(logical_line):
    if re.search(r"\bxrange\s*\(", logical_line):
        yield (
            0, "N325: Do not use xrange. Use range, or six.moves.range for "
            "large loops.",
        )


@core.flake8ext
def check_no_basestring(logical_line):
    if re.search(r"\bbasestring\b", logical_line):
        msg = (
            "N326: basestring is not Python3-compatible, use "
            "six.string_types instead."
        )
        yield (0, msg)


@core.flake8ext
def check_python3_no_iteritems(logical_line):
    if re.search(r".*\.iteritems\(\)", logical_line):
        msg = "N327: Use six.iteritems() instead of dict.iteritems()."
        yield (0, msg)


@core.flake8ext
def check_assert_true(logical_line, filename):
    if "radloggerpy/tests/" in filename:
        if re.search(r"assertEqual\(\s*True,[^,]*(,[^,]*)?\)", logical_line):
            msg = (
                "N328: Use assertTrue(observed) instead of "
                "assertEqual(True, observed)"
            )
            yield (0, msg)


@core.flake8ext
def check_assert_false(logical_line, filename):
    if "radloggerpy/tests/" in filename:
        if re.search(r"assertEqual\(\s*False,[^,]*(,[^,]*)?\)", logical_line):
            msg = (
                "N328: Use assertFalse(observed) instead of "
                "assertEqual(False, observed)"
            )
            yield (0, msg)


@core.flake8ext
def check_assert_empty(logical_line, filename):
    if "radloggerpy/tests/" in filename:
        msg = (
            "N330: Use assertEqual(*empty*, observed) instead of "
            "assertEqual(observed, *empty*). *empty* contains "
            "{}, [], (), set(), '', \"\""
        )
        empties = r"(\[\s*\]|\{\s*\}|\(\s*\)|set\(\s*\)|'\s*'|\"\s*\")"
        reg = r"assertEqual\(([^,]*,\s*)+?%s\)\s*$" % empties
        if re.search(reg, logical_line):
            yield (0, msg)


@core.flake8ext
def check_assert_is_instance(logical_line, filename):
    if "radloggerpy/tests/" in filename:
        if re.search(r"assertTrue\(\s*isinstance\(\s*[^,]*,\s*[^,]*\)\)", logical_line):
            msg = (
                "N331: Use assertIsInstance(observed, type) instead "
                "of assertTrue(isinstance(observed, type))"
            )
            yield (0, msg)


@core.flake8ext
def check_log_warn_deprecated(logical_line, filename):
    """LOG.warn is deprecated but still possible

    N333(watcher/foo.py): LOG.warn("example")
    Okay(watcher/foo.py): LOG.warning("example")
    """

    msg = "N333: Use LOG.warning due to compatibility with py3"
    if log_warn.match(logical_line):
        yield (0, msg)


@core.flake8ext
def check_builtins_gettext(logical_line, tokens, filename, lines, noqa):
    """Check usage of builtins gettext _().

    N341(radloggerpy/foo.py): _('foo')
    Okay(radloggerpy/i18n.py): _('foo')
    Okay(radloggerpy/_i18n.py): _('foo')
    Okay(radloggerpy/foo.py): _('foo')  # noqa
    """

    if noqa:
        return

    modulename = os.path.normpath(filename).split("/")[0]

    if "%s/tests" % modulename in filename:
        return

    if os.path.basename(filename) in ("i18n.py", "_i18n.py"):
        return

    token_values = [t[1] for t in tokens]
    i18n_wrapper = "%s._i18n" % modulename

    if "_" in token_values:
        i18n_import_line_found = False
        for line in lines:
            split_line = [elm.rstrip(",") for elm in line.split()]
            if (
                len(split_line) > 1 and split_line[0] == "from" and
                split_line[1] == i18n_wrapper and "_" in split_line
            ):
                i18n_import_line_found = True
                break
        if not i18n_import_line_found:
            msg = (
                "N341: _ from python builtins module is used. "
                "Use _ from %s instead." % i18n_wrapper
            )
            yield (0, msg)


@core.flake8ext
def no_redundant_import_alias(logical_line):
    """Checking no redundant import alias.

    N342(radloggerpy/foo.py): from X import Y as Y
    Okay(radloggerpy/foo.py): from X import Y as Z
    """

    if re.match(re_redundant_import_alias, logical_line):
        yield (0, "N342: No redundant import alias.")
