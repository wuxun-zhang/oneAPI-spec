.. SPDX-FileCopyrightText: 2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

-----
PReLU
-----

**Versioned name**: *PReLU-1*

**Category**: *Activation*

**Short description**:
Parametric rectified linear unit element-wise activation function.

**Detailed description**:
*PReLU* operation is introduced in this 'article <https://arxiv.org/abs/1502.01852v1>'.
*PReLU* performs element-wise *parametric ReLU* operation on a given input
tensor, based on the following mathematical formula:

.. math::
    PReLU(x) = \left\{\begin{array}{r}
    x \quad \mbox{if } x \geq  0 \\
    \alpha x \quad \mbox{if } x < 0
    \end{array}\right.

**Attributes**:

* *data_format*

  * **Description**: *data_format* denotes the data format of the input and
    output data.
  * **Range of values**: *NXC* or *NCX* (X means HW for 2D, DHW for 3D)
  * **Type**: string
  * **Default value**: *NXC*
  * **Required**: *no*

* *per_channel_broadcast*

  * **Description**: *per_channel_broadcast* denotes whether to apply
    per_channel broadcast when slope is 1D tensor.
  * **Type**: boolean
  * **Default value**: *True*
  * **Required**: *no*

**Inputs**:

* **1**: data – input tensor. **Required.**

  * **Type**: T

* **2**: slope – slope tensor. **Required.**

  * **Type**: T

**Outputs**

* **1**: The result tensor.

  * **Type**: T

**Types**:

* **T**: f32, f16, bf16
* **Note**: Inputs and outputs have the same data type denoted by *T*. For
  example, if input is f32 tensor, then all other tensors have f32 data type.

**Broadcast rules**:

Only slope tensor supports broadcast-semantics. Slope tensor is unidirectional
broadcastable to *data* if one of the following rules is true:

* **1**: slope is 1D tensor and per_channel_broadcast = True, length of slope is
  equal to the length of *data* in channle dimensions.

* **2**: slope is 1D tensor and per_channel_broadcast = False, length of slope
  is equal to the length of *data* in the right most dimensions.

* **3**: slope is nD tensor, starting from the rightmost dimension, the two
  inputs tensor dimension sizes must be equal or slope size in that dimension 1,
  or slope in that dimension doesn't exist.
