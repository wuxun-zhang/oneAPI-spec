.. SPDX-FileCopyrightText: 2020-2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

---------------
SigmoidBackprop
---------------

**Versioned name**: *SigmoidBackprop-1*

**Category**: *Activation*

**Short description**: *SigmoidBackprop* computes gradient for Sigmoid

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
  Sigmoid.

  * **Type**: T

**Types**:

* **T**: f32, f16, bf16.
* **Note**: Inputs and outputs have the same data type denoted by *T*. For
  example, if input is f32 tensor, then all other tensors have f32 data type.

