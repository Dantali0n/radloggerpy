# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from sqlalchemy import Column, Integer, String, Enum

from radloggerpy.database.declarative_base import base
from radloggerpy.types import account_types as at


class Account(base):
    id = Column(Integer, primary_key=True)
    type = Column(Enum(at.AccountTypes))
    username = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
