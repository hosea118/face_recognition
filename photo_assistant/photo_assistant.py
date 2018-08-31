import sys
import os,shutil
import re
from PIL import Image
from PIL.ExifTags import TAGS
import photo_exif
import debug
import recognize_faces_in_pictures as rec_face
import face_recognition
import cv2

classify_photo_by_date = 0

known_faces_dic = {}
known_faces_encodeing = {}

support_photo = ['jpg', 'jpeg', 'JPG', 'png', 'PNG']
ignore_path = ['.git', 'category_result', 'log']
video_suffix = ['MOV', 'mp4', 'MP4', 'mov', 'HEIC']
global logger

def copy_file(dst, src):
    if not os.path.exists(src):
        logger.error('%s not exists' % src)
        return None
    if not os.path.exists(dst):
        os.mkdir(dst)
    dst_name = dst + '/' + src.split('/')[-1]
    logger.info('src_name is %s' % src)
    logger.info('dst_name is %s' % dst_name)
    shutil.copyfile(src, dst_name)
    
def classify_by_date(out_dir, file_name):
    logger.info(file_name)
    date = photo_exif.get_photo_time(file_name)
    date = re.sub('[:-]', '', date)
    date = date.split(' ')[0]
    copy_path = out_dir + '/' + date
    copy_file(copy_path, file_name)

def classify_by_face(out_dir, file_name, known_faces_encodeing):
    result = rec_face.face_recognition_in_pic(file_name, known_faces_encodeing)
    logger.info('result is %s' % result)

    copy_path = out_dir + '/' + result
    copy_file(copy_path, file_name)

'''
def resize_image(image, file_name):
    img_w, img_h = photo_exif.get_photo_res(file_name)
    if img_w > 1800 or img_h > 1600:
        if img_w > img_h:
            image = cv2.resize(image, (1800, 1600))
        else:
            image = cv2.resize(image, (1600, 1800))
    elif img_w == img_h == 0:
            image = cv2.resize(image, (1800, 1600))
    return image
'''

def init_known_faces(known_faces_dir):
    for fpath, dirs, files in os.walk(known_faces_dir):
        if fpath == known_faces_dir:
            for name in files:
                pic_list = []
                pic_list.append(os.path.join(fpath, name))
                known_faces_dic[name.split('.')[0]] = pic_list
        else:
            pic_list = []
            for name in files:
                pic_list.append(os.path.join(fpath, name))
            known_faces_dic[fpath.split('/')[-1]] = pic_list
    print(known_faces_dic.items())

    print('init known faces start')
    for key in known_faces_dic.keys():
        pic_encode_list = []
        for picture in known_faces_dic[key]:
            image = cv2.imread(picture)
            #image = face_recognition.load_image_file(picture)
            #image = resize_image(image, picture)
            #face_bounding_boxes = face_recognition.face_locations(image, number_of_times_to_upsample=0, model='cnn')
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_bounding_boxes = rec_face.detect_faces_in_image(image_rgb)

            if (len(face_bounding_boxes)):
                face_encoding = face_recognition.face_encodings(image_rgb, known_face_locations=face_bounding_boxes, num_jitters=100)[0]
                pic_encode_list.append(face_encoding)
        known_faces_encodeing[key] = pic_encode_list
    print('init known faces done')
    
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('param error!\n\
            eg, ./a.out input_dir output_dir known_faces_dir')
    else:
        root_dir = sys.argv[1]
        out_dir = sys.argv[2] + '/category_result'
        known_faces_dir = sys.argv[3]
        #log 保存到文件
        log_dir = sys.argv[2] + '/log'
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        global logger
        logger = debug.logger_init(log_dir, 'debug')
        #创建分类文件夹
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        if classify_photo_by_date != 1:
            init_known_faces(known_faces_dir)

        for fpath, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in ignore_path]
            for file in files:
                #如果文件是图片则处理
                file_path = os.path.join(fpath, file)
                if file.split('.')[-1] in support_photo:
                    #file_path = os.path.join(fpath, file)
                    if classify_photo_by_date:
                        classify_by_date(out_dir, file_path)
                    else:
                        classify_by_face(out_dir, file_path, known_faces_encodeing)
                elif file.split('.')[-1] in video_suffix:
                    video_out_dir = out_dir + '/video_files'
                    if not os.path.exists(video_out_dir):
                        os.mkdir(video_out_dir)
                    dst = video_out_dir + '/' + file
                    print('dst is ' + dst)
                    shutil.copyfile(file_path, dst)
                else:
                    unknown_out_dir = out_dir + '/unknown_files'
                    if not os.path.exists(unknown_out_dir):
                        os.mkdir(unknown_out_dir)
                    dst = unknown_out_dir + '/' + file
                    print('dst is ' + dst)
                    if os.path.isfile(file):
                        shutil.copyfile(file_path, dst)
                    elif os.path.isdir(file):
                        shutil.copytree(file_path, dst)


