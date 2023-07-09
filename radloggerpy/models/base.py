# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0


class BaseModel:
    def __init__(self):
        """Do not declare any attributes in models their constructor

        By declaring the attributes outside of the constructor it will be
        easier to see which attributes certain models have. Additionally, it
        will improve testing as the attributes can be AutoSpec=True by mock.
        Remember though that all attributes outside the constructor are
        statically accessible as well. The constructor can still be used to
        assign a proper value to the declared attributes.

        """
        pass
