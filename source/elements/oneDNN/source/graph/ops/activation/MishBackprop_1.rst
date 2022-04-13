.. SPDX-FileCopyrightText: 2022 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

--------------
MishBackprop
--------------

**Versioned name**: *MishBackprop-1*

**Category**: *Activation*

**Short description**: *MishBackprop* computes gradient for Mish.

.. math::
   ds &= dd \cdot \frac{e^s \cdot \omega }{\delta ^2}, \text{where} \\
   \omega &= e^{3s} + 4 \cdot e^{2s} + e^s \cdot (4 \cdot s + 6) + 4 \cdot (s+1) \\
   \delta &= e^{2s} + 2 \cdot e^s + 2

**Attributes**:

* *use_dst*

  * **Description**: If true, use ``dst`` to calculate gradient; else use *src*.
  * **Range of values**: True or False
  * **Type**: bool
  * **Default value**: True
  * **Required**: *no*

**Inputs**:

* **1**:  ``data`` - If *use_dst* is true, data is result of forward. Else,
  data is *src* of forward. **Required.**

  * **Type**: T

* **2**: ``output_delta`` - gradients tensor with respect to the output.
  **Required.**

  * **Type**: T

**Outputs**

* **1**: ``input_delta`` - the gradient tensor with respect to the input of
  Mish.

  * **Type**: T
  
**Types**:

* **T**: f32, f16, bf16.
* **Note**: Inputs and outputs have the same data type denoted by *T*. For
  example, if input is f32 tensor, then all other tensors have f32 data type.

