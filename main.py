import sys
from java_creator import SpringMvcCreator

if __name__ == '__main__':
    try:
        creator_type = sys.argv[1]
        if creator_type.lower() == 'springmvc':
            # 输出路径
            out_dir = sys.argv[2]
            # Group Id
            group_id = sys.argv[3]
            # Artifact Id
            artifact_id = sys.argv[4]
            # 版本号
            version = sys.argv[5]
            # 数据库连接
            db_conn = sys.argv[6]
            print('正在生成...')
            SpringMvcCreator().create(out_dir, group_id, artifact_id, version, db_conn)
            print('已生成')
        else:
            print('还没做呢')
    except IndexError as e:
        print('命令格式: python3 main.py 类型 输出文件夹 groupId artifactId 版本 数据库连接')
        print('数据库连接: 主机/端口/用户名/密码/数据库名')
        raise e
