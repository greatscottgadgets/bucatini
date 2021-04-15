#
# This file is part of Bucatini.
#
# Copyright (c) 2021 Great Scott Gadgets <info@greatscottgadgets.com>
#
# Code based in part on ``usb3_pipe``.
# SPDX-License-Identifier: BSD-3-Clause
""" SerDes-based PIPE PHY. """

#
# Quick-use aliases
#
__all__ = ['SerDesPHY', 'LunaECP5SerDes']

# Backends.
from .backends.ecp5   import LunaECP5SerDes
