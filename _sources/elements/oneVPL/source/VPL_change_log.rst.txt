.. SPDX-FileCopyrightText: 2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

==========
Change Log
==========

This section describes the API evolution from version to version.

.. contents::
   :local:
   :depth: 1

-----------
Version 2.4
-----------

* Added ability to retrieve path to the shared library with the implementation.
* Added 3DLUT (Three-Dimensional Look Up Table) filter in VPP.
* Added mfxGUID structure to specify Globally Unique Identifiers (GUIDs).
* Added QueryInterface function to mfxFrameSurfaceInterface.
* Added AdaptiveRef and alias for ExtBrcAdaptiveLTR.
* Added MFX_FOURCC_BGRP FourCC for Planar BGR format.
* Enviromental variables to control dispatcher's logger.

-----------
Version 2.3
-----------

* Encoding in Hyper mode.
* New product names for platforms:

    * Code name Rocket Lake,
    * Code name Alder Lake S,
    * Code name Alder Lake P,
    * Code name for Arctic Sound P.
    * For spec version 2.3.1 MFX_PLATFORM_XEHP_SDV alias was added

* mfx.h header file is added which includes all header files.
* Added deprecation messages (deprecation macro) to the functions MFXInit and
  MFXInitEx functions definition.
