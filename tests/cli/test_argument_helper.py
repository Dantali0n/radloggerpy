# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Dantali0n
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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
