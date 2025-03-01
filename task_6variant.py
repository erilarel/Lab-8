import cv2

my_image = cv2.imread('images/variant-6.png')
b, g, r = cv2.split(my_image)


res = (cv2.resize(my_image, (2*my_image.shape[0], 2*my_image.shape[1]))) #Растягиваем в 2 раза по ширине и высоте
res1 = (cv2.resize(my_image, (2*my_image.shape[0], my_image.shape[1]))) #Растягиваем в 2 раза по ширине
res2 = (cv2.resize(my_image, (my_image.shape[0], 2*my_image.shape[1]))) #Растягиваем в 2 раза по высоте
cv2.imshow('Ordinary image', my_image)
cv2.imshow('Stretched in 2 times in width and height', res)
cv2.imshow('Stretched 2 times in width', res1)
cv2.imshow('Stretched 2 times in height', res2)


cv2.waitKey(0)
cv2.destroyAllWindows()
