# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 10:48:31 2019

@author: Patrik_Zelena
"""

import pymysql

def user_hotel_rating_connection():
    config = pymysql.connect (
            user = 'root',
           password = 'WjFB7P^M9WzaDQ8W',
           host = 'demo.database.com',
           port = 3306,
           database =  'user_hotel_rating',
            )
    a = config.cursor()
    return a, config

def hotel_data_connection():
    config = pymysql.connect (
            user = 'root',
           password = 'WjFB7P^M9WzaDQ8W',
           host = 'demo.database.com',
           port = 3307,
           database = 'hotel_data',
            )
    a = config.cursor()
    return a, config
