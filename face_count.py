import cv2 as cv
import dlib
'''
src=cv.imread('/home/ashik/PycharmProjects/pythonProject/count.jpg')
detector=dlib.get_frontal_face_detector()
gray=cv.cvtColor(src,cv.COLOR_BGRA2GRAY)
faces=detector(gray)
num=0
for face in faces:
    num+=1
print(num)
'''
def cnt(src):
    src = cv.imread(src)
    detector = dlib.get_frontal_face_detector()
    gray = cv.cvtColor(src, cv.COLOR_BGRA2GRAY)
    faces = detector(gray)
    num = 0
    for face in faces:
        num += 1
    return num
path='/home/ashik/PycharmProjects/pythonProject/detect.jpg'
res=cnt(path)
print(res)
