#-*-coding:utf-8-*-
import urllib, urllib2, sys
import ssl
import json
import base64
import cv2

group_id = 'face_classifier'
global access_token
def get_access_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=G2RivbYHWqdyvLhVKGuG63fW&client_secret=mjDVXo01XAlASh7An2XNWcA8pz7sFZeB'
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    content_dict =  json.loads(content)

    if 'access_token' in list(content_dict.keys()):
        return content_dict['access_token']
    else:
        return None

def base64_photo(file_name):
    img = cv2.imread(file_name)
    #img = cv2.resize(img, (1800, 1350))
    #cv2.imwrite('/tmp/tmpPic.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 9])
    cv2.imwrite('/tmp/tmpPic.jpg', img)

    fp = open('/tmp/tmpPic.jpg', 'r')
    photo = fp.read()
    return base64.b64encode(photo)

def detect_face(file_name):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

    encode_photo = base64_photo(file_name)
    params = {}
    params['image'] = encode_photo 
    params['image_type'] = 'BASE64'
    params['max_face_num'] = 5

    params = json.dumps(params)

    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read()
    #print(content)
    content_dict =  json.loads(content)
    if content_dict['error_msg'] == 'SUCCESS':
        #print('face_probability is %f' % content_dict['result']['face_list'][0]['face_probability'])
        if content_dict['result']['face_list'][0]['face_probability'] > 0.5:
            return content_dict['result']['face_num'], encode_photo
        else:
            return 0, None
    elif content_dict['error_msg'] == 'pic not has face':
        return 0, None
    else:
        return -1, None

def search_face(base64_photo):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"

    params = {}
    params['image'] = base64_photo
    params['image_type'] = 'BASE64'
    params['group_id_list'] = group_id
    params = json.dumps(params)

    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read()
    content_dict = json.loads(content)
    if content_dict['error_msg'] == 'SUCCESS':
        user_id = content_dict['result']['user_list'][0]['user_id']
        if content_dict['result']['user_list'][0]['score'] > 50:
            return user_id
    else:
        return None
    #if content:
    #    print content

def regist_face(base64_photo, user_id):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"

    params = {}
    params['image'] = base64_photo
    params['image_type'] = 'BASE64'
    params['group_id'] = group_id
    params['user_id'] = user_id
    params = json.dumps(params)

    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read()
    #if content:
    #    print content

def get_user_num(group_id):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getusers"

    params = {}
    params['group_id'] = group_id
    params = json.dumps(params)

    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read()
    content_dict = json.loads(content)
    user_num = len(content_dict['result']['user_id_list'])

    return user_num

def delet_face_group():
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/delete"

    params = {}
    params['group_id'] = group_id
    params = json.dumps(params)

    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read()

def init_face_sdk():
    global access_token
    access_token = get_access_token()

def deinit_face_sdk():
    delet_face_group()

def recognize_face(file_name):
    #print("get access_token")
    face_num, base64_photo = detect_face(file_name)
    if face_num < 0:
        return 'error_photo'
    elif face_num == 2:
        return 'two_face'
    elif face_num == 3:
        return 'three_face'
    elif face_num > 3:
        return 'more_face'
    else:
        result = search_face(base64_photo)
        if result == None:
            user_num = get_user_num(group_id)
            regist_face(base64_photo, 'person'+str(user_num))
            return 'person'+str(user_num)
        else:
            print('find a face: %s' % result)
            return result


if __name__ == '__main__':

    access_token = get_access_token()

    deinit_face_sdk()
    #print(get_user_num(group_id))
    print(recognize_face(sys.argv[1]))

