# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import gettext
import os
from unittest import mock

import locale
import oslo_i18n
from oslo_i18n._gettextutils import _BABEL_ALIASES
from oslo_i18n import _locale

from radloggerpy import _i18n
from radloggerpy._i18n import DOMAIN

from tests import base


class Testi18n(base.TestCase):
    def setUp(self):
        super().setUp()

    def test_domain(self):
        self.assertEqual(_i18n.DOMAIN, _i18n._translators.domain)

    @mock.patch.object(oslo_i18n._gettextutils, "_AVAILABLE_LANGUAGES")
    @mock.patch.object(os, "environ")
    def test_translate_nl(self, m_environ, m_languages_get):
        m_languages_get.return_value = None
        m_environ.get.side_effect = ["nl", "nl", "nl", "nl", "locale"]

        m_translated_nl = _i18n._("RadLoggerPy opstarten met PID %s")  # noqa: N341
        m_untranslated = _i18n._("Starting RadLoggerPy service on PID %s")  # noqa: N341

        self.assertEqual(m_translated_nl, _i18n.translate(m_untranslated, "nl_NL"))

    def test_get_available_languages(self):
        m_languages = ["en_US"]

        self.assertEqual(m_languages, _i18n.get_available_languages())

    @mock.patch.object(oslo_i18n._gettextutils, "_AVAILABLE_LANGUAGES")
    @mock.patch.object(os, "environ")
    def test_get_available_languages_real(self, m_environ, m_languages_get):
        """Ensure all languages are registered if the localedir is set

        :param m_environ: patch os.environ.get to fake RADLOGGERPY_LOCALEDIR
        :param m_languages_get: reset _factory _AVAILALE_LANGUAGES variable
        :return:
        """
        m_languages_get.return_value = None
        m_environ.get.return_value = "locale"

        m_languages = ["en_US"]
        locale_identifiers = set(locale.windows_locale.values())
        localedir = os.environ.get(_locale.get_locale_dir_variable_name(DOMAIN))

        m_locale = "locale"
        m_locale_dirs = [
            o for o in os.listdir(m_locale) if os.path.isdir(os.path.join(m_locale, o))
        ]

        for m_locale_dir in m_locale_dirs:
            m_languages.extend(
                language for language in locale_identifiers if m_locale_dir in language
            )

        m_languages.extend(  # noqa: N341
            alias
            for alias, _ in _BABEL_ALIASES.items()
            if gettext.find(DOMAIN, localedir=localedir, languages=[alias])
        )

        self.assertItemsEqual(m_languages, _i18n.get_available_languages())
