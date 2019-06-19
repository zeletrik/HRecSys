# -*- coding: utf-8 -*-
'''
Created on Mon Jun 17 11:38:06 2019

@author: Patrik_Zelena
'''
from EvaluationData import EvaluationData
from EvaluatedAlgorithm import EvaluatedAlgorithm
import joblib 
from HotelKNNAlgorithm import HotelKNNAlgorithm
import logging

class Evaluator:
    
    log = logging.getLogger('RecSys.Evaluator')
    hotelKNNAlgorithm = HotelKNNAlgorithm()
    algorithm = EvaluatedAlgorithm(hotelKNNAlgorithm, 'HotelKNNAlgorithm')
    
    def __init__(self, dataset, rankings):
        ed = EvaluationData(dataset, rankings)
        self.dataset = ed
        
    def SetAlgorithm(self, algorithm, name):
        self.algorithm = EvaluatedAlgorithm(algorithm, name)
        
    def Evaluate(self, doTopN):
        results = {}
        self.log.info('Evaluating algorithm={}'.format(self.algorithm.GetName()))
        results[self.algorithm.GetName()] = self.algorithm.Evaluate(self.dataset, doTopN)
        if (doTopN):
             self.log.info('{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}'.format(
                    'Algorithm', 'RMSE', 'MAE', 'HR', 'cHR', 'ARHR', 'Coverage', 'Diversity', 'Novelty'))
             for (name, metrics) in results.items():
                 self.log.info('{:<10} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f}'.format(
                        name, metrics['RMSE'], metrics['MAE'], metrics['HR'], metrics['cHR'], metrics['ARHR'],
                                      metrics['Coverage'], metrics['Diversity'], metrics['Novelty']))
        else:
            self.log.info('{:<10} {:<10} {:<10}'.format('Algorithm', 'RMSE', 'MAE'))
            for (name, metrics) in results.items():
                 self.log.info('{:<10} {:<10.4f} {:<10.4f}'.format(name, metrics['RMSE'], metrics['MAE']))
            
    def TrainAndSaveAlgorithm(self):
        trainSet = self.dataset.GetFullTrainSet()
        algo = self.algorithm.GetAlgorithm();
        self.log.info('\nBuilding recommendation model using recommender={}'.format(self.algorithm.GetName()))
        algo.fit(trainSet)
        joblib.dump(algo, 'hotels_knn.pkl')            
        self.log.info('Retrain completed!')
    def GetTopNRecs(self, testSubject, k):        
        # Load the model from the file 
        knn_from_joblib = joblib.load('hotels_knn.pkl')  
  
        # Use the loaded model to make predictions         
        testSet = self.dataset.GetAntiTestSetForUser(testSubject)
    
        predictions = knn_from_joblib.test(testSet) 
                
        recommendations = []
        
        for userID, hotelID, actualRating, estimatedRating, _ in predictions:
            intHotelID = int(hotelID)
            recommendations.append((intHotelID, estimatedRating))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        result = []
        for ratings in recommendations[:k]:
            result.append(ratings[0])
            
        return result
                