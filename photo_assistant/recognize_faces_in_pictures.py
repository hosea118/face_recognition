#-*-coding:utf-8-*-
import face_recognition
import logging as logger
import os
import photo_exif
import cv2
import numpy as np

#空列表
known_faces = []

def face_recognition_in_pic(file_name):
    if not os.path.exists(file_name):
        logger.error('%s not exists' % file_name)

    try:
        unknown_image = face_recognition.load_image_file(file_name)
    except OSError:
        logger.error('load_image_file error')
        return 'error_img'

    img_w, img_h = photo_exif.get_photo_res(file_name)
    if img_w > 1800 or img_h > 1600:
        if img_w > img_h:
            unknown_image = cv2.resize(unknown_image, (1800, 1600))
        else:
            unknown_image = cv2.resize(unknown_image, (1600, 1800))
    elif img_w == img_h == 0:
            unknown_image = cv2.resize(unknown_image, (1800, 1600))

    try:
        face_bounding_boxes = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=0, model='cnn')
        faces = len(face_bounding_boxes)
        if faces > 3:
            return 'more_faces'
        elif faces == 3:
            return 'three_faces'
        elif faces == 2:
            return 'two_faces'
        elif len(face_bounding_boxes) == 0:
            return 'no_face'
        else:
            unknown_face_encoding = face_recognition.face_encodings(unknown_image, known_face_locations=face_bounding_boxes)[0]
    except IndexError:
        logger.error('no face find in the image')
        return 'no_face'
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding, tolerance=0.40)
    if not True in results:
        known_faces.append(unknown_face_encoding)
        return 'person' + str(len(known_faces)-1)
    else:
        for i in range(len(known_faces)):
            if results[i]:
                return 'person' + str(i)
