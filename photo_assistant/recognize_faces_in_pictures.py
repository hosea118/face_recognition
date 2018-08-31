import face_recognition
import logging as logger
import os
import photo_exif
import cv2
import numpy as np

#空列表
#known_faces = []

def detect_faces_in_image(image):
    #print('loading model...')
    net = cv2.dnn.readNetFromCaffe('photo_assistant/deploy.prototxt.txt', 'photo_assistant/res10_300x300_ssd_iter_140000.caffemodel')
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300,300)), 1.0, (300,300), (104.0, 177.0, 123.0))
    #print('computing face detections...')
    net.setInput(blob)
    detections = net.forward()
    face_bounding_boxes = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0,0,i,3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype('int')
            logger.info('find a face, (%d, %d, %d, %d) %2f' % (startX, startY, endX, endY, confidence))
            face_bounding_boxes.append((startY, startX, endY, endX))
    return face_bounding_boxes

def face_recognition_in_pic(file_name, known_faces_encodeing):
    if not os.path.exists(file_name):
        logger.error('%s not exists' % file_name)

    try:
        unknown_image = cv2.imread(file_name)
        #unknown_image = face_recognition.load_image_file(file_name)
    except OSError:
        logger.error('load_image_file error')
        return 'error_img'

    image_rgb = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)
    face_bounding_boxes = detect_faces_in_image(unknown_image)

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
        unknown_face_encoding = face_recognition.face_encodings(image_rgb, known_face_locations=face_bounding_boxes, num_jitters=100)[0]
    for key in known_faces_encodeing.keys():
        results = face_recognition.compare_faces(known_faces_encodeing[key], unknown_face_encoding, tolerance=0.30)
        if True in results:
            logger.info('find a known face: '+ key)
            return key
            
    print('unknown face, add to known_faces_encodeing')
    new_key = 'person' + str(len(known_faces_encodeing)-1)
    unknown_face_list = []
    unknown_face_list.append(unknown_face_encoding)
    known_faces_encodeing[new_key] = unknown_face_list 
    return new_key
