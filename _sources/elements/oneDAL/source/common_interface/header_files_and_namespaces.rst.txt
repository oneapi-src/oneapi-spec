.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

============
Header files
============

oneDAL public identifiers are represented in the following header files:

.. list-table::
   :widths:  10 50
   :header-rows: 1

   * - Header file
     - Description
   * - ``oneapi/dal.hpp``
     - The main header file of oneDAL library.
   * - ``oneapi/dal/%FILE%.hpp``
     - The common type definitions used in other |dal_short_name| layers.
       For example, ``data_type`` or ``range``.
   * - ``oneapi/dal/algo/%ALGO%.hpp``
     - A header file for a particular algorithm.
       The folder for the algorithm itself is ``oneapi/dal/algo/%ALGO%/``.

       The string %ALGO% should be substituted with the name of the algorithm,
       for example, ``kmeans`` or ``knn``.

   * - ``oneapi/dal/algo/misc/%FUNC%.hpp``
     - A header file for miscellaneous data types and functionality that is
       intended to be used by oneDAL algorithms and applications
       of the analytical pipeline.

       The string %FUNC% should be substituted with the name of the
       functionality, for example, ``mt19937`` or ``cross_enthropy_loss``.

   * - ``oneapi/dal/table/%FILE%.hpp``
     - A header file for the types related to the :txtref:`table` concept.

       The string %FILE% should be substituted with the name of the
       functionality, for example, ``common`` for key concepts related to table
       types (e.g., ``table``, ``table_metadata``, ``data_layout`` classes). For
       entities that have the ``_table`` suffix in their names, the related
       header file shall not contain this suffix in its name, for example,
       ``homogen`` for ``homogen_table`` class.

   * - ``oneapi/dal/io/%FILE%.hpp``
     - A header file for the types and entities of input-output functionality.

       The string %FILE% should be substituted with the name of the
       functionality, for example, ``csv`` for reading and writing csv files.

   * - ``oneapi/dal/util/%UTIL%.hpp```
     - A header file for auxiliary functionality, such as memory allocators or
       type traits, that is intended to be used for the design of classes and
       implementation of various methods.

       The string %UTIL% should be substituted with the name of the auxiliary
       functionality, for example, ``usm_allocator`` or ``type_traits``.


.. _common_namespaces:

==========
Namespaces
==========

oneDAL functionality is represented with a system of C++ namespaces described below:

.. list-table::
   :widths:  10 50
   :header-rows: 1

   * - Namespace
     - oneDAL content
   * - ``oneapi::dal``
     - The namespace of the library that contains externally visible data
       types, data management entities, processing and service functionality of
       oneDAL.
   * - ``oneapi::dal::%ALGORITHM%``

     - The namespace of the algorithm.
       All classes and structures related to that algorithm shall be defined
       within this particular namespace.

       To define a namespace for a specific algorithm, the string %ALGORITHM%
       should be substituted with its name, for example, ``oneapi::dal::kmeans``
       or ``oneapi::dal::knn``.

   * - ``oneapi::dal::%DATA_SOURCE%``

     - The namespace of the data source.
       All classes and structures related to that data source shall be defined within a particular namespace.

       To define a specific data source, the string %DATA_SOURCE% should be substituted with its name,
       for example, ``oneapi::dal::csv``.

   * - ``oneapi::dal::misc``
     - The namespace that contains miscellaneous data types and functionality
       intended to be used by oneDAL algorithms and applications for algorithm
       customization and optimization on various stages of the analytical
       pipeline.

   * - ``%PARENT%::detail``
     - The namespace that contains implementation details of the data types and
       functionality for the parent namespace.
       The namespace can be on any level in the namespace hierarchy.

       To define a specific namespace, the string %PARENT% should be substituted
       with the namespace for which the details are provided, for example,
       ``oneapi::dal::detail`` or ``oneapi::dal::kmeans::detail``.

       The application shall not use any data types nor call any functionality
       located in the ``detail`` namespaces.
