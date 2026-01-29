# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Clock: 10 us period (100 kHz)  (same as the lab manual style)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # -------- Reset --------
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Give 1 tiny delay so nonblocking assignments settle cleanly
    await Timer(1, units="ns")

    # After reset, Q should be 0
    q = int(dut.uo_out[0].value)
    assert q == 0, f"Q should be 0 after reset, got {q}"

    # -------- Test: T=0 (hold) --------
    dut._log.info("Test: T=0 -> hold")
    dut.ui_in.value = 0b00000000  # T = ui_in[0] = 0
    await ClockCycles(dut.clk, 3)
    await Timer(1, units="ns")

    q_hold = int(dut.uo_out[0].value)
    assert q_hold == q, f"With T=0, Q should hold (expected {q}, got {q_hold})"

    # -------- Test: T=1 (toggle each clock) --------
    dut._log.info("Test: T=1 -> toggle each clock")
    dut.ui_in.value = 0b00000001  # T = 1

    # Check several toggles
    for i in range(4):
        await ClockCycles(dut.clk, 1)
        await Timer(1, units="ns")  # key: let NBA updates settle
        q_next = int(dut.uo_out[0].value)
        assert q_next == (q ^ 1), f"Toggle {i}: expected {q ^ 1}, got {q_next}"
        q = q_next

    dut._log.info("All tests passed.")
