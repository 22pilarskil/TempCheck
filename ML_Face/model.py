import tensorflow as tf 
import numpy as np 
import cv2
import os

import sys
from pylepton.Lepton3 import Lepton3

#mtcnn = MTCNN()

def capture(flip_v = False, device = "/dev/spidev0.1"):
  with Lepton3(device) as l:
    a,_ = l.capture()
  if flip_v:
    cv2.flip(a,0,a)
  cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
  np.right_shift(a, 8, a)
  return np.uint8(a)

os.system("sh model_download.sh")

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
    image = capture(flip_v = False, device = "/dev/spidev0.1")
    expanded = np.expand_dims(img, axis=0)

    boxes, scores, classes = list(model["sess"].run(model["output_tensors"], feed_dict={model["input_tensor"]: expanded}))
    combined = zip(np.squeeze(boxes), np.squeeze(scores), np.squeeze(classes))
    bounds = []
    boxes, scores, classes = zip(*(list(filter(lambda x: sum(x[0]) > 0 and x[2] == 1 and x[1] > .5, combined)))) 
    for box in boxes:
        bounds.append([int(box[i] * img.shape[i%2]) for i in range(len(box))])

    for bound in bounds:
        color=(0,255,0) 
        cv2.rectangle(img, (bound[1],bound[0]), (bound[3],bound[2]), color=color, thickness=4)
        #results = mtcnn.detect_faces(image)
        #for result in results:
      #box = result['box']
      #cv2.rectangle(image, (box[0], box[1]),(box[0]+box[2], box[1]+box[3]), color=(0, 255, 0), thickness=4)
    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
      break
