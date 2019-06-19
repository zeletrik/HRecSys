# -*- coding: utf-8 -*-
'''
Created on Mon Jun 17 11:34:02 2019

@author: Patrik_Zelena
'''
from DatabaseHelper import DatabaseHelper
from HotelKNNAlgorithm import HotelKNNAlgorithm
from Evaluator import Evaluator
from surprise import Dataset, Reader
import random
import numpy as np
import logging

log = logging.getLogger('RecSys.Recommender')

def LoadData():
    helper = DatabaseHelper()
    data = helper.loadDataset()
    rankings = helper.getPopularityRanks()
    return (data, rankings)

def LoadDataForLocation(lat, lon, user):
    helper = DatabaseHelper()
    data = helper.loadDatasetForLocation(lat, lon, user)
    rankings = helper.getPopularityRanks()
    return (data, rankings)

def BuildRecModel():
    np.random.seed(0)
    random.seed(0)
    
    # Load up common data set for the recommender algorithms
    (evaluationData, rankings) = LoadData()
    # Construct an Evaluator to, you know, evaluate them
    evaluator = Evaluator(evaluationData, rankings)
    
    hotelKNNAlgorithm = HotelKNNAlgorithm()
    log.info('Algorithm=K-Nearest Neighbour')
    evaluator.SetAlgorithm(hotelKNNAlgorithm, 'HotelKNNAlgorithm')
    
    evaluator.Evaluate(False)
    evaluator.TrainAndSaveAlgorithm()
    
def GetRecommendations(user, k, lat, lon):
    np.random.seed(0)
    random.seed(0)
    # Load up common data set for the recommender algorithms
    (evaluationData, rankings) = LoadDataForLocation(lat, lon, user)
    if (evaluationData.size > 100):
        # Construct an Evaluator to, you know, evaluate them
        reader = Reader(rating_scale=(0, 3))
        filteredData = Dataset.load_from_df(evaluationData, reader=reader)
        evaluator = Evaluator(filteredData, rankings)
        hotelKNNAlgorithm = HotelKNNAlgorithm()
        evaluator.SetAlgorithm(hotelKNNAlgorithm, 'HotelKNNAlgorithm')
        return evaluator.GetTopNRecs(user, k)
    else:
        log.error('Not enough hotel in range')
        return []
    
BuildRecModel()