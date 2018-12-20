import uuid
import datetime
from src.common.database import Database
from bson.objectid import ObjectId


class Road(object):

    def __init__(self, block, rd_code, rd_name, rd_cat, hab_name, bus_rut_num, mgn_yn,
                 pm_rout_code, hill_yn, last_upd_date=datetime.datetime.utcnow(), rd_width=None,
                 rd_ty_earth=None, rd_ty_gravel=None, rd_ty_wbm2=None, _id=None, rd_ty_wbm3=None, rd_ty_bt=None,
                 rd_ty_cc=None, rd_length=None, last_upd_yr=None):

        self._id = uuid.uuid4().hex if _id is None else _id
        self.block = block
        self.rd_code = rd_code
        self.rd_name = rd_name
        self.rd_cat = rd_cat
        self.hab_name = hab_name
        self.bus_rut_num = bus_rut_num
        self.mgn_yn = mgn_yn
        self.hill_yn = hill_yn
        self.pm_rout_code = pm_rout_code
        self.last_upd_date = last_upd_date
        self.rd_width = rd_width
        self.rd_ty_earth = rd_ty_earth
        self.rd_ty_gravel = rd_ty_gravel
        self.rd_ty_wbm2 = rd_ty_wbm2
        self.rd_ty_wbm3 = rd_ty_wbm3
        self.rd_ty_bt = rd_ty_bt
        self.rd_ty_cc = rd_ty_cc
        self.rd_length = rd_length
        self.last_upd_yr = last_upd_yr

    @classmethod
    def delete_from_road(cls, _id):
        if Database.is_valid(_id):
            Database.delete_from_mongo(collection='roads', query={'_id': ObjectId(_id)})
        else:
            Database.delete_from_mongo(collection='roads', query={'_id': _id})

    @classmethod
    def update_roads(cls, block, rds_id, rd_code, rd_name, rd_cat, hab_name, bus_rut_num, mgn_yn, pm_rout_code, hill_yn,
                     rd_width, rd_ty_earth, rd_ty_gravel, rd_ty_wbm2, rd_ty_wbm3, rd_ty_bt,
                     rd_ty_cc, rd_length, last_upd_yr):

        if Database.is_valid(rds_id):
            Database.update_roads(collection='roads', query={'_id': ObjectId(rds_id)}, block=block, rd_code=rd_code,
                                  rd_name=rd_name, rd_cat=rd_cat, hab_name=hab_name, bus_rut_num=bus_rut_num,
                                  mgn_yn=mgn_yn, pm_rout_code=pm_rout_code,
                                  hill_yn=hill_yn, rd_width=rd_width, rd_ty_earth=rd_ty_earth,
                                  rd_ty_gravel=rd_ty_gravel, rd_ty_wbm2=rd_ty_wbm2, rd_ty_wbm3=rd_ty_wbm3,
                                  rd_ty_bt=rd_ty_bt, rd_ty_cc=rd_ty_cc, rd_length=rd_length, last_upd_yr=last_upd_yr,
                                  last_upd_date=datetime.datetime.now())
        else:
            Database.update_roads(collection='roads', query={'_id': rds_id}, block=block, rd_code=rd_code,
                                  rd_name=rd_name, rd_cat=rd_cat, hab_name=hab_name, bus_rut_num=bus_rut_num,
                                  mgn_yn=mgn_yn, pm_rout_code=pm_rout_code,
                                  hill_yn=hill_yn, rd_width=rd_width, rd_ty_earth=rd_ty_earth,
                                  rd_ty_gravel=rd_ty_gravel, rd_ty_wbm2=rd_ty_wbm2, rd_ty_wbm3=rd_ty_wbm3,
                                  rd_ty_bt=rd_ty_bt, rd_ty_cc=rd_ty_cc,  rd_length=rd_length, last_upd_yr=last_upd_yr,
                                  last_upd_date=datetime.datetime.now())

    def json(self):
        return {
            'Road_code': self.rd_code,
            'Road_name': self.rd_name,
            'Category_of_road': self.rd_cat,
            'Block': self.block,
            'Road_width': self.rd_width,
            'Road_type_earth': self.rd_ty_earth,
            'Road_type_gravel': self.rd_ty_gravel,
            'Road_type_wbII': self.rd_ty_wbm2,
            'Road_type_wbIII': self.rd_ty_wbm3,
            'Road_type_bt': self.rd_ty_bt,
            'Road_type_cc': self.rd_ty_cc,
            'Road_length': self.rd_length,
            'Last_upgrade_yr': self.last_upd_yr,
            'Bus_ply_route_num': self.bus_rut_num,
            'Hill_road_yn': self.hill_yn,
            'MGNRGES_yn': self.mgn_yn,
            'PMGSY_thro_lnk_rout_code': self.pm_rout_code,
            'Habit_name' : self.hab_name,
            'Last_update_date': self.last_upd_date,
            '_id': self._id
                }

    def save_to_road(self):
        Database.insert(collection='roads', data=self.json())

    @classmethod
    def from_road(cls, _id):
        road_data = Database.find_one(collection='roads', query={'_id': _id})
        return cls(**road_data)

    @classmethod
    def get_road_code(cls, rd_code):
        road_data = Database.find_one(collection='roads', query={'Road_code': rd_code})
        if road_data is not None:
            return cls(**road_data)


    @staticmethod
    def from_road_blog():
        return [road for road in Database.find(collection='roads', query={})]





