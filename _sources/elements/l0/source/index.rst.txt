.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _l0-section:

==========
Level Zero
==========

The |l0_full_name| (Level Zero) provides low-level
direct-to-metal interfaces that are tailored to the devices in a
oneAPI platform.  Level Zero supports broader language
features such as function pointers, virtual functions, unified memory,
and I/O capabilities while also providing fine-grain explicit controls
needed by higher-level runtime APIs including:

* Device discovery
* Memory allocation
* Peer-to-peer communication
* Inter-process sharing
* Kernel submission
* Asynchronous execution and scheduling
* Synchronization primitives
* Metrics reporting

The API architecture exposes both physical and logical abstractions of
the underlying oneAPI platform devices and their capabilities. The
device, sub-device, and memory are exposed at a physical level while
command queues, events, and synchronization methods are defined as
logical entities. All logical entities are bound to device-level
physical capabilities.  The API provides a scheduling model that is
tailored to multiple uses including a low-latency submission model to
the devices as well as one that is tailored to the construction and
submission of work across simultaneous host threads.  While heavily
influenced by other low-level APIs, such as OpenCL, Level Zero is designed
to evolve independently. While heavily influenced by GPU architecture,
Level Zero is supportable across different oneAPI compute device
architectures, such as FPGAs.


Detailed API Descriptions
-------------------------

The detailed specification can be found online in the specification_.

.. _specification: https://spec.oneapi.com/level-zero/latest/index.html
