# Copyright (c) 2015 b<>com
# SPDX-License-Identifier: Apache-2.0
#

import oslo_i18n

from radloggerpy import __package_folder__ as package_folder
from radloggerpy.config import translation

# The domain is the name of the App which is used to generate the folder
# containing the translation files (i.e. the .pot file and the various locales)
DOMAIN = package_folder


def dummy(msg: str):
    return msg


_translators = None
for directory in translation.translation_dirs():
    if translation.has_translation_files(directory):
        _translators = oslo_i18n.TranslatorFactory(
            domain=DOMAIN, localedir=directory
        )

# The primary translation function using the well-known name "_"
_ = dummy
if _translators:
    _ = _translators.primary

# The contextual translation function using the name "_C"
# _C = _translators.contextual_form

# The plural translation function using the name "_P"
# _P = _translators.plural_form

oslo_i18n.enable_lazy()


def translate(value: str, user_locale: str):
    return oslo_i18n.translate(value, user_locale)


def get_available_languages():
    return oslo_i18n.get_available_languages(DOMAIN)
