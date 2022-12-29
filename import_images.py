import mysql.connector
import pandas as pd

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertBLOB(connection, cursor, emp_number,epic_picture,epic_filename,epic_type,epic_file_size,epic_file_width,epic_file_height):
    try:
        sql_insert_blob_query = """ INSERT INTO hs_hr_emp_picture
                            (emp_number,epic_picture,epic_filename,epic_type,epic_file_size,epic_file_width,epic_file_height)
                            VALUES (%s,%s,%s,%s,%s,%s,%s)"""

        empPicture = convertToBinaryData(epic_picture)

        # Convert data into tuple format
        insert_blob_tuple = (emp_number, empPicture, epic_filename, epic_type, epic_file_size, epic_file_width, epic_file_height)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))


try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                            port='3333',
                                            database='orangehrm',
                                            user='root',
                                            password='orangehrm')

    cursor = connection.cursor()

    df = pd.read_csv(
        './get_images/result/combine_images.csv',
        header=None,
        names=['emp_number', 'epic_picture','epic_filename','epic_type','epic_file_size','epic_file_width','epic_file_height'],
        sep=';'
    )
    for _, row in df.iterrows():
        insertBLOB(
            connection,
            cursor,
            row['emp_number'],
            row['epic_picture'],
            row['epic_filename'],
            row['epic_type'],
            row['epic_file_size'],
            row['epic_file_width'],
            row['epic_file_height']
        )
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")