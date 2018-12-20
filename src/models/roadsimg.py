import uuid
from datetime import datetime

from src.common.database import Database
from bson.objectid import ObjectId


class Roadimg(object):
        def __init__(self, _id, rdcode, rdname, culv_ty_rccslab_img, culv_ty_pipe_img, culv_ty_vt_csway_img,
            culv_ty_pip_csway_img, culv_ty_hdbed_img, culv_ty_oth_img, brge_ty_oth_img, rdwidth_img):
            self._id = uuid.uuid4().hex if _id is None else _id
            self.rdcode = rdcode
            self.rdname = rdname
            self.culv_ty_rccslab_img = culv_ty_rccslab_img
            self.culv_ty_pipe_img = culv_ty_pipe_img
            self.culv_ty_vt_csway_img = culv_ty_vt_csway_img
            self.culv_ty_pip_csway_img = culv_ty_pip_csway_img
            self.culv_ty_hdbed_img = culv_ty_hdbed_img
            self.culv_ty_oth_img = culv_ty_oth_img
            self.brge_ty_oth_img = brge_ty_oth_img
            self.rdwidth_img = rdwidth_img


     def save_to_mongo(self):
        Database.insert(collection='roadimage', data=self.json())

    @classmethod
    def deletefrom_mongo(cls,_id):
        if Database.is_valid(_id):
            Database.delete_from_mongo(collection='roadimages', query={'_id': ObjectId(_id)})
        else:
            Database.delete_from_mongo(collection='roadimages', query={'_id': _id})

    @classmethod
    def update_roadimages(cls, road_id, rdcode, rdname, culv_ty_rccslab_img, culv_ty_pipe_img, culv_ty_vt_csway_img,
                     culv_ty_pip_csway_img, culv_ty_hdbed_img, culv_ty_oth_img, brge_ty_oth_img, rdwidth_img):

        if Database.is_valid(road_id):
            Database.update_roadimages(collection='roaddetails', query={'_id': ObjectId(road_id)},
                                          rdcode=rdcode, rdname=rdname, culv_ty_rccslab_img=culv_ty_rccslab_img,
                                          culv_ty_pipe_img=culv_ty_pipe_img, culv_ty_vt_csway_img=culv_ty_vt_csway_img,
                                          culv_ty_pip_csway_img=culv_ty_pip_csway_img,culv_ty_hdbed_img=culv_ty_hdbed_img,
                                          culv_ty_oth_img=culv_ty_oth_img, brge_ty_oth_img=brge_ty_oth_img, rdwidth_img=rdwidth_img)


        else:
            Database.update_roadimages(collection='roaddetails', query={'_id': road_id},
                                       rdcode=rdcode, rdname=rdname, culv_ty_rccslab_img=culv_ty_rccslab_img,
                                       culv_ty_pipe_img=culv_ty_pipe_img, culv_ty_vt_csway_img=culv_ty_vt_csway_img,
                                       culv_ty_pip_csway_img=culv_ty_pip_csway_img, culv_ty_hdbed_img=culv_ty_hdbed_img,
                                       culv_ty_oth_img=culv_ty_oth_img, brge_ty_oth_img=brge_ty_oth_img,
                                       rdwidth_img=rdwidth_img)
    def json(self):
        return {
            'Road_code': self.rdcode,
            'Road_name': self.rdname,
            'Culvert_type_rccslab_img': self.culv_ty_rccslab_img,
            'Culvert_type_pipe_img': self.culv_ty_pipe_img,
            'Culvert_type_vented_causeway_img': self.culv_ty_vt_csway_img,
            'Culvert_type_piped_causeway_img': self.culv_ty_pip_csway_img,
            'Culvert_type_hardbed_img': self.culv_ty_hdbed_img,
            'Culvert_type_other_img': self.culv_ty_oth_img,
            'Bridge_type_other_img': self.brge_ty_oth_img,
            'Road_width': self.rdwidth_img,
            '_id':self._id,
        }

    @classmethod
    def from_mongo(cls, road_id):
        roadimg = Database.find_one(collection='roadimages', query={'road_id': road_id})
        return cls(** roadimg)

    @staticmethod
    def from_mongo_blog():
        return [roadimages for roadimages in Database.find(collection='roadimages', query={})]


