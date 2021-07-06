.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. highlight:: cpp
.. default-domain:: cpp

.. _column_accessor:

===============
Column accessor
===============

The ``column_accessor`` class provides a read-only access to the column values
of the :txtref:`table` as :capterm:`contiguous <contiguous data>`
:capterm:`homogeneous <homogeneous data>` array.

-------------
Usage example
-------------

::

   #include <CL/sycl.hpp>
   #include <iostream>

   #include "oneapi/dal/table/homogen.hpp"
   #include "oneapi/dal/table/column_accessor.hpp"

   using namespace oneapi;

   int main() {
      sycl::queue queue { sycl::default_selector() };

      constexpr float host_data[] = {
         1.0f, 1.5f, 2.0f,
         2.1f, 3.2f, 3.7f,
         4.0f, 4.9f, 5.0f,
         5.2f, 6.1f, 6.2f
      };

      constexpr std::int64_t row_count = 4;
      constexpr std::int64_t column_count = 3;

      auto shared_data = sycl::malloc_shared<float>(row_count * column_count, queue);
      auto event = queue.memcpy(shared_data, host_data, sizeof(float) * row_count * column_count);
      auto t = dal::homogen_table::wrap(queue, data, row_count, column_count, { event });

      // Accessing whole elements in a first column
      dal::column_accessor<const float> acc { t };

      auto block = acc.pull(queue, 0);
      for(std::int64_t i = 0; i < block.get_count(); i++) {
         std::cout << block[i] << ", ";
      }
      std::cout << std::endl;

      sycl::free(shared_data, queue);
      return 0;
   }

---------------------
Programming interface
---------------------

All types and functions in this section shall be declared in the
``oneapi::dal`` namespace and be available via inclusion of the
``oneapi/dal/table/column_accessor.hpp`` header file.

.. onedal_class:: oneapi::dal::column_accessor
