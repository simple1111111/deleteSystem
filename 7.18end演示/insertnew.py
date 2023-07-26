from flask import Flask, request
import json
import mysql.connector

app = Flask(__name__)

@app.route('/receive_files', methods=['POST'])
def receive_files():
    # 从请求中获取上传的文件
    files = request.files.getlist('file')

    # 调用处理函数来解析JSON文件并插入到数据库
    result = process_json_files(files)

    if result:
        return 'Files received and data inserted successfully.'
    else:
        return 'An error occurred while processing the files.'

def process_json_files(files):
    # 连接到数据库
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='test',
        password='123456',
        database='evaluationSystem',
        charset='utf8mb4'
    )
    cursor = cnx.cursor()

    # 创建 delete logs table...
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS `delete_logs_table` (
            `deletePerformer` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `deletePerformTime` VARCHAR(100) DEFAULT NULL,
            `Log_Type` VARCHAR(100) DEFAULT NULL,
            `infoType` INT DEFAULT NULL,
            `infoOwner` VARCHAR(100) DEFAULT NULL,
            `infoCreator` VARCHAR(100) DEFAULT NULL,
            `infoCreateTime` VARCHAR(100) DEFAULT NULL,
            `infoCreateLoc` VARCHAR(100) DEFAULT NULL,
            `infoID` VARCHAR(100) DEFAULT NULL,
            `delete_granularity` VARCHAR(100) DEFAULT NULL,
            `deleteDupInfoID` VARCHAR(100) DEFAULT NULL,
            `deleteIntention` VARCHAR(100) DEFAULT NULL,
            `deleteRequirements` VARCHAR(100) DEFAULT NULL,
            `deleteControlSet` TEXT DEFAULT NULL,
            `deleteAlg` VARCHAR(100) DEFAULT NULL,
            `deleteAlgParam` VARCHAR(100) DEFAULT NULL,
            `deleteLevel` INT DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
    cursor.execute(create_table_query)

    print(create_table_query)

    # 解析JSON文件并插入到数据库
    for file in files:
        # 解析JSON数据
        json_data = json.load(file)

        print(json_data)

        # 从JSON数据中提取字段的值，如果字段不存在，则设置为None
        deletePerformer = json_data.get('deletePerformer', None)
        deletePerformTime = json_data.get('deletePerformTime', None)
        log_type = json_data.get('Log_Type', None)
        infoType = json_data.get('infoType', None)
        infoOwner = json_data.get('infoOwner', None)
        infoCreator = json_data.get('infoCreator', None)
        infoCreateTime = json_data.get('infoCreateTime', None)
        infoCreateLoc = json_data.get('infoCreateLoc', None)
        infoID = json_data.get('infoID', None)
        delete_granularity = json_data.get('delete_granularity', None)
        deleteDupInfoID = json_data.get('deleteDupInfoID', None)
        deleteIntention = json_data.get('deleteIntention', None)
        deleteRequirements = json_data.get('deleteRequirements', None)
        deleteControlSet = json_data.get('deleteControlSet', None)
        deleteAlg = json_data.get('deleteAlg', None)
        deleteAlgParam = json_data.get('deleteAlgParam', None)
        deleteLevel = json_data.get('deleteLevel', None)

        # 将 deleteDupInfoID 列表转换为逗号分隔的字符串
        deleteDupInfoID = ','.join(deleteDupInfoID) if isinstance(deleteDupInfoID, list) else None

        # 将 deleteControlSet 列表转换为字符串
        deleteControlSet = json.dumps(deleteControlSet) if isinstance(deleteControlSet, list) else None

        # 构建插入SQL语句
        insert_query = '''
            INSERT INTO `delete_logs_table` (`deletePerformer`, `deletePerformTime`, `Log_Type`, `infoType`, `infoOwner`,
            `infoCreator`, `infoCreateTime`, `infoCreateLoc`, `infoID`, `delete_granularity`, `deleteDupInfoID`,
            `deleteIntention`, `deleteRequirements`, `deleteControlSet`, `deleteAlg`, `deleteAlgParam`, `deleteLevel`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
        values = (
            deletePerformer, deletePerformTime, log_type, infoType, infoOwner, infoCreator, infoCreateTime,
            infoCreateLoc, infoID, delete_granularity, deleteDupInfoID, deleteIntention, deleteRequirements,
            deleteControlSet, deleteAlg, deleteAlgParam, deleteLevel
        )

        # 执行插入操作
        cursor.execute(insert_query, values)

    # 提交事务
    cnx.commit()

    cursor.close()
    cnx.close()

    return True




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
