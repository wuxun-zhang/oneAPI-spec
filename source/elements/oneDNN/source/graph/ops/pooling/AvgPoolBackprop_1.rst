.. SPDX-FileCopyrightText: 2020-2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

---------------
AvgPoolBackprop
---------------

**Versioned name**: *AvgPoolBackprop-1*

**Category**: *Pooling*

**Short description**: `Reference
<http://caffe.berkeleyvision.org/tutorial/layers/pooling.html>`__

**Detailed description**: `Reference
<http://cs231n.github.io/convolutional-networks/#pool>`__

**Attributes**:

* *strides*

  * **Description**: *strides* is a distance (in pixels) to slide the window on
    the feature map over the *(z, y, x)* axes for 3D poolings and *(y, x)* axes
    for 2D poolings. For example, *strides* equal *(4,2,1)* means sliding the
    window 4 pixel at a time over depth dimension, 2 over height dimension and
    1 over width dimension.
  * **Range of values**: Non-negative s64 values.
  * **Type**: s64[]
  * **Default value**: None
  * **Required**: *yes*

* *pads_begin*

  * **Description**: *pads_begin* is a number of pixels to add to the beginning
    along each axis. For example, *pads_begin* equal *(1,2)* means adding 1
    pixel to the top of the input and 2 to the left of the input.
  * **Range of values**: Non-negative s64 values.
  * **Type**: s64[]
  * **Default value**: None
  * **Required**: *yes*
  * **Note**: the attribute is ignored when *auto_pad* attribute is specified.

* *pads_end*

  * **Description**: *pads_end* is a number of pixels to add to the ending along
    each axis. For example, *pads_end* equal *(1,2)* means adding 1 pixel to the
    bottom of the input and 2 to the right of the input.
  * **Range of values**: Non-negative s64 values.
  * **Type**: s64[]
  * **Default value**: None
  * **Required**: *yes*
  * **Note**: the attribute is ignored when *auto_pad* attribute is specified.

* *kernel*

  * **Description**: *kernel* is a size of each filter. For example, *kernel*
    equal *(2, 3)* means that each filter has height equal to 2 and width equal
    to 3.
  * **Range of values**: positive s64 values.
  * **Type**: s64[]
  * **Default value**: None
  * **Required**: *yes*
  
* *exclude_pad*

  * **Description**: *exclude_pad* is a type of pooling strategy for values in
    the padding area. For example, if *exclude_pad* is *true*, zero-values in
    the padding are not used.
  * **Range of values**: True or False
  * **Type**: bool
  * **Default value**: None
  * **Required**: *yes*

* *auto_pad*

  * **Description**: *auto_pad* how the padding is calculated. Possible values:

    * None (not specified): use explicit padding values.
    * *same_upper (same_lower)* the input is padded to match the output size.
      In case of odd padding value an extra padding is added at the end (at the
      beginning).
    * *valid* - do not use padding.

  * **Type**: string
  * **Default value**: None
  * **Required**: *no*
  * **Note**: *pads_begin* and *pads_end* attributes are ignored when *auto_pad*
    is specified.

* *data_format*

  * **Description**: *data_format* denotes the data format of the output_delta
    and input_delta.
  * **Range of values**: *NXC* or *NCX* (X means HW for 2D, DHW for 3D)
  * **Type**: string
  * **Default value**: *NXC*
  * **Required**: *no*

* *input_shape*

  * **Description**: *input_shape* denotes the shape of the forward input tensor.
  * **Type**: s64[]
  * **Default value**: None
  * **Required**: *no*

**Inputs**:

* **1**: ``output_delta`` - the gradient tensor with respect to output of avg
  pool. **Required.**

  * **Type**: T

* **2**: ``input_shape`` - the dimensions of forward input. **Optional**.
  If specified, *input_shape* attribute will be ignored. If not specified,
  users should define *input_shape* through attribute.

  * **Type**: s64

**Outputs**

* **1**: ``input_delta`` - the the gradient tensor with respect to the input of
  avg pool.

  * **Type**: T

**Types**:

* **T**: f32, f16, bf16.
* **Note**: Inputs and outputs have the same data type denoted by *T*. For
  example, if input is f32 tensor, then all other tensors have f32 data type.
