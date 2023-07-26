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
    database='evaluationsystem',
    charset='utf8'
)

@app.route('/compare', methods=['POST'])
def compare():
    # Get infoID from the POST request
    info_id = request.json.get('infoID', None)

    if info_id is None:
        return 'Missing infoID', 400

    cursor = cnx.cursor()

    # Execute the query with the given infoID
    query = '''
    SELECT *
    FROM `delete_logs_table`
    WHERE `Log_Type` IN ('Delete_Notification', 'Delete_Confirmation') AND `infoID` = %s
    '''
    cursor.execute(query, (info_id,))

    # Get the query results
    results = cursor.fetchall()

    # Extract "Delete Request" and "Delete Notification" rows
    delete_request = None
    delete_notification = None

    for row in results:
        log_type = row[2]

        if log_type == 'Delete_Notification':
            delete_request = row
        elif log_type == 'Delete_Confirmation':
            delete_notification = row

    # Compare and build the result dictionary
    result_dict = {}

    if delete_request is not None and delete_notification is not None:
        column_names = cursor.column_names
        deleteConEvaRet = 1  # Deletion consistency evaluation result, default value is 1

        for column_name in column_names:
            if column_name not in ['Log_Type']:
                request_value = delete_request[column_names.index(column_name)]
                notification_value = delete_notification[column_names.index(column_name)]

                if request_value != notification_value:
                    deleteConEvaRet = 0
                    break

        result_dict['deleteConEvaRet'] = deleteConEvaRet

    # Generate the JSON file
    #output_file = f'comparison_result2_{info_id}.json'
    output_file = f'comparison_result2.json'

    with open(output_file, 'w') as f:
        json.dump(result_dict, f, indent=4)

    cursor.close()

    return f"Comparison result for infoID {info_id} has been saved to the file: {output_file}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
