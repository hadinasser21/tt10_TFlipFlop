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

    # ---------------- Reset ----------------
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # After reset, Q should be 0
    q = int(dut.uo_out.value) & 0x1
    assert q == 0, f"Q should be 0 after reset, got {q}"

    # ---------------- Test T=0 (hold) ----------------
    dut._log.info("Test: T=0 -> hold")
    dut.ui_in[0].value = 0

    q0 = int(dut.uo_out.value) & 0x1
    await ClockCycles(dut.clk, 3)
    q1 = int(dut.uo_out.value) & 0x1

    assert q1 == q0, f"With T=0, Q should hold (q0={q0}, q1={q1})"

    # ---------------- Test T=1 (toggle) ----------------
    dut._log.info("Test: T=1 -> toggle each clock")
    dut.ui_in[0].value = 1

    q = int(dut.uo_out.value) & 0x1
    await ClockCycles(dut.clk, 1)
    q_next = int(dut.uo_out.value) & 0x1
    assert q_next == (q ^ 1), f"With T=1, Q should toggle (q={q}, q_next={q_next})"

    q = q_next
    await ClockCycles(dut.clk, 1)
    q_next = int(dut.uo_out.value) & 0x1
    assert q_next == (q ^ 1), f"With T=1, Q should toggle again (q={q}, q_next={q_next})"

    # ---------------- Reset again check ----------------
    dut._log.info("Test: Reset forces Q=0 again")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    q = int(dut.uo_out.value) & 0x1
    assert q == 0, f"After reset again, Q should be 0, got {q}"

    dut._log.info("All tests passed.")
