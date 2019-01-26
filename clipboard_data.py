# Author: chenqihui
query = "{query}"
import time
import oss2
import json
import tinify
import re

from AppKit import NSPasteboard, NSPasteboardTypePNG, NSFilenamesPboardType

access_key_id = '<yourAccessKeyId>'
access_key_secret = '<yourAccessKeySecret>'
bucket_name = '<yourBucketName>'
tinify.key = "YOUR_API_KEY"

def get_paste_img_file():
    """
    将剪切板数据保存到本地文件并返回文件路径
    """
    pb = NSPasteboard.generalPasteboard()  # 获取当前系统剪切板数据
    data_type = pb.types()  # 获取剪切c板数据的格式类型

    # 根据剪切板数据类型进行处理
    if NSPasteboardTypePNG in data_type:          # PNG处理
        data = pb.dataForType_(NSPasteboardTypePNG)
        filename = '%s.png' % int(time.time())
        filepath = '/tmp/%s' % filename            # 保存文件的路径
        ret = data.writeToFile_atomically_(filepath, False)    # 将剪切板数据保存为文件
        if ret:   # 判断文件写入是否成功
            return filepath

    elif NSFilenamesPboardType in data_type:
        return pb.propertyListForType_(NSFilenamesPboardType)[0]

def upload_file():

    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', bucket_name)
    fileDir = get_paste_img_file()
    fileName = fileDir[fileDir.rfind('/') + 1:]
    date = time.strftime("%Y-%m", time.localtime())
    key = date + '/'  + fileName
    compressedImage(fileDir);
    result = bucket.put_object_from_file(key, fileDir)
    # print(result.resp.response.__dict__)
    url = result.resp.response.url
    url = url.replace("yangxinyujy-images.oss-cn-beijing.aliyuncs.com","images.xyang.xin")
    data = {
        'items' : [
            {'title' : 'url', 'arg': url,  "icon":
                {
                    'type': 'png',
                    'path': 'icon.png'
                }
             },
            {'title': 'md', 'arg': '![' + fileName + '](%s)' % url, 'icon':
                {
                    'type': 'png',
                    'path': 'icon.png'
                }
             }
        ]
    }
    url_result = json.dumps(data)
    print(url_result)

def compress_path(path, compress):
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', bucket_name)
    resultArray = []
    for root, dirs, files in os.walk(fromFilePath):
        for name in files:
            fileName, fileSuffix = os.path.splitext(name)
            if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg':
                fileName = fileDir[fileDir.rfind('/') + 1:]
                key = date + '/'  + fileName
                if compress:
                    compressedImage(fileDir);
                result = bucket.put_object_from_file(key, fileDir)
                url = result.resp.response.url
                resultArray.append(url)
        break
    print(resultArray)

def compressedImage(fileDir):
    """
    图像压缩
    """
    m = re.search(r'.gif', fileDir)
    if m is None:
        source = tinify.from_file(fileDir)
        source.to_file(fileDir)
    

if __name__ == '__main__':
    upload_file()
