# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0


from radloggerpy.models import base as base_model

from tests import base


class TestBaseModel(base.TestCase):
    def test_no_instance_attributes(self):
        """Test that the class has no instance variables"""

        test = base_model.BaseModel()
        self.assertEqual(len(dir(base_model.BaseModel)), len(dir(test)))
