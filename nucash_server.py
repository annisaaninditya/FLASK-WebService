from flask import Flask, request
from flask_mysqldb import MySQL
from flask import jsonify
import flask
import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'dananutest'
mysql = MySQL(app)

#GET Provinsi
@app.route('/nu-server/api/dananu/App')
def prov():
    headers = request.headers
    auth = headers.get("dananu-key")
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM `keys` WHERE `key`= " + "'" + str(auth) +"'")
    
    if result and request.method == "GET":
        cur.execute("SELECT * FROM `provinsi`")
        row_headers=[x[0] for x in cur.description] 
        res = cur.fetchall()
        json_data=[]
        for result in res:
            json_data.append(dict(zip(row_headers,result)))
            return jsonify({
                    'status': True, 
                    'responsecode': 200,
                    'data': json_data
                    })
    else:
         return not_found
     
#GET Kota/ID
@app.route('/nu-server/api/dananu/App&id_provinsi=<int:id_provinsi_fk>')
def kota(id_provinsi_fk):
    headers = request.headers
    auth = headers.get("dananu-key")
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM `keys` WHERE `key`= " + "'" + str(auth) +"'")
    
    if result and request.method == "GET":
        cur.execute("SELECT * FROM `kota` WHERE `id_provinsi_fk` =" + str(id_provinsi_fk))
        row_headers=[x[0] for x in cur.description] 
        res = cur.fetchall()
        json_data=[]
        for result in res:
            json_data.append(dict(zip(row_headers,result)))
            return jsonify({
                    'status': True,
                    'responsecode': 200,
                    'data': json_data
                    })
    else:
         return not_found
    
#GET Kecamatan/ID
@app.route('/nu-server/api/dananu/App&id_kota=<int:id_kota_fk>')
def Kecamatan(id_kota_fk):
    headers = request.headers
    auth = headers.get("dananu-key")
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM `keys` WHERE `key`= " + "'" + str(auth) +"'")
    
    if result and request.method == "GET":
        cur.execute("SELECT * FROM `kecamatan` WHERE `id_kota_fk` =" + str(id_kota_fk))
        row_headers=[x[0] for x in cur.description] 
        res = cur.fetchall()
        json_data=[]
        for result in res:
            json_data.append(dict(zip(row_headers,result)))
            return jsonify({
                    'status': True,
                    'responsecode': 200,
                    'data': json_data
                    })
    else:
         return not_found

#GET USER/Card No
@app.route('/nu-server/api/dananu/&card_no =<int:CARD_NO>')
def user(CARD_NO):
    headers = request.headers
    auth = headers.get("dananu-key")
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM `keys` WHERE `key`= " + "'" + str(auth) +"'")
    
    if result and request.method == "GET":
        cur.execute("SELECT * FROM `nu_user_information` WHERE `CARD_NO` =" + str(CARD_NO))
        row_headers=[x[0] for x in cur.description] 
        res = cur.fetchall()
        json_data=[]
        for result in res:
            json_data.append(dict(zip(row_headers,result)))
            return jsonify({
                    'status': True, 
                    'responsecode': 200, 
                    'data': json_data
                    })
    else:
         return not_found

#GET user banom
@app.route('/user/<banom>')
def banom(banom):
    headers = request.headers
    auth = headers.get("dananu-key")
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM `keys` WHERE `key`= " + "'" + str(auth) +"'")
    
    if result and request.method == "GET":
        cur.execute("SELECT * FROM `nu_user_information` WHERE `banom` =" + str(banom))
        row_headers=[x[0] for x in cur.description] 
        res = cur.fetchall()
        json_data=[]
        for result in res:
            json_data.append(dict(zip(row_headers,result)))
            return jsonify({
                    'status': True, 
                    'responsecode': 200, 
                    'data': json_data
                    })
    else:
         return not_found
     
#GET banom
@app.route('/banom_id')
def banom_id():
    headers = request.headers
    auth = headers.get("dananu-key")
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM `keys` WHERE `key`= " + "'" + str(auth) +"'")
    
    if result and request.method == "GET":
        cur.execute("SELECT * FROM `nu_banom`")
        row_headers=[x[0] for x in cur.description] 
        res = cur.fetchall()
        json_data=[]
        for result in res:
            json_data.append(dict(zip(row_headers,result)))
            return jsonify({
                    'status': True,
                    'responsecode': 200,
                    'data': json_data
                    })
    else:
         return not_found
     

#post user
@app.route('/nu-server/api/dananu/', methods=['POST'])
def adduser():
    headers = request.headers
    auth = headers.get("dananu-key")
    db = mysql.connection
    cur = db.cursor()
    input_body = request.get_json()
    USER_ID = input_body['USER_ID']
    CARD_NO = input_body['CARD_NO']
    NAME = input_body['NAME']
    NIK = input_body['NIK']
    PBNU = input_body['PBNU']
    PWNU = input_body['PWNU']
    PCNU = input_body['PCNU']
    MWC = input_body['MWC']
    PCI = input_body['PCI']
    code_referal = input_body['code_referal']
    simpatisan = input_body['simpatisan']
    banom = input_body['banom']
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    query = """
        SELECT * FROM `keys` WHERE `key`= '%s'
    """ % (auth)
    dananu_key = cur.execute(query)
    
    if dananu_key:
        query = """
            SELECT * FROM nu_user_information WHERE CARD_NO= '%s'
        """ % (CARD_NO)
        card_id = cur.execute(query)

        if card_id:
            query = """
                UPDATE nu_user_information 
                SET PBNU = '%s', PWNU = '%s', PCNU = '%s', MWC = '%s', PCI = '%s', code_referal = '%s', simpatisan = '%s', banom = '%s' 
                WHERE CARD_NO = '%s'
            """ % (PBNU, PWNU, PCNU, MWC, PCI, code_referal, simpatisan, banom, CARD_NO)
            cur.execute(query)
            db.commit()
            return flask.jsonify({
                "status": True,
                "responscode": 201,
                "message": "insert successful"
            })
        else:
            query = """
                INSERT INTO nu_user_information (USER_ID, CARD_NO, NAME, NIK, PBNU, PWNU, PCNU, MWC, PCI, code_referal, simpatisan, banom, insert_date) 
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
            """ % (USER_ID, CARD_NO, NAME, NIK, PBNU, PWNU, PCNU, MWC, PCI, code_referal, simpatisan, banom, now)
            cur.execute(query)
            db.commit()
            return flask.jsonify({
                "status": True,
                "responscode": 201,
                "message": "insert successful"
            })
    else:
        return insert_failed
    
@app.errorhandler(404)
def insert_failed(error=None):
    message = {
            "status": False,
            "responscode": 404,
            "message": "insert failed",
            }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': False,
        'error': 'Invalid API key',
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':
   app.run()