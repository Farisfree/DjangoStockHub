import os
import chardet

# 指定要检测的文件夹
folder = './'

# 遍历所有子文件夹和文件
for root, dirs, files in os.walk(folder):
    for file in files:
        # 获取文件路径
        file_path = os.path.join(root, file)

        # 读取文件内容并检测编码
        with open(file_path, 'rb') as f:
            content = f.read()
            encoding = chardet.detect(content)['encoding']

        # 输出文件名和编码格式
        print(f'{file_path}: {encoding}')
