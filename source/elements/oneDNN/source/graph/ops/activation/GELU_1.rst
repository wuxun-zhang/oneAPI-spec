.. SPDX-FileCopyrightText: 2020-2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

----
GELU
----

**Versioned name**: *GELU-1*

**Category**: *Activation*

**Short description**:
`Reference <https://pytorch.org/docs/stable/nn.functional.html#gelu>`__

**OpenVINO description**: This OP is as same as `OpenVINO OP
<https://docs.openvino.ai/2021.1/openvino_docs_ops_activation_GELU_2.html>`__

**Detailed description**:
`Reference <https://arxiv.org/abs/1606.08415>`__

**Attributes**: *Gelu* operation has no attributes.

**Mathematical Formulation**
:math:`Gelu(x)=x*Φ(x)`, where :math:`Φ(x)` is the Cumulative Distribution
Function for Gaussian Distribution. The following equivalent combination is
recognized and fused into single Gelu op: 

.. math::
   Gelu(x) = 0.5*x*(1.0 + erf((x) / \sqrt{2})

Similarly, the following Gelu approximation (typical for the TensorFlow*) is
recognized and fused into single Gelu op

.. math::
   Gelu(x) \approx 0.5x(1.0 + tanh(\sqrt{2.0/pi} * (x + 0.044715 * x ^ 3))

**Inputs**:

* **1**: Multidimensional input tensor. **Required.**

  * **Type**: T

**Outputs**

* **1**: Result of GELU function applied to the input tensor x. **Required.**

  * **Type**: T

**Types**:

* **T**: f32, f16, bf16.
* **Note**: Inputs and outputs have the same data type denoted by *T*. For
  example, if input is f32 tensor, then all other tensors have f32 data type.
