import pymysql


class MySqlUtil:
    def __init__(self, host, port, user, password, database, charset='utf8'):
        """
        初始化数据库连接
        :param host: 数据库主机地址
        :param port: 端口
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名
        :param charset: 编码
        """
        if not type(port) == int:
            port = int(port)
        conn = pymysql.connect(host=host, port=port,
                               user=user, password=password,
                               database=database, charset=charset)
        self._connection = conn
        self._cursor = conn.cursor()

    def get_tables(self):
        """
        查询数据库中的所有表
        :return: 表集合
        """
        sql = 'show tables'
        self._cursor.execute(sql)
        result = []
        for table in self._cursor.fetchall():
            result.append(table[0])
        return result

    def get_columns(self, table_name):
        """
        获取表中的所有列
        :param table_name: 表名
        :return: (列名+类型)集合
        """
        sql = 'desc ' + table_name
        self._cursor.execute(sql)
        result = []
        for column in self._cursor.fetchall():
            result.append({'name': column[0], 'type': column[1], 'is_primary_key': column[3] == 'PRI'})
        return result

    def get_db_info(self):
        """
        获取数据库的信息
        :return: 表名和对应的列
        """
        result = {}
        table_arr = self.get_tables()
        for item in table_arr:
            column_arr = self.get_columns(item)
            result[item] = column_arr
        return result
