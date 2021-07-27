from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'oldFaithfulGeyser'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'SU2021 IS601'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM ERUPTION_DATA')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, data=result)


@app.route('/view/<int:event_id>', methods=['GET'])
def record_view(event_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM ERUPTION_DATA WHERE eventID=%s', event_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', data=result[0])


@app.route('/edit/<int:event_id>', methods=['GET'])
def form_edit_get(event_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM ERUPTION_DATA WHERE eventID=%d', event_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', data=result[0])


@app.route('/edit/<int:event_id>', methods=['POST'])
def form_update_post(event_id):
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('eruptionLength'), request.form.get('eruptionWait'))
    sql_update_query = """UPDATE ERUPTION_DATA t SET t.eruptionLength = %d, t.eruptionWait = %d WHERE t.eventID = %d """
    cursor.execute(sql_update_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='Geyser Eruption Log')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('eruptionLength'), request.form.get('eruptionWait'))
    sql_insert_query = """INSERT INTO ERUPTION_DATA (eruptionLength,eruptionWait) VALUES (%d, %d) """
    cursor.execute(sql_insert_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:event_id>', methods=['POST'])
def form_delete_post(event_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM ERUPTION_DATA WHERE eventID = %d """
    cursor.execute(sql_delete_query, event_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM ERUPTION_DATA')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:event_id>', methods=['GET'])
def api_retrieve(event_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM ERUPTION_DATA WHERE eventID=%d', event_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:event_id>', methods=['PUT'])
def api_edit(event_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/cities/<int:event_id>', methods=['DELETE'])
def api_delete(event_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
