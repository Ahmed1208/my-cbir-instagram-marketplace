from flask import Flask,render_template,request,send_from_directory
from os import path,mkdir
from werkzeug.utils import secure_filename
from instagram_app import *
from shutil import move
from pathlib import Path
from server_for_description import *
import random
import time

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static/uploads"

# global list to show 
shownItems = []
# global list with avalible usernames 
globalUsername = []

# global for query image
query_image_url = ""

counter = int()

@app.route("/instagram")
def GetInstagram():
    return render_template("instagram.html",maxShownImages=None)


def show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name,indecis=None,maxShownImages=True):
    if(indecis == None):
        for x in range(len(image_instagramLinks)):
            shownItems.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})
    else:
        for x in range(len(image_instagramLinks)):
            if(x in indecis):
                shownItems.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})

    print(shownItems)
    if maxShownImages:
        return render_template("instagram.html",results=shownItems,maxShownImages=len(shownItems),query_image_url = query_image_url.replace("\\","/"), badges = globalUsername)
    else:
        return render_template("instagram.html",results=shownItems,maxShownImages=None,query_image_url = query_image_url.replace("\\","/"),badges = globalUsername)

@app.route('/instagram/imageSimilarity',methods=['POST'])
def uploadI2():
    file = request.files.get("file")
    print(file)
    filename = secure_filename(file.filename)
    file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
    queryImage = path.join(app.config['UPLOAD_FOLDER'], filename)
    print(queryImage)

    global query_image_url
    query_image_url = queryImage
    # for file in files:
    #         filename = secure_filename(file.filename)
    #         file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
    #         queryImage = path.join(app.config['UPLOAD_FOLDER'], filename)
    #         break


    #retrive all data
    image_instagramLinks, image_paths, image_descriptions, image_featureVectors, store_name = get_history_data("dataset.p")
    
    query_features = prepare_query_image(queryImage)

    #get similar images
    shownImages = request.form.get("resCount")
    print(type(shownImages))
    shownImages = int(shownImages)
    print(type(shownImages))
    similar_images_indices = get_closest_images(query_features, image_featureVectors, shownImages)

    global counter
    counter = shownImages

    global shownItems
    shownItems = []
    return show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name,similar_images_indices)


@app.route('/instagram/store',methods=['POST'])
def getAllItems_route():

    global shownItems
    global globalUsername

    username = request.form.getlist("username")
    
    if set(username)-set(globalUsername):
        # update showItems if new username is added
        ############################
        ######## model code ########
        ############################
        posts_lists = [[], [], [], [] , []]

        for user in username:
            #get images from instagram
            posts = get_username(user)

            print(posts)
            #make a list for each post variable
            for x in posts:
                posts_lists[0].append(x.image_instagramLink)
                posts_lists[1].append(x.image_path)
                posts_lists[2].append(x.image_description)
                posts_lists[4].append(user)
                
        print("before prepare",posts_lists)

        #get feature vector of images
        posts_lists = prepare_dataset(posts_lists)

        print("not gonna run")

        #save the dataset
        save_dataset(posts_lists)

        #retrive all data
        image_instagramLinks, image_paths, image_descriptions, image_featureVectors, store_name = get_history_data("dataset.p")

        print("creating database......")
        # #create our database
        input_docs_for_description("instagram_database",image_descriptions,image_paths)
        print("database created")

        #generate random data
        length_of_data = len(image_descriptions)
        for x in range(4):
            random_int = random.randint(0, length_of_data)

            random_index = random.randint(0, length_of_data)
            image_instagramLinks.insert(random_index,image_instagramLinks[random_int])
            image_paths.insert(random_index,image_paths[random_int])
            image_descriptions.insert(random_index,"Fake"+str(x))
            store_name.insert(random_index,store_name[-4])

        # global shownItems
        shownItems = []



        # for x in range(len(image_instagramLinks)):
        #     shownItems.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})

        #query image get feature vector of image
        
        # print(len(query_features))


        

        # links = []
        # # #get similar images links
        # for x in similar_images_indices:
        #     links.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})

        for user in username:
            if Path(path.join(app.config['UPLOAD_FOLDER'], user)).is_dir() == False:
                move(user,path.join(app.config['UPLOAD_FOLDER'], user))
        
        globalUsername = username
        
        return show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name)

    if set(globalUsername)-set(username):
        # update showItems if a username was deleted
        newShownItems = []
        for item in shownItems:
            if item['username'] in username:
                newShownItems.append(item)

        shownItems = newShownItems
        globalUsername = username
        
    
    return render_template("instagram.html",results=shownItems,maxShownImages=len(shownItems),query_image_url = query_image_url.replace("\\","/"),badges = globalUsername)
    
    

@app.route('/instagram/filter',methods=['POST'])
def uploadIupdate():

    username = request.form.getlist("username")
    # print(username)
    # posts_lists = [[], [], [], [] , []]

    # for user in username:
    #     #get images from instagram
    #     posts = get_username(user)

    #     #make a list for each post variable
    #     for x in posts:
    #         posts_lists[0].append(x.image_instagramLink)
    #         posts_lists[1].append(x.image_path)
    #         posts_lists[2].append(x.image_description)
    #         posts_lists[4].append(user)
            

    # #get feature vector of images
    # posts_lists = prepare_dataset(posts_lists)

    # #save the dataset
    # save_dataset(posts_lists)

    # #retrive all data
    # image_instagramLinks, image_paths, image_descriptions, image_featureVectors, store_name = get_history_data("dataset.p")
    

    # for x in range(len(image_instagramLinks)):
    #     shownItems.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})

    #query image get feature vector of image
    
    # print(len(query_features))


    

    # links = []
    # # #get similar images links
    # for x in similar_images_indices:
    #     links.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})

    for user in username:
        if Path(path.join(app.config['UPLOAD_FOLDER'], user)).is_dir() == False:
            move(user,path.join(app.config['UPLOAD_FOLDER'], user))
    # print(links)
    return render_template("instagram.html",results=shownItems,query_image_url = query_image_url.replace("\\","/"),badges = globalUsername)
    # show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name)
    


black_listed = []

@app.route('/instagram/imageSimilarity/removeImage',methods=['POST'])
def update():
    id = request.form.get("id")
    print(id)
    print(id.split(',')[0])
    print(id.split(',')[1])
    print(type(id))

    global query_image_url
    query_image_url = id.split(',')[0]

    # retrive all data
    image_instagramLinks, image_paths, image_descriptions, image_featureVectors, store_name = get_history_data("dataset.p")

    query_features = prepare_query_image(query_image_url)


    # get similar images
    global counter
    counter+=1
    shownImages = counter

    print(type(shownImages))

    similar_images_indices = get_closest_images(query_features, image_featureVectors, shownImages)

    temp_index = image_paths.index(id.split(',')[1].split('\\')[1])
    print(temp_index)
    black_listed.append(temp_index)


    for x in black_listed:
        try:
            similar_images_indices.remove(x)
        except:
            pass
    #counter-=1


    global shownItems
    shownItems = []
    return show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name,similar_images_indices)







@app.route('/instagram/refresh')
def refresh():

    global query_image_url
    query_image_url = ""

    global shownItems
    shownItems = []

    # retrive all data
    image_instagramLinks, image_paths, image_descriptions, image_featureVectors, store_name = get_history_data("dataset.p")

    # generate random data
    length_of_data = len(image_descriptions)
    for x in range(4):
        random_int = random.randint(0, length_of_data)
        image_instagramLinks.append(image_instagramLinks[random_int])
        image_paths.append(image_paths[random_int])
        image_descriptions.append("Fake" + str(x))
        store_name.append(store_name[-4])

    return show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name)



@app.route('/instagram/removeDuplicate')
def remove_duplicate():

    global query_image_url
    query_image_url = ""

    global shownItems
    shownItems = []

    # retrive all data
    image_instagramLinks, image_paths, image_descriptions, image_featureVectors, store_name = get_history_data("dataset.p")

    time.sleep(10)
    return show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name)


@app.route('/instagram/descriptonSearch',methods=['POST'])
def search_by_texts():

    input_text = request.form.get("id")

    print(input_text)
    print(type(input_text))

    # #search in our database
    description , images = search_by_text("instagram_database",input_text)
    # #save it at dictionary
    # dictionary_history = {'rolex':[0,2,7,17,20],
    #                       '$':[*range(0,21,1)],
    #                       'casio':[1,4],
    #                       'nike':[*range(22,84,1)],
    #                       '60':[*range(87,162,1)],
    #                       'blue':[35,55,74]
    #                      }





    print(input_text)

    # retrive all data
    image_instagramLinks, image_paths, image_descriptions, image_featureVectors, store_name = get_history_data("dataset.p")

    #indices = dictionary_history[input_text]

    indices = []
    for x in images:
        index = image_paths.index(x)
        indices.append(index)

    print(indices)

    global counter
    counter = len(indices)

    global query_image_url
    query_image_url = ""



    if input_text == "":
        return show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name)

    global shownItems
    shownItems = []
    return show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name,indices)


if __name__ == "__main__":
    app.run()