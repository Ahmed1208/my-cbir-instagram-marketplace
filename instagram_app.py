import os
import instaloader

import argparse
import glob
import time
import random
import pickle

import tensorflow as tf
from tensorflow import keras
from keras.preprocessing import image
from keras.applications.imagenet_utils import decode_predictions, preprocess_input
from keras.models import Model
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

class Post:

    image_instagramLink = ''
    image_path = ''
    image_description = ''
    image_featureVector = None

    def __init__(self, image_instagramLink):
        self.image_instagramLink = image_instagramLink

    def set_image_path(self,image_path):
        self.image_path = image_path

    def set_description(self,image_description):
        self.image_description = image_description

    def set_featureVector(self, image_featureVector ):
        self.image_featureVector = image_featureVector

def create_text_file(images_folder,text_file ,sort = 1):
  image_extensions = ['.jpg', '.png', '.jpeg']   # case-insensitive (upper/lower doesn't matter)


  images = [os.path.join(dp, f) for dp, dn, filenames in os.walk(images_folder) for f in filenames if os.path.splitext(f)[1].lower() in image_extensions]
  imgs = list()
  for i in images:
      i = i.replace("\\","/")
      i = i.replace("\\\\","/")
      imgs.append(i)
  # print(imgs)

  if(sort == 1):
    imgs.sort()

  a = open(text_file, "w")

  for path in imgs:
      a.write(str(path) + '\n')
  #return a

def get_username(username):
    # get instance
    L = instaloader.Instaloader()

    L.login("asu.cbirteam", "cbirteam1998")  # (login)

    # get profile instance
    profile = instaloader.Profile.from_username( L.context, username )

    posts = []

    # download posts
    for post in profile.get_posts():

        #set instagram link
        instagram_link = "https://www.instagram.com/p/" + post.shortcode
        p = Post(instagram_link)
        posts.append( p )


        L.download_post(post, target=profile.username)

    # get path,description
    images_folder = username
    text_file = "username_images_paths.txt"
    create_text_file( images_folder , text_file )

    f = open(text_file, "r")
    for i in range(len(posts)):             # read next line
        line = f.readline()   # if line is empty, you are done with all lines in the file
        if not line:break     #you can access the lineprint(line.strip())

        #set the image path
        line = line.replace("\n", "")
        posts[i].set_image_path(line)

        line = line.replace(".jpg",".txt")

        try:
            with open(line,encoding="utf8") as y:
                description = y.read()
                #set the image descriprion
                posts[i].set_description(description)
            y.close()
        except:
            posts[i].set_description("")
    f.close()

    os.remove(text_file)

    return posts

class ModelExtractor:

    vgg_16_model = None
    fc2_model = None

    def __init__(self):
        # print("hello")
        model = tf.keras.applications.VGG16(weights='imagenet', include_top=True)
        feat_extractor = Model(inputs=model.input, outputs=model.get_layer("fc2").output)

        self.vgg_16_model = model
        self.fc2_model = feat_extractor

    def extract(self, image_path):
        img = image.load_img(image_path, target_size=self.fc2_model.input_shape[1:3])
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = self.fc2_model.predict(x)[0]
        return features

    def extract_features(self, images_paths):  # for Dataset
        images = images_paths                  # must pass the full paths
        tic = time.process_time()

        features = []
        for i, image_path in enumerate(images):
            if i % 500 == 0:
                toc = time.process_time()
                elap = toc - tic;
                print("analyzing image %d / %d. Time: %4.4f seconds." % (i, len(images), elap))
                tic = time.process_time()
            feat = self.extract(image_path)
            features.append(feat)

        return features
    def query_image_features(self ,image_path):
        return self.extract(image_path)

def get_pca_features(features,number_of_components=300):        #for Dataset ONLY!!!!!!!!!!!!!
    features = np.array(features)
    pca = PCA(n_components=number_of_components)
    pca.fit(features)
    pca_features = pca.transform(features)

    pickle.dump([pca], open('pca_pickle_file.p', 'wb'))

    return pca_features

def query_pca_features(query_features):
    objects = []
    with (open('pca_pickle_file.p', "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break

    pca = objects[0][0]
    #print(pca)

    pca_features = pca.transform([query_features][0:1])[0]

    return pca_features

def prepare_dataset(posts_lists):

    #init the model
    m = ModelExtractor()

    print(posts_lists[1])
    #extract features from dataset
    features = m.extract_features(posts_lists[1])

    pca_features = get_pca_features(features,min(len(posts_lists[1]),300))

    posts_lists[3] = pca_features

    return posts_lists

def prepare_query_image(image_path):

    #init the model
    m = ModelExtractor()

    #extract features from query image
    features = m.extract(image_path)

    pca_features = query_pca_features( features )

    return pca_features

def save_dataset(posts_lists):
    pickle.dump([posts_lists[0],posts_lists[1],posts_lists[2],posts_lists[3],posts_lists[4]], open("dataset.p", 'wb'))

def get_history_data(pickle_path):

    objects = []
    with (open(pickle_path, "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break

    image_instagramLinks = objects[0][0]
    image_paths = objects[0][1]
    image_descriptions = objects[0][2]
    image_featureVectors = objects[0][3]
    store_name = objects[0][4]

    return image_instagramLinks,image_paths,image_descriptions,image_featureVectors,store_name

def get_closest_images(new_pca_features, pca_features , num_results=6):

    # calculate its distance to all the other images pca feature vectors
    distances = [distance.cosine(new_pca_features, feat) for feat in pca_features]
    idx_closest = sorted(range(len(distances)), key=lambda k: distances[k])[0:num_results]  # grab first 6
    return idx_closest

# if __name__ == '__main__':

#     #get images from instagram
#     posts = get_username("store_clocks")

#     #make a list for each post variable
#     posts_lists = [[], [], [], []]
#     for x in posts:
#         posts_lists[0].append(x.image_instagramLink)
#         posts_lists[1].append(x.image_path)
#         posts_lists[2].append(x.image_description)

#     #get feature vector of images
#     posts_lists = prepare_dataset(posts_lists)

#     #save the dataset
#     save_dataset(posts_lists)

#     #retrive all data
#     image_instagramLinks, image_paths, image_descriptions, image_featureVectors = get_history_data("dataset.p")


#     #query image get feature vector of image
#     query_features = prepare_query_image("store_clocks/2013-09-17_14-59-55_UTC.jpg")
#     print(len(query_features))

#     #get similar images
#     similar_images_indices = get_closest_images(query_features, image_featureVectors, 6)

#     #get similar images links
#     for x in similar_images_indices:
#         print(image_instagramLinks[x])









    """
    for x in posts:
        print(x.image_instagramLink)
        print(x.image_path)
        print(x.image_description)
        print("###################################")
    """
    """
    for x in posts:
        print(x.image_featureVector)
        print("###################################")
    """

    """
    for x in image_instagramLinks:
        print(x)
        print("###################################")
    """


