/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_nasser_hadi_tff (
    input  wire [7:0] ui_in,   // Dedicated inputs
    output wire [7:0] uo_out,  // Dedicated outputs
    input  wire [7:0] uio_in,  // IOs: Input path
    output wire [7:0] uio_out, // IOs: Output path
    output wire [7:0] uio_oe,  // IOs: Enable path
    input  wire ena,           // Enable
    input  wire clk,           // Clock
    input  wire rst_n           // Active-low reset
);

    // Input mapping
    wire T = ui_in[0];

    // Output register
    reg Q;

    // T Flip-Flop behavior
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            Q <= 1'b0;
        else if (ena) begin
            if (T)
                Q <= ~Q;
            else
                Q <= Q;
        end
    end

    // Output mapping
    assign uo_out[0] = Q;
    assign uo_out[7:1] = 7'b0000000;

    // Unused IOs
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // Prevent unused signal warnings
    wire _unused = &{ui_in[7:1], uio_in, 1'b0};

endmodule
