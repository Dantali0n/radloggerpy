# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0


# TODO(Dantali0n): Dd.get_device_implementations() causes circular import pls
#                  fix.

# from radloggerpy.device.device_manager import DeviceManager as Dm
# IMPLEMENTATION_CHOICES = [(imp.NAME, imp.NAME.lower()) for imp in
#                          Dm.get_device_implementations()]

IMPLEMENTATION_CHOICES = [("ArduinoGeigerPCB", "arduinogeigerpcb")]
