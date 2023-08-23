from flask import Flask, render_template , request , redirect ,url_for
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '22@Pugazh'
app.config['MYSQL_DB'] = 'store'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
@app.route('/')
def nav():
    cur = mysql.connection.cursor()
    cur.execute("SELECT cname,cashbal FROM company")
    fetchd = cur.fetchall()
    
    cur.execute("SELECT items.ino,items.iname,astocks.rqty,astocks.rate,astocks.sp FROM items inner join astocks on items.ino = astocks.ino")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template("home.html", users=fetchdata,com=fetchd)

@app.route('/purchase', methods=['GET','POST'])
def pur():
    msg=''
    if request.method == 'POST' and 'itemName' in request.form and 'quantity' in request.form and 'rate' in request.form and 'sellingPrice' in request.form:
        n = request.form['itemName']
        t = request.form['quantity']
        d = request.form['rate']
        g = request.form['sellingPrice']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT iname FROM items WHERE iname = % s', (n))
        result = cursor.fetchone()
        if result:
            msg = 'already exists !'
        else:
            cursor.execute('INSERT INTO astocks(rqty,rate,sp) VALUES (% s, % s, % s)', (t, d, g))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
        return render_template('/', msg=msg)    
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("purchase.html", msg=msg)



@app.route('/sales')
def sales():
    msg=''
    if request.method == 'POST' and 'itemName' in request.form and 'quantity' in request.form:
        n = request.form['itemName']
        t = request.form['quantity']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT iname FROM sales WHERE iname = % s', (n))
        result = cursor.fetchone()
        if result:
            msg = 'already exists !'
        else:
            cursor.execute('INSERT INTO astocks(rqty,rate,sp) VALUES (% s, %s)', (n,t))
            mysql.connection.commit()
            msg = 'You have successfully Sold the product !'
        return render_template('/', msg=msg)    
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("sales.html",msg=msg)

@app.route('/success')
def success():
    return render_template("success.html")
if __name__ == "__main__":
    app.run(debug=True)
