import sys
import os,shutil
import re
from PIL import Image
from PIL.ExifTags import TAGS
import photo_exif
import debug
import recognize_faces_in_pictures as rec_face

classify_photo_by_date = 0

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

def classify_by_face(out_dir, file_name):
    result = rec_face.face_recognition_in_pic(file_name)
    logger.info('result is %s' % result)

    copy_path = out_dir + '/' + result
    copy_file(copy_path, file_name)
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('param error!\n\
            eg, ./a.out input_dir output_dir')
    else:
        root_dir = sys.argv[1]
        out_dir = sys.argv[2] + '/category_result'
        #log 保存到文件
        log_dir = sys.argv[2] + '/log'
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        global logger
        logger = debug.logger_init(log_dir, 'debug')
        #创建分类文件夹
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
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
                        classify_by_face(out_dir, file_path)
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


