from flask import Flask, render_template, request, redirect, url_for, flash,jsonify, request
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcrud'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/getAll',methods=['GET'])
def getAll():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return jsonify({"data":data})


@app.route('/getAllById/<id>',methods=['GET'])
def getAllById(id):
    print("holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(id)
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    return jsonify({"data":data})


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.json['fullname']
        phone = request.json['phone']
        email = request.json['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro exitoso"})

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.json['fullname']
        phone = request.json['phone']
        email = request.json['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro actualizado"})

@app.route('/delete/<id>', methods = ['GET'])
def delete_contact(id):
    
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = %s', (id,))
    mysql.connection.commit()
    return jsonify({"informacion":"Registro eliminado"})

@app.route('/login',methods=['GET'])
def login():
    user = request.json['user']
    password = request.json['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE user = %s and password =%s", (user,password))
    ###cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    print("enviado")
   
    if len(data)==0 :
        return jsonify({"data":0})
    else :
        return jsonify({"data":data})

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
