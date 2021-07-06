.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. highlight:: cpp
.. default-domain:: cpp

=====
Array
=====

The array is a simple concept over the data in |dal_short_name|. It represents
a storage that:

1. Holds the data allocated inside it or references to the external data. The
   data are organized as one :term:`homogeneous <Homogeneous data>` and
   :term:`contiguous <Contiguous data>` memory block.

2. Contains information about the memory block's size.

3. Represents either :term:`immutable <Immutability>` or mutable data.

4. Provides an ability to change the data state from immutable to
   mutable one.

5. Holds ownership information on the data (see the :txtref:`data_ownership_requirements` section).

6. Ownership information on the data can be shared between several arrays. It is
   possible to create a new array from another one without any data copies.

-------------
Usage example
-------------

The following listing provides a brief introduction to the array API and an example of basic
usage scenario:

::

   #include <CL/sycl.hpp>
   #include <iostream>
   #include <string>
   #include "oneapi/dal/array.hpp"

   using namespace oneapi;

   void print_property(const std::string& description, const auto& property) {
      std::cout << description << ": " << property << std::endl;
   }

   int main() {
      sycl::queue queue { sycl::default_selector() };

      constexpr std::int64_t data_count = 4;
      const float data[] = { 1.0f, 2.0f, 3.0f, 4.0f };

      // Creating an array from immutable user-defined memory
      auto arr_data = dal::array<float>::wrap(data, data_count);

      // Creating an array from internally allocated memory filled by ones
      auto arr_ones = dal::array<float>::full(queue, data_count, 1.0f);

      print_property("Is arr_data mutable", arr_data.has_mutable_data()); // false
      print_property("Is arr_ones mutable", arr_ones.has_mutable_data()); // true

      // Creating new array from arr_data without data copy - they share ownership information.
      dal::array<float> arr_mdata = arr_data;

      print_property("arr_mdata elements count", arr_mdata.get_count()); // equal to data_count
      print_property("Is arr_mdata mutable", arr_mdata.has_mutable_data()); // false

      /// Copying data inside arr_mdata to new mutable memory block.
      /// arr_data still refers to the original data pointer.
      arr_mdata.need_mutable_data(queue);

      print_property("Is arr_data mutable", arr_data.has_mutable_data()); // false
      print_property("Is arr_mdata mutable", arr_mdata.has_mutable_data()); // true

      queue.submit([&](sycl::handler& cgh){
         auto mdata = arr_mdata.get_mutable_data();
         auto cones = arr_ones.get_data();
         cgh.parallel_for<class array_addition>(sycl::range<1>(data_count), [=](sycl::id<1> idx) {
            mdata[idx[0]] += cones[idx[0]];
         });
      }).wait();

      std::cout << "arr_mdata values: ";
      for(std::int64_t i = 0; i < arr_mdata.get_count(); i++) {
         std::cout << arr_mdata[i] << ", ";
      }
      std::cout << std::endl;

      return 0;
   }

.. _data_ownership_requirements:

---------------------------
Data ownership requirements
---------------------------

The array shall satisfy the following requirements on managing the memory blocks:

1. An array shall retain:

   -  A pointer to the immutable data block of size ``count``;

   -  A pointer to the mutable data block of size ``count``.

2. If an array represents mutable data, both pointers shall point to the mutable data block.

3. If an array represents immutable data, pointer to the mutable data block shall be ``nullptr``.

4. An array shall use shared ownership semantics to manage the lifetime of the stored data block:

   - Several array objects may own the same data block;

   - An array releases the ownership when one of the following happens:

     - The array owning the data block is destroyed;

     - The array owning the data block is assigned another memory block via
       ``operator=`` or ``reset()``;

   - If the array that releases the ownership is the last remaining object owning the data block,
     the release of ownership is followed by the data block deallocation.

   - The data block is deallocated using the deleter object that is provided to array during
     construction. If no deleter object provided, an array calls the default deallocating
     function that corresponds to the internal memory allocation mechanism.

5. If a managed pointer to the data block is replaced by another pointer via ``reset()``, the
   array that managed the pointer releases the ownership of it and starts managing the lifetime of the data block
   represented by the other pointer.

6. If an array changes its state from immutable to mutable via ``need_mutable_data()``, it releases
   the ownership of immutable data block and start managing lifetime of the mutable data block.

7. An array object may own no data. An array like this is called **zero-sized**:

   - Pointers to the immutable and mutable data of the zero-sized array shall be ``nullptr``;
   - The data block size ``count`` shall be ``0``.


.. _implementation_notes:

--------------------
Implementation notes
--------------------
A typical array implementation may be organized in the following way:

1. An array class has the following member variables:

   - A pointer to the immutable data block;

   - A pointer to the mutable data block;

   - A pointer to the ownership structure that implements the shared ownership semantics;

   - The data block size ``count``;

2. An ownership structure is an object that stores:

   - A pointer to either immutable or mutable data block;

   - The deleter object;

   - The reference count (the number of array objects that own the associated data block);

3. If an array starts managing the lifetime of the data block represented by the pointer ``p`` and
   deleter ``d``, it creates the ownership structure object and initialize it with ``p`` and ``d``.
   The reference count of the ownership structure is assigned one.

4. If an array object releases the ownership, the reference count of the ownership structure is
   decremented.

   - If that count reaches zero, the ownership structure deallocates the memory block and
     the array destroys the ownership structure.

   - If that count is greater than zero, the ownership structure is not destroyed.

5. If a copy of the array object is created, the reference count of the ownership structure is
   incremented and a pointer to the same ownership structure is assigned to the created copy.
   The other member variables of an array class are copied as is.

.. TODO: Add note regarding thread safety

.. note::
   You may choose an arbitrary implementation strategy that satisfies array requirements.


.. _programming_interface:

---------------------
Programming interface
---------------------

All types and functions in this section shall be declared in the
``oneapi::dal`` namespace and be available via inclusion of the
``oneapi/dal/array.hpp`` header file.

All the ``array`` class methods can be divided into several groups:

1. Constructors that are used to create an array from external, mutable or
   immutable memory.

2. Constructors and assignment operators that are used to create an array that shares its data
   with another one.

3. The group of ``reset()`` methods that are used to re-assign an array to another external
   memory block.

4. The group of ``reset()`` methods that are used to re-assign an array to an internally
   allocated memory block.

5. The methods that are used to access the data.

6. Static methods that provide simplified ways to create an array either from external
   memory or by allocating it within a new object.

.. onedal_class:: oneapi::dal::array
