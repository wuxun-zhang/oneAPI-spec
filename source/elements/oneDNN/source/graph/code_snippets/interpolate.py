import math
import numpy as np
from enum import Enum, unique

class GetNearestPixel:
    def __init__(self, mode: str):
        self.func = {
            'round_prefer_floor': GetNearestPixel.prefer_floor_func,
            'round_prefer_ceil': GetNearestPixel.prefer_ceil_func,
            'floor': GetNearestPixel.floor_func,
            'ceil': GetNearestPixel.ceil_func,
            'simple': GetNearestPixel.simple_func
        }[mode]

    def __call__(self, x_original, is_downsample):
        return self.func(x_original, is_downsample)

    @staticmethod
    def prefer_floor_func(x_original, is_downsample):
        if x_original == int(x_original) + 0.5:
            return int(math.floor(x_original))
        else:
            return int(round(x_original))

    @staticmethod
    def prefer_ceil_func(x_original, is_downsample):
        return int(round(x_original))

    @staticmethod
    def floor_func(x_original, is_downsample):
        return int(math.floor(x_original))

    @staticmethod
    def ceil_func(x_original, is_downsample):
        return int(math.ceil(x_original))

    @staticmethod
    def simple_func(x_original, is_downsample):
        if is_downsample:
            return int(math.ceil(x_original))
        else:
            return int(x_original)


class GetOriginalCoordinate:
    def __init__(self, mode: str):
        self.func = {
            'half_pixel': GetOriginalCoordinate.half_pixel_func,
            'pytorch_half_pixel': GetOriginalCoordinate.pytorch_half_pixel_func,
            'asymmetric': GetOriginalCoordinate.asymmetric_func,
            'tf_half_pixel_for_nn': GetOriginalCoordinate.tf_half_pixel_for_nn_func,
            'align_corners': GetOriginalCoordinate.align_corners_func
        }[mode]

    def __call__(self, x_resized, x_scale, length_resized, length_original):
        return self.func(x_resized, x_scale, length_resized, length_original)

    @staticmethod
    def half_pixel_func(x_resized, x_scale, length_resized, length_original):
        return ((x_resized + 0.5) / x_scale) - 0.5

    @staticmethod
    def pytorch_half_pixel_func(x_resized, x_scale, length_resized, length_original):
        return (x_resized + 0.5) / x_scale - 0.5 if length_resized > 1 else 0.0

    @staticmethod
    def asymmetric_func(x_resized, x_scale, length_resized, length_original):
        return x_resized / x_scale

    @staticmethod
    def tf_half_pixel_for_nn_func(x_resized, x_scale, length_resized, length_original):
        return (x_resized + 0.5) / x_scale

    @staticmethod
    def align_corners_func(x_resized, x_scale, length_resized, length_original):
        return  0 if length_resized == 1 else  x_resized * (length_original - 1) / (length_resized - 1)


def get_cubic_coeff(s, a):
    abs_s = abs(s)
    coeff = np.zeros(4)
    coeff[0] = a * (abs_s - 1.0) * (abs_s - 1.0) * abs_s
    coeff[1] = ((a + 2.0) * abs_s - (a + 3.0)) * abs_s * abs_s + 1.0
    coeff[2] = (((-a -2.0) * abs_s+ (2.0 * a + 3.0)) * abs_s - a) * abs_s
    coeff[3] = - a * abs_s * abs_s * (abs_s - 1.0)
    return coeff


def triangle_coeffs(dz):
    return np.maximum(0.0, 1.0 - np.abs(dz))


@unique
class ShapeCalculationMode(Enum):
    SIZES = 0
    SCALES = 1


class InterpolateCalculation:
    def __init__(self, attrs: dict):
        self.mode = attrs['mode']
        self.func = {
            'nearest': self.nearest_interpolation,
            'linear': self.linear_interpolation,
            'cubic': self.cubic_interpolation,
            'linear_onnx': self.onnx_linear_interpolation
        }[self.mode]
        self.attrs = attrs

        self.pads_begin = attrs.get('pads_begin', [0])
        self.pads_end = attrs.get('pads_end', [0])
        self.coordinate_transformation_mode = attrs.get('coordinate_transformation_mode', 'half_pixel')
        self.nearest_mode = attrs.get('nearest_mode', 'round_prefer_floor')
        self.cube_coeff = attrs.get('cube_coeff', -0.75)
        self.antialias = attrs.get('antialias', False)

        self.shape_calculation_mode = {
            'sizes': ShapeCalculationMode.SIZES,
            'scales': ShapeCalculationMode.SCALES
        }[attrs['shape_calculation_mode']]

        self.get_original_coordinate = self.get_coordinate_transformation_mode()
        self.get_nearest_pixel = GetNearestPixel(self.nearest_mode)


    def get_coordinate_transformation_mode(self):
        return GetOriginalCoordinate(self.coordinate_transformation_mode)

    def shape_infer(self, input_data, sizes, scales):
        result = input_data.shape + self.pads_begin + self.pads_end

        if self.shape_calculation_mode == ShapeCalculationMode.SIZES:
            for i, axis in enumerate(self.axes):
                result[axis] = sizes[i]
        else:
            for i, axis in enumerate(self.axes):
                result[axis] = math.floor(scales[i] * result[axis])

        return result

    @staticmethod
    def correct_pad(pad, rank):
        pad_len = len(pad)
        if pad_len < rank:
            return np.pad(pad, (0, rank - pad_len), 'constant').astype(np.int64)
        elif pad_len > rank:
            return np.array(pad[: rank - 1]).astype(np.int64)
        else:
            return np.array(pad, dtype=np.int64)

    def __call__(self, input_data, sizes, scales, axes):
        rank = input_data.ndim
        self.pads_begin = InterpolateCalculation.correct_pad(self.pads_begin, rank)
        self.pads_end = InterpolateCalculation.correct_pad(self.pads_end, rank)
        self.pads = list(zip(self.pads_begin, self.pads_end))
        self.axes = np.array(axes).astype(np.int64)

        self.output_shape = self.shape_infer(input_data, sizes, scales)
        padded_data = np.pad(input_data, self.pads, 'constant')

        if self.shape_calculation_mode == ShapeCalculationMode.SIZES:
            num_of_axes = len(self.axes)
            self.scales = np.zeros(num_of_axes)
            for i, axis in enumerate(axes):
                self.scales[i] = self.output_shape[axis] / padded_data.shape[axis]
        else:
            self.scales = scales

        if self.mode == 'nearest':
            self.all_scales = np.ones(rank).astype(np.float)
            for i, axis in enumerate(self.axes):
                self.all_scales[axis] = self.scales[i]

        self.input_shape = padded_data.shape
        return self.func(padded_data)

    def clip_coord(self, coord, axis):
        return max(0, min(coord, self.input_shape[axis] - 1))

    def cubic_interpolation(self, input_data):
        rank = len(self.input_shape)
        result = np.zeros(self.output_shape)
        num_of_axes = len(self.axes)
        indices = [ind for ind in np.ndindex(tuple(4 for _ in range(num_of_axes)))]
        for coordinates in np.ndindex(tuple(self.output_shape)):
            input_coords = np.array(coordinates, dtype=np.int64)
            cubic_coeffs = np.zeros((rank, 4))
            for i, axis in enumerate(self.axes):
                in_coord = self.get_original_coordinate(coordinates[axis], self.scales[i], self.output_shape[axis], self.input_shape[axis])
                in_coord_int = math.floor(in_coord)
                input_coords[axis] = in_coord_int
                cubic_coeffs[axis] = get_cubic_coeff(in_coord - in_coord_int, self.cube_coeff)
            summa = 0.0
            for index in indices:
                coords_for_sum = input_coords.copy()
                coeffs_prod = 1.0
                for i, axis in enumerate(self.axes):
                    coords_for_sum[axis] = self.clip_coord(input_coords[axis] + index[i] - 1, axis)
                for i, axis in enumerate(self.axes):
                    coeffs_prod = coeffs_prod * cubic_coeffs[axis][index[i]]
                summa += coeffs_prod * input_data[tuple(coords_for_sum)]
            result[coordinates] = summa
        return result

    def linear_interpolation(self, input_data):
        result = np.zeros(self.output_shape)
        num_of_axes = len(self.axes)
        is_downsample = False

        for scale in self.scales:
            is_downsample = is_downsample or (scale < 1)

        antialias = is_downsample and self.antialias

        a = np.zeros(num_of_axes)
        for i, _ in enumerate(self.axes):
            a[i] = self.scales[i] if antialias else 1.0

        prod_of_a = np.prod(a)
        r = np.zeros(num_of_axes).astype(np.int64)
        for i, _ in enumerate(self.axes):
            r[i] = 2 if self.scales[i] > 1.0 else int(math.ceil(2.0/a[i]))

        indices = [tuple(np.array(ind).astype(np.int64) - r) for ind in np.ndindex(tuple(2 * r + 1))]

        for coordinates in np.ndindex(tuple(self.output_shape)):
            icoords = np.array(coordinates).astype(np.float64)
            icoords_r = np.array(coordinates).astype(np.float64)
            for i, axis in enumerate(self.axes):
                in_coord = self.get_original_coordinate(coordinates[axis], self.scales[i], self.output_shape[axis], self.input_shape[axis])
                icoords[axis] = in_coord
                icoords_r[axis] = round(in_coord)

            summa = 0.0
            wsum = 0.0

            for index in indices:
                inner_coords = np.array(coordinates)
                for i, axis in enumerate(self.axes):
                    inner_coords[axis] = index[i] + icoords_r[axis]

                conditions = [inner_coords[axis] >= 0 and inner_coords[axis] < self.input_shape[axis] for axis in self.axes]
                if not all(conditions):
                    continue

                dz = np.zeros(num_of_axes)
                for i, axis in enumerate(self.axes):
                    dz[i] = icoords[axis] - inner_coords[axis]

                w = prod_of_a * np.prod(triangle_coeffs(a * dz))
                wsum += w
                summa += w * input_data[tuple(inner_coords)]

            if wsum == 0:
                result[coordinates] = 0.0
            else:
                result[coordinates] = summa / wsum

        return result

    def onnx_linear_interpolation(self, input_data):
        rank = len(self.input_shape)
        assert rank in [2, 4], "mode 'linear_onnx' supports only 2D or 4D tensors"
        assert set(self.axes) == {2, 3} or set(self.axes) == {0, 1}, \
            "mode 'linear_onnx' supports only case when axes = {2, 3} or axes = {0, 1}"

        result = np.zeros(self.output_shape)

        if rank == 2:
            reshaped_data = np.reshape(input_data, (1, 1, self.input_shape[0], self.input_shape[1]))
            result = np.reshape(result,  (1, 1, self.output_shape[0], self.output_shape[1]))
        else:
            reshaped_data = input_data

        input_shape = np.array(reshaped_data.shape).astype(np.int64)
        output_shape = np.array(result.shape).astype(np.int64)

        output_height = output_shape[2]
        output_width = output_shape[3]
        input_height = input_shape[2]
        input_width = input_shape[3]
        height_scale = self.scales[0]
        width_scale = self.scales[1]
        batch_size = input_shape[0]
        num_channels = input_shape[1]

        y_original = np.zeros(output_height).astype(np.float)
        x_original = np.zeros(output_width).astype(np.float)

        in_y1 = np.zeros(output_height).astype(np.int64)
        in_y2 = np.zeros(output_height).astype(np.int64)
        in_x1 = np.zeros(output_width).astype(np.int64)
        in_x2 = np.zeros(output_width).astype(np.int64)

        dy1 = np.zeros(output_height).astype(np.float)
        dy2 = np.zeros(output_height).astype(np.float)

        dx1 = np.zeros(output_width).astype(np.float)
        dx2 = np.zeros(output_width).astype(np.float)

        for y in range(0, output_height):
            in_y = self.get_original_coordinate(y, height_scale, output_height, input_height)
            y_original[y] = in_y
            in_y = max(0, min(in_y, input_height - 1))
            in_y1[y] = max(0, min(int(in_y), input_height - 1))
            in_y2[y] = min(in_y1[y] + 1, input_height - 1)
            dy1[y] = abs(in_y - in_y1[y])
            dy2[y] = abs(in_y - in_y2[y])

            if in_y1[y] == in_y2[y]:
                dy1[y] = 0.5
                dy2[y] = 0.5

        for x in range(0, output_width):
            in_x = self.get_original_coordinate(x, width_scale, output_width, input_width);
            x_original[x] = in_x
            in_x = max(0.0, min(in_x, input_width - 1));

            in_x1[x] = min(in_x, input_width - 1);
            in_x2[x] = min(in_x1[x] + 1, input_width - 1);

            dx1[x] = abs(in_x - in_x1[x]);
            dx2[x] = abs(in_x - in_x2[x]);
            if in_x1[x] == in_x2[x]:
                dx1[x] = 0.5
                dx2[x] = 0.5

        for n in range(0, batch_size):
            for c in range(0, num_channels):
                for y in range(0, output_height):
                    for x in range(0, output_width):
                        x11 = reshaped_data[n, c, in_y1[y], in_x1[x]]
                        x21 = reshaped_data[n, c, in_y1[y], in_x2[x]]
                        x12 = reshaped_data[n, c, in_y2[y], in_x1[x]]
                        x22 = reshaped_data[n, c, in_y2[y], in_x2[x]]
                        temp = dx2[x] * dy2[y] * x11 + dx1[x] * dy2[y] * x21 + dx2[x] * dy1[y] * x12 + dx1[x] * dy1[y] * x22
                        result[n, c, y, x] = temp

        return np.reshape(result, self.output_shape)

    def nearest_interpolation(self, input_data):
        result = np.zeros(self.output_shape)

        num_of_axes = len(self.axes)
        for coordinates in np.ndindex(tuple(self.output_shape)):
            input_coords = np.array(coordinates, dtype=np.int64)
            for axis, scale in enumerate(self.all_scales):
                in_coord = self.get_original_coordinate(coordinates[axis], scale, self.output_shape[axis], self.input_shape[axis])
                nearest_pixel = self.get_nearest_pixel(in_coord, scale < 1)
                input_coords[axis] = max(0, min(nearest_pixel, self.input_shape[axis] - 1))
            result[coordinates] = input_data[tuple(input_coords)]

        return result