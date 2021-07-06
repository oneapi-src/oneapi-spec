.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. highlight:: cpp
.. default-domain:: cpp

.. _descriptors:

===========
Descriptors
===========
**A descriptor** is an object that represents an algorithm including all its
meta-parameters, dependencies on other algorithms, floating-point types,
computational methods and tasks. A descriptor serves as:

- A dispatching mechanism for :txtref:`operations`. Based on a descriptor
  type, an operation executes a particular algorithm implementation.

- An aggregator of meta-parameters. It provides an interface for setting up
  meta-parameters at either compile-time or run-time.

- An object that stores the state of the algorithm. In the general case, a descriptor is
  a stateful object whose state changes after an operation is applied.

Each oneDAL algorithm has its own dedicated namespace, where the corresponding
descriptor is defined (for more details, see :txtref:`Namespaces
<common_namespaces>`). Descriptor, in its turn, defines the following:

- **Template parameters.** A descriptor is allowed to have any number of template
  parameters, but shall support at least three:

   + ``Float`` is a `floating-point type <floating-point_>`_ that the algorithm
     uses for computations. This parameter is defined first and has the
     ``oneapi::dal::default_float_t`` default value.

   + ``Method`` is a tag-type that specifies the `computational method
     <methods_>`_. This parameter is defined second and has the
     ``method::by_default`` default value.

   + ``Task`` is a tag-type that specifies the `computational task <tasks_>`_.
     This parameter is defined third and has the ``task::by_default`` default
     value.

- **Properties.** A property is a run-time parameter that can be accessed by
  means of the corresponding :term:`getter <Getter>` and :term:`setter <Setter>`
  methods.

`The following code sample <descriptor_template_>`_ shows the common structure
of a descriptor's definition for an abstract algorithm. To define a particular
algorithm, the following strings shall be substituted:

- ``%ALGORITHM%`` is the name of an algorithm and its namespace. All classes and
  structures related to that algorithm are defined within the namespace.

- ``%PROPERTY_NAME%`` and ``%PROPERTY_TYPE%`` are the name and the type of one
  of the algorithm's properties.

.. code-block:: cpp
   :name: descriptor_template

   namespace oneapi::dal::%ALGORITHM% {

   template <typename Float  = default_float_t,
             typename Method = method::by_default,
             typename Task   = task::by_default,
             /* more template parameters */>
   class descriptor {
   public:
      /* Constructor */
      descriptor(const %PROPERTY_TYPE%& %PROPERTY_NAME%,
                 /* more properties */)

      /* Getter & Setter for the property called `%PROPERTY_NAME%` */
      descriptor& set_%PROPERTY_NAME%(%PROPERTY_TYPE% value);
      %PROPERTY_TYPE% get_%PROPERTY_NAME%() const;

      /* more properties */
   };

   } // namespace oneapi::dal::%ALGORITHM%


Each meta-parameter of an algorithm is mapped to a property that shall satisfy
the following requirements:

.. _property_reqs:

- Properties are defined with getter and setter methods. The underlying
  class member variable that stores the property's value is never exposed in the
  descriptor interface.

- The getter returns the value of the underlying class member variable.

- The setter accepts only one parameter of the property's type and assigns it
  to the underlying class member variable.

- Most of the properties are preset with default values, others
  are initialized by passing the required parameters to the constructor.

- The setter returns a reference to the descriptor object to allow chaining
  calls as shown in the example below.

  .. code-block:: cpp

     auto desc = descriptor{}
        .set_property_name_1(value_1)
        .set_property_name_2(value_2)
        .set_property_name_3(value_3);


.. _floating-point:

--------------------
Floating-point Types
--------------------
It is required for each algorithm to support at least one implementation-defined
floating-point type. Other floating-point types are optional, for example ``float``,
``double``, ``float16``, and ``bfloat16``. It is up to a specific oneDAL
implementation whether or not to support these types.

The floating-point type used as a default in descriptors is
implementation-defined and shall be declared within the top-level namespace.

.. code-block:: cpp

   namespace oneapi::dal {
      using default_float_t = /* implementation defined */;
   } // namespace oneapi::dal


.. _methods:

---------------------
Computational Methods
---------------------
The supported computational methods are declared within the
``%ALGORITHM%::method`` namespace using tag-types. Algorithm shall support at
least one method and declare the ``by_default`` type alias that refers to one of
the methods as shown in the example below.

.. code-block:: cpp

   namespace oneapi::dal::%ALGORITHM% {
      namespace method {
         struct x {};
         struct y {};
         using by_default = x;
      } // namespace method
   } // namespace oneapi::dal::%ALGORITHM%


.. _tasks:

-------------------
Computational Tasks
-------------------
The supported computational tasks are declared within the ``%ALGORITHM%::task``
namespace using tag-types. Algorithm shall support at least one task and declare
the ``by_default`` type alias that refers to one of the tasks as shown in the
example below.

If an algorithm assumes both ``classification`` and ``regression`` tasks, the
default task shall be ``classification``. In some cases where an algorithm does
not have the well-defined training and inference stages an algorithm may define
only one task.

.. code-block:: cpp

   namespace oneapi::dal::%ALGORITHM% {
      namespace task {
         struct classification {};
         struct regression {};
         using by_default = classification;
      } // namespace task
   } // namespace oneapi::dal::%ALGORITHM%


