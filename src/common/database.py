import os

import pymongo
from bson import ObjectId
from bson.errors import InvalidId


class Database(object):
    URI = os.environ['MONGODB_URI']
    DATABASE = None

    @staticmethod
    def initialize():
       client = pymongo.MongoClient(Database.URI)
       Database.DATABASE = client['heroku_dl5cdgz5']

    #URI = "mongodb://127.0.0.1:27017"
    #DATABASE = None

    #@staticmethod
    #def initialize():
    #     client = pymongo.MongoClient(Database.URI)
    #     Database.DATABASE = client['RMI']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def is_valid(oid):
        try:
            ObjectId(oid)
            return True
        except (InvalidId, TypeError):
            return False

    @staticmethod
    def update_roads(collection, query, block, rd_code, rd_name, rd_cat, rd_width, hab_name, bus_rut_num,
                     mgn_yn, pm_rout_code, hill_yn, rd_ty_earth, rd_ty_gravel, rd_ty_wbm2, rd_ty_wbm3,
                     rd_ty_bt, rd_ty_cc, rd_length, last_upd_yr, last_upd_date):

        return Database.DATABASE[collection].update_one(query, {'$set': {'Road_code': rd_code,
                                                                         'Road_name': rd_name,
                                                                         'Category_of_road': rd_cat,
                                                                         'Block': block,
                                                                         'Road_width': rd_width,
                                                                         'Road_type_earth': rd_ty_earth,
                                                                         'Road_type_gravel': rd_ty_gravel,
                                                                         'Road_type_wbmII': rd_ty_wbm2,
                                                                         'Road_type_wbmIII': rd_ty_wbm3,
                                                                         'Road_type_bt': rd_ty_bt,
                                                                         'Road_type_cc': rd_ty_cc,
                                                                         'Road_length': rd_length,
                                                                         'Last_upd_date': last_upd_date,
                                                                         'Bus_ply_route_num': bus_rut_num,
                                                                         'Hill_road_yn': hill_yn,
                                                                         'MGNRGES_yn': mgn_yn,
                                                                         'PMGSY_thro_lnk_rout_code': pm_rout_code,
                                                                         'Habit_name': hab_name,
                                                                         'Last_upgrade_yr': last_upd_yr}}, True)

    @staticmethod
    def update_road_name(collection, query, rd_name):
        return Database.DATABASE[collection].update_one(query, {'$set': {'Road_name': rd_name}}, False)

    @staticmethod
    def update_road_para(collection, query, rd_code, rd_name, block, culvert_type, culvert_chain, culvert_width,
                         culvert_number):

        return Database.DATABASE[collection].update_one(query, {'$set': {'Road_code': rd_code,
                                                                         'Road_name': rd_name,
                                                                         'Block': block,
                                                                         'Culvert_type': culvert_type,
                                                                         'Culvert_chain': culvert_chain,
                                                                         'Culvert_number': culvert_number,
                                                                         'Culvert_width': culvert_width}}, True)

    @staticmethod
    def change_password(collection, query, password):
        return Database.DATABASE[collection].update_one(query, {'$set': {'password': password}}, True)

    @staticmethod
    def delete_from_mongo(collection, query):
        print(query)
        Database.DATABASE[collection].remove(query)


