import face_recognition as fc
import cv2 as cv
img=fc.load_image_file('Images/abc.jpg')
img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
encodings=fc.face_encodings(img)

img1=fc.load_image_file('Images/Bharti_Singh.jpg')
img1=cv.cvtColor(img1,cv.COLOR_BGR2RGB)
unknown=fc.face_encodings(img)[0]

result=fc.compare_faces([encodings],unknown)
print(result)
#face_location=fc.face_landmarks(img)
#print(face_location)
cv.imshow('Image',img)
cv.waitKey(0)