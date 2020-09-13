import tensorflow as tf 
import numpy as np 
import cv2
import os
import time
from sklearn.neighbors import NearestNeighbors
import sys
from pylepton.Lepton3 import Lepton3
import pymongo
import datetime as dt
#from pylepton import Lepton
#mtcnn = MTCNN()

CameraID = "824209"

pw="hack"
user="Liam-Pilarski"

connectionURL = f"mongodb+srv://{user}:{pw}@tempcheck.cfwko.mongodb.net/<dbname>?retryWrites=true&w=majority"
client = pymongo.MongoClient(connectionURL)
mydb=client["LeptonData"]
mainCollection=mydb["DATA"]

def capture(flip_v = False, device = "/dev/spidev0.1"):
  with Lepton3(device) as l:
    a,_ = l.capture()
    b,_ = l.capture()
  if flip_v:
    cv2.flip(a,0,a)
  cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
  np.right_shift(a, 8, a)
  print(b)
  return np.uint8(a), b

os.system("sh model_download.sh")

def calc_overlap(bounds):
    nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(bounds)
    distances, indices = nbrs.kneighbors(bounds)
    mask = np.ma.masked_equal(distances, 0.0, copy=False)
    min_dist = int(np.argmin(mask) / 2)

    indices_ = indices[min_dist]

    rect1 = bounds[indices_[0]]
    rect1_area = abs((rect1[2] - rect1[0]) * (rect1[3] - rect1[1]))

    rect2 = bounds[indices_[1]]
    rect2_area = abs((rect2[2] - rect2[0]) * (rect2[3] - rect2[1]))

    overlap_area = abs((max(rect1[1], rect2[1]) - min(rect1[3], rect2[3])) *
        (max(rect1[2], rect2[2]) - max(rect1[0], rect2[0])))
    overlap_percentage = overlap_area / min(rect1_area, rect2_area)

    if len(bounds) > 2 and (overlap_percentage > .5 or max(rect1_area, rect2_area) / min(rect1_area, rect2_area) > 1.3):
        del(bounds[0 if rect1_area < rect2_area else 1])
        calc_overlap(bounds)
    else: 
        return bounds

def build_model(model_path, output_tensor_names, input_tensor_name, session="tf", placeholder=None):
    graph_def = None

    with tf.gfile.FastGFile(model_path, "rb") as graph_file:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(graph_file.read())

    if session == "tf":
        sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    elif session == "keras":
        sess = keras.backend.get_session()
    tf.import_graph_def(graph_def, name='')

    output_tensors = [sess.graph.get_tensor_by_name(name) for name in output_tensor_names]
    input_tensor = sess.graph.get_tensor_by_name(input_tensor_name)

    if placeholder:
        placeholder = tf.placeholder(tf.float64,placeholder)

    return {"sess": sess, "output_tensors": output_tensors, "input_tensor": input_tensor, "placeholder":placeholder}


model = build_model(
        model_path="frozen_inference_graph.pb",
        output_tensor_names=["detection_boxes:0", "detection_scores:0", "detection_classes:0"],
        input_tensor_name="image_tensor:0",
        placeholder=(1, None, None, 3)
        )

while(True):
    img, temp = capture(flip_v = False, device = "/dev/spidev0.1")
    print(img.shape)
    print(temp.shape)
    print('next')
    expanded = np.expand_dims(img, axis=0)
    stretched = np.repeat(expanded, 3, axis=3)
    temperatures = []
    peopleData = []

    boxes, scores, classes = list(model["sess"].run(model["output_tensors"], feed_dict={model["input_tensor"]: stretched}))
    combined = zip(np.squeeze(boxes), np.squeeze(scores), np.squeeze(classes))
    bounds = []
    try:
        boxes, scores, classes = zip(*(list(filter(lambda x: sum(x[0]) > 0 and x[2] == 1 and x[1] > .5, combined)))) 
        for box in boxes:
            bounds.append([int(box[i] * img.shape[i%2]) for i in range(len(box))])
        bounds = calc_overlap(bounds) if len(bounds) > 1 else bounds
        if bounds:
            for bound in bounds:
                color=(0,255,0) 
                cv2.rectangle(img, (bound[1],bound[0]), (bound[3],bound[2]), color=color, thickness=4)
        for bound in bounds:
            temperatures.append(temp.flatten()[0])
            temp_ = temp[bound[0]:bound[2], bound[1]:bound[3]].flatten()
            toptenpercent = np.mean(temp_[np.argsort(temp_)[-int(len(temp.flatten())*.1):]])
            calculation = (toptenpercent*0.01)-273.15
            print(calculation)
            # calculation = sum(toptenpercent)/len(toptenpercent)
            # faceAverage = sum(temp_)/len(temp_)
            # print(calculation)
            # print(faceAverage)
            time.sleep(4)
            isSick = False
            if calculation >= 38:
                isSick = True
            peopleData.append([calculation, isSick])
        
        final = {
            "CameraID":CameraID,
            "PeopleData":peopleData,
            "NumbOfPeople":len(peopleData),
        }
        if mainCollection.find_one({"CameraID":CameraID}):
            mainCollection.replace({"CameraID":CameraID}, final)
        else:
            mainCollection.insert_one(final)

        
    except (ValueError, TypeError) as e:
        print(e)
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
