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
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)
        if len(unknown_face_encoding) > 1:
            return 'more_faces'
        else:
            unknown_face_encoding = unknown_face_encoding[0]
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
