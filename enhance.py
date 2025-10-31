from PIL import Image, ImageMorph
import numpy as np
from typing import Any, Literal


def binarize(img, threshold: Any ='auto'):
    """
    Binarize the image using the given threshold.
    """
    if type(img) == str:
        img = Image.open(img)
    img = img.convert('L')
    img = np.array(img)
    if threshold=='auto':
        threshold = np.median(img)
    img[img < threshold] = 0
    img[img >= threshold] = 255
    return  Image.fromarray(img)
def dilate(img, size: int = 4):
    """
    Dilate the image using the given size.
    """
    if type(img) == str:
        img = Image.open(img)
    img = img.convert('L')
    # img = np.array(img)
    morph=ImageMorph.MorphOp(op_name='dilation'+str(size))
    _,img=morph.apply(img)


    return img
def erode(img, size: int = 4):
    """
    Erode the image using the given size.
    """
    if type(img) == str:
        img = Image.open(img)
    img = img.convert('L')
    # img = np.array(img)
    morph=ImageMorph.MorphOp(op_name='erosion'+str(size))
    _,img=morph.apply(img)

    return img
def extractGradient(img,gradient=120,gradientRange=30):
    """
    Extract the gradient of the image using the given gradient value.
    """
    if type(img) == str:
        img = Image.open(img)
    img = img.convert('RGB')
    size=img.size
    
    gradientRange=[(i,i,i) for i in range(gradient-gradientRange,gradient+gradientRange+1)]
    newImage=Image.new('L',size)
    for x in range(size[0]):
        for y in range(size[1]):
            # print(img.getpixel((x,y)))
            if img.getpixel((x,y)) in gradientRange:
                newImage.putpixel((x,y),0)
            else:
                newImage.putpixel((x,y),255)
    return newImage

# if __name__ == '__main__':
#     img='conversation.png'
#     img = binarize(img,100)
#     img.save('binarized.png')
#     img = dilate(erode(img,8))
#     img.save('processed.png')
#     img = extractGradient('conversation.png',161)
#     img.save('gradient.png')

def getConversation(img) -> Literal['Extractedconversation.png']:
    """
    Extract the conversation part of the image.
    """
    if type(img) == str:
        img = Image.open(img)
    img = binarize(img,140)
    img.save('Extractedconversation.png')
    return 'Extractedconversation.png'

def getNames(img) -> Literal['Extractedgradient.png']:
    """
    Extract the names of the people in the image.
    """
    if type(img) == str:
        img = Image.open(img)
    
    img = extractGradient(img,161,10)
    img.save('Extractedgradient.png')
    return 'Extractedgradient.png'

if __name__ == '__main__':
    img='conversation.png'
    getConversation(img)
    getNames(img)