.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _kd_tree:

========
k-d Tree
========

:math:`k`-:math:`d` tree is a space-partitioning binary tree [Bentley80]_, where

- Each non-leaf node induces the hyperplane that splits the feature space into
  two parts. To define the splitting hyperplane explicitly, a non-leaf node
  stores the identifier of the feature (that defines axis in the feature space)
  and `a cut-point <kd_tree_cut_point_>`_

- Each leaf node of the tree has an associated subset (*a bucket*) of elements of
  the training data set. Feature vectors from a bucket belong to the region of
  the space defined by tree nodes on the path from the root node to the
  respective leaf.


-------------
Related terms
-------------

.. _kd_tree_cut_point:

A cut-point
   A feature value that corresponds to a non-leaf node of a :math:`k`-:math:`d`
   tree and defines the splitting hyperplane orthogonal to the axis specified by
   the given feature.
