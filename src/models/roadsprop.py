import uuid
import datetime
from src.common.database import Database

from bson.objectid import ObjectId


class Roadpara(object):

    def __init__(self,  rd_code, rd_name, block, culvert_type, last_upd_date=datetime.datetime.utcnow(), _id=None,
                 culvert_chain=None, culvert_width=None, culvert_number=None):

            self._id = uuid.uuid4().hex if _id is None else _id
            self.rd_code = rd_code
            self.rd_name = rd_name
            self.block = block
            self.last_upd_date = last_upd_date
            self.culvert_type = culvert_type
            self.culvert_chain = culvert_chain
            self.culvert_width = culvert_width
            self.culvert_number = culvert_number

    def save_to_road_det(self):
        Database.insert(collection='road_details', data=self.json())

    @classmethod
    def delete_from_road_det(cls, _id):
        if Database.is_valid(_id):
            Database.delete_from_mongo(collection='road_details', query={'_id': ObjectId(_id)})
        else:
            Database.delete_from_mongo(collection='road_details', query={'_id': _id})

    @classmethod
    def update_road_para(cls, rds_id, rd_code, rd_name, block, culvert_type, culvert_chain, culvert_width,
                         culvert_number):

        if Database.is_valid(rds_id):
            Database.update_road_para(collection='road_details', query={'_id': ObjectId(rds_id)}, rd_code=rd_code,
                                      rd_name=rd_name, block=block,  culvert_type=culvert_type,
                                      culvert_chain=culvert_chain, culvert_width=culvert_width,
                                      culvert_number=culvert_number)
        else:
            Database.update_road_para(collection='road_details', query={'_id': rds_id}, rd_code=rd_code,
                                      rd_name=rd_name, block=block,culvert_type=culvert_type, culvert_chain=culvert_chain,
                                      culvert_width=culvert_width, culvert_number=culvert_number)

    def json(self):
        return {
            'Road_code': self.rd_code,
            'Road_name': self.rd_name,
            'Block': self.block,
            'Culvert_type': self.culvert_type,
            'Culvert_chain': self.culvert_chain,
            'Culvert_width': self.culvert_width,
            'Culvert_number': self.culvert_number,
            '_id': self._id
                }

    @classmethod
    def from_road_prop(cls, _id):
        road_para = Database.find_one(collection='road_details', query={'_id': _id})
        return cls(** road_para)

    @classmethod
    def update_name(cls, rd_code, rd_name):
        Database.update_road_name(collection='road_details', query={'Road_code': rd_code}, rd_name=rd_name)


    @staticmethod
    def from_road_query_prop():
        return [roaddetails for roaddetails in Database.find(collection='road_details', query={})]



