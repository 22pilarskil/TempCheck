import sys
import numpy as np
import cv2
#from mtcnn import MTCNN
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

if __name__ == '__main__':
  from optparse import OptionParser

  usage = "usage: %prog [options] output_file[.format]"
  parser = OptionParser(usage=usage)

  parser.add_option("-f", "--flip-vertical",
                    action="store_true", dest="flip_v", default=False,
                    help="flip the output image vertically")

  parser.add_option("-d", "--device",
                    dest="device", default="/dev/spidev0.1",
                    help="specify the spi device node (might be /dev/spidev0.1 on a newer device)")

  (options, args) = parser.parse_args()
  while(True):
    image = capture(flip_v = options.flip_v, device = options.device)
    cv2.imwrite("image.jpg", image)
    #results = mtcnn.detect_faces(image)
    #for result in results:
      #box = result['box']
      #cv2.rectangle(image, (box[0], box[1]),(box[0]+box[2], box[1]+box[3]), color=(0, 255, 0), thickness=4)
    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
      break
