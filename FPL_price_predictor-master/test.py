import pickle

import requests
import pandas as pd
import PricePredictor

pp = PricePredictor.PricePredictor()
pp.fit_svm()
pp.predict_svm()
