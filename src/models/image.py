from PIL.ExifTags import TAGS

from PIL import Image

from datetime import datetime as dt


def get_if_exist(data, key):
        if key in data:
            return data[key]
        return None


def get_exif(fn):
        ret = {}
        i = Image.open(fn)
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret


def lat_lon(file):
        """
        returns a dict of lat, lon, alt, filename values, given
        an input file path as string
        example: latlong("path/to/file") or latlon(variable)
        """
        img = Image.open(file)
#        info = img._getexif()

        filename = path_leaf(file)
        # build a dict of decoded exif keys and values
        decoded = dict((TAGS.get(key, key), value) for key, value in info.items())
        info: Dict[str, Union[Union[None, float, str], Any]] = {
            "filename": filename,
            "lat": None,
            "lon": None,
            "timestamp": None,
            "altitude": None,
        }
        # ensure that this photo contains GPS data, or return an empty dict:
        if not decoded.get('GPSInfo'):
            return info
        lat = [float(x) / float(y) for x, y in decoded['GPSInfo'][2]]
        lon = [float(x) / float(y) for x, y in decoded['GPSInfo'][4]]
        alt = float(decoded['GPSInfo'][6][0]) / float(decoded['GPSInfo'][6][1])
        timestamp = decoded['DateTimeOriginal']
        # assign values to dict
        info['filename'] = filename
        info['lat'] = (lat[0] + lat[1] / 60)
        info['lon'] = (lon[0] + lon[1] / 60)
        info['timestamp'] = dt.strptime(
             timestamp,
             "%Y:%m:%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        info['altitude'] = alt

        # corrections if necessary
        if decoded['GPSInfo'][1] == "S":
            info['lat'] *= -1
        if decoded['GPSInfo'][3] == "W":
            info['lon'] *= -1
        # if we're below sea level, the value's negative
        if decoded['GPSInfo'][5] == 1:
            info['altitude'] *= -1
        return info

