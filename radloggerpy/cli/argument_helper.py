# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc


class ArgumentHelper(metaclass=abc.ABCMeta):
    """Simplifies the adding of arguments when using argparse

    Implement this abstract class to simplify adding of argparse arguments.
    Add elements to the :py:attr:`arguments` dictionary were the key is the
    desired argument name and the value is an
    :py:class:`radloggerpy.cli.argument.Argument` instance.

    To register the arguments defined in :py:attr:`arguments` call the
    :py:func:`register_arguments` function passing the desired argparse
    ArgumentParser instance.

    The expected structure of :py:attr:`arguments` could look as follows:

    `{  'name' : Argument(),  '--interface' : Argument('-i', required=True)  }`

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
        for key, value in self.arguments.items():
            parser.add_argument(key, *value.args(), **value.kwargs())
