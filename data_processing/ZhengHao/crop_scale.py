import json
from PIL import Image, ImageDraw
from treelib import Node, Tree
import math


# 以1_keypoints为例，standard值表示人体每段的长度，目前是手动预设的
# 效果：以1点为中心保留各部位相对方向不变，调整人体每段的长度到定值，再进行裁剪
# 只保留了骨架中0~14的节点



fadr = "E:\\1_keypoints.json"
imgadr = 'E:\\1_rendered.png'


def loadFile(fadr):
    file = open(fadr, encoding='utf-8')
    jfile = json.load(file)
    pose_point = jfile['people'][0]['pose_keypoints_2d']
    pose_point = pose_point[0:3 * 15]
    print("pose_point:", pose_point)
    return pose_point


def pose_tree():
    tree = Tree()
    tree.create_node(1, 1)
    tree.create_node(0, 0, parent=1)
    tree.create_node(2, 2, parent=1)
    tree.create_node(5, 5, parent=1)
    tree.create_node(8, 8, parent=1)
    tree.create_node(3, 3, parent=2)
    tree.create_node(4, 4, parent=3)
    tree.create_node(6, 6, parent=5)
    tree.create_node(7, 7, parent=6)
    tree.create_node(9, 9, parent=8)
    tree.create_node(12, 12, parent=8)
    tree.create_node(10, 10, parent=9)
    tree.create_node(11, 11, parent=10)
    tree.create_node(13, 13, parent=12)
    tree.create_node(14, 14, parent=13)
    # print(tree.root)
    # print(tree.children(14))
    return tree



standard = [100, 0, 10, 100, 100, 18, 130, 120, 250, 5, 160, 130, 10, 180, 200]
tree = pose_tree()
pose_point = loadFile(fadr)


def scale(standard, tree, pose_point):
    new_point = pose_point.copy()
    list = []
    list.append(tree.root)
    while len(list) != 0:
        node = list.pop()
        nx = new_point[3 * node]
        ny = new_point[3 * node + 1]
        children = tree.children(node)
        if children != [] and nx != 0:

            for i in range(len(children)):

                c = children[i].tag
                # print("c:",c)
                cx = pose_point[3 * c]
                cy = pose_point[3 * c + 1]
                list.append(c)
                if cx != 0:
                    vecx = cx - pose_point[3 * node]  # old x
                    vecy = cy - pose_point[3 * node + 1]  # old y
                    veclen = math.sqrt(math.pow(vecx, 2) + math.pow(vecy, 2))  # old distance
                    stdlen = standard[c]  # standard[c] represents the std distance from c to its parent
                    stdx = stdlen / veclen * vecx  # relative x from parent new x
                    stdy = stdlen / veclen * vecy  # relative y from parent new y
                    new_point[3 * c] = nx + stdx  # update child new x and y
                    new_point[3 * c + 1] = ny + stdy
    return new_point


scaled_pose_point = scale(standard, tree, pose_point)


def crop(scaled_pose_point, imgadr):
    minx = 1000000000
    miny = 1000000000
    maxx = 0
    maxy = 0
    for i in range(15):
        if scaled_pose_point[3 * i] < minx and scaled_pose_point[3*i] != 0:
            minx = scaled_pose_point[3 * i]
        if scaled_pose_point[3 * i] > maxx:
            maxx = scaled_pose_point[3 * i]
        if scaled_pose_point[3 * i + 1] < miny and scaled_pose_point[3*i+1] != 0:
            miny = scaled_pose_point[3 * i + 1]
        if scaled_pose_point[3 * i + 1] > maxy:
            maxy = scaled_pose_point[3 * i + 1]
    # image_size = image.size
    # image.rotate(3)  # 左正右负
    image = Image.open(imgadr)
    region = image.crop((minx, miny, maxx, maxy))
    draw = ImageDraw.Draw(region)
    print(minx,miny,maxx,maxy)
    for i in range(15):
        scaled_pose_point[3 * i] = scaled_pose_point[3 * i] - minx
        scaled_pose_point[3 * i + 1] = scaled_pose_point[3 * i + 1] - miny
        draw.ellipse((scaled_pose_point[3 * i] - 10, scaled_pose_point[3 * i + 1] - 10, scaled_pose_point[3 * i] + 10,
                      scaled_pose_point[3 * i + 1] + 10), fill=(0, 0, 0))
    print(scaled_pose_point)
    with open("E:\\1_scaled_keypoints.json", "w") as f:
        f.write(json.dumps(scaled_pose_point))


    region.show()
    region.save("E:\\crop.png")

crop(scaled_pose_point,imgadr)