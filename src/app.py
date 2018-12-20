import codecs
import json
import os

import exifread as ef
import gridfs
import pymongo
from bson import json_util
from bson.objectid import ObjectId
from flask import Flask, render_template, request, session

from src.common.database import Database
from src.models.roads import Road
from src.models.roadsprop import Roadpara
from src.models.user import User

app = Flask(__name__)  #main
app.secret_key = "commercial"


@app.route('/')
def home():
    return render_template('home.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/change_password/<string:_id>', methods=['POST', 'GET'])
def change_password(_id):
    user = User.get_by_id(_id)
    if request.method == 'GET':
        return render_template('update_password.html', user=user)
    else:
        old_password = request.form['oldPassword']
        newPassword = request.form['newPassword']
        newPasswordAgain = request.form['newPasswordAgain']

    if user.password == old_password:
        if newPassword == newPasswordAgain:
            User.change_password(user._id, new_password=newPassword)
            return render_template('passwords_changed.html', user=user)
        else:
            return render_template('passwords_dont_match.html', user=user)
    else:
        return render_template('passwords_dont_match.html', user=user)


@app.route('/login')
def login_form():
    return render_template('login.html')


@app.route('/register')
def register_form():
    return render_template('register.html')


@app.route('/authorize/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    valid = User.valid_login(email, password)
    User.login(email)
    user = User.get_by_email(email)

    if valid:
        if user.designation == "HQ":
            return render_template('profile_admin.html', user=user)

        else:
            return render_template('profile.html', user=user)

    else:
        return render_template('login_fail.html')


@app.route('/authorize/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']
    designation= request.form['designation']
    block = request.form['block']
    User.register(email, password, username, designation, block)

    user = User.get_by_email(email)

    return render_template('profile.html', user=user)


@app.route('/profile_landing')
def profileLanding():
    email = session['email']
    if email is not None:
        user = User.get_by_email(email)
        if user.designation == "Admin":
            return render_template('profile_admin.html', user=user)
        else:
            return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    email = session['email']
    if email is not None:
        session['email'] = None
    return render_template('home.html')


@app.route('/road/new', methods=['POST','GET'])
def create_new_road():
    email = session['email']
    if email is not None:
        if request.method == 'GET':
            user = User.get_by_email(email)
            if user.block == "ALL":
                return render_template('road_new.html', block=user.block)
            else:
                return render_template('road_new_block.html', block=user.block)
        else:
            block = request.form['block']
            rd_code = request.form['rd_code']
            rd_name = request.form['rd_name']
            rd_cat = request.form['rd_cat']
            rd_width = request.form['rd_width']
            rd_ty_earth = request.form['rd_ty_earth']
            rd_ty_gravel = request.form['rd_ty_gravel']
            rd_ty_wb2 = request.form['rd_ty_wb2']
            rd_ty_wb3 = request.form['rd_ty_wb3']
            rd_ty_bt = request.form['rd_ty_bt']
            rd_ty_cc = request.form['rd_ty_cc']
            rd_length = request.form['rd_length']
            last_upd_yr = request.form['last_upd_yr']
            bus_rut_num = request.form['bus_rut_num']
            pm_rout_code = request.form['pm_rout_code']
            mgn_yn = request.form['mgn_yn']
            hill_yn = request.form['hill_yn']
            hab_name = request.form['hab_name']

            roads = Road(block=block, rd_code=rd_code, rd_name=rd_name, rd_cat=rd_cat, rd_width=rd_width,
                         rd_ty_earth=rd_ty_earth, rd_ty_gravel=rd_ty_gravel, rd_ty_wbm2=rd_ty_wb2, rd_ty_wbm3=rd_ty_wb3,
                         rd_ty_bt=rd_ty_bt, rd_ty_cc=rd_ty_cc, rd_length=rd_length, last_upd_yr=last_upd_yr,
                         bus_rut_num=bus_rut_num, hill_yn=hill_yn, mgn_yn=mgn_yn, pm_rout_code=pm_rout_code,
                         hab_name=hab_name)
            roads.save_to_road()
            return render_template('record_saved.html', roads=roads)
    else:
        return render_template('login_fail.html')


@app.route('/roads_update/')
def render_roads_update():
    email = session['email']
    if email is not None:
        user = User.get_by_email(email)
        if user.block == "ALL":
            return render_template('view_roads_all.html', block=user.block)
        else:
            return render_template('view_roads_block.html', block=user.block)
    else:
        return render_template('login_fail.html')


@app.route('/road/new/update/<string:_id>', methods=['POST', 'GET'])
def road_update(_id):
    if request.method == 'GET':
        return render_template('road_update.html', rds_id=_id)
    else:
        block = request.form['block']
        rd_code = request.form['rd_code']
        rd_name = request.form['rd_name']
        rd_cat = request.form['rd_cat']
        rd_width = request.form['rd_width']
        rd_ty_earth = request.form['rd_ty_earth']
        rd_ty_gravel = request.form['rd_ty_gravel']
        rd_ty_wb2 = request.form['rd_ty_wb2']
        rd_ty_wb3 = request.form['rd_ty_wb3']
        rd_ty_bt = request.form['rd_ty_bt']
        rd_ty_cc = request.form['rd_ty_cc']
        rd_length = request.form['rd_length']
        last_upd_yr = request.form['last_upd_yr']
        bus_rut_num = request.form['bus_rut_num']
        pm_rout_code = request.form['pm_rout_code']
        mgn_yn = request.form['mgn_yn']
        hill_yn = request.form['hill_yn']
        hab_name = request.form['hab_name']

    roads = Road(block=block,  rd_code=rd_code, rd_name=rd_name, rd_cat=rd_cat, rd_width=rd_width,
                 rd_ty_earth=rd_ty_earth, rd_ty_gravel=rd_ty_gravel, rd_ty_wbm2=rd_ty_wb2, rd_ty_wbm3=rd_ty_wb3,
                 rd_ty_bt=rd_ty_bt, rd_ty_cc=rd_ty_cc, rd_length=rd_length, last_upd_yr=last_upd_yr,
                 bus_rut_num=bus_rut_num, hill_yn=hill_yn,  mgn_yn=mgn_yn, pm_rout_code=pm_rout_code, hab_name=hab_name)

    roads.update_roads(rds_id=_id, block=block, rd_code=rd_code, rd_name=rd_name, rd_cat=rd_cat, rd_width=rd_width,
                       rd_ty_earth=rd_ty_earth, rd_ty_gravel=rd_ty_gravel, rd_ty_wbm2=rd_ty_wb2, rd_ty_wbm3=rd_ty_wb3,
                       rd_ty_bt=rd_ty_bt, rd_ty_cc=rd_ty_cc, rd_length=rd_length, last_upd_yr=last_upd_yr,
                       bus_rut_num=bus_rut_num, hill_yn=hill_yn, mgn_yn=mgn_yn, pm_rout_code=pm_rout_code,
                       hab_name=hab_name)

    Roadpara.update_name(rd_code=rd_code, rd_name=rd_name)

 #   URI = "mongodb://127.0.0.1:27017"
 #   client = pymongo.MongoClient(URI)
 #   DATABASE = client['RMI']

 #   DATABASE['road_images'].update_many({'road_code': rd_code}, {'$set': {'road_name': rd_name}}, False)

    return render_template('record_saved.html', roads=roads)


@app.route('/roads_table/')
def road_data():
    roads = Database.find("roads", query={})
    json_roads = []
    for road in roads:
        json_roads.append(road)
    all_road = json.dumps(json_roads, default=json_util.default)
    return all_road


@app.route('/road_block_table/<string:Block>')
def render_block_roads(Block):
    block_roads_array = []
    block_roads_dict = Database.find("roads", {'Block': Block})
    for road in block_roads_dict:
        block_roads_array.append(road)

    all_roads_block = json.dumps(block_roads_array, default=json_util.default)

    return all_roads_block


@app.route('/road_para_block_table/<string:Block>')
def render_block_roads_para(Block):
    block_roads_array = []
    block_roads_dict = Database.find("road_details", {'Block': Block})
    for road in block_roads_dict:
        block_roads_array.append(road)

    all_roads_para_block = json.dumps(block_roads_array, default=json_util.default)

    return all_roads_para_block


@app.route('/road_display/<string:_id>')
def render_individual_road(_id):
        single_road_array = []
        if Database.is_valid(_id):
            single_road_dict = Database.find("roads", {'_id': ObjectId(_id)})
        else:
            single_road_dict = Database.find("roads", {'_id': _id})

        for Rds in single_road_dict:
            single_road_array.append(Rds)

        single_road_block = json.dumps(single_road_array, default=json_util.default)

        return single_road_block


@app.route('/roads_prop_new/')
def render_roads_prop():
    email = session['email']
    if email is not None:
        user = User.get_by_email(email)
        if user.block == "ALL":
                return render_template('new_prop_add.html', block=user.block)
        else:
                return render_template('new_prop_add_block.html', block=user.block)
    else:
        return render_template('login_fail.html')


@app.route('/roads_para_table/')
def road_para_data():
    roads = Database.find("road_details", query={})
    json_roads = []
    for road in roads:
        json_roads.append(road)
    all_road_para = json.dumps(json_roads, default=json_util.default)
    return all_road_para


@app.route('/roads_para_update/')
def roads_para_update():
    email = session['email']
    if email is not None:
        user = User.get_by_email(email)
        if user.block == "ALL":
                return render_template('view_road_properties_all.html', block=user.block)
        else:
                return render_template('view_road_properties_block.html', block=user.block)
    else:
        return render_template('login_fail.html')


@app.route('/road/prop/<string:_id>', methods=['POST', 'GET'])
def create_road_prop(_id):
    if request.method == 'GET':
        return render_template('road_new_properties.html', rds_id=_id)
    else:
        rd_code = request.form['rd_code']
        rd_name = request.form['rd_name']
        block = request.form['block']
        culvert_number = request.form['member']

        for i in range(int(culvert_number)):
            ctype = "culvert_type" + str(i)
            cchain = "culvert_chain" + str(i)
            cwidth = "culvert_width" + str(i)

            culvert_type = request.form[ctype]
            culvert_chain = request.form[cchain]
            culvert_width = request.form[cwidth]

            road_para = Roadpara(rd_code=rd_code, rd_name=rd_name, block=block, culvert_type=culvert_type,
                                 culvert_chain=culvert_chain, culvert_width=culvert_width,
                                 culvert_number=culvert_number)

            road_para.save_to_road_det()

        return render_template('record_saved.html')


@app.route('/road/prop/update/<string:_id>', methods=['POST', 'GET'])
def road_prop_update(_id):
    if request.method == 'GET':
        return render_template('road_properties_update.html', rds_id=_id)
    else:
        rd_code = request.form['rd_code']
        rd_name = request.form['rd_name']
        block = request.form['block']
        culvert_type = request.form['culvert_type']
        culvert_chain = request.form['culvert_chain']
        culvert_width = request.form['culvert_width']
        culvert_number = request.form['culvert_number']

        road_para_upd = Roadpara(rd_code=rd_code, block=block, rd_name=rd_name, culvert_type=culvert_type,
                                 culvert_chain=culvert_chain, culvert_width=culvert_width,
                                 culvert_number=culvert_number)

        road_para_upd.update_road_para(rd_code=rd_code, rd_name=rd_name, block=block, culvert_type=culvert_type,
                                       culvert_chain=culvert_chain, culvert_width=culvert_width,
                                       culvert_number=culvert_number, rds_id=_id)

        return render_template('record_saved.html', road_para_upd=road_para_upd)


@app.route('/roads_image_new/')
def render_roads_img():
    email = session['email']
    if email is not None:
        user = User.get_by_email(email)
        if user.block == "ALL":
            return render_template('new_image_add.html', block=user.block)
        else:
            return render_template('new_image_add_block.html', block=user.block)
    else:
        return render_template('login_fail.html')


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


def getGPS(f):
 #       global lng_value
        tags = ef.process_file(f)
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')
        altitude = tags.get('GPS GPSAltitude')
        date_taken = tags.get('EXIF DateTimeOriginal')

        if latitude:
            lat_value = _convert_to_degress(latitude)
            if latitude_ref.values != 'N':
                lat_value = -lat_value
        else:
            lat_value = None
        if longitude:
            lng_value = _convert_to_degress(longitude)
            if longitude_ref.values != 'E':
                lng_value = -lng_value
        else:
            lng_value = None
        return {'latitude': lat_value, 'longitude': lng_value, "altitude": altitude, "date_taken": date_taken}


@app.route('/road/image/<string:_id>', methods=['POST', 'GET'])
def store_road_image(_id):
    if request.method == 'GET':
        return render_template('road_new_image.html', rds_id=_id)
    else:
        rd_code = request.form['rd_code']
        rd_name = request.form['rd_name']
        block = request.form['block']
        category = request.form['category']
        sub_category = request.form['subcategory']
        culvert_chain = request.form['culvert_chain']
        upload_by = request.form['upload_by']
        inspect_by = request.form['inspect_by']
        rd_ins_desc = request.form['rd_ins_desc']

        for file, file1 in zip(request.files.getlist("Image_upload"), request.files.getlist("Image_upload2")):

            gps = getGPS(file1)
            if gps['longitude'] is not None:
                lat = gps['longitude']
                lon = gps['latitude']
                alt = gps['altitude']
                img_date = gps['date_taken']

                filename = file.filename
#                URI = "mongodb://127.0.0.1:27017"
#                client = pymongo.MongoClient(URI)
#                DATABASE = client['RMI']

                URI = os.environ['MONGODB_URI']
                client = pymongo.MongoClient(URI)
                DATABASE = client['heroku_dl5cdgz5']

                fs = gridfs.GridFS(DATABASE)

                #            print(file)
                fileid = fs.put(file, filename=filename)
                #            fileid = fs.put(request.files['Image_upload'].read(), filename=filename)

                DATABASE['road_images'].insert_one({"Image_upload": filename, "fileid": fileid, "road_code": rd_code,
                                                    "road_name": rd_name, "block": block, "sub_category": sub_category,
                                                    "culvert_chain": culvert_chain, "category": category,
                                                    "rd_ins_desc": rd_ins_desc, "inspect_by": inspect_by,
                                                    "upload_by": upload_by,
                                                    "longitude": str(lon), "latitude": str(lat), "altitude": str(alt),
                                                    'Image_date': str(img_date)})
            else:
                return render_template('record_failed.html')
        return render_template('record_saved.html')


@app.route('/roads_image_table/')
def road_image_data():
    URI = "mongodb://127.0.0.1:27017"
    client = pymongo.MongoClient(URI)
    DATABASE = client['RMI']
    roads_image = DATABASE['road_images'].find({})
    json_roads = []
    for road in roads_image:
        json_roads.append(road)
    all_road_img = json.dumps(json_roads, default=json_util.default)
    return all_road_img


@app.route('/roads_image_table_block/<string:Block>')
def road_image_data_block(Block):
#    URI = "mongodb://127.0.0.1:27017"
#    client = pymongo.MongoClient(URI)
#    DATABASE = client['RMI']

    URI = os.environ['MONGODB_URI']
    client = pymongo.MongoClient(URI)
    DATABASE = client['heroku_dl5cdgz5']

    roads_image = DATABASE['road_images'].find({'block': Block})
    json_roads = []
    for road in roads_image:
        json_roads.append(road)
    all_road_img_block = json.dumps(json_roads, default=json_util.default)
    return all_road_img_block


@app.route('/habitations/<string:Block>')
def road_new_habitation(Block):
    block_roads_hab = []
    block_roads_dict = Database.find("block", {'Block Name': Block})
    for road in block_roads_dict:
        block_roads_hab.append(road)

    all_hab_block = json.dumps(block_roads_hab, default=json_util.default)

    return all_hab_block


@app.route('/roads_image_find/')
def road_image_data_id(fileid):
#    URI = "mongodb://127.0.0.1:27017"
#    client = pymongo.MongoClient(URI)
#    DATABASE = client['RMI']

    URI = os.environ['MONGODB_URI']
    client = pymongo.MongoClient(URI)
    DATABASE = client['heroku_dl5cdgz5']

    roads_image = DATABASE['road_images'].find({'fileid': fileid})
    json_roads = []
    for road in roads_image:
        json_roads.append(road)
    all_road_img = json.dumps(json_roads, default=json_util.default)
    return all_road_img


@app.route('/roads_image_list/')
def roads_img_list():
    email = session['email']
    if email is not None:
        user = User.get_by_email(email)
        if user.block == "ALL":
            return render_template('view_roads_image.html', block=user.block)
        else:
            return render_template('view_roads_image_block.html', block=user.block)
    else:
        return render_template('login_fail.html')


@app.route('/road/image/load/<string:_id>', methods=['POST', 'GET'])
def preview_road_image(_id):
#                URI = "mongodb://127.0.0.1:27017"
#                client = pymongo.MongoClient(URI)
#                DATABASE = client['RMI']

                URI = os.environ['MONGODB_URI']
                client = pymongo.MongoClient(URI)
                DATABASE = client['heroku_dl5cdgz5']

                fid = ""
                fs = gridfs.GridFS(DATABASE)

                for output_data1 in DATABASE['road_images'].find({'fileid': ObjectId(_id)}):
                    fid = output_data1["fileid"]

                output_data = fs.get(ObjectId(fid)).read()

                base64_data = codecs.encode(output_data, 'base64')
                image = base64_data.decode('utf-8')

                return render_template('road_image_display.html', images=image)


@app.route('/roads_list/')
def roads_show():
    return render_template('list_road.html')


@app.route('/road/prop/list/<string:_id>')
def roads_prop_show(_id):
    return render_template('list_road_properties.html', rds_id=_id)


@app.route('/test/')
def render_test():
    return render_template('test.html')


@app.route('/roads_table_code/<string:road_code>')
def road_data_code(road_code):
    roads = Database.find("roads", query={'Road_code': road_code})
    json_roads = []
    for road in roads:
        json_roads.append(road)
    all_road_code = json.dumps(json_roads, default=json_util.default)
    return all_road_code


@app.route('/roads_para_table_code/<string:road_code>')
def road_para_data_code(road_code):
    roads = Database.find("road_details", query={'Road_code': road_code})
    json_roads = []
    for road in roads:
        json_roads.append(road)
    all_road_code = json.dumps(json_roads, default=json_util.default)
    return all_road_code


@app.route('/road_display_para/<string:_id>')
def render_individual_road_para(_id):
        single_road_array = []
        if Database.is_valid(_id):
            single_road_dict = Database.find("road_details", {'_id': ObjectId(_id)})
        else:
            single_road_dict = Database.find("road_details", {'_id': _id})

        for Rds in single_road_dict:
            single_road_array.append(Rds)

        single_road_para = json.dumps(single_road_array, default=json_util.default)

        return single_road_para


if __name__ == '__main__':
    app.run(port=4095, debug=True)