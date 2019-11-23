import os
import shutil
import re


def _get_template(template_file):
    with open(template_file, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def _write_file(content, target_file):
    with open(target_file, 'w', encoding='utf-8') as file:
        file.write(content)


def _write_default_file(template_file, target_file):
    content = _get_template(template_file)
    _write_file(content, target_file)


def create_java(java_dir, base_package):
    packages = base_package.split('.')
    for package in packages:
        java_dir = os.path.join(java_dir, package)
    controller_package = os.path.join(java_dir, 'controller')
    os.makedirs(controller_package)
    f = os.path.join(controller_package, 'TestController.java')
    content = _get_template('templates/spring-mvc/TestController.java')
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)
    dao_package = os.path.join(java_dir, 'dao')
    os.makedirs(dao_package)
    f = os.path.join(dao_package, 'TestDao.java')
    content = _get_template('templates/spring-mvc/TestDao.java')
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)
    service_package = os.path.join(java_dir, 'service')
    os.makedirs(service_package)
    f = os.path.join(service_package, 'TestService.java')
    content = _get_template('templates/spring-mvc/TestService.java')
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)
    service_impl_package = os.path.join(service_package, 'impl')
    os.makedirs(service_impl_package)
    pojo_package = os.path.join(java_dir, 'pojo')
    os.makedirs(pojo_package)
    f = os.path.join(pojo_package, 'TestPoJo.java')
    content = _get_template('templates/spring-mvc/TestPoJo.java')
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)
    filter_package = os.path.join(java_dir, 'filter')
    os.makedirs(filter_package)
    f = os.path.join(filter_package, 'CORSFilter.java')
    content = _get_template('templates/spring-mvc/CORSFilter.java')
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)
    interceptor_package = os.path.join(java_dir, 'interceptor')
    os.makedirs(interceptor_package)
    f = os.path.join(interceptor_package, 'AuthorityInterceptor.java')
    content = _get_template('templates/spring-mvc/AuthorityInterceptor.java')
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)


def create_resources(resources_dir, base_package):
    os.makedirs(resources_dir)
    # app.properties
    f = os.path.join(resources_dir, 'app.properties')
    _write_default_file('templates/spring-mvc/app.properties', f)
    # applicationContext.xml
    f = os.path.join(resources_dir, 'applicationContext.xml')
    content = _get_template('templates/spring-mvc/applicationContext.xml')
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)
    # applicationContext-datasource.xml
    f = os.path.join(resources_dir, 'applicationContext-datasource.xml')
    content = _get_template('templates/spring-mvc/applicationContext-datasource.xml')
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)
    # dispatcher-servlet.xml
    f = os.path.join(resources_dir, 'dispatcher-servlet.xml')
    content = _get_template('templates/spring-mvc/dispatcher-servlet.xml')
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)
    # logback.xml
    f = os.path.join(resources_dir, 'logback.xml')
    content = _get_template('templates/spring-mvc/logback.xml')
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)
    # datasource.properties
    f = os.path.join(resources_dir, 'datasource.properties')
    _write_default_file('templates/spring-mvc/datasource.properties', f)
    # TestMapper.xml
    mappers_dir = os.path.join(resources_dir, 'mappers')
    os.makedirs(mappers_dir)
    f = os.path.join(mappers_dir, 'TestMapper.xml')
    content = _get_template('templates/spring-mvc/TestMapper.xml')
    # 替换占位符
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)


def create_webapp(webapp_dir, base_package):
    os.makedirs(webapp_dir)
    # index.jsp
    f = os.path.join(webapp_dir, 'index.jsp')
    _write_default_file('templates/spring-mvc/index.jsp', f)
    # web.xml
    web_inf_dir = os.path.join(webapp_dir, 'WEB-INF')
    os.makedirs(web_inf_dir)
    f = os.path.join(web_inf_dir, 'web.xml')
    content = _get_template('templates/spring-mvc/web.xml')
    # 替换占位符
    content = re.sub('%BASE_PACKAGE', base_package, content)
    _write_file(content, f)


def create_test(test_dir):
    os.makedirs(os.path.join(test_dir, 'java'))
    os.makedirs(os.path.join(test_dir, 'resources'))


def create_pom(project_dir, group_id, artifact_id, version):
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    # pom.xml
    f = os.path.join(project_dir, 'pom.xml')
    content = _get_template('templates/spring-mvc/pom.xml')
    # 替换占位符
    content = re.sub('%GROUP_ID', group_id, content)
    content = re.sub('%ARTIFACT_ID', artifact_id, content)
    content = re.sub('%VERSION', version, content)
    _write_file(content, f)


def create_git_ignore(project_dir):
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    # .gitignore
    f = os.path.join(project_dir, '.gitignore')
    _write_default_file('templates/spring-mvc/.gitignore', f)


def create_spring_mvc_project(root_dir, group_id, artifact_id, version):
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    else:
        shutil.rmtree(root_dir)
        os.makedirs(root_dir)
    # 项目文件夹
    project_dir = os.path.join(root_dir, artifact_id)
    # pom
    create_pom(project_dir, group_id, artifact_id, version)
    # git
    create_git_ignore(project_dir)
    # src文件夹
    src_dir = os.path.join(project_dir, 'src')
    # main文件夹
    main_dir = os.path.join(src_dir, 'main')
    # java源文件文件夹
    java_dir = os.path.join(main_dir, 'java')
    create_java(java_dir, group_id)
    # 资源文件文件夹
    resources_dir = os.path.join(main_dir, 'resources')
    create_resources(resources_dir, group_id)
    # webapp文件夹
    webapp_dir = os.path.join(main_dir, 'webapp')
    create_webapp(webapp_dir, group_id)
    # 单元测试文件夹
    test_dir = os.path.join(src_dir, 'test')
    create_test(test_dir)


if __name__ == '__main__':
    create_spring_mvc_project('out', 'com.test', 'test-project', '1.0')
