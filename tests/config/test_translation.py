# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import os

import radloggerpy
from radloggerpy.config import translation

from unittest import mock

from tests import base


class TestTranslation(base.TestCase):
    def setUp(self):
        super(TestTranslation, self).setUp()

    def test_get_package_locale_dir(self):
        """Test locale dir should be subdirectory of project source path"""

        path = os.path.dirname(
            os.path.abspath(radloggerpy.__file__)
        ) + "/locale"

        self.assertEqual(path, translation.get_package_locale_dir())

    @mock.patch.object(os.path, "isdir")
    @mock.patch.object(os, "listdir")
    def test_translation_languages(self, m_list, m_isdir):
        t_list = ["nl", "de"]

        m_isdir.return_value = True
        m_list.return_value = ["nl", "de"]

        self.assertListEqual(t_list, translation.translation_languages())

    @mock.patch.object(os.environ, "get")
    def test_translation_dirs(self, m_environ):
        """Find all system translation dirs"""

        t_environ_path = os.path.dirname(os.path.abspath(__file__))

        m_environ.return_value = t_environ_path

        dirs = translation.translation_dirs()

        if "/usr/share/locale" in dirs:
            self.assertIn("/usr/share/locale", dirs)
        else:
            self.assertIn("/usr/local/share/locale", dirs)
        self.assertIn(t_environ_path, dirs)
        self.assertIn(translation.get_package_locale_dir(), dirs)
