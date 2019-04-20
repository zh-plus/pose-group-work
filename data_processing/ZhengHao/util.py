import cv2
import json
import numpy as np

from pprint import pprint


def get_info(path):
    image = cv2.imread(path)

    file_name = path[:path.rindex('rendered')]
    with open(file_name + 'keypoints.json', 'r', encoding='utf-8') as f:
        j_dict = json.load(f)

    return image, np.array(j_dict['people'][0]['pose_keypoints_2d']).reshape((-1, 3))


def corner_resize(image, info, dst_size):
    resize_image = cv2.resize(image, dst_size, interpolation=cv2.INTER_AREA)
    origin_size = image.shape
    scales = (dst_size[0] / origin_size[0], dst_size[1] / origin_size[1], 1)

    resize_info = info * scales

    return resize_image, resize_info


def crop(image, info):
    valid_info = np.array([a for a in info if a[-1] > 0.1])

    # pprint(valid_info)

    max_x, max_y = np.ceil(valid_info.max(axis=0)[:2]).astype(int)
    min_x, min_y = np.floor(valid_info.min(axis=0)[:2]).astype(int)

    cropped_image = image[min_y: max_y, min_x: max_x, :]
    cropped_info = info - np.array([min_x, min_y, 0])
    cropped_info[cropped_info < 0] = 0

    print(min_x, max_x, min_y, max_y)

    return cropped_image, cropped_info


if __name__ == '__main__':
    image, info = get_info('output/1_rendered.png')
    print(info.shape)

    image2, info2 = crop(image, info)
    print(info.shape)
    print(info2.shape)

    # cv2.imshow("cropped_image", image2)
    # cv2.waitKey(0)
    # cv2.imwrite('test.png', image2)
    pprint(info)
    pprint(info2)

    image3, info3 = corner_resize(image2, info2, (300, 1000))
    pprint(info3)
    cv2.imshow("cropped_resized_image", image3)
    cv2.waitKey(0)
