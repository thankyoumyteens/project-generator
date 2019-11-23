import os
import shutil
import re


class SpringMvcCreator:

    @staticmethod
    def _get_template(template_file):
        """
        读取模板文件内容
        :param template_file: 模板文件路径
        :return: 模板文件内容
        """
        with open(template_file, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    @staticmethod
    def _write_file(content, target_file):
        """
        将内容写入文件
        :param content: 内容
        :param target_file: 文件路径
        :return:
        """
        with open(target_file, 'w', encoding='utf-8') as file:
            file.write(content)

    def _write_default_file(self, template_file, target_file):
        """
        将模板文件的内容写入新文件
        :param template_file: 模板文件路径
        :param target_file: 新文件路径
        :return:
        """
        content = self._get_template(template_file)
        self._write_file(content, target_file)

    def _create_file_with_replace(self, file_dir, file, base_package):
        """
        生成文件, 并将包名写入
        :param file_dir: 文件所在的文件夹
        :param file: 文件名
        :param base_package: 包
        :return:
        """
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = os.path.join(file_dir, file)
        content = self._get_template('templates/spring-mvc/' + file)
        # 替换包名
        content = re.sub('%BASE_PACKAGE', base_package, content)
        self._write_file(content, f)

    def _create_java(self, java_dir, base_package):
        """
        生成java源代码
        :param java_dir: java文件夹
        :param base_package: 包
        :return:
        """
        packages = base_package.split('.')
        for package in packages:
            java_dir = os.path.join(java_dir, package)
        # controller
        controller_package = os.path.join(java_dir, 'controller')
        self._create_file_with_replace(controller_package, 'TestController.java', base_package)
        # dao
        dao_package = os.path.join(java_dir, 'dao')
        self._create_file_with_replace(dao_package, 'TestDao.java', base_package)
        # service
        service_package = os.path.join(java_dir, 'service')
        self._create_file_with_replace(service_package, 'TestService.java', base_package)
        # service impl
        service_impl_package = os.path.join(service_package, 'impl')
        os.makedirs(service_impl_package)
        # 实体类
        pojo_package = os.path.join(java_dir, 'pojo')
        self._create_file_with_replace(pojo_package, 'TestPoJo.java', base_package)
        # 过滤器
        filter_package = os.path.join(java_dir, 'filter')
        self._create_file_with_replace(filter_package, 'CORSFilter.java', base_package)
        # 拦截器
        interceptor_package = os.path.join(java_dir, 'interceptor')
        self._create_file_with_replace(interceptor_package, 'AuthorityInterceptor.java', base_package)

    def _create_resources(self, resources_dir, base_package):
        """
        生成资源文件夹
        :param resources_dir: 资源文件夹
        :param base_package: 包
        :return:
        """
        os.makedirs(resources_dir)
        # app.properties
        f = os.path.join(resources_dir, 'app.properties')
        self._write_default_file('templates/spring-mvc/app.properties', f)
        # applicationContext.xml
        self._create_file_with_replace(resources_dir, 'applicationContext.xml', base_package)
        # applicationContext-datasource.xml
        self._create_file_with_replace(resources_dir, 'applicationContext-datasource.xml', base_package)
        # dispatcher-servlet.xml
        self._create_file_with_replace(resources_dir, 'dispatcher-servlet.xml', base_package)
        # logback.xml
        self._create_file_with_replace(resources_dir, 'logback.xml', base_package)
        # datasource.properties
        f = os.path.join(resources_dir, 'datasource.properties')
        self._write_default_file('templates/spring-mvc/datasource.properties', f)
        # TestMapper.xml
        mappers_dir = os.path.join(resources_dir, 'mappers')
        self._create_file_with_replace(mappers_dir, 'TestMapper.xml', base_package)

    def _create_webapp(self, webapp_dir, base_package):
        """
        生成webapp
        :param webapp_dir: webapp文件夹
        :param base_package: 包
        :return:
        """
        os.makedirs(webapp_dir)
        # index.jsp
        f = os.path.join(webapp_dir, 'index.jsp')
        self._write_default_file('templates/spring-mvc/index.jsp', f)
        # web.xml
        web_inf_dir = os.path.join(webapp_dir, 'WEB-INF')
        self._create_file_with_replace(web_inf_dir, 'web.xml', base_package)

    @staticmethod
    def _create_test(test_dir):
        """
        生成test文件夹
        :param test_dir: test文件夹
        :return:
        """
        os.makedirs(os.path.join(test_dir, 'java'))
        os.makedirs(os.path.join(test_dir, 'resources'))

    def _create_pom(self, project_dir, group_id, artifact_id, version):
        """
        生成pom.xml文件
        :param project_dir: 项目文件夹
        :param group_id: Group Id
        :param artifact_id: Artifact Id
        :param version: 版本号
        :return:
        """
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

    def _create_git_ignore(self, project_dir):
        """
        生成.gitignore文件
        :param project_dir: 项目文件夹
        :return:
        """
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        # .gitignore
        f = os.path.join(project_dir, '.gitignore')
        self._write_default_file('templates/spring-mvc/.gitignore', f)

    def create(self, root_dir, group_id, artifact_id, version):
        # 清理输出文件夹
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
        else:
            shutil.rmtree(root_dir)
            os.makedirs(root_dir)
        # 项目文件夹
        project_dir = os.path.join(root_dir, artifact_id)
        # pom
        self._create_pom(project_dir, group_id, artifact_id, version)
        # git
        self._create_git_ignore(project_dir)
        # src文件夹
        src_dir = os.path.join(project_dir, 'src')
        # main文件夹
        main_dir = os.path.join(src_dir, 'main')
        # java源文件文件夹
        java_dir = os.path.join(main_dir, 'java')
        self._create_java(java_dir, group_id)
        # 资源文件文件夹
        resources_dir = os.path.join(main_dir, 'resources')
        self._create_resources(resources_dir, group_id)
        # webapp文件夹
        webapp_dir = os.path.join(main_dir, 'webapp')
        self._create_webapp(webapp_dir, group_id)
        # 单元测试文件夹
        test_dir = os.path.join(src_dir, 'test')
        self._create_test(test_dir)
