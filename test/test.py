# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Clock: 10 us period (100 kHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # -------- Reset --------
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # After reset, Q should be 0 (uo_out[0])
    assert int(dut.uo_out.value) & 0x1 == 0, "Q should be 0 after reset"

    dut._log.info("Test: T=0 -> hold")
    # T = ui_in[0] = 0
    dut.ui_in.value = 0b00000000
    q0 = int(dut.uo_out.value) & 0x1
    await ClockCycles(dut.clk, 3)
    q1 = int(dut.uo_out.value) & 0x1
    assert q1 == q0, "With T=0, Q should hold"

    dut._log.info("Test: T=1 -> toggle each clock")
    # Set T=1
    dut.ui_in.value = 0b00000001

    # Capture current Q then expect toggles
    q = int(dut.uo_out.value) & 0x1
    await ClockCycles(dut.clk, 1)
    q_next = int(dut.uo_out.value) & 0x1
    assert q_next == (q ^ 1), "With T=1, Q should toggle_
