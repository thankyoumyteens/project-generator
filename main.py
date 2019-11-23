import sys
from java_creator import *

if __name__ == '__main__':
    try:
        creator_type = sys.argv[1]
        if creator_type.lower() == 'springmvc':
            out_dir = input('输出路径: ')
            group_id = input('Group Id: ')
            artifact_id = input('Artifact Id: ')
            version = input('版本号: ')
            print('正在生成...')
            SpringMvcCreator().create(out_dir, group_id, artifact_id, version)
            print('已生成')
        else:
            print('还没做呢')
    except IndexError as e:
        print('命令格式: python3 main.py type')
