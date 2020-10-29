import numpy as np
import cv2
from imageio import imread
import io
import base64
import random


def pairwise_dif(colors): #returns 2x the total pairwise difference between a number of colors (since the division by two is not needed for comparing)
  class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag',
                 'Ankle boot']
  if len(colors)==0: return 0
  elif len(colors)==1: return np.sum(colors[0])
  result=(0,0,0)
  for c1 in colors:
      for c2 in colors:
        if (c1==c2).all(): continue
        result = result + abs(c1-c2)
  return np.sum(result)

def detect(probability_model, b64_string):
  # USE (PREFERABLY SQUARE) IMAGES WITH SINGLE-COLOR/TRANSPARENT BACKGROUNDS, WITH FRONT-FACING CLOTHING (LEFT-FACING FOR FOOTWEAR)
  #Returns: “<name>&<b1>?<g1>?<r1>&…&<bn>?<gn>?<rn>&$”. If image has transparent background and no color was detected somehow, b,g,r will be -1,-1,-1 in output

  ###################################################################################################################
  #image_name="sn3.jpg"
  desired_bgcolor=[1,1,1] #b,g,r -- should be the same as model training images (white)
  bgmargin= 0.1           #threshold for masking out background color from the clothing item
  cmargin= 0.2            #threshold for filtering out similar colored pixels once a color has been picked
  pmargin= 0.025          #minimum percentage of image a color needs to cover to not be skipped
  colorsize= 128          #how downscaled the image will be for color detection
  color_repeat= 8        #amount of times color detection will be applied to get a better result
  ###################################################################################################################

    # reconstruct image as an numpy array
  class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag',
                 'Ankle boot']
  img = imread(io.BytesIO(base64.b64decode(b64_string)))/255
  #img = cv2.imread(image_name,cv2.IMREAD_UNCHANGED)/255
  img = img.astype("float32")
  img= cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)

  #split image
  try:
    b,g,r,a = cv2.split(img);
  except ValueError:
    a = np.full(b.shape, 1)
  img = cv2.merge((b,g,r))

  ## create background mask ##
  if(a.all()): #non transparent img
    col=len(img)
    row=len(img[0])
    topleft=img[0][0]
    topright=img[0][row-1]
    bottomleft=img[col-1][0]
    bottomright=img[col-1][row-1]
    bgcolor=(topleft+topright+bottomleft+bottomright)/4.0

    mask = np.ones(img.shape, dtype="uint8")
    mask[np.where((abs(img-bgcolor)<bgmargin))] = [0]
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

  else: #transparent img
    mask = np.ones(a.shape, dtype="uint8")
    mask[np.where((a==[0]))] = [0]
  ####

  ## color detection ##
  cmask = mask.copy()
  resizedmask = cv2.resize(cmask, (colorsize,colorsize), interpolation = cv2.INTER_AREA)
  resizedimg = cv2.resize(img, (colorsize,colorsize), interpolation = cv2.INTER_AREA)

  row=len(resizedimg)
  col=len(resizedimg[0])
  row_R=list(range(row))
  col_R=list(range(row))
  dim=row*col

  color_results=[]
  for it in range(color_repeat): #repeat the color detection to find more accurate results (choose the result with the least number of colors and highest total pairwise difference)
    clist = []
    reusablemask = resizedmask.copy()
    #random iteration for higher chance of accurate color selection
    random.shuffle(row_R)
    random.shuffle(col_R)
    for i in row_R:
      for j in col_R:
        if(reusablemask[i][j] == 0): continue
        else:
          color = resizedimg[i][j]
          colorcount = 0
          for ii in row_R:
            for jj in col_R:
              if(reusablemask[ii][jj] == 0):
                continue
              elif((abs(color - resizedimg[ii][jj]) > cmargin).any()):
                continue
              else:
                colorcount+=1
                reusablemask[ii][jj] = 0
          if(colorcount / dim < pmargin):
            continue
          clist.append(color)
    color_results.append(clist)
  if(a.all()):  #non-transparent
    if color_results==[]:
      color_results.append(bgcolor)
    img[np.where((mask==[0]))] = [bgcolor]
  else:         #transparent
    if color_results==[]:
      color_results = [np.full(desired_bgcolor.shape,-1)]
    img[np.where((a==[0]))] = desired_bgcolor
  ####

  ## object detection ##
  small = cv2.resize(img, (28,28), interpolation = cv2.INTER_AREA)

  img=cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
  img = (np.expand_dims(img,0))
  predictions_single = probability_model.predict(img)
  ####

  colors_choice = color_results[0]
  colors_count= len(color_results[0])
  colors_pairwise_difference = pairwise_dif(colors_choice)
  for colors in color_results:
    #print (colors)
    #for c in colors:
    #  te=np.full(resizedimg.shape,c)
    #  plt.imshow(cv2.cvtColor(te, cv2.COLOR_BGR2RGB))
    #  plt.show()

    cln = len(colors)
    if cln < 1: continue
    elif cln < colors_count:
      colors_count = cln
      colors_choice = colors
      #print(pwd)
      #print("---------------------")
    elif cln == colors_count:
      pwd = pairwise_dif(colors)
      #print(pwd)
      #print("---------------------")
      if pwd > colors_pairwise_difference:
        colors_pairwise_difference = pwd
        colors_choice = colors
    else: continue

  ## output ##
  out=[]
  out.append(class_names[np.argmax(predictions_single[0])])
  for c in colors_choice:
    #te=np.full(resizedimg.shape,c)
    #print(c)
    #plt.imshow(cv2.cvtColor(te, cv2.COLOR_BGR2RGB))
    #plt.show()
    out.append(c)
  return out