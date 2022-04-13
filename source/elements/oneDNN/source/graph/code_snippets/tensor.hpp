class tensor {
logical_tensor_t data;
public:
/// Constructs a tensor object according to the given logical tensor
///
/// @param lt The given logical tensor
/// @param aengine Engine to store the data on.
/// @param handle Handle of memory buffer to use as an underlying storage,
///    if the ndims in the logical tensor is 0, data handle holds a scalar
tensor(const logical_tensor &lt, const engine &aengine, void *handle);

/// Returns the underlying memory buffer with the specific type
///
/// @tparam T Type of the request buffer
/// @returns The underlying memory buffer
template <typename T>
typename std::add_pointer<T>::type get_data_handle() const;
 
/// Sets the underlying memory buffer
///
/// @param handle Data handle. For the CPU engine, the data handle
///     is a pointer to the actual data.
void set_data_handle(void *handle);

/// Returns the number of elements in the tensor
///
/// @returns Number of elements
int64_t get_element_num() const;

/// Returns the associated engine.
///
/// @returns An engine object
engine get_engine() const;
};
