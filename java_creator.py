import os
import shutil
import re
import db
import util


# 生成spring mvc项目
class SpringMvcCreator:

    # 读取模板文件内容
    @staticmethod
    def _get_template(template_file):
        with open(template_file, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    # 将内容写入文件
    @staticmethod
    def _write_file(content, target_file):
        with open(target_file, 'w', encoding='utf-8') as file:
            file.write(content)

    # 将模板文件的内容写入新文件
    def _write_default_file(self, template_file, target_file):
        content = self._get_template(template_file)
        self._write_file(content, target_file)

    # 生成文件, 并将包名写入
    def _create_file_with_replace(self, file_dir, file, base_package):
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = os.path.join(file_dir, file)
        content = self._get_template('templates/spring-mvc/' + file)
        # 替换包名
        content = re.sub('%BASE_PACKAGE', base_package, content)
        self._write_file(content, f)

    # 获取表的主键
    @staticmethod
    def _get_primary_key(columns):
        primary_key = 'id'
        primary_key_type = 'java.lang.Long'
        primary_key_type_short = 'Long'
        primary_key_jdbc_type = 'BIGINT'
        for column in columns:
            name = column['name']
            db_type = column['type']
            java_type, jdbc_type = util.get_type_map(db_type)
            java_type_short = util.get_java_type(db_type)
            is_primary_key = column['is_primary_key']
            if is_primary_key:
                primary_key = name
                primary_key_type = java_type
                primary_key_type_short = java_type_short
                primary_key_jdbc_type = jdbc_type
        return primary_key, primary_key_type, primary_key_type_short, primary_key_jdbc_type

    # 生成实体类的成员变量
    @staticmethod
    def _generate_fields(columns):
        fields_str = ''
        for column in columns:
            name = column['name']
            db_type = column['type']
            field_name = util.get_field_name(name)
            java_type = util.get_java_type(db_type)
            fields_str += '\tprivate ' + java_type + ' ' + field_name + ';\n'
        return fields_str

    # 生成实体类的setter方法
    @staticmethod
    def _generate_setters(columns):
        setters_str = ''
        for column in columns:
            name = column['name']
            db_type = column['type']
            method_name = util.get_class_name(name)
            field_name = util.get_field_name(name)
            java_type = util.get_java_type(db_type)
            setters_str += '\tpublic void set' + method_name + '(' + java_type + ' ' + \
                           field_name + ') { this.' + field_name + ' = ' + field_name + '; }\n'
        return setters_str

    # 生成实体类的getter方法
    @staticmethod
    def _generate_getters(columns):
        getters_str = ''
        for column in columns:
            name = column['name']
            db_type = column['type']
            method_name = util.get_class_name(name)
            field_name = util.get_field_name(name)
            java_type = util.get_java_type(db_type)
            getters_str += '\tpublic ' + java_type + ' get' + method_name + '() { return ' + field_name + '; }\n'
        return getters_str

    # 生成实体类
    def _create_pojo(self, pojo_package, base_package, db_info):
        if not os.path.exists(pojo_package):
            os.makedirs(pojo_package)
        for table_info in db_info.items():
            # 为每一张表创建一个对应的实体类
            table_name = table_info[0]
            columns = table_info[1]
            content = ''
            class_name = util.get_class_name(table_name)
            file_name = os.path.join(pojo_package, class_name + '.java')
            package_str = 'package ' + base_package + '.pojo;'
            class_str = 'public class ' + class_name + ' {'
            class_str += '\n'
            class_str += self._generate_fields(columns)
            class_str += '\n'
            class_str += self._generate_setters(columns)
            class_str += '\n'
            class_str += self._generate_getters(columns)
            class_str += '}'

            content += package_str
            content += '\n\n'
            content += class_str
            self._write_file(content, file_name)

    # 生成Dao接口
    def _create_dao(self, dao_package, base_package, db_info):
        if not os.path.exists(dao_package):
            os.makedirs(dao_package)
        for table_info in db_info.items():
            # 为每一张表创建一个对应的Dao
            table_name = table_info[0]
            columns = table_info[1]
            # 找到主键
            primary_key, primary_key_type, primary_key_type_short, primary_key_jdbc_type = \
                self._get_primary_key(columns)
            # 内容
            content = ''
            class_name = util.get_class_name(table_name)
            file_name = os.path.join(dao_package, class_name + 'Dao.java')
            package_str = 'package ' + base_package + '.dao;'
            import_str = 'import ' + base_package + '.pojo.' + class_name + ';'
            class_str = 'public interface ' + class_name + 'Dao {'
            class_str += '\n'
            class_str += '\tint deleteByPrimaryKey(' + primary_key_type_short + ' ' + primary_key + ');\n\n'
            class_str += '\tint insert(' + class_name + ' record);\n\n'
            class_str += '\tint insertSelective(' + class_name + ' record);\n\n'
            class_str += '\t' + class_name + ' selectByPrimaryKey(' + \
                         primary_key_type_short + ' ' + primary_key + ');\n\n'
            class_str += '\tint updateByPrimaryKeySelective(' + class_name + ' record);\n\n'
            class_str += '\tint updateByPrimaryKey(' + class_name + ' record);\n'
            class_str += '}'

            content += package_str
            content += '\n\n'
            content += import_str
            content += '\n\n'
            content += class_str
            self._write_file(content, file_name)

    # 生成mapper中的ResultMap
    @staticmethod
    def _generate_result_map(base_package, class_name, columns):
        result = '\t<resultMap id="BaseResultMap" type="' + base_package + '.pojo.' + class_name + '">\n'
        result += '\t\t<constructor>\n'
        for column in columns:
            name = column['name']
            db_type = column['type']
            java_type, jdbc_type = util.get_type_map(db_type)
            is_primary_key = column['is_primary_key']
            if is_primary_key:
                result += '\t\t\t<idArg column="' + name + '" javaType="' + \
                          java_type + '" jdbcType="' + jdbc_type + '" />\n'
            else:
                result += '\t\t\t<arg column="' + name + '" javaType="' + \
                          java_type + '" jdbcType="' + jdbc_type + '" />\n'
        result += '\t\t</constructor>\n'
        result += '\t</resultMap>\n'
        return result

    # 生成MyBatis的sql映射文件
    def _create_mapper(self, mappers_dir, base_package, db_info):
        if not os.path.exists(mappers_dir):
            os.makedirs(mappers_dir)
        for table_info in db_info.items():
            # 为每一张表创建一个对应的mybatis映射
            table_name = table_info[0]
            columns = table_info[1]
            # 找到主键
            primary_key, primary_key_type, primary_key_type_short, primary_key_jdbc_type = \
                self._get_primary_key(columns)
            # 内容
            content = ''
            class_name = util.get_class_name(table_name)
            file_name = os.path.join(mappers_dir, class_name + 'Mapper.xml')
            # header
            header_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
            header_str += '<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" ' \
                          '"http://mybatis.org/dtd/mybatis-3-mapper.dtd">\n'
            # 指定Dao接口
            mapper_str = '<mapper namespace="' + base_package + '.dao.' + class_name + 'Dao">\n'
            # BaseResultMap
            mapper_str += self._generate_result_map(base_package, class_name, columns)
            # Base_Column_List
            mapper_str += '\t<sql id="Base_Column_List">\n'
            mapper_str += '\t\t'
            for column in columns:
                mapper_str += column['name'] + ', '
            mapper_str = mapper_str[0: len(mapper_str) - 2]
            mapper_str += '\n'
            mapper_str += '\t</sql>\n'
            # 实现dao接口的selectByPrimaryKey方法
            mapper_str += '\t<select id="selectByPrimaryKey" parameterType="' + \
                          primary_key_type + '" resultMap="BaseResultMap">\n'
            mapper_str += '\t\tselect \n'
            mapper_str += '\t\t<include refid="Base_Column_List" /> \n'
            mapper_str += '\t\tfrom ' + table_name + ' \n'
            mapper_str += '\t\twhere ' + primary_key + ' = #{' + primary_key + \
                          ',jdbcType=' + primary_key_jdbc_type + '} \n'
            mapper_str += '\t</select>\n'
            # 实现dao接口的deleteByPrimaryKey方法
            mapper_str += '\t<delete id="deleteByPrimaryKey" parameterType="' + \
                          primary_key_type + '">\n'
            mapper_str += '\t\tdelete from ' + table_name + ' \n'
            mapper_str += '\t\twhere ' + primary_key + ' = #{' + primary_key + \
                          ',jdbcType=' + primary_key_jdbc_type + '} \n'
            mapper_str += '\t</delete>\n'
            # 实现dao接口的insert方法
            mapper_str += '\t<insert id="insert" parameterType="' + base_package + \
                          '.pojo.' + class_name + '">\n'
            mapper_str += '\t\tinsert into ' + table_name + ' ( \n'
            for column in columns:
                mapper_str += '\t\t\t' + column['name'] + ', \n'
            mapper_str = mapper_str[0: len(mapper_str) - 3]
            mapper_str += ')\n'
            mapper_str += '\t\tvalues (\n'
            for column in columns:
                jdbc_type = util.get_type_map(column['type'])[1]
                mapper_str += '\t\t\t#{' + column['name'] + ',jdbcType=' + jdbc_type + '}, \n'
            mapper_str = mapper_str[0: len(mapper_str) - 3]
            mapper_str += ')\n'
            mapper_str += '\t</insert>\n'
            # 实现dao接口的updateByPrimaryKey方法
            mapper_str += '\t<update id="updateByPrimaryKey" parameterType="' + \
                          base_package + '.pojo.' + class_name + '">\n'
            mapper_str += '\t\tupdate ' + table_name + ' \n'
            mapper_str += '\t\tset \n'
            for column in columns:
                if not column['is_primary_key']:
                    jdbc_type = util.get_type_map(column['type'])[1]
                    mapper_str += '\t\t\t' + column['name'] + ' = #{' + column['name'] + \
                                  ',jdbcType=' + jdbc_type + '}, \n'
            mapper_str = mapper_str[0: len(mapper_str) - 3]
            mapper_str += '\n'
            mapper_str += '\t\twhere ' + primary_key + ' = #{' + primary_key + \
                          ',jdbcType=' + primary_key_jdbc_type + '} \n'
            mapper_str += '\t</update>\n'
            # 实现dao接口的insertSelective方法
            mapper_str += '\t<insert id="insertSelective" parameterType="' + \
                          base_package + '.pojo.' + class_name + '">\n'
            mapper_str += '\t\tinsert into ' + table_name + ' \n'
            mapper_str += '\t\t<trim prefix="(" suffix=")" suffixOverrides=",">\n'
            for column in columns:
                mapper_str += '\t\t\t<if test="' + util.get_field_name(column['name']) + ' != null">\n'
                mapper_str += '\t\t\t\t' + column['name'] + ',\n'
                mapper_str += '\t\t\t</if>\n'
            mapper_str += '\t\t</trim>\n'
            mapper_str += '\t\t<trim prefix="values (" suffix=")" suffixOverrides=",">\n'
            for column in columns:
                mapper_str += '\t\t\t<if test="' + util.get_field_name(column['name']) + ' != null">\n'
                jdbc_type = util.get_type_map(column['type'])[1]
                mapper_str += '\t\t\t\t#{' + column['name'] + ',jdbcType=' + jdbc_type + '}, \n'
                mapper_str += '\t\t\t</if>\n'
            mapper_str += '\t\t</trim>\n'
            mapper_str += '\t</insert>\n'
            # 实现dao接口的updateByPrimaryKeySelective方法
            mapper_str += '\t<update id="updateByPrimaryKeySelective" parameterType="' + \
                          base_package + '.pojo.' + class_name + '">\n'
            mapper_str += '\t\tupdate ' + table_name + ' \n'
            mapper_str += '\t\t<set>\n'
            for column in columns:
                if not column['is_primary_key']:
                    mapper_str += '\t\t\t<if test="' + util.get_field_name(column['name']) + ' != null">\n'
                    jdbc_type = util.get_type_map(column['type'])[1]
                    mapper_str += '\t\t\t\t' + column['name'] + ' = #{' + column['name'] + \
                                  ',jdbcType=' + jdbc_type + '}, \n'
                    mapper_str += '\t\t\t</if>\n'
            mapper_str += '\t\t</set>\n'
            mapper_str += '\t\twhere ' + primary_key + ' = #{' + primary_key + \
                          ',jdbcType=' + primary_key_jdbc_type + '} \n'
            mapper_str += '\t</update>\n'
            mapper_str += '</mapper>\n'

            content += header_str
            content += mapper_str
            self._write_file(content, file_name)

    # 生成service接口
    def _create_service(self, service_package, base_package, db_info):
        if not os.path.exists(service_package):
            os.makedirs(service_package)
        for table_info in db_info.items():
            # 为每一张表创建一个对应的Service
            table_name = table_info[0]
            columns = table_info[1]
            # 找到主键
            primary_key, primary_key_type, primary_key_type_short, primary_key_jdbc_type = \
                self._get_primary_key(columns)
            # 内容
            content = ''
            class_name = util.get_class_name(table_name)
            file_name = os.path.join(service_package, class_name + 'Service.java')
            package_str = 'package ' + base_package + '.service;'
            import_str = 'import ' + base_package + '.pojo.' + class_name + ';'
            class_str = 'public interface ' + class_name + 'Service {'
            class_str += '\n'
            class_str += '\tint deleteByPrimaryKey(' + primary_key_type_short + ' ' + primary_key + ');\n\n'
            class_str += '\tint insert(' + class_name + ' record);\n\n'
            class_str += '\tint insertSelective(' + class_name + ' record);\n\n'
            class_str += '\t' + class_name + ' selectByPrimaryKey(' + primary_key_type_short + \
                         ' ' + primary_key + ');\n\n'
            class_str += '\tint updateByPrimaryKeySelective(' + class_name + ' record);\n\n'
            class_str += '\tint updateByPrimaryKey(' + class_name + ' record);\n'
            class_str += '}'

            content += package_str
            content += '\n\n'
            content += import_str
            content += '\n\n'
            content += class_str
            self._write_file(content, file_name)

    # 生成service实现类
    def _create_service_impl(self, service_impl_package, base_package, db_info):
        if not os.path.exists(service_impl_package):
            os.makedirs(service_impl_package)
        for table_info in db_info.items():
            # 为每一张表创建一个对应的Impl
            table_name = table_info[0]
            columns = table_info[1]
            # 找到主键
            primary_key, primary_key_type, primary_key_type_short, primary_key_jdbc_type = \
                self._get_primary_key(columns)
            # 内容
            content = ''
            class_name = util.get_class_name(table_name)
            file_name = os.path.join(service_impl_package, class_name + 'ServiceImpl.java')
            package_str = 'package ' + base_package + '.service.impl;'
            import_str = 'import ' + base_package + '.service.' + class_name + 'Service;\n'
            import_str += 'import ' + base_package + '.pojo.' + class_name + ';\n'
            import_str += 'import javax.annotation.Resource;'
            class_str = '@Service("' + util.get_field_name(table_name) + 'Service")\n'
            class_str += 'public class ' + class_name + 'ServiceImpl implements ' + class_name + 'Service {'
            class_str += '\n\n'
            class_str += '\t@Resource\n'
            class_str += '\tprivate ' + class_name + 'Dao dao;'
            class_str += '\n\n'
            class_str += '\t@Override\n'
            class_str += '\tint deleteByPrimaryKey(' + primary_key_type_short + ' ' + primary_key + ') ' + \
                         '{ return -1; }\n\n'
            class_str += '\t@Override\n'
            class_str += '\tint insert(' + class_name + ' record) { return -1; }\n\n'
            class_str += '\t@Override\n'
            class_str += '\tint insertSelective(' + class_name + ' record) { return -1; }\n\n'
            class_str += '\t@Override\n'
            class_str += '\t' + class_name + ' selectByPrimaryKey(' + primary_key_type_short + ' ' + \
                         primary_key + ') { return null; }\n\n'
            class_str += '\t@Override\n'
            class_str += '\tint updateByPrimaryKeySelective(' + class_name + ' record) { return -1; }\n\n'
            class_str += '\t@Override\n'
            class_str += '\tint updateByPrimaryKey(' + class_name + ' record) { return -1; }\n'
            class_str += '}'

            content += package_str
            content += '\n\n'
            content += import_str
            content += '\n\n'
            content += class_str
            self._write_file(content, file_name)

    # 生成java源代码
    def _create_java(self, java_dir, base_package, db_conn):
        packages = base_package.split('.')
        for package in packages:
            java_dir = os.path.join(java_dir, package)
        # 获取所有表
        db_arr = db_conn.split('/')
        if len(db_arr) == 6:
            db_util = db.MySqlUtil(db_arr[0], db_arr[1], db_arr[2], db_arr[3], db_arr[4], db_arr[5])
        else:
            db_util = db.MySqlUtil(db_arr[0], db_arr[1], db_arr[2], db_arr[3], db_arr[4])
        db_info = db_util.get_db_info()
        # 控制器
        controller_package = os.path.join(java_dir, 'controller')
        self._create_file_with_replace(controller_package, 'TestController.java', base_package)
        # 持久层
        dao_package = os.path.join(java_dir, 'dao')
        self._create_dao(dao_package, base_package, db_info)
        # 业务层接口
        service_package = os.path.join(java_dir, 'service')
        self._create_service(service_package, base_package, db_info)
        # 业务层实现类
        service_impl_package = os.path.join(service_package, 'impl')
        self._create_service_impl(service_impl_package, base_package, db_info)
        # 实体类
        pojo_package = os.path.join(java_dir, 'pojo')
        self._create_pojo(pojo_package, base_package, db_info)
        # 过滤器
        filter_package = os.path.join(java_dir, 'filter')
        self._create_file_with_replace(filter_package, 'CORSFilter.java', base_package)
        # 拦截器
        interceptor_package = os.path.join(java_dir, 'interceptor')
        self._create_file_with_replace(interceptor_package, 'AuthorityInterceptor.java', base_package)

    # 生成资源文件夹
    def _create_resources(self, resources_dir, base_package, db_conn):
        os.makedirs(resources_dir)
        # 全局配置文件
        self._write_default_file('templates/spring-mvc/app.properties', os.path.join(resources_dir, 'app.properties'))
        # Spring配置文件
        self._create_file_with_replace(resources_dir, 'applicationContext.xml', base_package)
        # Spring数据源配置文件
        self._create_file_with_replace(resources_dir, 'applicationContext-datasource.xml', base_package)
        # SpringMVC配置文件
        self._create_file_with_replace(resources_dir, 'dispatcher-servlet.xml', base_package)
        # 日志配置文件
        self._create_file_with_replace(resources_dir, 'logback.xml', base_package)
        # 数据库连接配置文件
        content = self._get_template('templates/spring-mvc/datasource.properties')
        db_arr = db_conn.split('/')
        content = re.sub('%USERNAME', db_arr[2], content)
        content = re.sub('%PASSWORD', db_arr[3], content)
        content = re.sub('%HOST', db_arr[0], content)
        content = re.sub('%PORT', db_arr[1], content)
        content = re.sub('%DB', db_arr[4], content)
        self._write_file(content, os.path.join(resources_dir, 'datasource.properties'))
        # MyBatis映射文件
        db_arr = db_conn.split('/')
        if len(db_arr) == 6:
            db_util = db.MySqlUtil(db_arr[0], db_arr[1], db_arr[2], db_arr[3], db_arr[4], db_arr[5])
        else:
            db_util = db.MySqlUtil(db_arr[0], db_arr[1], db_arr[2], db_arr[3], db_arr[4])
        db_info = db_util.get_db_info()
        self._create_mapper(os.path.join(resources_dir, 'mappers'), base_package, db_info)

    # 生成webapp
    def _create_webapp(self, webapp_dir, base_package):
        os.makedirs(webapp_dir)
        # index.jsp
        self._write_default_file('templates/spring-mvc/index.jsp', os.path.join(webapp_dir, 'index.jsp'))
        # web.xml
        self._create_file_with_replace(os.path.join(webapp_dir, 'WEB-INF'), 'web.xml', base_package)

    # 生成test文件夹
    @staticmethod
    def _create_test(test_dir):
        os.makedirs(os.path.join(test_dir, 'java'))
        os.makedirs(os.path.join(test_dir, 'resources'))

    # 生成pom.xml文件
    def _create_pom(self, project_dir, group_id, artifact_id, version):
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        # pom.xml
        f = os.path.join(project_dir, 'pom.xml')
        content = self._get_template('templates/spring-mvc/pom.xml')
        # 替换占位符
        content = re.sub('%GROUP_ID', group_id, content)
        content = re.sub('%ARTIFACT_ID', artifact_id, content)
        content = re.sub('%VERSION', version, content)
        self._write_file(content, f)

    # 生成.gitignore文件
    def _create_git_ignore(self, project_dir):
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        # .gitignore
        f = os.path.join(project_dir, '.gitignore')
        self._write_default_file('templates/spring-mvc/.gitignore', f)

    # 入口
    def create(self, root_dir, group_id, artifact_id, version, db_conn):
        # 清理输出文件夹
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
        else:
            shutil.rmtree(root_dir)
            os.makedirs(root_dir)
        # 项目文件夹
        project_dir = os.path.join(root_dir, artifact_id)
        # pom.xml
        self._create_pom(project_dir, group_id, artifact_id, version)
        # .gitignore
        self._create_git_ignore(project_dir)
        # src文件夹
        src_dir = os.path.join(project_dir, 'src')
        # main文件夹
        main_dir = os.path.join(src_dir, 'main')
        # java源文件文件夹
        self._create_java(os.path.join(main_dir, 'java'), group_id, db_conn)
        # 资源文件文件夹
        self._create_resources(os.path.join(main_dir, 'resources'), group_id, db_conn)
        # webapp文件夹
        self._create_webapp(os.path.join(main_dir, 'webapp'), group_id)
        # 单元测试文件夹
        self._create_test(os.path.join(src_dir, 'test'))
