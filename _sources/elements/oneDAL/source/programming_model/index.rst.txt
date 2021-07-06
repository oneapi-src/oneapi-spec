.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

=================
Programming model
=================
oneDAL primarily targets algorithms that are extensively used in data analytics.
These algorithms typically have many parameters, i.e. knobs to control its
internal behavior and produced result. In machine learning, those parameters are
often referred as *meta-parameters* to distinguish them from the model
parameters learned during the training. `Some algorithms <xgboost_params_>`_
define a dozen meta-parameters, while others depend on another algorithm as, for
example, the logistic regression training procedure depends on an optimization
algorithm.

.. _xgboost_params: https://xgboost.readthedocs.io/en/latest/parameter.html

Besides meta-parameters, machine learning algorithms may have different
*stages*, such as :capterm:`training` and :capterm:`inference`. Moreover, the
stages of an algorithm may be implemented in a variety of *computational
methods*. For instance, a linear regression model could be trained by solving a
system of linear equations [Friedman17]_ or by applying an iterative
optimization solver directly to the empirical risk function [Zhang04]_.

The same machine learning techniques are often applied for solving problems of
different types. In the example with linear regression, the same mathematical
model used for solving :capterm:`regression` problem is generalized for solving
a :capterm:`classification` problem, for example, logistic regression. Such
techniques differ only in few problem-specific aspects, but share the same
subset of meta-parameters and have a common computational flow. oneDAL does not
distinguish these techniques into different algorithms. Instead, from oneDAL
perspective, the same algorithm may perform different *computational tasks*.

From computational perspective, algorithm implementation may rely on different
*floating-point types*, such as ``float``, ``double`` or ``bfloat16``. Having a
capability to specify what type is needed is important for the end user as their
precision requirements vary depending on a workload.

To best tackle the mentioned challenges, each algorithm is decomposed into
:txtref:`descriptors` and :txtref:`operations`.

.. toctree::
   end_to_end_example.rst
   descriptors.rst
   operations/index.rst
   computational_modes.rst
