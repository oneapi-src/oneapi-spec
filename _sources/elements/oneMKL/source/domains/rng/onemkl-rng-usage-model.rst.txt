.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_rng_usage_model:

oneMKL RNG Usage Model
======================


.. rubric:: Description

A typical algorithm for random number generators is as follows:


1. Create and initialize the object for basic random number
    generator.


-  Use the skip_ahead or leapfrog function if it is required (used
    in parallel with random number generation for Host and CPU
    devices).


2. Create and initialize the object for distribution generator.


3. Call the generate routine to get random numbers with appropriate
    statistical distribution.


The following example demonstrates generation of random numbers that
is output of basic generator (engine) PHILOX4X32X10. The seed is
equal to 777. The generator is used to generate 10,000 normally
distributed random numbers with parameters ``a`` = 5 and ``sigma``\ =
2. The purpose of the example is to calculate the sample mean for
normal distribution with the given parameters.

Buffer-based example
--------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>

    #include "CL/sycl.hpp"
    #include "oneapi/mkl/rng.hpp"

    int main() {
        sycl::queue queue;
        const size_t n = 10000;
        const std::uint64_t seed = 777;
        std::vector<double> r(n);

        oneapi::mkl::rng::philox4x32x10 engine(queue, seed); // basic random number generator object
        oneapi::mkl::rng::gaussian<double, oneapi::mkl::rng::gaussian_method::box_muller2> distr(5.0, 2.0); //  distribution object

        {
            //create buffer for random numbers
            sycl::buffer<double, 1> r_buf(r.data(), r.size());
            oneapi::mkl::rng::generate(distr, engine, n, r_buf); // perform generation
        }

        double s = 0.0;
        for(int i = 0; i < n; i++) {
            s += r[i];
        }
        s /= n;

        std::cout << "Average = " << s << std::endl;
        return 0;
    }


USM-based example
-----------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>

    #include "CL/sycl.hpp"
    #include "oneapi/mkl/rng.hpp"

    int main() {
        sycl::queue queue;
        const size_t n = 10000;
        const std::uint64_t seed = 777;

        // create USM allocator
        sycl::usm_allocator<double, sycl::usm::alloc::shared> allocator(queue.get_context(), queue.get_device());

        // create vector with USM allocator
        std::vector<double, decltype(allocator)> r(n, allocator);

        oneapi::mkl::rng::philox4x32x10 engine(queue, seed); // basic random number generator object
        oneapi::mkl::rng::gaussian<double, oneapi::mkl::rng::gaussian_method::box_muller2> distr(5.0, 2.0); // distribution object

        auto event = oneapi::mkl::rng::generate(distr, engine, n, r.data()); // perform generation
        // sycl::event object is returned by generate function for synchronization
        event.wait(); // synchronization can be also done by queue.wait()

        double s = 0.0;
        for(int i = 0; i < n; i++) {
            s += r[i];
        }
        s /= n;

        std::cout << "Average = " << s << std::endl;
        return 0;
    }


.. rubric:: USM usage

You can also use USM with raw pointers by using the sycl::malloc_shared/malloc_device functions.

**Parent topic:** :ref:`onemkl_rng`
