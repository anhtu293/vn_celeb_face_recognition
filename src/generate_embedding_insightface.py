import argparse
import cv2
import sys
import numpy as np
sys.path.append("../backbones/insightface/deploy")
import face_model
import pandas as pd
import csv

parser = argparse.ArgumentParser(description='face model test')
# general
parser.add_argument('--image-size', default='112,112', help='')
parser.add_argument('--model', default='', help='path to load model.')
parser.add_argument('--ga-model', default='', help='path to load model.')
parser.add_argument('--gpu', default=0, type=int, help='gpu id')
parser.add_argument('--det', default=0, type=int, help='mtcnn option, 1 means using R+O, 0 means detect from begining')
parser.add_argument('--flip', default=0, type=int, help='whether do lr flip aug')
parser.add_argument('--threshold', default=1.24, type=float, help='ver dist threshold')
args = parser.parse_args()

data_path  = '../data/train_112x112'

if __name__ == '__main__':
    model = face_model.FaceModel(args)
    img_file = []
    output_dir = './embeddings/insightface/{}'.format(data_path("/")[-1])
    labels = pd.read_csv("../data/train.csv")

    for i in len(labels):
        img = cv2.imread(labels["image"][i])
        img = cv2.cvtColor(cv2.COLOR_BGR2RGB)
        embeddings = model.get_feature(img)
        np.save(output_dir + '%s.npy'%labels["image"][i][:-4], embeddings)
        img_file.append(['/%s.npy'%labels["image"][i][:-4], labels['class'][i]])

        img_flip = cv2.flip(img, 1)
        embeddings = model.get_feature(img_flip)
        np.save(output_dir + '%s_flip.npy'%labels["image"][i][:-4], embeddings)
        img_file.append([labels["image"][i][:-4] + "_flip.npy", labels['class'][i]])
    
    with open("./embedding/insightface/embs_class_{}.csv".format(data_path[8:]), 'a') as file:
        writer = csv.writer(file)
        writer.writerows(img_file)