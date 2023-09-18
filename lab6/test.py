from operator import add
from functools import reduce
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def split4(image):
    half_split = np.array_split(image, 2)
    res = map(lambda x: np.array_split(x, 2, axis=1), half_split)
    return reduce(add, res)


def concatenate4(north_west, north_east, south_west, south_east):
    top = np.concatenate((north_west, north_east), axis=1)
    bottom = np.concatenate((south_west, south_east), axis=1)
    return np.concatenate((top, bottom), axis=0)


def calculate_mean(img):
    return np.mean(img, axis=(0, 1))


def checkEqual(myList):
    first = myList[0]
    return all((x == first).all() for x in myList)


class QuadTree:

    def insert(self, img, level=0):
        self.level = level
        self.mean = calculate_mean(img).astype(int)
        self.resolution = (img.shape[0], img.shape[1])
        self.final = True

        if not checkEqual(img):
            split_img = split4(img)

            self.final = False
            self.north_west = QuadTree().insert(split_img[0], level + 1)
            self.north_east = QuadTree().insert(split_img[1], level + 1)
            self.south_west = QuadTree().insert(split_img[2], level + 1)
            self.south_east = QuadTree().insert(split_img[3], level + 1)

        return self

    def get_image(self, level):
        if self.final or (self.level == level):
            self.data = np.tile(self.mean, (self.resolution[0], self.resolution[1], 1))
            return self.data

        return concatenate4(
            self.north_west.get_image(level),
            self.north_east.get_image(level),
            self.south_west.get_image(level),
            self.south_east.get_image(level))

img = mpimg.imread('sea.jpeg')
img.shape

quadtree = QuadTree().insert(img)

for i in range(1, 15):
    plt.imshow(quadtree.get_image(i))
    plt.show()


