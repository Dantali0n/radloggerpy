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

from radloggerpy.cli.argument import Argument

from tests import base


class TestArgument(base.TestCase):
    def setUp(self):
        super(TestArgument, self).setUp()

    def test_construct_args(self):
        arg = Argument("-t")

        self.assertEqual(1, len(arg.args()))
        self.assertEqual(("-t",), arg.args())

    def test_construct_kwargs(self):
        arg = Argument(default="test", required=True)

        self.assertEqual(2, len(arg.kwargs()))
        self.assertEqual({"default": "test", "required": True}, arg.kwargs())

    def test_add_kwarg(self):
        arg = Argument()

        self.assertEqual(0, len(arg.kwargs()))

        arg.add_kwarg("test", "example")
        self.assertEqual({"test": "example"}, arg.kwargs())

    def test_add_kwarg_duplicate(self):
        arg = Argument()

        self.assertEqual(0, len(arg.kwargs()))

        self.assertTrue(arg.add_kwarg("test", "example"))
        self.assertFalse(arg.add_kwarg("test", "example2"))
        self.assertEqual({"test": "example"}, arg.kwargs())

    def test_add_kwarg_none_str(self):
        arg = Argument()

        self.assertTrue(arg.add_kwarg(False, "example"))
        self.assertEqual({False: "example"}, arg.kwargs())
