.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

============
Introduction
============

Open Image Denoise is an open, high-quality,
efficient, and easy-to-use denoising library that allows one to
significantly reduce rendering times in ray tracing based rendering
applications. It filters out the Monte Carlo noise inherent to
stochastic ray tracing methods like path tracing, reducing the amount
of necessary samples per pixel by even multiple orders of magnitude
(depending on the desired closeness to the ground truth). A simple but
flexible C/C++ API ensures that the library can be easily integrated
into most existing or new rendering solutions.

At the heart of the Open Image Denoise library is a collection of
efficient deep learning based denoising filters, which were trained to
handle a wide range of samples per pixel (spp), from 1 spp to almost
fully converged. Thus it is suitable for both preview and final-frame
rendering. The filters can denoise images either using only the noisy
color (beauty) buffer, or, to preserve as much detail as possible, can
optionally utilize auxiliary feature buffers as well (e.g. albedo,
normal). Such buffers are supported by most renderers as arbitrary
output variables (AOVs) or can be usually implemented with little
effort.

Although the library ships with a set of pre-trained filter models, it
is not mandatory to use these. To optimize a filter for a specific
renderer, sample count, content type, scene, etc., it is possible to
train the model using the included training toolkit and user-provided
image datasets.
