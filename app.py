from flask import Flask, render_template, flash, request, redirect, url_for, session
from form import saveForm, registerForm, loginForm
import json
from flask import jsonify
from flask_mysqldb import MySQL

app = Flask("__name__")
app.config['SECRET_KEY'] = 'something is here'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'
mysql = MySQL(app)

#----------------- SAVE DATA FROM HOME -------------------#
@app.route('/home', methods=['GET','POST'])
def home():
    form = saveForm(request.form)
    if request.method == 'POST':
        if(request.form['action'] == "Save"):
                if(form.validate()):
                        cur = mysql.connection.cursor()
                        sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
                        values = (request.form['id'], request.form['name'], request.form['dob'], request.form['rank'], request.form['address'])
                        cur.execute(sql,values)
                        mysql.connection.commit()
                        cur.close()
                        flash('Saving sucessful!')
                else:
                        flash('Error: All fields are required')

        elif(request.form['action'] == "List"):

                return redirect(url_for('list'))

    else:
            print('Error: something is wrong with form!')

    return render_template('index.html',form=form)


#----------------- SHOW LIST -------------------#
@app.route('/list', methods=['GET', 'POST'])
def list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee")
    data = cur.fetchall()    
    return render_template('list.html', data=data)


#----------------- SEARCH -------------------#
@app.route('/search', methods=["GET", "POST"]) 
def search():
        searchVal = request.form['searchval']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employee WHERE id LIKE %s OR name LIKE %s", ("%" + searchVal + "%","%" + searchVal + "%"))
        data = cur.fetchall()
        return render_template('search.html', data=data)


#----------------- REGISTER -------------------#
@app.route('/register', methods=["GET","POST"])
def register():
        form = registerForm(request.form)
        if request.method == "POST" and form.validate():
                username = request.form["username"]
                email = request.form["email"]
                password = request.form["password"]

                cur = mysql.connection.cursor()
                sql = "INSERT INTO user (username,email,password) VALUES (%s, %s, %s)"
                values = (username, email, password)
                cur.execute(sql,values)
                mysql.connection.commit()
                cur.close()
                flash('Registered sucessful!')
        return render_template('register.html', form=form)


#----------------- LOGIN -------------------#
@app.route('/', methods = ["GET", "POST"])
def login():
        form = loginForm(request.form)
        if session.get("userdata") is None:
                session["userdata"] = []

                if request.method == "POST" and form.validate():
                        login_user = request.form["username"]
                        password = request.form["password"]

                        cur = mysql.connection.cursor()
                        sql = ("SELECT * FROM user WHERE username='"+login_user+"'")
                        cur.execute(sql)
                        data = cur.fetchall()

                        if data:
                                for pass_in_db in data:
                                        if pass_in_db[3] == password:
                                                session["userdata"].append(login_user)
                                                session["userdata"].append(password)
                                                userdata = session["userdata"]
                                                return redirect(url_for('home'))
                                        else:
                                                flash("Error: Username and password combination is wrong!!")
                        else:
                                flash("Error: There is no account for this username!!")
        
        else:
                userdata = session["userdata"]
                return redirect(url_for('home'))

        return render_template("login.html", form=form)
             

#----------------- RETRIEVE DATA FOR UPDATING -------------------#
@app.route("/update/<string:i_d>")
def update(i_d):
        cur = mysql.connection.cursor()
        sql = ("SELECT * FROM employee where id=" + i_d)
        cur.execute(sql)
        data = cur.fetchone()
        
        return render_template("update.html",data=data)


#----------------- DOING NEW, DELETE, UPDATE -------------------#
@app.route("/feature", methods = ["GET", "POST"])
def feature():
        
        if request.method == "POST":
                id = request.form["id"]
                name = request.form["name"]
                dob = request.form["dob"]
                rank = request.form["rank"]
                address = request.form["address"]
                action = request.form["action"]
                
                if action == "Delete":
                        cur = mysql.connection.cursor()
                        sql = ("DELETE from employee WHERE id="+ id)
                        cur.execute(sql)
                        mysql.connection.commit()
                        cur.close()
                        flash('Deleted sucessful!')
                        form = saveForm(request.form)
                        return redirect(url_for("home", form=form))  
                
                elif action == "Update":
                        cur = mysql.connection.cursor()
                        sql = ("""UPDATE employee SET name=%s, dob=%s, `rank`=%s, address=%s WHERE id=%s""")
                        values =(name, dob, rank, address, id)
                        cur.execute(sql,values)
                        mysql.connection.commit()
                        cur.close()
                        flash('Update sucessful!') 
                
                elif action == "New":
                        form = saveForm(request.form)
                        return redirect(url_for("home", form=form))

                elif action == "List":
                        return redirect(url_for("list"))
        data = []
        data.append(id)
        data.append(name)
        data.append(dob)
        data.append(rank)
        data.append(address)    
        return render_template("update.html",data=data)
                 
if __name__ == '__main__':
   app.run()