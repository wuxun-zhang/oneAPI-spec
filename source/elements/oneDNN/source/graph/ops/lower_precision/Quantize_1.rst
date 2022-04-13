.. SPDX-FileCopyrightText: 2020-2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

--------
Quantize
--------

**Versioned name**: *Quantize-1*

**Category**: lower_precision

**Short description**: *Quantize* converts a fp32 tensor to a quantized(int8 or uint8) tensor.  
It supports both per tensor and per channel asymmetric linear quantization. Output data type is specified
in output tensor data_type. Nearest round is used in this OP. For per-tensor quantization:

.. math:: 
    q_{x}=round(x/scale+zp)

For per-channel quantization, take channel axis = 2 as example:

.. math:: 
    q_{x_{...,i,...,...}}=round(x_{...,i,...,...}/scale_i+zp_i),i\in{[0, channelNum-1]}
    
**Attributes**

* *qtype*

  * **Description**: specifies which quantization type is used.
  * **Range of values**: "per_tensor" or "per_channel"
  * **Type**: string
  * **Default value**: "per_tensor"
  * **Required**: *no*

* *axis*

  * **Description**: specifies dimension on which apply per-channel quantization. Only valid when *qtype* is "per_channel". 
  * **Range of values**: integers in [-r, r-1] where r = rank(input)
  * **Type**: s64
  * **Default value**: 1
  * **Required**: *no*

* *scales*

  * **Description**: apply in quantization formula.
  * **Range of values**: arbitrary valid f32 value
  * **Type**: fp32[]
  * **Default value**: None
  * **Required**: *yes*

* *zps*

  * **Description**: offset value that maps to float zero.
  * **Range of values**: arbitrary valid s64 value
  * **Type**: s64[]
  * **Default value**: None
  * **Required**: *yes*

**Inputs**:

* **1**: ``input`` - fp32 tensor to be quantized. **Required.**
  
  * **Type**: T1

**Outputs**:

* **1**: ``output`` -- quantized tensor.
  
  * **Type**: T2

**Types**:

* **T1**: fp32.
* **T2**: s8, u8.