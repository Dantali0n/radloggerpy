# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

"""Starter script for RadLoggerCli."""

import sys

from radloggerpy.cli.radlogger_shell import RadLoggerShell


def main():
    # Run interactive command line interface
    return RadLoggerShell().run(sys.argv[1:])
