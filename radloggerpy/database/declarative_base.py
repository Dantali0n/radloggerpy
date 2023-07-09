# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base


class Base:
    """Base object all sqlalchemy models will extend"""

    @declared_attr
    def __tablename__(cls):
        """Generate tablename based on class name

        Setting the model its __tablename__ attribute will override this
        generated name.
        """
        return cls.__name__.lower()


base = declarative_base(cls=Base)
