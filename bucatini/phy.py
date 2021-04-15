#
# This file is part of Bucatini.
#
# Copyright (c) 2021 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause

import logging

from abc import ABC
from nmigen import *

class BucatiniPHY(Elaboratable, ABC):
    """ Abstract base class for Bucatini soft PIPE implementations. 
    
    Currently compliant with the PHY Interface for PCI Express, revision 3.0,
    with the following tweaks:

        - Following nMigen conventions, reset is active high, rather than active low.

    See Table 5-2 in the PIPE specification r3 for a definition of these signals. Documenting them
    locally is pending; and should be completed once we've settled on a spec version.
    """

    # Default to implementing the 32-bit PIPE standard, but allow subclasses to override this.
    INTERFACE_WIDTH = 32

    # Mappings of interface widths to DataBusWidth parameters.
    _DATA_BUS_WIDTHS = {
        32: 0b00,
        16: 0b01,
        8 : 0b10
    }

    def __init__(self, invert_reset=True):

        # Ensure we have a valid interface width.
        if self.INTERFACE_WIDTH not in self._DATA_BUS_WIDTHS:
            raise ValueError(f"Bucatini does not support a data bus width of {self.INTERFACE_WIDTH}!")
        
        # Compute the width of our data and control signals for this class.
        data_width = self.INTERFACE_WIDTH * 8
        ctrl_width = self.INTERFACE_WIDTH * 1

        #
        # PIPE interface standard.
        #

        # Full-PHY Control and status.
        self.rate             = Signal()
        self.reset            = Signal()
        self.phy_mode         = Signal(2)
        self.phy_status       = Signal()
        self.elas_buf_mode    = Signal()
        self.power_down       = Signal(2)
        self.pwrpresent       = Signal()
        self.data_bus_width   = Const(self._DATA_BUS_WIDTHS[self.INTERFACE_WIDTH], width=2)

        # Transmit bus.
        self.tx_clk           = Signal()
        self.tx_data          = Signal(data_width)
        self.tx_datak         = Signal(ctrl_width)
        self.tx_data_valid    = Signal()

        # Transmit configuration & status.
        self.tx_compliance    = Signal()
        self.tx_oneszeroes    = Signal()
        self.tx_deemph        = Signal(2)
        self.tx_margin        = Signal(3)
        self.tx_swing         = Signal()
        self.tx_detrx_lpbk    = Signal()
        self.tx_elecidle      = Signal()

        # Receive bus.
        self.pclk             = Signal()
        self.rx_data          = Signal(data_width)
        self.rx_datak         = Signal(ctrl_width)
        self.rx_valid         = Signal()

        # Receiver configuration & status.
        self.rx_status        = Array((Signal(3), Signal(3)))
        self.rx_polarity      = Signal()
        self.rx_elecidle      = Signal()
        self.rx_termination   = Signal()
