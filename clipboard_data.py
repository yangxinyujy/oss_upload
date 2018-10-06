# Author: chenqihui
query = "{query}"
import time
import oss2
import json
import tinify

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
        # file in machine
        return pb.propertyListForType_(NSFilenamesPboardType)[0]




def upload_file():

    auth = oss2.Auth(access_key_id, access_key_secret)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', bucket_name)
    file_name = get_paste_img_file()
    key_name = file_name[file_name.rfind('/'):]
    date = time.strftime("%Y-%m-%d", time.localtime())
    key = date + key_name
    # 图片压缩
    m = re.search(r'.gif', key_name);
    if m is None:
        source = tinify.from_file(file_name)
        source.to_file(file_name)
    result = bucket.put_object_from_file(key, file_name)
    url = result.resp.response.url
    data = {
        'items' : [
            {'title' : 'url', 'arg': url,  "icon":
                {
                    'type': 'png',
                    'path': 'icon.png'
                }
             },
            {'title': 'md', 'arg': '![](%s)' % url, 'icon':
                {
                    'type': 'png',
                    'path': 'icon.png'
                }
             }
        ]
    }
    url_result = json.dumps(data)
    print(url_result)



if __name__ == '__main__':
    upload_file()
