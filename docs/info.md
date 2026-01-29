<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.

-->

## How it works

A T flip-flop is a sequential digital logic circuit that stores a single bit of data. It changes its output
state based on the value of the toggle input (T) and a clock signal. When the T input is set to 1, the output
toggles its state on every rising edge of the clock. When the T input is set to 0, the output holds its
previous value. An active-low reset signal is used to initialize the output to 0.

## How to test

To test the T flip-flop, apply a clock signal and vary the value of the T input. When T is 0, the output
should remain unchanged across clock cycles. When T is 1, the output should toggle on each rising edge
of the clock. Asserting the reset signal should force the output to 0 regardless of the T input.

## External hardware

None

## Pinout

### Inputs

| Pin   | Name |
|------|------|
| ui[0] | T    |
| ui[1] |      |
| ui[2] |      |
| ui[3] |      |
| ui[4] |      |
| ui[5] |      |
| ui[6] |      |
| ui[7] |      |

### Outputs

| Pin   | Name |
|------|------|
| uo[0] | Q    |
| uo[1] |      |
| uo[2] |      |
| uo[3] |      |
| uo[4] |      |
| uo[5] |      |
| uo[6] |      |
| uo[7] |      |
