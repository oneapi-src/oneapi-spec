.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

.. _attributes-link:

##########
Attributes
##########

The parameters passed to create a primitive descriptor specify the problem. An
engine specifies where the primitive will be executed. An operation descriptor
specifies the basics: the operation kind; the propagation kind; the source,
destination, and other tensors; the strides (if applicable); and so on.

*Attributes* specify some extra properties of the primitive. Users must create
them before use and must set required specifics using the corresponding setters.
The attributes are copied during primitive descriptor creation, so users can
change or destroy attributes right after that.

If not modified, attributes can stay empty, which is equivalent to the default
attributes. Primitive descriptors' constructors have empty attributes as default
parameters, so, unless required, users can simply omit them.

Attributes can also contain *post-ops*, which are computations executed after
the primitive.

.. toctree::
   :maxdepth: 1

   post-ops.rst

***************
Scratchpad Mode
***************

Some primitives might require a temporary buffer while performing their
computations. For instance, the operations that do not have enough independent
work to utilize all cores on a system might use parallelization over the
reduction dimension (the K dimension in the GEMM notation). In this case
different threads compute partial results in private temporary buffers, and then
the private results are added to produce the final result. Another example is
using matrix multiplication (GEMM) to implement convolution. Before calling
GEMM, the source activations need to be transformed using the ``im2col``
operation. The transformation result is written to a temporary buffer that is
then used as an input for the GEMM.

In both of these examples, the temporary buffer is no longer required once the
primitive computation is completed. oneDNN refers to such kind of a memory
buffer as a *scratchpad*.

Both types of implementation might need extra space for the reduction in case
there are too few independent tasks. The amount of memory required by the
``im2col`` transformation is proportional to the size of the source image
multiplied by the weights spatial size. The size of a buffer for reduction is
proportional to the tensor size to be reduced (e.g., ``diff_weights`` in the
case of backward by weights) multiplied by the number of threads in the
reduction groups (the upper bound is the total number of threads).

By contrast, some other primitives might require very little extra space. For
instance, one of the implementation of the |sum| primitive requires temporary
space only to store the pointers to data for each and every input array (that
is, the size of the scratchpad is ``n * sizeof(void *)``, where ``n`` is the
number of summands).

oneDNN supports two modes for handling scratchpads:

.. doxygenenum:: dnnl::scratchpad_mode
   :project: oneDNN

The scratchpad mode is controlled though the
|primitive_attr::set_scratchpad_mode| primitive attributes.

If the user provides scratchpad memory to a primitive, this memory must be
created using the same engine that the primitive uses.

All primitives support both scratchpad modes.

.. note::

   Primitives are not thread-safe by default. The only way to make the primitive
   execution fully thread-safe is to use the |scratchpad_mode::user| mode and
   not pass the same scratchpad memory to two primitives that are executed
   concurrently.

Examples
========

Library Manages Scratchpad
--------------------------

As mentioned above, this is a default behavior. We only want to highlight how a
user can query the amount of memory consumed by a primitive due to a scratchpad.

.. code:: cpp

    // Use default attr, hence the library allocates scratchpad
    dnnl::primitive::primitive_desc op_pd(params, /* other arguments */);

    // Print how much memory would be hold by a primitive due to scratchpad
    std::cout << "primitive will use "
              << op_pd.query_s64(dnnl::query::memory_consumption_s64)
              << " bytes" << std::endl;

    // In this case scratchpad is internal, hence user visible scratchpad memory
    // descriptor should be empty:
    auto zero_md = dnnl::memory::desc();

User Manages Scratchpad
-----------------------

.. code:: cpp

    // Create an empty (default) attributes
    dnnl::primitive_attr attr;

    // Default scratchpad mode is `library`:
    assert(attr.get_scratchpad_mode() == dnnl::scratchpad_mode::library);

    // Set scratchpad mode to `user`
    attr.set_scratchpad_mode(dnnl::scratchpad_mode::user);

    // Create a primitive descriptor with custom attributes
    dnnl::primitive::primitive_desc op_pd(op_d, attr, engine);

    // Query the scratchpad memory descriptor
    dnnl::memory::desc scratchpad_md = op_pd.scratchpad_desc();

    // Note, that a primitive doesn't consume memory in this configuration:
    assert(op_pd.query_s64(dnnl::query::memory_consumption_s64) == 0);

    // Create a primitive
    dnnl::primitive prim(op_pd);

    // ... more code ..

    // Create a scratchpad memory
    // NOTE: if scratchpad is not required for a particular primitive the
    //       scratchpad_md.get_size() will return 0. It is fine to have
    //       scratchpad_ptr == nullptr in this case.
    void *scratchpad_ptr = user_memory_manager::allocate(scratchpad_md.get_size());
    // NOTE: engine here must much the engine of the primitive
    dnnl::memory scratchpad(scratchpad_md, engine, scratchpad_ptr);

    // Pass a scratchpad memory to a primitive
    prim.execute(stream, { /* other arguments */,
            {DNNL_ARG_SCRATCHPAD, scratchpad}});


.. _attributes-quantization-label:

************
Quantization
************

Primitives may support reduced precision computations which require
quantization.

Quantization Model
==================

The primary quantization model that the library assumes is the following:

.. math::

    x_{f32}[:] = scale_{f32} \cdot (x_{int8}[:] - 0_{x_{int8}})

where :math:`scale_{f32}` is a *scaling factor* that is somehow known in advance
and :math:`[:]` is used to denote elementwise application of the formula to the
arrays. Typically, the process of computing scale factors is called
*calibration*. The library cannot compute any of the scale factors at run-time
dynamically.  Hence, the model is sometimes called a *static* quantization
model. The main rationale to support only *static* quantization out-of-the-box
is higher performance. To use *dynamic* quantization:

1. Compute the result in higher precision, like |_s32|.
2. Find the required characteristics, like min and max values, and derive the
   scale factor.
3. Re-quantize to the lower precision data type.

oneDNN assumes a fixed zero position. For most of the primitives, the real zero
value is mapped to the zero for quantized values; that is, :math:`0_{x_{int8}} =
0`. For example, this is the only model that :ref:`convolution-label` and
:ref:`inner_product-label` currently support. The :ref:`rnn-label` primitives
have limited support of shifted zero.

For the rest of this section we that :math:`0_{x_{int8}} = 0`.

Example: Convolution Quantization Workflow
------------------------------------------

Consider a convolution without bias. The tensors are represented as:

- :math:`\src_{f32}[:] = scale_{\src} \cdot \src_{int8}[:]`
- :math:`\weights_{f32}[:] = scale_{\weights} \cdot \weights_{int8}[:]`
- :math:`\dst_{f32}[:] = scale_{\dst} \cdot \dst_{int8}[:]`

Here the :math:`\src_{f32}, \weights_{f32}, \dst_{f32}` are not computed at all,
the whole work happens with int8 tensors.  As mentioned above, we also somehow
know all the scaling factors: `scale_{\src}, scale_{\weights}, scale_{\dst}`.

So the task is to compute the :math:`\dst_{int8}` tensor.

Mathematically, the computations are:

.. math::

   \dst_{int8}[:] =
      \operatorname{f32\_to\_int8}(
         output\_scale \cdot
         conv_{s32}(\src_{int8}, \weights_{int8})
      ),

where

- :math:`output\_scale := \frac{scale_{\src} \cdot scale_{\weights}}{scale_{\dst}}`;

- :math:`conv_{s32}` is just a regular convolution which takes source and
  weights with int8 data type and compute the result in int32 data type (int32
  is chosen to avoid overflows during the computations);

- :math:`\operatorname{f32\_to\_s8}()` converts an `f32` value to `s8` with
  potential saturation if the values are out of the range of the int8 data
  type.

Note that in order to perform the operation, one doesn't need to know the exact
scaling factors for all the tensors; it is enough to know only the
`output\_scale`. The library utilizes this fact: a user needs to provide only
this one extra parameter to the convolution primitive (see the
:ref:`output_scaling-label` section below).


Per-Channel Scaling
-------------------

Primitives may have limited support of multiple scales for a quantized tensor.
The most popular use case is the :ref:`convolution-label` primitives that
support per-output-channel scaling factors for the weights, meaning that the
actual convolution computations would need to scale different output channels
differently.

Let :math:`\alpha` denote scales:

- :math:`\src_{f32}(n, ic, ih, iw) = \alpha_{\src} \cdot \src_{int8}(n, ic, ih, iw)`

- :math:`\weights_{f32}(oc, ic, kh, kw) = \alpha_{\weights}(oc) \cdot \weights_{int8}(oc, ic, kh, kw)`

- :math:`\dst_{f32}(n, oc, oh, ow) = scale_{\dst} \cdot \dst_{int8}(n, oc, oh, ow)`

Note that now the weights' scaling factor depends on the :math:`oc`.

To compute the :math:`\dst_{int8}` we need to perform the following:

.. math::

    \dst_{int8}(n, oc, oh, ow) =
        \operatorname{f32\_to\_int8}(
            output\_scale(oc) \cdot
            conv_{s32}(\src_{int8}, \weights_{int8})|_{(n, oc, oh, ow)}
        ),

where

.. math::

   output\_scale(oc) :=
    \frac{\alpha_{\src} \cdot \alpha_{\weights}(oc)}{\alpha_{\dst}}.

The user is responsible for preparing quantized weights accordingly. To do that,
oneDNN provides reorders that can perform per-channel scaling:

.. math::

    \weights_{int8}(oc, ic, kh, kw) =
        \operatorname{f32\_to\_int8}(
            output\_scale(oc) \cdot
            \weights_{f32}(oc, ic, kh, kw)
        ),

where

.. math::

   output\_scale(oc) := \frac{1}{\alpha_{\weights}(oc_{})}.

.. _output_scaling-label:

Output Scaling Attribute
========================

oneDNN provides |primitive_attr::set_output_scales| for setting scaling factors
for most of the primitives.

The primitives may not support output scales if source (and weights) tensors are
not of the int8 data type. In other words, convolution operating on the single
precision floating point data type may not scale the output result.

In the simplest case, when there is only one common scale the attribute changes
the op behavior from

.. math::
    \dst[:] = Op(...)

to

.. math::
    \dst[:] = scale \cdot Op(...).

To support scales per one or several dimensions, users must set the appropriate
mask.

Say the primitive destination is a :math:`D_0 \times ... \times D_{n-1}` tensor
and we want to have output scales per :math:`d_i` dimension (where :math:`0 \le
d_i < n`).

Then :math:`mask = \sum \limits_{d_i} 2^{d_i}` and the number of scales should
be :math:`\mathtt{scales.size()} = \prod \limits_{d_i} D_{d_i}`.

The scaling happens in the single precision floating point data type (|_f32|).
Before it is stored, the result is converted to the destination data type with
saturation if required. The rounding happens according to the current hardware
setting.

Example 1: weights quantization with per-output-channel-and-group scaling
-------------------------------------------------------------------------

.. code:: cpp

   // weights dimensions
   const int G, OC, IC, KH, KW;

   // original f32 weights in plain format
   dnnl::memory::desc wei_plain_f32_md(
           {G, OC/G, IC/G, KH, KW},          // dims
           dnnl::memory::data_type::f32,     // the data originally in f32
           dnnl::memory::format_tag::hwigo   // the plain memory format
           );

   // the scaling factors for quantized weights
   // An unique scale for each group and output-channel.
   std::vector<float> wei_scales(G * OC/G) = { /* values */ };

   // int8 convolution primitive descriptor
   dnnl::convolution_forward::primitive_desc conv_pd(/* see the next example */);

   // query the convolution weights memory descriptor
   dnnl::memory::desc wei_conv_s8_md = conv_pd.weights_desc();

   // prepare the inverse of the scales
   // (f32 = scale * int8 --> int8 = 1/scale * f32)
   std::vector<float> inv_wei_scales(wei_scales.size());
   for (size_t i = 0; i < wei_scales.size(); ++i)
       inv_wei_scales[i] = 1.f / wei_scales[i];

   // prepare the attributes for the reorder
   dnnl::primitive_attr attr;
   const int mask = 0
       | (1 << 0)  // scale per  G dimension, which is the dim #0
       | (1 << 1); // scale per OC dimension, which is the dim #1
   attr.set_output_scales(mask, inv_wei_scales);

   // create reorder that would perform:
   //   wei_s8(g, oc, ic, kh, kw) <- 1/scale(g, oc) * wei_f32(g, oc, ic, kh, kw)
   // including the data format transformation.
   auto wei_reorder_pd = dnnl::reorder::primitive_desc(
           wei_plain_f32_md, engine, // source
           wei_conv_s8_md, engine, // destination,
           attr);
   auto wei_reorder = dnnl::reorder(wei_reorder_pd);


Example 2: convolution with groups, with per-output-channel quantization
------------------------------------------------------------------------

This example is complementary to the previous example (which should ideally be
the first one). Let's say we want to create an int8 convolution with per-output
channel scaling.

.. code:: cpp

   const float src_scale; // src_f32[:] = src_scale * src_s8[:]
   const float dst_scale; // dst_f32[:] = dst_scale * dst_s8[:]

   // the scaling factors for quantized weights (as declared above)
   // An unique scale for each group and output-channel.
   std::vector<float> wei_scales(G * OC/G) = {...};


   // Src, weights, and dst memory descriptors for convolution,
   // with memory format tag == any to allow a convolution implementation
   // to chose the appropriate memory format

   dnnl::memory::desc src_conv_s8_any_md(
           {BATCH, IC, IH, IW},            // dims
           dnnl::memory::data_type::s8,  // the data originally in s8
           dnnl::memory::format_tag::any // let convolution to choose
           );

   dnnl::memory::desc wei_conv_s8_any_md(
           {G, OC/G, IC/G, KH, KW},        // dims
           dnnl::memory::data_type::s8,  // the data originally in s8
           dnnl::memory::format_tag::any // let convolution to choose
           );

   dnnl::memory::desc dst_conv_s8_any_md(...);  // ditto

   // Create a convolution operation descriptor
   dnnl::convolution_forward::desc conv_d(
           dnnl::prop_kind::forward_inference,
           dnnl::algorithm::convolution_direct,
           src_conv_s8_any_md,                     // what's important is that
           wei_conv_s8_any_md,                     // we specified that we want
           dst_conv_s8_any_md,                     // computations in s8
           strides, padding_l, padding_r,
           dnnl::padding_kind::zero
           );

   // prepare the attributes for the convolution
   dnnl::primitive_attr attr;
   const int mask = 0
       | (1 << 1); // scale per OC dimension, which is the dim #1 on dst tensor:
                   // (BATCH, OC, OH, OW)
                   //    0     1   2   3
   std::vector<float> conv_output_scales(G * OC/G);
   for (int g_oc = 0; G * OC/G; ++g_oc)
       conv_output_scales[g_oc] = src_scale * wei_scales(g_oc) / dst_scale;
   attr.set_output_scales(mask, conv_output_scales);

   // create a convolution primitive descriptor with the scaling factors
   auto conv_pd = dnnl::convolution_forward::primitive_desc(
           conv_d, // general (non-customized) operation descriptor
           attr,   // the attributes contain the output scaling
           engine);


Interplay of Output Scales with Post-ops
----------------------------------------

In general, the :ref:`post_ops-label` are independent from the output scales.
The output scales are applied to the result first; then post-ops will take
effect.

That has an implication on the scaling factors passed to the library, however.
Consider the following example of a convolution with :math:`\tanh` post-op:

.. math::
    \dst_{s8}[:] =
        \frac{1}{scale_{\dst}}
        \cdot
        \tanh(
                scale_{\src}
                \cdot
                scale_{\weights}
                \cdot
                conv_{s32}(\src_{s8}, wei_{s8})
        )

- The convolution output scales are
  :math:`conv\_output\_scale = scale_{\src} \cdot scale_{\weights}`,
  i.e. there is no division by :math:`scale_{\dst}`.
- And the post-ops scale for :math:`\tanh` is set to
  :math:`scale\_tanh\_post\_op = \frac{1}{scale_{\dst}}`.

.. _attributes_error_handling-link:

********************************
Attribute Related Error Handling
********************************

Since the attributes are created separately from the corresponding primitive
descriptor, consistency checks are delayed.  Users can successfully set
attributes in whatever configuration they want.  However, when they try to
create a primitive descriptor with the attributes they set, it might happen that
there is no primitive implementation that supports such a configuration. In this
case the library will throw the |error| exception.

***
API
***

.. doxygenstruct:: dnnl::primitive_attr
   :project: oneDNN
   :members:

.. vim: ts=3 sw=3 et spell spelllang=en
