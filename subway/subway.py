#!/usr/bin/python3

from tkinter import *
from mta import *
from argparse import ArgumentParser
import os
import glob
import numpy as np
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from PIL import ImageDraw, ImageFont, ImageFilter
from PIL import Image

class Subway(SampleBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def run(self):
        font = graphics.Font()
        font.LoadFont("fonts/6x10.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = 0

        dir = os.path.dirname(os.path.dirname('fonts/retro.TTF'))
        

        textFont = ImageFont.truetype(os.path.join(dir, 'fonts/retro.TTF'), 8)

        bImage = Image.new("RGB", (20,11))

        draw = ImageDraw.Draw(bImage)

        draw.rectangle((0,0, 18, 12), fill='navy', outline='navy')
        draw.text((1,-1), 'B38', fill='antiquewhite', align='center')

        jImage = Image.open("icons/JThumb.png")
        cImage = Image.open("icons/CThumb.png")

        jImage.thumbnail((10,10), Image.LANCZOS)
        cImage.thumbnail((10,10), Image.LANCZOS)
                    
        
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        offscreen_canvas.SetImage(jImage.convert('RGB'), 1,1)
        offscreen_canvas.SetImage(mImage.convert('RGB'),1,12)
        offscreen_canvas.SetImage(bImage, 0, 23)

        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        print("running subway")

        
        while True:
            tTimes = getTrainTimes("M11N","A49N")
            jTimes = (', ').join(str(time) for time in tTimes["JS"][:2])
            cTimes = (', ').join(str(time) for time in tTimes["CN"][:2])
            b26Times = (', ').join(str(time) for time in tTimes["B26"][:2])

            textTimes = Image.new("RGB", (43, 32))

            draw = ImageDraw.Draw(textTimes)

            draw.text((43,2), jTimes + ' min', font=textFont, fill='yellowgreen', anchor='ra', align='right')
            draw.text((43,13), cTimes + ' min', font=textFont, fill='yellowgreen', anchor='ra',align='right')
            draw.text((43,24), b38Times + ' min', font=textFont, fill='yellowgreen', anchor='ra',align='right')

            offscreen_canvas.Clear()
            offscreen_canvas.SetImage(jImage.convert('RGB'), 1,1)
            offscreen_canvas.SetImage(mImage.convert('RGB'),1,12)
            offscreen_canvas.SetImage(bImage, 0,23)
            offscreen_canvas.SetImage(textTimes,21,0)

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(5)
        

if __name__ == '__main__':
    while True:
        Subway().process()



