.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_dft:

Discrete Fourier Transform Functions
-------------------------------------

The general form of the d-dimensional discrete Fourier transform(DFT) is

.. _onemkl_dft_formula:

.. math::

   z_{k_1, k_2,\dots, k_d} = \sigma \displaystyle\sum_{j_d=0}^{n_d-1}\dots\displaystyle\sum_{j_2=0}^{n_2-1}\displaystyle\sum_{j_1=0}^{n_1-1} w_{j_1, j_2,\dots,j_d} \exp \left[ \delta 2\pi i\left( \sum_{\ell=1}^{d} \frac{j_{\ell}k_{\ell}}{n_{\ell}} \right) \right] .

for :math:`k_{\ell} = 0,\dots, n_{\ell}-1` and :math:`\ell\in\{1, \dots, d\}`, where :math:`\sigma` is a scale factor, :math:`\delta=-1` for the forward transform, and :math:`\delta=+1` for the backward(inverse) transform.  In the forward transform, the input sequence :math:`\left(w_{j_1, j_2, \dots, j_d}\right)` belongs to the set of complex-valued sequences or real-valued sequences. Respective domains for the backward transform are represented by complex-valued sequences or complex conjugate-even sequences. 

The discrete Fourier transform to be performed is defined by the creation of a :ref:`onemkl_dft_descriptor` class, with the associated configuration parameters, described in :ref:`onemkl_dft_enums`.  Once the descriptor class is defined and :ref:`onemkl_dft_descriptor_commit` is called and provided with a ``sycl::queue`` to define the device and context, it can be used for computing the forward and/or backward transformations. The available data storage formats for the various configurations are described in :ref:`onemkl_dft_config_storage_formats`.

.. container::

   The routines and objects associated with computing a discrete Fourier transform.

   .. container:: tablenoborder

      .. 

      .. list-table:: 
         :header-rows: 1
         :widths: 33 64   

         * -     Routines and Objects
           -     Description     
         * -     :ref:`onemkl_dft_descriptor`
           -     A class to define the specific discrete Fourier transform problem to be applied.
         * -     :ref:`descriptor::set_value<onemkl_dft_descriptor_set_value>`
           -     A member function of descriptor class to set non-default configuration parameters and define the DFT transformation to be applied.
         * -     :ref:`descriptor::get_value<onemkl_dft_descriptor_get_value>`
           -     A member function of descriptor class to query configuration parameters that define the DFT transformation to be applied.
         * -     :ref:`descriptor::commit<onemkl_dft_descriptor_commit>`
           -     A member function of descriptor class to finalize the DFT descriptor before computations.
         * -     :ref:`onemkl_dft_compute_forward`
           -     Computes the in-place/out-of-place forward transformation.
         * -     :ref:`onemkl_dft_compute_backward`
           -     Computes the in-place/out-of-place backward transformation.


**Parent topic:** :ref:`onemkl_domains`

.. toctree::
    :hidden:

    enums_and_config_params
    descriptor
    compute_forward
    compute_backward

