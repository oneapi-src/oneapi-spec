.. SPDX-FileCopyrightText: 2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

============
Introduction
============

Open Volume Kernel Library (Open VKL) is a collection of
high-performance volume computation kernels. The target users of Open
VKL are graphics application engineers who want to improve the
performance of their volume rendering applications by leveraging Open
VKL’s performance-optimized kernels, which include volume traversal
and sampling functionality for a variety of volumetric data
formats.

Open VKL provides a C API, and also supports applications written with
the Intel® SPMD Program Compiler (ISPC) by also providing an ISPC
interface to the core volume algorithms. This makes it possible to
write a renderer in ISPC that automatically vectorizes and leverages
SSE, AVX, AVX2, and AVX-512 instructions. ISPC also supports runtime
code selection, thus ISPC will select the best code path for your
application.
