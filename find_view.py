import cv2
import sys
import os
import glob
import random
import argparse
import json


class View():
    def __init__(self):
        self.images = []
        self.images_path = []
        self.fineshed = False
        self.connection = {}

def match_images(img1, img2):
    orb = cv2.ORB_create(nfeatures = 1000)
    # orb = cv2.xfeatures2d.SIFT_create(1000)
    # find the keypoints with ORB
    kp1 = orb.detect(img1, None)
    # compute the descriptors with ORB
    kp1, des1 = orb.compute(img1, kp1)

    # find the keypoints with ORB
    kp2 = orb.detect(img2, None)
    # compute the descriptors with ORB
    kp2, des2 = orb.compute(img2, kp2)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)
    # print(len(matches))

    # Lowes Ratio
    good_matches = []
    for m, n in matches:
        if m.distance < .75 * n.distance:
            good_matches.append(m)

    if len(good_matches) > 20:
        # src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]) \
        #     .reshape(-1, 1, 2)
        # dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]) \
        #     .reshape(-1, 1, 2)
        # M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5)
        return True
    else:
        # M = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        # # print("not a good match")
        return False

def new_list(index_under_consideration, view_under_construction, views, openlist, closed_list, input_im, input_im_path):
    l = list(range(len(input_im)))
    exclusion_list = []
    while len(openlist) !=0:

        exclusion_list.append(index_under_consideration)
        new_input_list = [x for i, x in enumerate(l) if i not in  exclusion_list]
        # print("image under consd ", index_under_consideration)
        # print("new_input_list  ", new_input_list)

        for i in new_input_list:
            flag = match_images(input_im[index_under_consideration], input_im[i])
            if flag:
                if i not in openlist:
                    openlist.append(i)
                else:
                    continue

        openpath_list = []
        # print("openlist  ", openlist)

        closed_list.append(openlist.pop(0))

        # print("closed_list", closed_list)
        # print("openlist  ", openlist)

        if len(openlist) != 0:
            index_under_consideration = openlist[0]
        for index in openlist:
            openpath_list.append(input_im_path[index])
        views[view_under_construction].connection.update({input_im_path[index_under_consideration]: openpath_list})

    return  exclusion_list


def make_views(input_im, input_im_path, views):

    while len(input_im) != 0:
        openlist = []
        closed_list= []
        # print("length of input_list ", len(input_im))
        temp_list = list(range(len(input_im)))
        index_under_consideration = random.choice(temp_list)
        if len(views) == 0:
            view_under_construction = 0
        else:
            view_under_construction = len(views)


        if len(openlist) == 0:
            new_view = View()
            views.append(new_view)
            openlist.append(index_under_consideration)
            exc = new_list(index_under_consideration, view_under_construction, views, openlist, closed_list, input_im, input_im_path)
            # print("##################")
            # print("exc  ", exc)
            for ind in exc:
                views[view_under_construction].images.append(input_im[ind])
                views[view_under_construction].images_path.append(input_im_path[ind])

                # print(input_im_path[ind])

            # print("****#######******")
            temp_list_1 = [x for i, x in enumerate(temp_list) if i not in  exc]
            temp_in_list=[]
            temp_in_p_list= []
            # print("temp_list_1", temp_list_1)
            for index in temp_list_1:
                temp_in_list.append(input_im[index])
                temp_in_p_list.append(input_im_path[index])
            input_im = temp_in_list
            input_im_path = temp_in_p_list


    return views


def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""

    parser = argparse.ArgumentParser(description='The program takes a folder of images of different views '
                                                 'and groups them and outputs a json file.')
    parser.add_argument('--inputDirectory',
                    help='Path to the input directory contaning images.')

    return parser

def make_json(views, path):
    p = path.split('/')


    if path[len(path) - 1] == '/':
        file_name = p[len(p) - 2]
    else:
        path = path + "/"
        file_name = p[len(p) -1]

    data = {}
    c = 1
    for v in views:
        imgs = []
        for img_path in v.images_path:
            temp = img_path.split('/')
            imgs.append(temp[len(temp) - 1])
        s = "VIEW_" + str(c)
        data.update({s : imgs})
        c+= 1
    print(data)
    with open(path + str(file_name) + '.json', 'w') as f:
        json.dump(data,f, indent=2)




def main(path):
    # reading all the images in the subfloders
    input_im = []
    input_im_path = []


    for imgs in  glob.glob(path + "/*.jpg"):
        input_im_path.append(imgs)
        n = cv2.imread(imgs)
        # n = cv2.GaussianBlur(n, (5,5), 0)
        input_im.append(n)
    # for path in input_im_path:
    #     print(path)
    views = []
    make_views(input_im, input_im_path, views)
    make_json(views, path)



if __name__ == "__main__":
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    if os.path.exists(parsed_args.inputDirectory):
        main(parsed_args.inputDirectory)
    else:
        print("path provided doesn't exsist")













