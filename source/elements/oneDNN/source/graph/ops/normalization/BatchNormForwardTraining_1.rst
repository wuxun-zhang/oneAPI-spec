.. SPDX-FileCopyrightText: 2020-2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

------------------------
BatchNormForwardTraining
------------------------

**Versioned name**: *BatchNormForwardTraining-1*

**Category**: *Normalization*

**Short description**: *BatchNormForwardTraining* works on forward pass at
training mode.

**Attributes**:

* *epsilon*

  * **Description**: *epsilon* is the number to be added to the variance to
    avoid division by zero when normalizing a value. For example, *epsilon*
    equal to 0.001 means that 0.001 is added to the variance.
  * **Range of values**: arbitrary positive f32 value
  * **Type**: f32
  * **Required**: *yes*

* *momentum*

  * **Description**: *momentum* is used for the computation of running_mean and
    running_var. If it's not available, a cumulative moving average (i.e. simple
    average) will be computed.
  * **Range of values**: arbitrary positive f32 value
  * **Type**: f32
  * **Required**: *no*

* *data_format*

  * **Description**: *data_format* denotes the data format of the input and
    output data.
  * **Range of values**: *NXC* or *NCX* (X means HW for 2D, DHW for 3D)
  * **Type**: string
  * **Default value**: *NXC*
  * **Required**: *no*

**Inputs**

* **1**: ``input`` - input tensor with data for normalization.  The format is
  specified by *data_format*. **Required.**

  * **Type**: T1

* **2**: ``gamma`` - gamma scaling for normalized value. A 1D tensor with the
  same span as input's channel axis. **Optional.**

  * **Type**: T2

* **3**: ``beta`` - beta added to the scaled normalized value. A 1D tensor with
  the same span as input's channel axis. **Optional.**

  * **Type**: T2

* **4**: ``mean`` - value for mean normalization. A 1D tensor with the same span
  as input's channel axis. **Required.**

  * **Type**: T2

* **5**: ``variance`` - value for variance normalization. A 1D tensor with the
  same span as input's channel axis. **Required.**

  * **Type**: T2

**Outputs**

* **1**: ``output`` - the result of normalization. A tensor of the same shape
  and format with 1st input tensor.

  * **Type**: T1

* **2**: ``running mean`` - the computed running mean.

  * **Type**: T2

* **3**: ``running variance`` - the computed running variance.

  * **Type**: T2

* **4**: ``batch mean`` - the computed batch mean.

  * **Type**: T2

* **5**: ``batch variance`` - the computed batch variance.

  * **Type**: T2

**Types**

* *T1*: f32, f16, bf16.
* *T2*: f32, bf16.
* Constraints: *T2* can be bf16 only when *T1* is bf16.

**Mathematical Formulation**

*BatchNormForwardTraining*  normalizes the output in each hidden layer.

* **Input**: Values of :math:`x` over a mini-batch:

  .. math::
     \beta = \{ x_{1...m} \}

* **Parameters to learn**: :math:`\gamma, \beta`
* **Output**:

  .. math::
     \{ o_{i} = BN_{\gamma, \beta} ( b_{i} ) \}

* **Mini-batch mean**:

  .. math::
     \mu_{\beta} \leftarrow \frac{1}{m}\sum_{i=1}^{m}b_{i}

* **Mini-batch variance**:

  .. math::
     \sigma_{\beta }^{2}\leftarrow \frac{1}{m}\sum_{i=1}^{m}
     ( b_{i} - \mu_{\beta} )^{2}

* **Normalize**:

  .. math::
     \hat{b_{i}} \leftarrow \frac{b_{i}
     - \mu_{\beta}}{\sqrt{\sigma_{\beta }^{2} + \epsilon }}

* **Scale and shift**:

  .. math::
     o_{i} \leftarrow \gamma\hat{b_{i}}
     + \beta = BN_{\gamma ,\beta } ( b_{i} )

