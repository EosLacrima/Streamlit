# 开发人员
# 开发时间  2022/6/10
import json
import os
import requests
import tqdm


if __name__ == '__main__':
    dirpath = "/Users/apple/Downloads/Home/待处理数据/离散帧第四批/62f0e6bc7168aad4743477fc"
    for i in os.listdir(dirpath):
        file_path = os.path.join(dirpath, i)
        with open(file_path, encoding="utf-8") as f:
            json_data = json.loads(f.read())
            name = json_data.get('point_cloud_oss').split('/')[-1]
            url = json_data.get('point_cloud_http')
            print(name, url)
            path = f"/Users/apple/Downloads/Home/待处理数据/{name}"
            r = requests.get(url)
            print(r)
            pcd = r.content
            with open(path, 'wb+') as file:  # 保存到本地的文件名
                file.write(pcd)