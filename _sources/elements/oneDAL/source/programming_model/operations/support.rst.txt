.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _op_supported:

====================
Supported operations
====================
This section describes all operations supported by oneDAL. For more information
about general operation definition, refer to :txtref:`Operations <operations>`
section.

The table bellow specifies whether an algorithm's descriptor can be used together
with each operation.

.. |train| replace:: :txtref:`Train <op_train>`
.. |infer| replace:: :txtref:`Infer <op_infer>`
.. |compute| replace:: :txtref:`Compute <op_compute>`

.. |kmeans| replace:: :txtref:`K-Means <alg_kmeans>`
.. |kmeans_init| replace:: :txtref:`K-Means Initialization <alg_kmeans_init>`
.. |knn| replace:: :txtref:`k-NN <alg_knn>`
.. |pca| replace:: :txtref:`PCA <alg_pca>`

+------------------+------------------------------------+
|                  |             Operations             |
|  Algorithm       +-----------+----------+-------------+
|                  |  |train|  |  |infer| |  |compute|  |
+==================+===========+==========+=============+
| |kmeans|         |   Yes     |   Yes    |    No       |
+------------------+-----------+----------+-------------+
| |kmeans_init|    |   No      |   No     |    Yes      |
+------------------+-----------+----------+-------------+
| |knn|            |   Yes     |   Yes    |    No       |
+------------------+-----------+----------+-------------+
| |pca|            |   Yes     |   Yes    |    No       |
+------------------+-----------+----------+-------------+

.. _op_train:

Train
-----
The ``train`` operation performs :capterm:`training` procedure of a machine
learning algorithm. The result obtained after the training contains a
:capterm:`model` that can be passed to the ``infer`` operation.

.. code-block:: cpp

   namespace oneapi::dal {

   template <typename Descriptor>
   using train_input_t = /* implementation defined */;

   template <typename Descriptor>
   using train_result_t = /* implementation defined */;

   template <typename Descriptor>
   train_result_t<Descriptor> train(
      sycl::queue& queue,
      const Descriptor& desc,
      const train_input_t<Descriptor>& input);

   } // namespace oneapi::dal


.. _op_infer:

Infer
-----
The ``infer`` operation performs :capterm:`inference` procedure of a machine
learning algorithm based on the model obtained as a result of training.

.. code-block:: cpp

   namespace oneapi::dal {

   template <typename Descriptor>
   using infer_input_t = /* implementation defined */;

   template <typename Descriptor>
   using infer_result_t = /* implementation defined */;

   template <typename Descriptor>
   infer_result_t<Descriptor> infer(
      sycl::queue& queue,
      const Descriptor& desc,
      const infer_input_t<Descriptor>& input);

   } // namespace oneapi::dal


.. _op_compute:

Compute
-------
The ``compute`` operation is used if an algorithm does not have the well-defined
training and inference stages.

.. code-block:: cpp

   namespace oneapi::dal {

   template <typename Descriptor>
   using compute_input_t = /* implementation defined */;

   template <typename Descriptor>
   using compute_result_t = /* implementation defined */;

   template <typename Descriptor>
   compute_result_t<Descriptor> compute(
      sycl::queue& queue,
      const Descriptor& desc,
      const compute_input_t<Descriptor>& input);

   } // namespace oneapi::dal
