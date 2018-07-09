import face_recognition
import logging as logger
import os

#空列表
known_faces = []

def face_recognition_in_pic(file_name):
    if not os.path.exists(file_name):
        logger.error('%s not exists' % file_name)

    unknown_image = face_recognition.load_image_file(file_name)
    try:
        face_bounding_boxes = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=0, model='cnn')
        if len(face_bounding_boxes) > 1:
            return 'more_faces'
        elif len(face_bounding_boxes) == 0:
            return 'no_face'
        else:
            unknown_face_encoding = face_recognition.face_encodings(unknown_image, known_face_locations=face_bounding_boxes)[0]
    except IndexError:
        logger.error('no face find in the image')
        return 'no_face'
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
    if not True in results:
        known_faces.append(unknown_face_encoding)
        return 'person' + str(len(known_faces)-1)
    else:
        for i in range(len(known_faces)):
            if results[i]:
                return 'person' + str(i)
