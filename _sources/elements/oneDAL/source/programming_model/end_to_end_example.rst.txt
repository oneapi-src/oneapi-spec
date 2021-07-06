.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

==================
End-to-end example
==================
Below you can find a typical workflow of using oneDAL algorithm on GPU. The
example is provided for :txtref:`Principal Component Analysis algorithm (PCA)
<alg_pca>`.

The following steps depict how to:

- Read the data from CSV file
- Run the training and inference operations for PCA
- Access intermediate results obtained at the training stage

#. Include the following header that makes all oneDAL declarations available.

   .. code-block::

      #include "oneapi/dal.hpp"

      /* Standard library headers required by this example */
      #include <cassert>
      #include <iostream>

#. Create a SYCL* queue with the desired device selector. In this case,
   GPU selector is used:

   .. code-block:: cpp

      const auto queue = sycl::queue{ sycl::gpu_selector{} };

#. Since all oneDAL declarations are in the ``oneapi::dal`` namespace,
   import all declarations from the ``oneapi`` namespace to use ``dal``
   instead of ``oneapi::dal`` for brevity:

   .. code-block:: cpp

      using namespace oneapi;


#. Use :txtref:`CSV data source <csv-data-source>` to read the data
   from the CSV file into a :txtref:`table`:

   .. code-block:: cpp

      const auto data = dal::read<dal::table>(queue, dal::csv::data_source{"data.csv"});

#. Create a :txtref:`PCA <alg_pca>` descriptor, configure its parameters, and
   run the training algorithm on the data loaded from CSV.

   .. code-block:: cpp

      const auto pca_desc = dal::pca::descriptor<float>
         .set_component_count(3)
         .set_deterministic(true);

      const dal::pca::train_result train_res = dal::train(queue, pca_desc, data);

#. Print the learned eigenvectors:

   .. code-block:: cpp

      const dal::table eigenvectors = train_res.get_eigenvectors();

      const auto acc = dal::row_accessor<const float>{eigenvectors};
      for (std::int64_t i = 0; i < eigenvectors.row_count(); i++) {

         /* Get i-th row from the table, the eigenvector stores pointer to USM */
         const dal::array<float> eigenvector = acc.pull(queue, {i, i + 1});
         assert(eigenvector.get_count() == eigenvectors.get_column_count());

         std::cout << i << "-th eigenvector: ";
         for (std::int64_t j = 0; j < eigenvector.get_count(); j++) {
            std::cout << eigenvector[j] << " ";
         }
         std::cout << std::endl;
      }

#. Use the trained model for inference to reduce dimensionality of the data:

   .. code-block:: cpp

      const dal::pca::model model = train_res.get_model();

      const dal::table data_transformed =
         dal::infer(queue, pca_desc, data).get_transformed_data();

      assert(data_transformed.column_count() == 3);
