# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 18:16:02 2016

@author: Luc
"""

import json
import StringIO
from PIL import Image


from watson_developer_cloud import VisualRecognitionV3 as VisualRecognition

test_url = 'https://www.ibm.com/ibm/ginni/images/ginni_bio_780x981_v4_03162016.jpg'



with open('bril.jpg', 'rb') as img:
	print(json.dumps(visual_recognition.classify(img), indent=2))
#width = img.size[0]*0.8
#height = img.size[1]*0.8

#img = img.resize(())





