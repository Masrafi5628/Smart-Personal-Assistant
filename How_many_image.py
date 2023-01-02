import cv2 as cv
import dlib

def count_image(src):
    src=cv.imread(src)
    detector=dlib.get_frontal_face_detector()
    gray=cv.cvtColor(src,cv.COLOR_BGRA2GRAY)
    faces=detector(gray)
    num=0
    for face in faces:
        num+=1
    return  num