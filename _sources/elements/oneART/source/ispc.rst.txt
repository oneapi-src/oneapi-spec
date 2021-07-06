.. SPDX-FileCopyrightText: 2019-2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _ispc-section:

===================================
ISPC Implicit SPMD Program Compiler
===================================

ISPC is a compiler for a variant of the C programming language, with 
extensions for "single program, multiple data" (SPMD) programming. 
Under the SPMD model, the programmer writes a program that generally 
appears to be a regular serial program, though the execution model is 
actually that a number of program instances execute in parallel on 
the hardware.

ISPC compiles a C-based SPMD programming language to run on the 
SIMD units of CPUs and GPUs; it frequently provides a 3x or more 
speedup on architectures with 4-wide vector SSE units and 5x-6x on 
archituctures with 8-wide AVX vector units, without any of the difficulty 
of writing intrinsics code. Parallelization across multiple cores is 
also supported by ispc, making it possible to write programs that 
achieve performance improvement that scales by both number of 
cores and vector unit size.

More information can be found at the `ISPC Implicit SPMD Program Compiler website`_.

.. _`ISPC Implicit SPMD Program Compiler website`: https://ispc.github.io
