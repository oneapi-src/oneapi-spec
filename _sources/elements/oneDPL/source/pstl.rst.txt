.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

Extensions to Parallel STL
--------------------------

oneDPL extends Parallel STL with the following APIs.

DPC++ Execution Policy
++++++++++++++++++++++

A DPC++ execution policy specifies where and how an algorithm runs.

.. code:: cpp

  // Defined in <oneapi/dpl/execution>

  namespace oneapi {
    namespace dpl {
      namespace execution {

        template <typename KernelName = /*unspecified*/>
        class device_policy;

        device_policy<> dpcpp_default;

        template <typename KernelName = /*unspecified*/>
        device_policy<KernelName>
        make_device_policy( sycl::queue );

        template <typename KernelName = /*unspecified*/>
        device_policy<KernelName>
        make_device_policy( sycl::device );

        template <typename NewKernelName, typename OldKernelName>
        device_policy<NewKernelName>
        make_device_policy( const device_policy<OldKernelName>& = dpcpp_default );
      }
    }
  }

``dpcpp_default`` is a predefined execution policy object to run algorithms on the default DPC++ device.

device_policy class
^^^^^^^^^^^^^^^^^^^

.. code:: cpp

  template <typename KernelName = /*unspecified*/>
  class device_policy
  {
  public:
      using kernel_name = KernelName;

      device_policy();
      template <typename OtherName>
      device_policy( const device_policy<OtherName>& );
      explicit device_policy( sycl::queue );
      explicit device_policy( sycl::device );

      sycl::queue queue() const;
      operator sycl::queue() const;
  };

An object of the ``device_policy`` type is associated with a ``sycl::queue`` that is used
to run algorithms on a DPC++ compliant device.

The ``KernelName`` template parameter, also aliased as ``kernel_name`` within the class template,
is to explicitly provide a name for DPC++ kernels executed by an algorithm the policy is passed to. 

.. code:: cpp

  device_policy()

Construct a policy object associated with a queue created with the default device selector.
  
.. code:: cpp

  template <typename OtherName>
  device_policy( const device_policy<OtherName>& policy )

Construct a policy object associated with the same queue as ``policy``, by changing
the kernel name of the given policy to ``kernel_name`` defined for the new policy.

.. code:: cpp

  explicit device_policy( sycl::queue queue )

Construct a policy object associated with the given queue.

.. code:: cpp

  explicit device_policy( sycl::device device )

Construct a policy object associated with a queue created for the given device.

.. code:: cpp

  sycl::queue queue() const

Return the queue the policy is associated with.

.. code:: cpp

  operator sycl::queue() const

Allow implicit conversion of the policy to a ``sycl::queue`` object.

make_device_policy function
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``make_device_policy`` function templates simplify ``device_policy`` creation.

.. code:: cpp

  template <typename KernelName = /*unspecified*/>
  device_policy<KernelName>
  make_device_policy( sycl::queue queue )

Return a policy object associated with ``queue``, with a kernel name possibly provided
as the template argument, otherwise unspecified.

.. code:: cpp

  template <typename KernelName = /*unspecified*/>
  device_policy<KernelName>
  make_device_policy( sycl::device device )

Return a policy object to run algorithms on ``device``, with a kernel name possibly provided
as the template argument, otherwise unspecified.
  
.. code:: cpp

  template <typename NewKernelName, typename OldKernelName>
  device_policy<NewKernelName>
  make_device_policy( const device_policy<OldKernelName>& policy = dpcpp_default )

Return a policy object constructed from ``policy``, with a new kernel name provided as the template
argument. If no policy object is provided, the new policy is constructed from ``dpcpp_default``.

Buffer wrappers
++++++++++++++++

.. code:: cpp

  // Defined in <oneapi/dpl/iterator>

  namespace oneapi {
    namespace dpl {

      template < typename T, typename AllocatorT, sycl::access::mode Mode >
      /*unspecified*/ begin( sycl::buffer<T, /*dim=*/1, AllocatorT> buf,
                             sycl::mode_tag_t<Mode> tag = sycl::read_write );

      template < typename T, typename AllocatorT, sycl::access::mode Mode >
      /*unspecified*/ begin( sycl::buffer<T, /*dim=*/1, AllocatorT> buf,
                             sycl::mode_tag_t<Mode> tag, sycl::property::noinit );

      template < typename T, typename AllocatorT >
      /*unspecified*/ begin( sycl::buffer<T, /*dim=*/1, AllocatorT> buf,
                             sycl::property::noinit );


      template < typename T, typename AllocatorT, sycl::access::mode Mode >
      /*unspecified*/ end( sycl::buffer<T, /*dim=*/1, AllocatorT> buf,
                           sycl::mode_tag_t<Mode> tag = sycl::read_write );

      template < typename T, typename AllocatorT, sycl::access::mode Mode >
      /*unspecified*/ end( sycl::buffer<T, /*dim=*/1, AllocatorT> buf,
                           sycl::mode_tag_t<Mode> tag, sycl::property::noinit );

      template < typename T, typename AllocatorT >
      /*unspecified*/ end( sycl::buffer<T, /*dim=*/1, AllocatorT> buf,
                           sycl::property::noinit );

    }
  }

``oneapi::dpl::begin`` and ``oneapi::dpl::end`` are helper functions
for passing DPC++ buffers to oneDPL algorithms.
These functions accept a buffer and return an object
of an unspecified type that satisfies the following requirements:

- it is ``CopyConstructible``, ``CopyAssignable``, and comparable
  with operators ``==`` and ``!=``;
- the following expressions are valid: ``a + n``, ``a - n``,
  ``a - b``, where ``a`` and ``b`` are objects of the type,
  and ``n`` is an integer value;
- it provides the ``get_buffer()`` method that returns the buffer
  passed to the ``begin`` or ``end`` function.

When invoking an algorithm, the buffer passed to ``begin`` should be the same
as the buffer passed to ``end``. Otherwise, the behavior is undefined.

``sycl::mode_tag_t`` and ``sycl::property::noinit`` parameters allow to specify
an access mode to be used for accessing the buffer by algorithms.
The mode serves as a hint, and can be overridden depending on semantics of the algorithm.
When invoking an algorithm, the same access mode arguments should be used
for ``begin`` and ``end``. Otherwise, the behavior is undefined.

.. code:: cpp
      
      using namespace oneapi;
      auto buf_begin = dpl::begin(buf, sycl::write_only);
      auto buf_end_1 = dpl::end(buf, sycl::write_only);
      auto buf_end_2 = dpl::end(buf, sycl::write_only, sycl::noinit);
      dpl::fill(dpl::dpcpp_default, buf_begin, buf_end_1, 42); // allowed
      dpl::fill(dpl::dpcpp_default, buf_begin, buf_end_2, 42); // not allowed

