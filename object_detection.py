import cv2
import numpy as np

#Funções:

#Função para mostrar imagem na tela
def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#Função para segmentar os tons de cinza da imagem

def grayscale_17_levels(gray):
    high = 255
    while(1):
        low = high - 15
        col_to_be_changed_low = np.array([[low]])
        col_to_be_changed_high = np.array([high])
        curr_mask = cv2.inRange(gray, col_to_be_changed_low, col_to_be_changed_high)
        gray[curr_mask>0] = (high)
        high -= 15
        if (low == 0):
            break
            
#Função para encontrar o maior contorno (localizar o objeto)
def findGreatestContour(contours, image):
    width, height, _ = image.shape
    largest_area = 0
    largest_contour_index = -1
    i = 0
    total_contours = len(contours)
    while(i < total_contours):
        area = cv2.contourArea(contours[i])
        #Consertar essa gambiarra depois... width*height*0.9
        if(area > largest_area and area < width*height*0.9):
            largest_area = area
            largest_contour_index = i
        i+=1
        
    return largest_area, largest_contour_index

#Esse código serve pra homogeneizar a imagem para achar o contorno posteriormente
leaf_img = cv2.imread('/home/marcos/Documents/PIBITI/Midia/stage.png')
hsv_leaf_img = cv2.cvtColor(leaf_img, cv2.COLOR_BGR2HSV)
green_low = np.array([0,50,50])
green_high = np.array([16,255,255])
mask = cv2.inRange(hsv_leaf_img, green_low, green_high)
hsv_leaf_img[mask>0] = ([16,255,0])
viewImage(leaf_img)

#Esse código transforma a imagem pra RGB e depois pra Grayscale
leaf_rgb_again = cv2.cvtColor(hsv_leaf_img, cv2.COLOR_HSV2BGR)
leaf_gray = cv2.cvtColor(leaf_rgb_again, cv2.COLOR_BGR2GRAY)
viewImage(leaf_gray)

#Esse código encontra os contornos e aplica-os à imagem original
ret, thresh = cv2.threshold(leaf_gray, 200, 220, 0 )
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
leaf_contours = cv2.drawContours(leaf_img, contours, -1, (0,255,0), 3)
viewImage(leaf_contours)

area, index = findGreatestContour(contours, leaf_img)

contour = contours[index]

#Aqui a gente encontra os momentos do contorno (olhar documentação)
M = cv2.moments(contour)

#Não sei porque funciona, mas é assim que se acha o centro usando momento no openCV
cX = int(M["m10"]/M["m00"])
cY = int(M["m01"]/M["m00"])