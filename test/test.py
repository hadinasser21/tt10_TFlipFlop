# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

def qbit(dut):
    return int(dut.uo_out.value) & 1

@cocotb.test()
async def test_tff(dut):
    # Start clock (required)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # After reset Q = 0
    assert qbit(dut) == 0

    # T = 1 → toggle to 1
    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 1)
    assert qbit(dut) == 1

    # T = 1 → toggle to 0
    await ClockCycles(dut.clk, 1)
    assert qbit(dut) == 0

    # T = 0 → hold (stay 0)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 2)
    assert qbit(dut) == 0

    # T = 1 → toggle to 1 again
    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 1)
    assert qbit(dut) == 1
