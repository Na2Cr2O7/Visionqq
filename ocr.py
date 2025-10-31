from typing import Any, Generator
from PIL import Image, ImageDraw
import logging


logging.debug("importing easyocr")
import easyocr
import logging

logging.debug("initializing reader")
reader = easyocr.Reader(['en', 'ch_sim'])

def getAllTextWithBoxesDrawn(imagePath:str):
    im=Image.open(imagePath)
    result=reader.readtext(imagePath)
    draw0=Image.open(imagePath)
    draw: ImageDraw.ImageDraw=ImageDraw.Draw(draw0)
    
    for r in result:
        pos1,pos2,pos3,pos4=r[0] # type: ignore
        x=[pos1[0],pos2[0],pos3[0],pos4[0]]
        y=[pos1[1],pos2[1],pos3[1],pos4[1]]
        minX=int(min(x))
        maxX=int(max(x))
        minY=int(min(y))
        maxY=int(max(y))
        # print((minX,minY),(maxX,maxY))
        draw.rectangle(((minX,minY),(maxX,maxY)),outline="red")
        # print(r[1]) 
        logging.debug(f"text: {r[1]}") # type: ignore
    draw0.save(imagePath.replace(".png","_result.png"))
    
    return [r[1] for r in result]  # type: ignore
def yieldAllBBoxes(imagePath:str) -> Generator[tuple[int, int, int, int], Any, None]:
    im=Image.open(imagePath)
    result=reader.readtext(imagePath)
    for r in result:
        pos1,pos2,pos3,pos4=r[0] # type: ignore
        x=[pos1[0],pos2[0],pos3[0],pos4[0]]
        y=[pos1[1],pos2[1],pos3[1],pos4[1]]
        minX=int(min(x))
        maxX=int(max(x))
        minY=int(min(y))
        maxY=int(max(y))
        logging.debug(f"bbox: {minX,minY,maxX,maxY}")
        yield (minX,minY,maxX,maxY) 

