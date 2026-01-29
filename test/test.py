# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

def qbit(dut):
    return int(dut.uo_out.value) & 1

async def tick_and_settle(dut, settle_ns=1):
    """Wait one rising edge, then let NBAs/comb settle."""
    await RisingEdge(dut.clk)
    await Timer(settle_ns, units="ns")

@cocotb.test()
async def test_tff(dut):
    # Start clock
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # Reset (active low)
    dut.rst_n.value = 0
    for _ in range(5):
        await tick_and_settle(dut)
    dut.rst_n.value = 1
    await tick_and_settle(dut)

    # After reset Q = 0
    assert qbit(dut) == 0

    # T = 1 → toggle to 1
    dut.ui_in.value = 1
    await tick_and_settle(dut)
    assert qbit(dut) == 1

    # T = 1 → toggle to 0
    await tick_and_settle(dut)
    assert qbit(dut) == 0

    # T = 0 → hold (stay 0)
    dut.ui_in.value = 0
    await tick_and_settle(dut)
    await tick_and_settle(dut)
    assert qbit(dut) == 0

    # T = 1 → toggle to 1 again
    dut.ui_in.value = 1
    await tick_and_settle(dut)
    assert qbit(dut) == 1
