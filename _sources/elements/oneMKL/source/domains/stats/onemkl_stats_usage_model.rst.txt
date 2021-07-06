.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_stats_usage_model:

oneMKL Summary Statistics Usage Model
=====================================


.. rubric:: Description

A typical algorithm for summary statistics is as follows:


#. Create and initialize an object for dataset.
#. Call the summary statistics routine to calculate the appropriate estimate.


The following example demonstrates how to calculate mean values for a 3-dimensional dataset filled with random numbers. For dataset creation, the :ref:`onemkl_stats_make_dataset` helper function is used.


Buffer-based example
--------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>

    #include "CL/sycl.hpp"
    #include "oneapi/mkl/stats.hpp"

    int main() {
        sycl::queue queue;

        const size_t n_observations = 1000;
        const size_t n_dims = 3;
        std::vector<float> x(n_observations * n_dims);
        // fill x storage with random numbers
        for(int i = 0; i < n_dims, i++) {
          for(int j = 0; j < n_observations; j++) {
                x[j + i * n_observations] = float(std::rand()) / float(RAND_MAX);
            }
        }
        //create buffer for dataset
        sycl::buffer<float, 1> x_buf(x.data(), x.size());
        // create buffer for mean values
        sycl::buffer<float, 1> mean_buf(n_dims);
        // create oneapi::mkl::stats::dataset
        auto dataset = oneapi::mkl::stats::make_dataset<oneapi::mkl::stats::layout::row_major>(n_dims, n_observations, x_buf);


        oneapi::mkl::stats::mean(queue, dataset, mean_buf);


        // create host accessor for mean_buf to print results
        auto acc = mean_buf.template get_access<sycl::access::mode::read>();


        for(int i = 0; i < n_dims; i++) {
          std::cout << "Mean value for dimension " << i << ": " << acc[i] << std::endl;
        }
        return 0;
    }


USM-based example
-----------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>

    #include "CL/sycl.hpp"
    #include "oneapi/mkl/stats.hpp"

    int main() {
        sycl::queue queue;

        const size_t n_observations = 1000;
        const size_t n_dims = 3;

        sycl::usm_allocator<float, sycl::usm::alloc::shared> allocator(queue);

        std::vector<float, decltype(allocator)> x(n_observations * n_dims, allocator);
        // fill x storage with random numbers
        for(int i = 0; i < n_dims, i++) {
          for(int j = 0; j < n_observations; j++) {
                x[j + i * n_observations] = float(std::rand()) / float(RAND_MAX);
            }
        }
        std::vector<float, decltype(allocator)> mean_buf(n_dims, allocator);
        // create oneapi::mkl::stats::dataset
        auto dataset = oneapi::mkl::stats::make_dataset<oneapi::mkl::stats::layout::row_major>(n_dims,  n_observations, x);

       sycl::event event = oneapi::mkl::stats::mean(queue, dataset, mean);
       event.wait();
       for(int i = 0; i < n_dims; i++) {
         std::cout << "Mean value for dimension " << i << ": " << mean[i] << std::endl;
       }
       return 0;
    }


.. rubric:: USM usage

You can also use USM with raw pointers by using the sycl::malloc_shared/malloc_device functions.

**Parent topic:** :ref:`onemkl_stats`
