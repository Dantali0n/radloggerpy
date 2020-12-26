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
