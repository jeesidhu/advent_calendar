from collections import Counter
from enum import Enum

from utils import read_file_as_string

WIDTH, HEIGHT = 25, 6


class Pixel(Enum):
    BLACK = "0"
    WHITE = "1"
    TRANSPARENT = "2"


class Layer:

    def __init__(self, digits):
        self.digits = digits
        self.freq = Counter(digits)

    def count(self, color):
        return self.freq[color]


def build_layers(digits, width, height):
    size = width * height
    return [Layer(digits[idx: idx + size]) for idx in range(0, len(digits), size)]


def verify_image_corruption(digits, width=WIDTH, height=HEIGHT):
    layers = build_layers(digits, width, height)
    layer = min(layers, key=lambda l: l.count(Pixel.BLACK.value))
    return layer.count(Pixel.WHITE.value) * layer.count(Pixel.TRANSPARENT.value)


def decode_image(digits, width=WIDTH, height=HEIGHT):
    size = width * height
    img = [Pixel.TRANSPARENT.value] * size
    layers = build_layers(digits, width, height)
    for layer in layers:
        for idx, digit in enumerate(layer.digits):
            if img[idx] == Pixel.TRANSPARENT.value:
                img[idx] = digit
    return "".join(img)


def display_image(digits, width=WIDTH, height=HEIGHT):
    convert = {Pixel.BLACK.value: " ", Pixel.WHITE.value: "*"}
    img = [["" for _ in range(width)] for _ in range(height)]
    for h in range(height):
        for w in range(width):
            img[h][w] = convert[digits[h * width + w]]
    print("\n".join("".join(row) for row in img))


def main():
    digits = read_file_as_string("input_8.txt")
    p1 = verify_image_corruption(digits)
    p2 = decode_image(digits)
    print(f'part 1: {p1}, part 2: {p2}')
    display_image(p2)


if __name__ == '__main__':
    main()
