import sys
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(fileName):
    ret = {}
    try:
        img = Image.open(fileName)
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag,tag)
                    ret[decoded] = value
    except IOError:
        print('IOError %s' % fileName)
    return ret

def get_photo_time(fileName):
    exif = get_exif_data(fileName)
    timeTag = 'DateTimeOriginal'
    if timeTag in list(exif.keys()):
        return exif[timeTag]
    else:
        return 'unknown'

def get_camera_model(fileName):
    exif = get_exif_data(fileName)
    modelTag = 'Model'
    if modelTag in list(exif.keys()):
        return exif[modelTag]
    else:
        return 'unknown'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('param error!\n\
            eg, ./a.out filename')
    else:
        fileName = sys.argv[1]
        #exif = get_exif_data(fileName)
        print(get_photo_time(fileName))
        print(get_camera_model(fileName))
