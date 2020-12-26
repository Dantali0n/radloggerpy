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


class Argument:
    """Small object to contain parameters for adding arguments to argparse"""

    def __init__(self, *args, **kwargs):
        """Initialize the object with potentially some arguments

        An example: `Argument(default="example", nargs="?")`

        Another: `Argument('-t', required=True, help="The type")`

        :param args: unnamed arguments
        :param kwargs: named arguments
        """

        self._args = list()
        for element in args:
            self._args.append(element)
        self._args = tuple(self._args)

        self._kwargs = dict()
        for key, value in kwargs.items():
            self._kwargs[key] = value

    def add_kwarg(self, key, value):
        """Add an additional named arguments after object construction

        :param key: Key to add to the dictionary
        :type key: str
        :param value: used as value for the dictionary key
        :return: True if the item was added successfully, false if it existed
                 already.
        :rtype: bool
        """

        if self._kwargs.get(key) is not None:
            return False

        self._kwargs[key] = value
        return True

    def args(self):
        """Return all unnamed arguments

        Use with * to pass as `*args` such as `*Argument.args()`
        """

        return self._args

    def kwargs(self):
        """Return all named arguments

        Use with ** to pass as `**kwargs` such as `**Argument.kwargs()`
        """

        return self._kwargs
