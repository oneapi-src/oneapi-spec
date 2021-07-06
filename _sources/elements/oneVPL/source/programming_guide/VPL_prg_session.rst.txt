.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _sdk-session:

==============
oneVPL Session
==============

Before calling any oneVPL functions, the application must initialize the
library and create a oneVPL session. A oneVPL session maintains context for the
use of any of :term:`DECODE`, :term:`ENCODE`, :term:`VPP`, :term:`DECODE_VPP` 
functions.

------------------------------------
|msdk_full_name| Dispatcher (Legacy)
------------------------------------

The :cpp:func:`MFXInit` or :cpp:func:`MFXInitEx` function starts (initializes)
a session. The :cpp:func:`MFXClose` function closes (de-initializes) the
session. To avoid memory leaks, always call :cpp:func:`MFXClose` after
:cpp:func:`MFXInit`.

.. important:: :cpp:func:`MFXInit` and :cpp:func:`MFXInitEx` are deprecated 
               starting from API 2.0. Applications must use :cpp:func:`MFXLoad`
               and :cpp:func:`MFXCreateSession` to initialize implementations.

.. important:: For backward compatibility with existent |msdk_full_name|
               applications oneVPL session can be created and initialized by
               the legacy dispacther through :cpp:func:`MFXInit` or
               :cpp:func:`MFXInitEx` calls.

The application can initialize a session as a software-based session
(:cpp:enumerator:`MFX_IMPL_SOFTWARE`) or a hardware-based session
(:cpp:enumerator:`MFX_IMPL_HARDWARE`). In a software-based session, the SDK
functions execute on a CPU. In a hardware-base session, the SDK functions
use platform acceleration capabilities. For platforms that expose multiple
graphic devices, the application can initialize a session on any
alternative graphic device using the :cpp:enumerator:`MFX_IMPL_HARDWARE`,
:cpp:enumerator:`MFX_IMPL_HARDWARE2`, :cpp:enumerator:`MFX_IMPL_HARDWARE3`, or
:cpp:enumerator:`MFX_IMPL_HARDWARE4` values of :cpp:type:`mfxIMPL`.

The application can also initialize a session to be automatic (
:cpp:enumerator:`MFX_IMPL_AUTO` or :cpp:enumerator:`MFX_IMPL_AUTO_ANY`),
instructing the dispatcher library to detect the platform capabilities and
choose the best SDK library available. After initialization, the SDK returns the
actual implementation through the :cpp:func:`MFXQueryIMPL` function.

Internally, the dispatcher works as follows:

#. Dispatcher searches for the shared library with the specific name:

   ========= =============== ====================================
   **OS**    **Name**        **Description**
   ========= =============== ====================================
   Linux\*   libmfxsw64.so.1 64-bit software-based implementation
   Linux     libmfxsw32.so.1 32-bit software-based implementation
   Linux     libmfxhw64.so.1 64-bit hardware-based implementation
   Linux     libmfxhw64.so.1 32-bit hardware-based implementation
   Windows\* libmfxsw32.dll  64-bit software-based implementation
   Windows   libmfxsw32.dll  32-bit software-based implementation
   Windows   libmfxhw64.dll  64-bit hardware-based implementation
   Windows   libmfxhw64.dll  32-bit hardware-based implementation
   ========= =============== ====================================

#. Once the library is loaded, the dispatcher obtains addresses for each SDK
   function. See the
   :ref:`Exported Functions/API Version table <export-func-version-table-2x>` for
   the list of functions to expose.

.. _legacy_search_order:

How the shared library is identified using the implementation search strategy
will vary according to the OS.

* On Windows, the dispatcher searches the following locations, in the specified
  order, to find the correct implementation library:

  #. The :file:`Driver Store` directory for the current adapter.
     All types of graphics drivers can install libraries in this directory. `Learn more about Driver Store <https://docs.microsoft.com/en-us/windows-hardware/drivers/install/driver-store>`__.
  #. The directory specified for the current hardware under the registry key
     ``HKEY_CURRENT_USER\Software\Intel\MediaSDK\Dispatch``.
  #. The directory specified for the current hardware under the registry key
     ``HKEY_LOCAL_MACHINE\Software\Intel\MediaSDK\Dispatch``.
  #. The directory that is stored in these registry keys: :file:`C:\Program Files\Intel\Media SDK`.
     This directory is where legacy graphics drivers install libraries.
  #. The directory where the current module (the module that links the dispatcher)
     is located (only if the current module is a dll).

  After the dispatcher completes the main search, it additionally checks:

  #. The directory of the exe file of the current process, where it looks for
     software implementation only, regardless of which implementation the
     application requested.
  #. Default dll search. This provides loading from the directory of the
     application's exe file and from the :file:`System32` and :file:`SysWOW64`
     directories. `Learn more about default dll search order <https://docs.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order?redirectedfrom=MSDN#search-order-for-desktop-applications>`__.
  #. The :file:`System32` and :file:`SysWOW64` directories, which is where DCH
     graphics drivers install libraries.

* On Linux, the dispatcher searches the following locations, in the specified
  order, to find the correct implementation library:

  #. Directories provided by the environment variable ``LD_LIBRARY_PATH``.
  #. Content of the :file:`/etc/ld.so.cache` cache file.
  #. Default path :file:`/lib`, then :file:`/usr/lib` or :file:`/lib64`, and then
     :file:`/usr/lib64` on some 64 bit OSs. On Debian: :file:`/usr/lib/x86_64-linux-gnu`.
  #. SDK installation folder.


-----------------
oneVPL Dispatcher
-----------------

The oneVPL dispatcher extends the legacy dispatcher by providing additional
ability to select the appropriate implementation based on the implementation
capabilities. Implementation capabilities include information about supported
decoders, encoders, and VPP filters. For each supported encoder, decoder, and
filter, capabilities include information about supported memory types, color
formats, and image (frame) size in pixels.

The recommended approach to configure the dispatcher's capabilities
search filters and to create a session based on a suitable implementation is as
follows:

#. Create loader with :cpp:func:`MFXLoad`.
#. Create loader's configuration with :cpp:func:`MFXCreateConfig`.
#. Add configuration properties with :cpp:func:`MFXSetConfigFilterProperty`.
#. Explore available implementations with :cpp:func:`MFXEnumImplementations`.
#. Create a suitable session with :cpp:func:`MFXCreateSession`.

The procedure to terminate an application is as follows:

#. Destroy session with :cpp:func:`MFXClose`.
#. Destroy loader with :cpp:func:`MFXUnload`.

.. note:: Multiple loader instances can be created.

.. note:: Each loader may have multiple configuration objects associated with it.
          When a configuration object is modified through :cpp:func:`MFXSetConfigFilterProperty`
          it implicitly impacts the state and configuration of the associated loader.

.. important:: One configuration object can handle only one filter property.

.. note:: Multiple sessions can be created by using one loader object.

When the dispatcher searches for the implementation, it uses the following
priority rules:

#. Hardware implementation has priority over software implementation.
#. General hardware implementation has priority over VSI hardware implementation.
#. Highest API version has higher priority over lower API version.

.. note:: Implementation has priority over the API version. In other words, the
          dispatcher must return the implementation with the highest API
          priority (greater than or equal to the implementation requested).

How the shared library is identified using the implementation search strategy
will vary according to the OS.

* On Windows, the dispatcher searches the following locations, in the specified
  order, to find the correct implementation library:

  #. The :file:`Driver Store` directory for all avialable adapters.
     All types of graphics drivers can install libraries in this directory. `Learn more about Driver Store <https://docs.microsoft.com/en-us/windows-hardware/drivers/install/driver-store>`__.
     Applicable only for Intel implementations.
  #. The directory of the exe file of the current process.
  #. Current working directory.
  #. `PATH` enviromental variable.
  #. For backward compatibility with older spec versions, dispatcher also checks
     user-defined search folders which are provided by `ONEVPL_SEARCH_PATH`
     enviromental variable.

* On Linux, the dispatcher searches the following locations, in the specified
  order, to find the correct implementation library:

  #. Directories provided by the environment variable ``LD_LIBRARY_PATH``.
  #. Content of the :file:`/etc/ld.so.cache` cache file.
  #. Default path :file:`/lib`, then :file:`/usr/lib` or :file:`/lib64`, and then
     :file:`/usr/lib64` on some 64 bit OSs. On Debian: :file:`/usr/lib/x86_64-linux-gnu`.
  #. Current working directory.
  #. For backward compatibility with older spec versions, dispatcher also checks
     user-defined search folders which are provided by `ONEVPL_SEARCH_PATH`
     enviromental variable.

When oneVPL dispatcher searchers for the legacy |msdk_full_name|
implementation it uses :ref:`legacy dispatcher search order <legacy_search_order>`.

The dispatcher supports different software implementations. The user can use
the :cpp:member:`mfxImplDescription::VendorID` field, the
:cpp:member:`mfxImplDescription::VendorImplID` field, or the
:cpp:member:`mfxImplDescription::ImplName` field to search for the specific
implementation.

Internally, the dispatcher works as follows:

#. Dispatcher loads any shared library with `libvpl*` prefix in the library name
   in the given search folders.
#. For each loaded library, the dispatcher tries to resolve address of the
   :cpp:func:`MFXQueryImplsDescription` function to collect the implementation's
   capabilities.
#. Once the user has requested to create the session based on this implementation,
   the dispatcher obtains addresses of each oneVPL function. See the
   :ref:`Exported Functions/API Version table <export-func-version-table-2x>` for
   the list of functions to export.

.. note:: For backward compatibility with |msdk_full_name|, the dispatcher will
          first try to load |msdk_full_name| if API version 1.x was requested.
          If loading fails, the dispatcher will search for the implementation with
          highest 2.x API version and load that version.

------------------------------------------
oneVPL Dispatcher Configuration Properties
------------------------------------------

The :ref:`Dispatcher Configuration Properties Table <dsp-conf-prop-table>` shows property strings
supported by the dispatcher. Table organized in the hierarchy way, to create the string, go from the
left to right from column to column and concatenate strings by using `.` (dot) as the separator.

.. _dsp-conf-prop-table:

.. table:: Dispatcher Configuration Properties
   :widths: 25 25 30 20

   +---------------------------------------+----------------------------+----------------------+---------------------------+
   | Structure name                        | Property                   | Value Data Type      | Comment                   |
   +=======================================+============================+======================+===========================+
   | :cpp:struct:`mfxImplDescription`      | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .Impl                    |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 | The mode will be used for |
   |                                       | | .AccelerationMode        |                      | session initilization     |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .ApiVersion              |                      |                           |
   |                                       | | .Version                 |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U16 |                           |
   |                                       | | .ApiVersion              |                      |                           |
   |                                       | | .Major                   |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U16 |                           |
   |                                       | | .ApiVersion              |                      |                           |
   |                                       | | .Minor                   |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_PTR | Pointer to the            |
   |                                       | | .ImplName                |                      | null-terminated string.   |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_PTR | Pointer to the            |
   |                                       | | .License                 |                      | null-terminated string.   |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_PTR | Pointer to the            |
   |                                       | | .Keywords                |                      | null-terminated string.   |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .VendorID                |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .VendorImplID            |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_PTR | Pointer to the            |
   |                                       | | .mfxDeviceDescription    |                      | null-terminated string.   |
   |                                       | | .device                  |                      |                           |
   |                                       | | .DeviceID                |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxDecoderDescription   |                      |                           |
   |                                       | | .decoder                 |                      |                           |
   |                                       | | .CodecID                 |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U16 |                           |
   |                                       | | .mfxDecoderDescription   |                      |                           |
   |                                       | | .decoder                 |                      |                           |
   |                                       | | .MaxcodecLevel           |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxDecoderDescription   |                      |                           |
   |                                       | | .decoder                 |                      |                           |
   |                                       | | .decprofile              |                      |                           |
   |                                       | | .Profile                 |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxDecoderDescription   |                      |                           |
   |                                       | | .decoder                 |                      |                           |
   |                                       | | .decprofile              |                      |                           |
   |                                       | | .Profile                 |                      |                           |
   |                                       | | .decmemdesc              |                      |                           |
   |                                       | | .MemHandleType           |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_PTR | Pointer to the            |
   |                                       | | .mfxDecoderDescription   |                      | :cpp:struct:`mfxRange32U` |
   |                                       | | .decoder                 |                      | object                    |
   |                                       | | .decprofile              |                      |                           |
   |                                       | | .Profile                 |                      |                           |
   |                                       | | .decmemdesc              |                      |                           |
   |                                       | | .Width                   |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_PTR | Pointer to the            |
   |                                       | | .mfxDecoderDescription   |                      | :cpp:struct:`mfxRange32U` |
   |                                       | | .decoder                 |                      | object                    |
   |                                       | | .decprofile              |                      |                           |
   |                                       | | .Profile                 |                      |                           |
   |                                       | | .decmemdesc              |                      |                           |
   |                                       | | .Height                  |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxDecoderDescription   |                      |                           |
   |                                       | | .decoder                 |                      |                           |
   |                                       | | .decprofile              |                      |                           |
   |                                       | | .Profile                 |                      |                           |
   |                                       | | .decmemdesc              |                      |                           |
   |                                       | | .ColorFormats            |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxEncoderDescription   |                      |                           |
   |                                       | | .encoder                 |                      |                           |
   |                                       | | .CodecID                 |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U16 |                           |
   |                                       | | .mfxEncoderDescription   |                      |                           |
   |                                       | | .encoder                 |                      |                           |
   |                                       | | .MaxcodecLevel           |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U16 |                           |
   |                                       | | .mfxEncoderDescription   |                      |                           |
   |                                       | | .encoder                 |                      |                           |
   |                                       | | .BiDirectionalPrediction |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxEncoderDescription   |                      |                           |
   |                                       | | .encoder                 |                      |                           |
   |                                       | | .encprofile              |                      |                           |
   |                                       | | .Profile                 |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxEncoderDescription   |                      |                           |
   |                                       | | .encoder                 |                      |                           |
   |                                       | | .encprofile              |                      |                           |
   |                                       | | .Profile                 |                      |                           |
   |                                       | | .encmemdesc              |                      |                           |
   |                                       | | .MemHandleType           |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_PTR | Pointer to the            |
   |                                       | | .mfxEncoderDescription   |                      | :cpp:struct:`mfxRange32U` |
   |                                       | | .encoder                 |                      | object                    |
   |                                       | | .encprofile              |                      |                           |
   |                                       | | .Profile                 |                      |                           |
   |                                       | | .encmemdesc              |                      |                           |
   |                                       | | .Width                   |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_PTR | Pointer to the            |
   |                                       | | .mfxEncoderDescription   |                      | :cpp:struct:`mfxRange32U` |
   |                                       | | .encoder                 |                      | object                    |
   |                                       | | .encprofile              |                      |                           |
   |                                       | | .Profile                 |                      |                           |
   |                                       | | .encmemdesc              |                      |                           |
   |                                       | | .Height                  |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxEncoderDescription   |                      |                           |
   |                                       | | .encoder                 |                      |                           |
   |                                       | | .encprofile              |                      |                           |
   |                                       | | .Profile                 |                      |                           |
   |                                       | | .encmemdesc              |                      |                           |
   |                                       | | .ColorFormats            |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxVPPDescription       |                      |                           |
   |                                       | | .filter                  |                      |                           |
   |                                       | | .FilterFourCC            |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U16 |                           |
   |                                       | | .mfxVPPDescription       |                      |                           |
   |                                       | | .filter                  |                      |                           |
   |                                       | | .MaxDelayInFrames        |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxVPPDescription       |                      |                           |
   |                                       | | .filter                  |                      |                           |
   |                                       | | .memdesc                 |                      |                           |
   |                                       | | .MemHandleType           |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_PTR | Pointer to the            |
   |                                       | | .mfxVPPDescription       |                      | :cpp:struct:`mfxRange32U` |
   |                                       | | .filter                  |                      | object                    |
   |                                       | | .memdesc                 |                      |                           |
   |                                       | | .Width                   |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_PTR | Pointer to the            |
   |                                       | | .mfxVPPDescription       |                      | :cpp:struct:`mfxRange32U` |
   |                                       | | .filter                  |                      | object                    |
   |                                       | | .memdesc                 |                      |                           |
   |                                       | | .Height                  |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxVPPDescription       |                      |                           |
   |                                       | | .filter                  |                      |                           |
   |                                       | | .memdesc                 |                      |                           |
   |                                       | | .format                  |                      |                           |
   |                                       | | .InFormat                |                      |                           |
   |                                       +----------------------------+----------------------+---------------------------+
   |                                       | | mfxImplDescription       | MFX_VARIANT_TYPE_U32 |                           |
   |                                       | | .mfxVPPDescription       |                      |                           |
   |                                       | | .filter                  |                      |                           |
   |                                       | | .memdesc                 |                      |                           |
   |                                       | | .format                  |                      |                           |
   |                                       | | .OutFormats              |                      |                           |
   +---------------------------------------+----------------------------+----------------------+---------------------------+
   | :cpp:struct:`mfxImplementedFunctions` | | mfxImplementedFunctions  | MFX_VARIANT_TYPE_PTR | Pointer to the buffer     |
   |                                       | | .FunctionsName           |                      | with string               |
   +---------------------------------------+----------------------------+----------------------+---------------------------+
   | N/A                                   | | DXGIAdapterIndex         | MFX_VARIANT_TYPE_U32 | Adapter index according   |
   |                                       | |                          |                      | to                        |
   |                                       | |                          |                      | IDXGIFactory::EnumAdapters|
   +---------------------------------------+----------------------------+----------------------+---------------------------+

.. important:: DXGIAdapterNum property is available for Windows only and filters only hardware implementations.

Examples of the property name strings:

- mfxImplDescription.mfxDecoderDescription.decoder.decprofile.Profile
- mfxImplDescription.mfxDecoderDescription.decoder.decprofile.decmemdesc.MemHandleType
- mfxImplementedFunctions.FunctionsName

Following properties are supported in a special manner: they are used to send
additional data to the implementation through the dispatcher. Application needs
to use :cpp:func:`MFXSetConfigFilterProperty` to set them up but they don't
influence on the implementation selection. They are used during the
:cpp:func:`MFXCreateSession` function call to fine tune the implementation.

.. list-table:: Dispatcher's Special Properties
   :header-rows: 1
   :widths: 50 50

   * - **Property**
     - **Value data type**
   * - :cpp:enum:`mfxHandleType`
     - :cpp:enumerator:`mfxVariantType::MFX_VARIANT_TYPE_U32`
   * - :cpp:type:`mfxHDL`
     - :cpp:enumerator:`mfxVariantType::MFX_VARIANT_TYPE_PTR`

------------------------------
oneVPL Dispatcher Interactions
------------------------------

This sequence diagram visualize how application communcates with implementations
via the dispacher.

Dispatcher API
    This API is implemented in the dispatcher.

Implementation API
    This API is provided by the any implementation.

.. uml::

   @startuml
   actor Application as A
   participant "oneVPL Dispatcher" as D
   participant "oneVPL Implementation 1" as I1
   participant "oneVPL Implementation 2" as I2
   participant "oneVPL Implementation 3" as I3

   ref over A, D : Dispatcher API
   ref over D, I1, I2, I3 : Implementation API

   activate A
   == Initialization ==
   group Dispatcher API [Enumerate and load implementations]
      A -> D: mfxLoad()
      activate D

      D -> D: Search for the available runtimes

      A -> D: MFXCreateConfig()
      A -> D: MFXSetConfigProperty()
      A -> D: MFXCreateConfig()
      A -> D: MFXSetConfigProperty()
      A -> D: MFXEnumImplementations()

      Activate I1

      D -> I1: MFXQueryImplsDescription()
      I1 --> D: mfxImplDescription

      Activate I2
      D -> I2: MFXQueryImplsDescription()
      I2 --> D: mfxImplDescription

      Activate I3
      D -> I3: MFXQueryImplsDescription()
      I3 --> D: mfxImplDescription

      D --> A: list of mfxImplDescription structures es for all implementations

      A -> D: MFXCreateSession(i=0)
      D -> I1: MFXInitilize()
      Activate I1 #DarkSalmon
      I1 --> D: mfxSession1
      D --> A: mfxSession1

      A -> D: MFXCreateSession(i=1)
      D -> I2: MFXInitilize()
      Activate I2 #DarkSalmon
      I2 --> D: mfxSession2
      D --> A: mfxSession2

      A -> D: MFXCreateSession(i=2)
      D -> I3: MFXInitilize()
      I3 --> D: mfxSession3
      Activate I3 #DarkSalmon
      D --> A: mfxSession3

      A -> D: MFXDispReleaseImplDescription(hdl=0)
      D -> I1: MFXReleaseImplDescription()

      A -> D: MFXDispReleaseImplDescription(hdl=1)
      D -> I2: MFXReleaseImplDescription()

      A -> D: MFXDispReleaseImplDescription(hdl=2)
      D -> I3: MFXReleaseImplDescription()
   end
   == Processing ==
   group Implementation API [Process the data]
      A -> I1: MFXVideoDECODE_Init()
      A -> I1: MFXVideoDECODE_Query()
      A -> I1: MFXVideoDECODE_DecodeFrameAsync()
      ...
      A -> I1: MFXVideoDECODE_Close()
      |||
      deactivate I1

      A -> I2: MFXVideoENCODE_Init()
      A -> I2: MFXVideoENCODE_Query()
      A -> I2: MFXVideoENCODE_EncodeFrameAsync()
      ...
      A -> I2: MFXVideoENCODE_Close()
      |||
      deactivate I2

      A -> I3: MFXVideoENCODE_Init()
      A -> I3: MFXVideoENCODE_Query()
      A -> I3: MFXVideoENCODE_EncodeFrameAsync()
      ...
      A -> I3: MFXVideoENCODE_Close()
      |||
      deactivate I3
   end
   == Finalization ==
   group Implementation API [Release the implementations]
      A -> I1: MFXClose()
      deactivate I1
      A -> I2: MFXClose()
      deactivate I2
      A -> I3: MFXClose()
      deactivate I3
   group Dispatcher API [Release the dispatcher's instance]
      A -> D: MFXUnload()
   end

   deactivate D
   @enduml

The oneVPL dispacther is capable to load and initialize |msdk_full_name| legacy
library. The sequence diagram below demonstrates the approach.

.. uml::

   @startuml
   actor Application as A
   participant "oneVPL Dispatcher" as D
   participant "MediaSDK (legacy)" as M
   A -> D: MFXLoad
   activate D
   D -> D: Search for the avialable runtimes
   A -> D: MFXCreateConfig
   
   note left of D
   Setting properties to filter implementation.
   MediaSDK supports only general parameters,
   no filtering for Decode/VPP/Encoder details.
   end note

   group MediaSDK LegacyAPI
      D -> M: MFXInitEx
      activate M

      M --> D: mfxSession
      D -> M: MFXQueryIMPL
      M --> D: Implementation speciefic

      D -> M: MFXQueryVersion
      M --> D: mfxVersion
   end

   D -> D: Fill mfxImplDescription for MediaSDK impl

   A -> D: mfxEnumImplementations
   D --> A: MediaSDK caps description

   A -> D: MFXCreateSession
   D --> A: mfxSession

   A -> M: MFXVideoDECODE_Init()
   A -> M: MFXVideoDECODE_Query()
   A -> M: MFXVideoDECODE_DecodeFrameAsync()
   ...
   A -> M: MFXVideoDECODE_Close()
   A -> M: MFXClose()

   deactivate M

   A -> D: MFXUnload()
   deactivate D
   @enduml

.. important:: The dispacther doesn't filter and report
               :cpp:struct:`mfxDeviceDescription`,
               :cpp:struct:`mfxDecoderDescription`,
               :cpp:struct:`mfxEncoderDescription`,
               :cpp:struct:`mfxVPPDescription` when enumerates or creates
               |msdk_full_name| implementation. Once |msdk_full_name| is loaded
               applications have to use legacy approach to query capabilities.

---------------------------
oneVPL Dispatcher Debug Log
---------------------------

The debug output of the dispatcher is controlled with the `ONEVPL_DISPATCHER_LOG`
environment variable. To enable log output, set the `ONEVPL_DISPATCHER_LOG`
environment variable value equals to "ON".

By default, oneVPL dispatcher prints all log messages to the console.
To redirect log output to the desired file, set the `ONEVPL_DISPATCHER_LOG_FILE`
environmental variable with the file name of the log file.

------------------------------
Examples of Dispathcer's Usage
------------------------------

This code illustrates simple usage of dispathcer to load first avialable
library:

.. literalinclude:: ../snippets/prg_disp.c
   :language: c++
   :start-after: /*beg1*/
   :end-before: /*end1*/
   :lineno-start: 1

This code illustrates simple usage of dispathcer to load first avialable HW
accelerated library:

.. literalinclude:: ../snippets/prg_disp.c
   :language: c++
   :start-after: /*beg2*/
   :end-before: /*end2*/
   :lineno-start: 1

This code illustrates how multiple sessions from multiple loaders can be
created:

.. literalinclude:: ../snippets/prg_disp.c
   :language: c++
   :start-after: /*beg3*/
   :end-before: /*end3*/
   :lineno-start: 1

This code illustrates how multiple decoders from single loader can be
created:

.. literalinclude:: ../snippets/prg_disp.c
   :language: c++
   :start-after: /*beg4*/
   :end-before: /*end4*/
   :lineno-start: 1

---------------------------------------
How To Check If Function is Implemented
---------------------------------------

There are two ways to check if particular function is implemented or not by the
implementation.

This code illustrates how application can iterate through the whole list of
implemented functions:

.. literalinclude:: ../snippets/prg_session.cpp
   :language: c++
   :start-after: /*beg1*/
   :end-before: /*end1*/
   :lineno-start: 1

This code illustrates how application can check that specific functions are
implemented:

.. literalinclude:: ../snippets/prg_session.cpp
   :language: c++
   :start-after: /*beg2*/
   :end-before: /*end2*/
   :lineno-start: 1

--------------------------------------------------------------
How To Search For The Avialable encoder/decoder implementation
--------------------------------------------------------------

The :ref:`CodecFormatFourCC <codec-format-fourcc>` enum specifies codec's FourCC
values. Application needs to assign this value to the field of
:cpp:member:`mfxDecoderDescription::decoder::CodecID` to search for the decoder
or :cpp:member:`mfxEncoderDescription::encoder::CodecID` to search for the
encoder.

This code illustrates decoder's implementation search procedure:

.. literalinclude:: ../snippets/prg_session.cpp
   :language: c++
   :start-after: /*beg3*/
   :end-before: /*end3*/
   :lineno-start: 1

---------------------------------------------------------
How To Search For The Avialable VPP Filter implementation
---------------------------------------------------------

Each VPP filter identified by the filter ID. Filter ID is defined by
corresponding to the filter extension buffer ID value which is defined in a form
of fourCC value.
Filter ID values are subset of the general :ref:`ExtendedBufferID <extendedbufferid>`
enum. The :ref:`table <vpp-filters-ids>` references avialable IDs of VPP filters
to search. Application needs to assign this value to the field of
:cpp:member:`mfxVPPDescription::filter::FilterFourCC` to search for the needed
VPP filter.

.. _vpp-filters-ids:

.. list-table:: VPP Filters ID
   :header-rows: 1
   :widths: 58 42

   * - **Filter ID**
     - **Description**
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_DENOISE`
     - Denoise filter (deprecated in 2.2)
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_DENOISE2`
     - Denoise filter
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_MCTF`
     - Motion-Compensated Temporal Filter (MCTF).
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_DETAIL`
     - Detail/edge enhancement filter.
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_FRAME_RATE_CONVERSION`
     - Frame rate conversion filter
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_IMAGE_STABILIZATION`
     - Image stabilization filter
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_PROCAMP`
     - ProcAmp filter
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_FIELD_PROCESSING`
     - Field processing filter
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_COLOR_CONVERSION`
     - Color Conversion filter
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_SCALING`
     - Resize filter
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_COMPOSITE`
     - Surfaces composition filter
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_DEINTERLACING`
     - Deinterlace filter
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_ROTATION`
     - Rotation filter
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_MIRRORING`
     - Mirror filter
   * - :cpp:enumerator:`MFX_EXTBUFF_VPP_COLORFILL`
     - ColorFill filter

This code illustrates VPP mirror filter implementation search procedure:

.. literalinclude:: ../snippets/prg_session.cpp
   :language: c++
   :start-after: /*beg4*/
   :end-before: /*end4*/
   :lineno-start: 1

-------------------------------------------------------------
How To Get Path to the Shared Library With the Implementation
-------------------------------------------------------------

Sessions can be created from different implementations, each implementations can
be located in different shared libraries. To get path of the shared library with
the implementation from which session can be or was created, application can use
:cpp:func:`MFXEnumImplementations` and pass :cpp:enumerator:`MFX_IMPLCAPS_IMPLPATH`
value as the outpt data request.

This code illustrates collection and print out path of implementations's
shared library:

.. literalinclude:: ../snippets/prg_session.cpp
   :language: c++
   :start-after: /*beg5*/
   :end-before: /*end5*/
   :lineno-start: 1

-----------------------------------------------------------------------------------------------------------
oneVPL implementation on |intel_r| platforms with X\ :sup:`e` architecture and |msdk_full_name| Coexistence 
-----------------------------------------------------------------------------------------------------------

oneVPL supersedes |msdk_full_name| and partially binary compartible with
|msdk_full_name|. Both oneVPL and |msdk_full_name| includes own dispatcher and
implementation. Coexistance of oneVPL and |msdk_full_name| dispatchers and
implementations on single system is allowed until |msdk_full_name| is not EOL.

Usage of the following combinations of dispatchers and implementations within
the single application is permitted for the legacy purposes only. In that
scenario legacy applications developed with |msdk_full_name| will continue to
work on any HW supported either by |msdk_full_name| or by the oneVPL.

.. attention:: Any application to work with the oneVPL API starting from version
               2.0 must use only oneVPL dispatcher.

|msdk_full_name| API
    |msdk_full_name| API of 1.x version.

Removed API
    |msdk_full_name| :ref:`API <deprecated-api>` which is removed from oneVPL.

Core API
    |msdk_full_name| API without removed API.

oneVPL API
    New :ref:`API <new-api>` introduced in oneVPL only started from API 2.0
    version.

oneVPL Dispatcher API
    Dispatcher :ref:`API <dispatcher-api>` introduced in oneVPL in 2.0
    API version. This is subset of oneVPL API.

.. list-table:: oneVPL for |intel_r| platforms with X\ :sup:`e` architecture and |msdk_full_name|
   :header-rows: 1
   :widths: 25 25 25 25

   * - **Dispatcher**
     - **Installed on the device**
     - **Loaded**
     - **Allowed API**
   * - oneVPL
     - oneVPL for |intel_r| platforms with X\ :sup:`e` architecture
     - oneVPL for |intel_r| platforms with X\ :sup:`e` architecture
     - Usage of any API except removed API is allowed.
   * - oneVPL
     - |msdk_full_name|
     - |msdk_full_name|
     - Usage of core API plus dispatcher API is allowed only.
   * - oneVPL
     - oneVPL for |intel_r| platforms with X\ :sup:`e` architecture and |msdk_full_name|
     - oneVPL for |intel_r| platforms with X\ :sup:`e` architecture
     - Usage of any API except removed API is allowed.
   * - |msdk_full_name|
     - oneVPL for |intel_r| platforms with X\ :sup:`e` architecture
     - oneVPL for |intel_r| platforms with X\ :sup:`e` architecture
     - Usage of core API is allowed only.
   * - |msdk_full_name|
     - oneVPL for |intel_r| platforms with X\ :sup:`e` architecture and |msdk_full_name|
     - |msdk_full_name|
     - Usage of |msdk_full_name| API is allowed.
   * - |msdk_full_name|
     - |msdk_full_name|
     - |msdk_full_name|
     - Usage of |msdk_full_name| API is allowed.

.. note:: if system has multiple devices the logic of selection and loading implementations
          will be applied to each device accordingly to the system enumeration.

-----------------
Multiple Sessions
-----------------

Each oneVPL session can run exactly one instance of the DECODE, ENCODE, and
VPP functions. This is adequate for a simple transcoding operation. If the
application needs more than one instance of DECODE, ENCODE, or VPP
in a complex transcoding setting or needs more simultaneous transcoding
operations, the application can initialize multiple
oneVPL sessions created from one or several oneVPL implementations. 

The application can use multiple oneVPL sessions independently or run a “joined”
session. To join two sessions together, the application can use the function
:cpp:func:`MFXJoinSession`. Alternatively, the application can use the
:cpp:func:`MFXCloneSession` function to duplicate an existing session. Joined
oneVPL sessions work together as a single session, sharing all session
resources, threading control, and prioritization operations except hardware
acceleration devices and external allocators. When joined, the first session
(first join) serves as the parent session and will schedule execution resources
with all other child sessions. Child sessions rely on the parent session for
resource management.

.. important:: Applications can join sessions created from the same oneVPL 
               implementation only.

With joined sessions, the application can set the priority of session operations
through the :cpp:func:`MFXSetPriority` function. A lower priority session
receives fewer CPU cycles. Session priority does not affect hardware accelerated
processing.

After the completion of all session operations, the application can use the
:cpp:func:`MFXDisjoinSession` function to remove the joined state of a session.
Do not close the parent session until all child sessions are disjoined or
closed.
