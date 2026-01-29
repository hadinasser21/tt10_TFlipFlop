/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_nasser_hadi_tff (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        ena,
    input  wire [7:0]  ui_in,
    input  wire [7:0]  uio_in,
    output wire [7:0]  uo_out,
    output wire [7:0]  uio_out,
    output wire [7:0]  uio_oe
);

    // T input
    wire T = ui_in[0];

    // Output register
    reg Q;

    // T flip-flop logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            Q <= 1'b0;
        else if (ena) begin
            if (T)
                Q <= ~Q;   // toggle
            else
                Q <= Q;    // hold
        end
    end

    // Output mapping
    assign uo_out  = {7'b0000000, Q};

    // No bidirectional IOs used
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // Unused inputs
    wire _unused = &{1'b0, ui_in[7:1], uio_in};

endmodule
