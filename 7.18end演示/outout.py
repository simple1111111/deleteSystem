import mysql.connector
import json
from flask import Flask, request

# Create a Flask application
app = Flask(__name__)

# Connect to the database
cnx = mysql.connector.connect(
    host='127.0.0.1',
    user='test',
    password='123456',
    database='evaluationSystem',
    charset='utf8'
)

@app.route('/compare', methods=['POST'])
def compare():
    # Get infoID from the POST request
    info_id = request.json.get('infoID', None)

    if info_id is None:
        return 'Missing infoID', 400

    cursor = cnx.cursor()

    # First comparison
    query1 = '''
    SELECT *
    FROM `delete_logs_table`
    WHERE `Log_Type` IN ('Delete_Request', 'Delete_Notification') AND `infoID` = %s
    '''
    cursor.execute(query1, (info_id,))
    results1 = cursor.fetchall()
    delete_request1 = None
    delete_notification1 = None

    for row in results1:
        log_type = row[2]
        if log_type == 'Delete_Request':
            delete_request1 = row
        elif log_type == 'Delete_Notification':
            delete_notification1 = row
    
    deleteConEvaRet1 = 0
    if delete_request1 is not None and delete_notification1 is not None:
        column_names = cursor.column_names
        deleteConEvaRet1 = 1  # Deletion consistency evaluation result, default value is 1

        for column_name in column_names:
            if column_name not in ['Log_Type']:
                request_value = delete_request1[column_names.index(column_name)]
                notification_value = delete_notification1[column_names.index(column_name)]

                if request_value != notification_value:
                    deleteConEvaRet1 = 0
                    break

    # Second comparison
    query2 = '''
    SELECT *
    FROM `delete_logs_table`
    WHERE `Log_Type` IN ('Delete_Notification', 'Delete_Confirmation') AND `infoID` = %s
    '''
    cursor.execute(query2, (info_id,))
    results2 = cursor.fetchall()
    delete_request2 = None
    delete_notification2 = None

    for row in results2:
        log_type = row[2]
        if log_type == 'Delete_Notification':
            delete_request2 = row
        elif log_type == 'Delete_Confirmation':
            delete_notification2 = row

    deleteConEvaRet2 = 0
    if delete_request2 is not None and delete_notification2 is not None:
        column_names = cursor.column_names
        deleteConEvaRet2 = 1  # Deletion consistency evaluation result, default value is 1

        for column_name in column_names:
            if column_name not in ['Log_Type']:
                request_value = delete_request2[column_names.index(column_name)]
                notification_value = delete_notification2[column_names.index(column_name)]

                if request_value != notification_value:
                    deleteConEvaRet2 = 0
                    break

    # Get DeletePerformer, deletePerformTime, deleteLevel from Delete Operation
    query3 = '''
    SELECT DeletePerformer, deletePerformTime, deleteLevel
    FROM `delete_logs_table`
    WHERE `Log_Type` = 'Delete_Operation' AND `infoID` = %s
    '''
    cursor.execute(query3, (info_id,))
    result3 = cursor.fetchone()

    if result3 is None:
        return 'No matching record found', 404

    delete_performer = result3[0]
    delete_perform_time = result3[1]
    delete_level = result3[2]

    delete_effect_eva_ret = 0
    if deleteConEvaRet1 == 1 and deleteConEvaRet2 == 1:
        delete_effect_eva_ret = 2
    elif deleteConEvaRet1 == 1 or deleteConEvaRet2 == 1:
        delete_effect_eva_ret = 1

    delete_perform_time = str(delete_perform_time)  # Convert delete_perform_time to string

    result_dict = {
    "DataType": 0x42,
    "content": {
        'deleteConEvaRet': deleteConEvaRet1 + deleteConEvaRet2,
        'DeletePerformer': delete_performer,
        'deletePerformTime': delete_perform_time,
        'deleteLevel': delete_level,
        'deleteEffectEvaRet': delete_effect_eva_ret
    }
}

    # Generate the JSON file
    output_file = 'result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, indent=4, ensure_ascii=False)

    print(f"结果已保存至{output_file}文件")

    cursor.close()
    cnx.close()

    return 'Comparison completed and result saved.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
