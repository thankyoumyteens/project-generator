def get_class_name(table_name):
    words = table_name.split('_')
    result = ''
    for word in words:
        result = result + word[0:1].upper() + word[1:]
    return result


def get_field_name(column_name):
    words = column_name.split('_')
    result = words.pop(0)
    for word in words:
        result = result + word[0:1].upper() + word[1:]
    return result


def get_java_type(column_type):
    db_type = column_type
    if '(' in column_type:
        db_type = column_type[:column_type.index('(')]
    if db_type == 'bigint':
        result = 'Long'
    elif db_type == 'integer':
        result = 'Integer'
    elif db_type == 'varchar':
        result = 'String'
    elif db_type == 'timestamp':
        result = 'java.util.Date'
    elif db_type == 'decimal':
        result = 'java.math.BigDecimal'
    elif db_type == 'bit':
        result = 'Boolean'
    else:
        result = 'String'
    return result


def get_type_map(column_type):
    db_type = column_type
    if '(' in column_type:
        db_type = column_type[:column_type.index('(')]
    if db_type == 'bigint':
        result = ('java.lang.Long', 'BIGINT')
    elif db_type == 'integer':
        result = ('java.lang.Integer', 'INTEGER')
    elif db_type == 'varchar':
        result = ('java.lang.String', 'VARCHAR')
    elif db_type == 'timestamp':
        result = ('java.util.Date', 'TIMESTAMP')
    elif db_type == 'decimal':
        result = ('java.math.BigDecimal', 'DECIMAL')
    elif db_type == 'bit':
        result = ('java.lang.Boolean', 'BIT')
    else:
        result = ('java.lang.String', 'VARCHAR')
    return result


if __name__ == '__main__':
    print(get_class_name('mobile_user_hahaha'))
    print(get_field_name('mobile_user_hahaha'))
    print(get_java_type('varchar(20)'))
