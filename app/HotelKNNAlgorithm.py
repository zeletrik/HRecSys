# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:06:59 2019

@author: Patrik_Zelena
"""

from surprise import AlgoBase
from surprise import PredictionImpossible
from DatabaseHelper import DatabaseHelper
import math
import numpy as np
import heapq
import logging

class HotelKNNAlgorithm(AlgoBase):
    log = logging.getLogger('RecSys.HotelKNNAlgorithm')
    
    def __init__(self, k=40, sim_options={}):
        AlgoBase.__init__(self)
        self.k = k

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)

        # Compute item similarity matrix based on content attributes
        # Load up vectors for every hotel
        helper = DatabaseHelper()
        guestRatings = helper.getHotelGuestRatings()
        hotelRatings = helper.getHotelRatings()
        foodAndDrinks = helper.getFoodAndDrink()
        thingsToDo = helper.getThingsToDo()
        homeComforts = helper.getHomeComforts()
        sleepWell = helper.getSleepWell()
        thingsToEnjoy = helper.getThingsToEnjoy()
        freshenUp = helper.getFreshenUp()
        beEntertained = helper.getBeEntertained()
        stayConnected = helper.getStayConnected()
        
        #Computing content-based similarity matrix
        self.similarities = np.zeros((self.trainset.n_items, self.trainset.n_items))
        for thisRating in range(self.trainset.n_items):
            if (thisRating % 100 == 0):
                self.log.debug(thisRating, ' of ', self.trainset.n_items)
            for otherRating in range(thisRating+1, self.trainset.n_items):
                thisHotelID = int(self.trainset.to_raw_iid(thisRating))
                otherHotelID = int(self.trainset.to_raw_iid(otherRating))
                foodAndDrinkSimilarity = self.computeMultiDataSimularity(thisHotelID, otherHotelID, foodAndDrinks)
                thingsToDoSimilarity = self.computeMultiDataSimularity(thisHotelID, otherHotelID, thingsToDo)
                homeComfortsSimilarity = self.computeMultiDataSimularity(thisHotelID, otherHotelID, homeComforts)
                sleepWellSimilarity = self.computeMultiDataSimularity(thisHotelID, otherHotelID, sleepWell)
                thingsToEnjoySimilarity = self.computeMultiDataSimularity(thisHotelID, otherHotelID, thingsToEnjoy)
                freshenUpSimilarity = self.computeMultiDataSimularity(thisHotelID, otherHotelID, freshenUp)
                beEntertainedSimilarity = self.computeMultiDataSimularity(thisHotelID, otherHotelID, beEntertained)
                stayConnectedSimilarity = self.computeMultiDataSimularity(thisHotelID, otherHotelID, stayConnected)
                guestRatingSimilarity = self.computeRatingSimilarity(thisHotelID, otherHotelID, guestRatings)
                hotelRatingsSimilarity = self.computeRatingSimilarity(thisHotelID, otherHotelID, hotelRatings)
                
                self.similarities[thisRating, otherRating] = foodAndDrinkSimilarity * (thingsToDoSimilarity * 1.5) * homeComfortsSimilarity * sleepWellSimilarity * thingsToEnjoySimilarity * freshenUpSimilarity * beEntertainedSimilarity * stayConnectedSimilarity * guestRatingSimilarity * hotelRatingsSimilarity  
                self.similarities[otherRating, thisRating] = self.similarities[thisRating, otherRating]
                
        return self
    
    def computeMultiDataSimularity(self, hotel1, hotel2, multiData):
        multiData1 = multiData[hotel1]
        multiData2 = multiData[hotel2]
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(multiData1)):
            x = multiData1[i]
            y = multiData2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
            
        return sumxy/math.sqrt(sumxx*sumyy)
    
    def computeRatingSimilarity(self, hotel1, hotel2, rating):
       diff = abs(rating[hotel1] - rating[hotel2])
       sim = math.exp(-diff / 10.0)
       return sim

    def estimate(self, u, i):
        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            self.log.error('User and/or item is unkown.')
            raise PredictionImpossible('User and/or item is unkown.')
        
        # Build up similarity scores between this item and everything the user rated
        neighbors = []
        for rating in self.trainset.ur[u]:
            simularity = self.similarities[i, rating[0]]
            neighbors.append((simularity, rating[1]))
        # Extract the top-K most-similar ratings
        k_neighbors = heapq.nlargest(self.k, neighbors, key=lambda t: t[0])
        
        # Compute average sim score of K neighbors weighted by user ratings
        simTotal = weightedSum = 0
        for (simScore, rating) in k_neighbors:
            if (simScore > 0):
                simTotal += simScore
                weightedSum += simScore * rating
            
        if (simTotal == 0):
            self.log.debug('No neighbors')
            raise PredictionImpossible('No neighbors')

        predictedRating = weightedSum / simTotal
        return predictedRating
    
