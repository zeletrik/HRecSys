# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 10:54:52 2019

@author: Patrik_Zelena
"""
from DatabaseConnection import user_hotel_rating_connection, hotel_data_connection

from surprise import Dataset
from surprise import Reader

from collections import defaultdict
import pandas as pd
import geopy.distance

class DatabaseHelper:
    
    userRatingsDF = pd.DataFrame
    hotelDataDF = pd.DataFrame
    
    def __init__(self):
        # Read all data from user_hotel_rating db
        a, config = user_hotel_rating_connection()
        statement = 'SELECT * FROM user_hotel_rating'
        self.userRatingsDF = pd.read_sql(statement, config)
            
        # Read data from hotel_data db
        a, config = hotel_data_connection()
        statement = 'SELECT * FROM hotel_data'
        self.hotelDataDF = pd.read_sql(statement, config)

    def GetGeoLocationForHotel(self, hotel):
        is_current_hotel = self.hotelDataDF['hotel_id'] == hotel
        filered = self.hotelDataDF[is_current_hotel]
        for index, row in filered.iterrows():
             latitude = row['latitude']   
             longitude = row['longitude']
    
        return latitude, longitude
    
    def loadDataset(self):
        reader = Reader(rating_scale=(0, 3))
        return Dataset.load_from_df(self.userRatingsDF, reader=reader)
    
    
    def GetTrainSetForDistance(self, evaluationDataFrame, lat, lon):
        coords_1  = (lat, lon)
        
        for index, row in evaluationDataFrame.iterrows():
            hotelID = int(row['hotel_id'])
            latitude, longitude = self.GetGeoLocationForHotel(hotelID)
            coords_2 = (latitude, longitude)

            distance = geopy.distance.geodesic(coords_1, coords_2).km
            if distance > 30: # 30 km for now
                evaluationDataFrame.drop(index, inplace=True)
        return evaluationDataFrame
    
    def loadDatasetForLocation(self, lat, lon, user):
        already_rated = self.userRatingsDF['user_id'] == user
        not_rated_hotel = self.userRatingsDF['user_id'] != user
        userRatings = self.userRatingsDF[already_rated]
        not_rated_filtered_hotels = self.userRatingsDF[not_rated_hotel]
        
        filtered = self.GetTrainSetForDistance(not_rated_filtered_hotels, lat, lon)

        return filtered.merge(userRatings)
         

    def getUserRatings(self, user):
        userRatings = []        
        is_current_user = self.userRatingsDF['user_id'] == user
        filered = self.userRatingsDF[is_current_user]

        for index, row in filered.iterrows():
             hotelID = int(row['hotel_id'])
             rating = int(row['rating'])
             userRatings.append((hotelID, rating))
        return userRatings
    
    def getHotelGuestRatings(self):
        guestRatings = defaultdict(float)
        for index, row in self.hotelDataDF.iterrows():
             hotelID = int(row['hotel_id'])     
             guestRating = row['guestRating']
             guestRatings[hotelID] = guestRating

        return guestRatings
    
    def getHotelRatings(self):
        hotelRatings = defaultdict(float)
        for index, row in self.hotelDataDF.iterrows():
             hotelID = int(row['hotel_id'])     
             hotelRating = row['score']
             hotelRatings[hotelID] = hotelRating

        return hotelRatings
    
    def getPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        
        for index, row in self.userRatingsDF.iterrows():
            hotelID = int(row['hotel_id'])
            ratings[hotelID] += int(row['rating'])
        rank = 1
        for hotelID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[hotelID] = rank
            rank += 1
            
        return rankings
    
    def GetMultiData(self, column):
        multiDatas = defaultdict(list)
        multiDataIDs = {}
        maxMultiDataID = 0
        for index, row in self.hotelDataDF.iterrows():
            hotelID = int(row['hotel_id'])
            multiDataList = row[column].split('|')
            multiDataIDList = []
            for multiData in multiDataList:
                if multiData in multiDataIDs:
                    multiDataID = multiDataIDs[multiData]
                else:
                    multiDataID = maxMultiDataID
                    multiDataIDs[multiData] = multiDataID
                    maxMultiDataID += 1
                multiDataIDList.append(multiDataID)
            multiDatas[hotelID] = multiDataIDList
        # Convert integer-encoded lists to bitfields that we can treat as vectors
        for (hotelID, multiDataIDList) in multiDatas.items():
            bitfield = [0] * maxMultiDataID
            for multiDataID in multiDataIDList:
                bitfield[multiDataID] = 1
            multiDatas[hotelID] = bitfield            
        return multiDatas
    
    def getFoodAndDrink(self):
         return self.GetMultiData('foodAndDrink')
    def getThingsToDo(self):
         return self.GetMultiData('thingsToDo')
    def getHomeComforts(self):
         return self.GetMultiData('homeComforts')
    def getSleepWell(self):
         return self.GetMultiData('sleepWell')
    def getThingsToEnjoy(self):
         return self.GetMultiData('thingsToEnjoy')
    def getFreshenUp(self):
         return self.GetMultiData('freshenUp')
    def getBeEntertained(self):
         return self.GetMultiData('beEntertained')
    def getStayConnected(self):
         return self.GetMultiData('stayConnected')
