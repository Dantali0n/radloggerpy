# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from unittest import mock

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.argument_helper import ArgumentHelper

from tests import base


class TestArgumentHelper(base.TestCase):
    class TestHelper(ArgumentHelper):
        arguments = {
            "test": Argument(default="example"),
            "--test": Argument("-t", required=True),
        }

    def setUp(self):
        super(TestArgumentHelper, self).setUp()

    def test_construct_helper(self):
        helper = TestArgumentHelper.TestHelper()
        m_parser = mock.Mock()

        helper.register_arguments(m_parser)

        m_parser.add_argument.assert_has_calls(
            [
                mock.call("test", default="example"),
                mock.call("--test", "-t", required=True),
            ],
            any_order=True,
        )
