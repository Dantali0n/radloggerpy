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

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class ArgumentHelper(object):
    """Simplifies the adding of arguments when using argparse

    Implement this abstract class to simplify adding of argparse arguments.
    Add elements to the :py:attr:`arguments` dictionary were the key is the
    desired argument name and the value is an
    :py:class:`radloggerpy.cli.argument.Argument` instance.

    To register the arguments defined in :py:attr:`arguments` call the
    :py:func:`register_arguments` function passing the desired argparse
    ArgumentParser instance.

    The expected structure of :py:attr:`arguments` could look as follows:

    `{  'name' : Argument(),  '--type' : Argument('-t', required=True)  }`

    When the extend of certain Argument parameters is not known at compile time
    these parameters can be added using
    :py:func:`radloggerpy.cli.argument.Argument.add_kwarg`
    """

    @property
    @abc.abstractmethod
    def arguments(self) -> dict:
        """Dictionary property that must be implemented to contain arguments"""
        pass

    def register_arguments(self, parser):
        """Register all arguments in :py:attr:`arguments` on the parser

        :param parser: argparse parser for command line strings
        :type parser: :py:class:`argparse.ArgumentParser`
        """
        for key, value in self._arguments.items():
            parser.add_argument(key, *value.args(), **value.kwargs())
