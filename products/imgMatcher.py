import numpy as np
from flask import current_app
from os import path
import csv
from cv2 import BFMatcher
from .featuresext import Descriptor
from .models import Addproduct
from shop import db

class ImgMatcher:
    def __init__(self,queryImg):
        d=Descriptor((8,12,13))
        self.cQueryFeatures=d.colorDescribe(path.join(current_app.root_path,"static\\searchImages\\"+queryImg))
        self.gQueryFeatures=d.grayFeatures(path.join(current_app.root_path,"static\\searchImages\\"+queryImg))
        
    def csearch(self):
        results = {}
        products = db.session.query(Addproduct.nparr).filter().all()
        c=Descriptor((8,12,13))
        for row in products:
            features = c.colorDescribe(path.join(current_app.root_path, "static\\images\\"+row[0].split('.')[0]+'.jpg'))
            # features = np.load(path.join(current_app.root_path, "static\\cnparrs\\"+row[0]))
            d = self.chi2_distance(features, self.cQueryFeatures)
            results[row] = d
        results = list(sorted(results.items(), key = lambda x: x[1]))
        return results

    def gsearch(self):
        results = {}
        products = db.session.query(Addproduct.nparr).filter().all()
        for row in products:
            print(path.join(current_app.root_path, "static\\nparrs\\"+row[0]))
            features = np.load(path.join(current_app.root_path, "static\\nparrs\\"+row[0]))
            results[row] = self.orb_Matcher(features,self.gQueryFeatures)
        results=list(sorted(results.items(), key = lambda x: x[1], reverse = True))
        return results

    def chi2_distance(self, histA, histB, eps = 1e-10):
        d = 0.5 * np.sum([((a-b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])
        return d

    def orb_Matcher(self,des1,des2):
        bf = BFMatcher()
        goodMatches = []
        matches = bf.knnMatch(des1,des2,k=2)
        for m, n, in matches:
            if m.distance < 0.75 * n.distance: # Use 75 as a threshold defining a good match
                goodMatches.append([m])
        return len(goodMatches)