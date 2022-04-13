.. SPDX-FileCopyrightText: 2020-2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

-----------
Convolution
-----------

**Versioned name**: *Convolution-1*

**Category**: Convolution

**Short description**: `Reference
<http://caffe.berkeleyvision.org/tutorial/layers/convolution.html>`__

**Detailed description**: `Reference
<http://cs231n.github.io/convolutional-networks/#conv>`__

In this description, :math:`r` denotes the spatial rank. We describe the
convolution for each sample in a batch of :math:`N` inputs; the results are
combined into an output batch of size :math:`N`.

The convolution is implemented as if each sample input first has :math:`p_b`
zeros inserted before and `p_e` zeros inserted for the channels on the spatial
axes, giving a padded input size of :math:`p_b+p_e+X_I`.

The kernel is stretched by a factor of `d` on each of its spatial dimensions.
The last index of the stretched kernel is then :math:`d(X_K-1)` so the shape is
:math:`d(X_K-1)+1`.

The padded input and the dilated kernel are then ungrouped into `g` equal-sized
input and kernel segments; padded input segment :math:`i` and dilated kernel
segment :math:`i` are convolved.
The convolution is only performed where there is complete spatial overlap between
the shifted kernel and the padded input, so there will be
:math:`p_b+p_e+X_I-d(X_K-1)` outputs. The output segments are then regrouped
along the output channel axis. Finally, all but the results on a multiple of
:math:`d` spatial axis are removed, so the output will have size:

.. math::
   \left\lfloor \frac{p_b+p_e+X_I-d(X_K-1)-1}{s} \right\rfloor +1

**Attributes**

* *strides*

  * **Description**: *strides* is how much the convolution output is
    down-sampled to produce the output.
  * **Range of values**: Non-negative s64 values.
  * **Type**: s64[]
  * **Default value**: None
  * **Required**: *yes*

* *pads_begin*

  * **Description**: *pads_begin* is a number of zeros to add to the beginning
    of each spatial axis.
  * **Range of values**: Non-negative s64 values.
  * **Type**: s64[]
  * **Default value**: None
  * **Required**: *yes*
  * **Note**: the attribute is ignored when *auto_pad* attribute is specified.

* *pads_end*

  * **Description**: *pads_end* is a number of zeros to add to the end of each
    spatial axis.
  * **Range of values**: Non-negative s64 values.
  * **Type**: s64[]
  * **Default value**: None
  * **Required**: *yes*
  * **Note**: the attribute is ignored when *auto_pad* attribute is specified.

* *dilations*

  * **Description**: *dilations* denotes the amount to stretch the kernel before
    convolving.
  * **Range of values**: positive s64 values.
  * **Type**: s64[]
  * **Default value**: None
  * **Required**: *yes*

* *auto_pad*

  * **Description**: *auto_pad* how the padding is calculated. Possible values:

    * None (not specified): use explicit padding values.
    * *same_upper (same_lower)* the input is padded to match the output size. In
      case of odd padding value an extra padding is added at the end (at the
      beginning).
    * *valid* - No padding (:math:`p_b=p_e=0`).

  * **Type**: string
  * **Default value**: None
  * **Required**: *no*
  * **Note**: *pads_begin* and *pads_end* attributes are ignored when *auto_pad*
    is specified.

With *same_upper* and *same_lower* the padding is chosen to make the pre-stride
output spatial shape the same as the input shape. When possible, :math:`p_b=p_e`.
If the total padding needed is odd, *same_upper* makes :math:`p_e=p_b+1`,
*same_lower* makes `p_b=p_e+1`. In either case,

.. math::
   p_b+p_e=d(X_I-1).

* *groups*

  * **Description**: *groups* denotes the number of groups input channels and
    output channels are divided into. In_channels and out_channels must both be
    divisible by groups
  * **Range of values**: A positive s64 value.
  * **Type**: s64
  * **Default value**: 1
  * **Required**: *no*

* *data_format*

  * **Description**: *data_format* denotes the data format of the input and
    output data.
  * **Range of values**: *NXC* or *NCX* (X means HW for 2D convolution, DHW for
    3D convolution)
  * **Type**: string
  * **Default value**: *NXC*
  * **Required**: *no*

* *filter_format*

  * **Description**: *filter_format* denotes the data format of the filter.
  * **Range of values**: *XIO* or *OIX* (X means HW for 2D convolution, DHW for
    3D convolution)
  * **Type**: string
  * **Default value**: *XIO*
  * **Required**: *no*

**Inputs**:

* **1**: ``input`` - the input tensor. The format is specified by *data_format*.
  **Required.**

  * **Type**: T

* **2**: ``filter`` - convolution filter tensor. The format is specified by
  *filter_format*. The shape of filter is (out_channels, in_channels / groups,
  spatial_shape) for OIX format and (spatial_shape, in_channels / groups,
  out_channels) for XIO format. In_channels and out_channels must both be
  divisible by groups. **Required.**

  * **Type**: T

* **3**: ``bias`` - a 1-D tensor adds to channel dimension of input.
  Broadcasting is supported. **Optional.**

  * **Type**: T

**Outputs**:

* **1**: ``output`` -- output tensor. The format is specified by *data_format*.

  * **Type**: T

**Types**: 

* **T**: f32, f16, bf16.
* **Note**: Inputs and outputs have the same data type denoted by *T*. For
  example, if input is f32 tensor, then all other tensors have f32 data type.
