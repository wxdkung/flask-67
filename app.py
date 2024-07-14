from flask import Flask, render_template, request, redirect, session 
import mysql.connector

app = Flask(__name__)

#for from
app.config['SECRET_KEY'] = 'Wudza555'

#for Db
db_host = "localhost"
db_user = "root"
db_pass = ""
db_name = "flower"

@app.route("/home")
def home():
    #return"<h1>Home</h1>"
    name = "Lisa"
    age = 27
    my_dict = {"name": "Lisa", "age": 27}
    return render_template("home.html", name=name, age=age, my_dict=my_dict)

@app.route("/create", methods=["GET"])
def create():
    return render_template("create.html")

@app.route("/store", methods=["POST"])
def store():
    if request.method == "POST":
        flower_name = request.form['flower_name']
        lat_num = request.form['lat_num']
        long_num = request.form['long_num']
        place = request.form['place']
        detail = request.form['detail']
        print(flower_name, lat_num, long_num, place, detail)


        my_db = mysql.connector.connect(
            host = db_host,
            user = db_user,
            password = db_pass,
            db = db_name
        )
        my_cursor = my_db.cursor(dictionary=True)
        sql = "INSERT INTO flowers (flower_name , lat_num , long_num , place , detail) VALUES (%s,%s,%s,%s,%s)"
        val = (flower_name, lat_num, long_num, place, detail)
        my_cursor.execute(sql, val)
        my_db.commit()
    
        session['alert_status'] = "success"
        session['alert_message'] = "Already Created!"
        return redirect('/')
    else :
        session['alert_status'] = "fail"
        session['alert_message'] = "Something went wrong!"
        return redirect('/')

@app.route("/")
def index():
        my_db = mysql.connector.connect(
            host = db_host,
            user = db_user,
            password = db_pass,
            db = db_name
        )
        my_cursor = my_db.cursor(dictionary=True)
        sql = "SELECT * FROM flowers"
        my_cursor.execute(sql)
        results = my_cursor.fetchall()

        #show Message
        if 'alert_status' in session and 'alert_message' in session:
            alert_message = {
                'status' : session['alert_status'],
                'message' : session['alert_message']
            }
            del session['alert_status']
            del session['alert_message']
        else:
            alert_message = {
                'status' : None,
                'message' : None
        }
        return render_template("index.html", alert_message = alert_message, results = results)

@app.route("/edit/<flower_id>", methods=['GET'])
def edit(flower_id):
    # Conect database
    my_db = mysql.connector.connect(
            host = db_host,
            user = db_user,
            password = db_pass,
            db = db_name
        )
    my_cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM flowers WHERE id = " + flower_id
    my_cursor.execute(sql)
    results = my_cursor.fetchall()
    return render_template("edit.html", results = results)

@app.route("/update/<flower_id>", methods=["POST"])
def update(flower_id):
    if request.method == "POST":
        flower_name = request.form['flower_name']
        lat_num = request.form['lat_num']
        long_num = request.form['long_num']
        place = request.form['place']
        detail = request.form['detail']
        print(flower_name, lat_num, long_num, place, detail)

        # Conect database
        my_db = mysql.connector.connect(
            host = db_host,
            user = db_user,
            password = db_pass,
            db = db_name
        )
        my_cursor = my_db.cursor(dictionary=True)
        sql = """
            UPDATE flowers
            SET flower_name = %s,
            lat_num = %s,
            long_num = %s,
            place = %s,
            detail = %s
            WHERE id = %s
        """ 
        val = (flower_name, lat_num, long_num, place, detail, flower_id)
        my_cursor.execute(sql, val)
        my_db.commit()


        session['alert_status'] = "success"
        session['alert_message'] = "Already Created!"
        return redirect('/')
    else :
        session['alert_status'] = "fail"
        session['alert_message'] = "Something went wrong!"
        return redirect('/')
    

@app.route("/delete/<flower_id>", methods=['GET'])
def delete(flower_id):
    # Conect database
    my_db = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_pass,
        db = db_name
    )
    my_cursor = my_db.cursor(dictionary=True)
    sql = "DELETE FROM flowers WHERE id = %s"
    val = (flower_id,)
    my_cursor.execute(sql, val)
    my_db.commit()

    session['alert_status'] = "success"
    session['alert_message'] = "Already Delete!"
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
    # app.run()

