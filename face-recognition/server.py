from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2 as cv
import base64
import io
from imageio import imread, imwrite
import os
import face_recognition as fg
import numpy
from PIL import Image
from datetime import date,datetime

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ["POST"])
def check_face():
    base64imagestr = request.form.get('image').split(',')[1]
    roll_id = request.form.get('roll_id')
    # path = request.form.get('test')
    # print(path)
    # print(roll_id)
    # detected = request.form.get('detected')
    # not_detected = request.form.get('not_detected')
    #ret = random.choice([True, False])
    img = imread(io.BytesIO(base64.b64decode(base64imagestr)))

    path = "../static/data/" + str(request.form.get('test')) + "/img/"
    print(path)
    list_img = os.listdir(path)  # list of images in directory
    base_img = []  # contain numpy array of images
    img_class = []  # list of images without extension
    base_encoding = []
    student_image=[]

    def encoding(base_img):
        img_encodings = []
        for i in base_img:
            i = cv.cvtColor(i, cv.COLOR_BGR2RGB)
            encode_value = fg.face_encodings(i)[0]
            img_encodings.append(encode_value)
        return img_encodings

    sturoll = str(roll_id)
    name_class = []
    a=0
    for i in list_img:
        # print(i)
        cur_img = cv.imread(f'{path}/{i}')
        # cur_img = fg.load_image_file(path + str(i))
        if(i.split(".")[0]==sturoll):
            a=1
            base_img.append(cur_img)
            img_class.append(i.split(".")[0])
            name_class.append(i.split(".")[1])
            break
    ret = "Face Not Found"
    if (a == 0):
        path = "../static/data/" + str(request.form.get('test')) + "/capture/"
        now = datetime.now()
        ctime = now.strftime("%H_%M_%S")
        # towrite.append(ctime)
        filename = path + str(sturoll) + "-" + str(ctime) + str(".jpg")
        print(filename)
        print(img.shape)
        image_to_write = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        cv.imwrite(filename, image_to_write)
        ret = "face not match"
        return {"match": ret}

    else:
        print(img_class)
        print(name_class)
        base_encoding = encoding(base_img)  # contains the list of encodings of all the images

        simg = cv.resize(img, (0, 0), None, 0.5, 0.5)
        simg = cv.cvtColor(simg, cv.COLOR_BGR2RGB)
        # print(simg.shape)
        faceinframe = fg.face_locations(simg)
        encodeframe = fg.face_encodings(simg, faceinframe)
        # print(faceinframe)
        # print(len(encodeframe))
        if(len(encodeframe)>1):
            # if (a == 0):
            path = "../static/data/" + str(request.form.get('test')) + "/capture/"
            now = datetime.now()
            ctime = now.strftime("%H_%M_%S")
            # towrite.append(ctime)
            filename = path + str(sturoll) + "-" + str(ctime) + str(".jpg")
            print(filename)
            print(img.shape)
            image_to_write = cv.cvtColor(img, cv.COLOR_RGB2BGR)
            cv.imwrite(filename, image_to_write)
            ret = "Multiple faces Detected"
            return {"match": ret}
        a=0
        for floc, fencode in zip(faceinframe, encodeframe):
            match = fg.compare_faces(base_encoding, fencode)
            facedistance = fg.face_distance(base_encoding, fencode)
            # print(name_class)
            index = numpy.argmin(facedistance)
            if (match[index]):
                ret = sturoll
                a=1
                print(ret , name_class[index])
        if (a == 0):
            path = "../static/data/" + str(request.form.get('test')) + "/capture/"
            now = datetime.now()
            ctime = now.strftime("%H_%M_%S")
            # towrite.append(ctime)
            filename = path + str(sturoll) + "-" + str(ctime) +str(".jpg")
            print(filename)
            print(img.shape)
            image_to_write = cv.cvtColor(img, cv.COLOR_RGB2BGR)
            cv.imwrite(filename, image_to_write)
            ret = "face not match"
            return {"match": ret}
        return {"match" : ret}

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    