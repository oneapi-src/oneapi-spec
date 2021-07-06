.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _operations:

==========
Operations
==========

**An operation** is a function that transforms :txtref:`a descriptor
<descriptors>` and other arguments represented via `an input <input_>`_ object
to `a result <result_>`_ object. An operation is responsible for:

- Executing all of an algorithm's computational routines represented by the
  descriptor.

- Passing SYCL* queue to computational routines.

- Verifying preconditions and postconditions before and after the execution
  of computational routines.

.. _general_operation:

----------------------------
General operation definition
----------------------------
`The following code sample <operation_template_>`_ shows the declaration of an
abstract operation. To declare a particular operation, the ``%OPERATION%`` shall
be substituted with the name of the operation.

.. code-block:: cpp
   :name: operation_template

   namespace oneapi::dal {

   template <typename Descriptor>
   using %OPERATION%_input_t = /* implementation defined */;

   template <typename Descriptor>
   using %OPERATION%_result_t = /* implementation defined */;

   template <typename Descriptor>
   %OPERATION%_result_t<Descriptor> %OPERATION%(
      sycl::queue& queue,
      const Descriptor& desc,
      const %OPERATION%_input_t<Descriptor>& input);

   } // namespace oneapi::dal


Each operation shall satisfy the following requirements:

- An operation shall accept three parameters in the following order:

  + The SYCL* queue object
  + The descriptor of the algorithm
  + The `input object <input_>`_

- An operation shall return the `result object <result_>`_.

- The ``%OPERATION%_input_t`` and ``%OPERATION%_result_t`` alias
  templates shall be used for inference of the input and return types.

- If a precondition is violated, an operation shall throw an exception derived
  from ``oneapi::dal::logic_error``.

- If a postcondition is violated, an operation shall throw an exception derived
  from ``oneapi::dal::runtime_error``.

- If the descriptor is incompatible with some operation, an error shall be
  reported at compile-time.

- The exact list of compatible operations and pre-/post- conditions shall be
  defined by :txtref:`a particular algorithm specification <algorithms>`.


-------------------
Operation shortcuts
-------------------
In order to make the code on user side less verbose, oneDAL defines the
following overloaded functions called *shortcuts* for each operation in addition
to the general one described in section `General operation definition
<general_operation_>`_.

- A shortcut for execution on :term:`host <Host/Device>` that performs the same
  operation as the general function on host, but does not require the
  queue to be passed explicitly.

  .. code-block:: cpp

     template <typename Descriptor>
     %OPERATION%_result_t<Descriptor> %OPERATION%(
        const Descriptor& desc,
        const %OPERATION%_input_t<Descriptor>& input);

- A shortcut that allows omitting explicit input creation.

  .. code-block:: cpp

     template <typename Descriptor, typename... Args>
     %OPERATION%_result_t<Descriptor> %OPERATION%(
        sycl::queue& queue,
        const Descriptor& desc,
        Args&&... args);

- A shortcut that allows omitting explicit queue and input creation. This is a
  combination of two previous shortcuts.

  .. code-block:: cpp

     template <typename Descriptor, typename... Args>
     %OPERATION%_result_t<Descriptor> %OPERATION%(
        const Descriptor& desc,
        Args&&... args);



.. _input:

-----
Input
-----
An input object aggregates all the data that the algorithm requires for
performing a specific operation. The data is represented via :txtref:`tables
<table>`, so, typically, an input is a collection of tables, but not limited to
them and can aggregate objects of an arbitrary type.

In general, input class definition is similar to :txtref:`descriptor
<descriptors>`. An input defines properties that can be accessed by means of the
corresponding :capterm:`getter` and :capterm:`setter` methods. Requirements to
the input's properties are the same as :txtref:`requirements for descriptor's
properties <property_reqs>`.

`The following code sample <input_template_>`_ shows the common structure of a
inputs's definition. To define an input for particular algorithm and operation,
the following strings shall be substituted:

- ``%ALGORITHM%`` is the name of an algorithm and its namespace.

- ``%OPERATION%`` is the name of operation.

- ``%PROPERTY_NAME%`` and ``%PROPERTY_TYPE%`` are the name and the type of one
  of the input's properties.

.. code-block:: cpp
   :name: input_template

   namespace oneapi::dal::%ALGORITHM% {

   template <typename Task = task::by_default>
   class OPERATION_input {
   public:
      /* Constructor */
      %OPERATION%_input(const %PROPERTY_TYPE%& %PROPERTY_NAME%,
                        /* more properties */)

      /* Getter & Setter for the property called `%PROPERTY_NAME%` */
      descriptor& set_%PROPERTY_NAME%(%PROPERTY_TYPE% value);
      %PROPERTY_TYPE% get_%PROPERTY_NAME%() const;

      /* more properties */
   };

   } // namespace oneapi::dal::%ALGORITHM%


.. note::

   An input is specific to algorithm and operation, so each
   ``%ALGORITHM%``-``%OPERATION%`` pair shall define its own set of the
   properties.


.. _result:

------
Result
------

A result object aggregates all output values computed by the algorithm. All
assumptions about `an input <input_>`_ are applied to a result as well.

.. code-block:: cpp
   :name: result_template

   namespace oneapi::dal::%ALGORITHM% {

   template <typename Task = task::by_default>
   class OPERATION_result {
   public:
      /* Constructor */
      %OPERATION%_result(const %PROPERTY_TYPE%& %PROPERTY_NAME%,
                         /* more properties */)

      /* Getter & Setter for the property called `%PROPERTY_NAME%` */
      descriptor& set_%PROPERTY_NAME%(%PROPERTY_TYPE% value);
      %PROPERTY_TYPE% get_%PROPERTY_NAME%() const;

      /* more properties */
   };

   } // namespace oneapi::dal::%ALGORITHM%


-------------------
Supported operation
-------------------
Refer to the :txtref:`Supported operations <op_supported>` section for
more information about particular operations.

.. toctree::
   :hidden:

   support.rst
