from flask import Flask ,jsonify,request,redirect,url_for,render_template,session
from config import ConfigClass
from flask_migrate import Migrate
from models import db, Employee
from flask_jwt_extended import JWTManager,create_access_token, jwt_required,create_refresh_token
#login auth we are doing here 
from flask_basicauth import BasicAuth
from flask_caching import Cache
import time

app = Flask(__name__)
app.config.from_object(ConfigClass) # here we are loading the config class 
db.init_app(app) # its going to make connection between flask and mysql ( before the database engine)
migrate = Migrate(app, db)
jwt = JWTManager(app)
#login auth we are doing here 
auth = BasicAuth(app)
#cache working 
cach = Cache(app)

#here we are creating the table 
with app.app_context():
    # db.drop_all()   # This deletes EVERYTHING
    db.create_all() # This recreates everything with new columns


#---------------------------------------------------#
@app.route("/home",methods=['GET']) #route decorator
def home_func():
    # return " this is first app "
    return jsonify(msg="restarted"),200


#path param 
@app.route("/pathparam/<id>",methods=['GET'])
#@app.route("/pathparam/<int:id>",methods=['GET'])

def path_param_view(id):
    return jsonify(msg=f'the path param is {id}')


#query param 

@app.route('/queryparam',methods=['GET'])
def query_param():
    # name=request.args.get("name")
    # age=request.args.get("age")
    # return jsonify(msg=f"query params are {name} and {age}")
    ##When want to give more values 
    # name=request.args.getlist("name")
    # age=request.args.getlist("age")
    # return jsonify(msg=f"query params are {name} and {age}")
    ##When we dont know the keys we are expecting and when we have duplicate we use flat = false 
    data =request.args.to_dict(flat=False)
    print(data,type(data))
    return data

# ==========================
#   DUMMY TODO BLOCK
# ==========================

# TODO:
# - Learn how git stash works
# - Practice stash save and pop

# End of dummy block

# stash pull is done last step i am doing now 


# redirect , post #
@app.route('/insertdata', methods=['POST'])
def insert_data_view():
    data = request.get_json()
    if not data:
        return jsonify(msg="please provide the full details")
    # Mapping JSON keys → DB columns
    employee_record = Employee(
        emp_name=data.get("user_emp_name"),   # JSON key "client_name" → DB column "emp_name"
        emp_age=data.get("user_password")      # JSON key "client_age" → DB column "emp_age"
    )
    db.session.add(employee_record)
    db.session.commit()

    return jsonify(
        id=employee_record.id,
        name=employee_record.emp_name,
        age=employee_record.emp_age
    )


@app.route('/redirect',methods=['GET'])
def redirect_func():
    return redirect(url_for('home_func'))



#render_template

@app.route('/template_html',methods=['GET'])
def template_view():
    return render_template("demo.html")


#RAW HTML
@app.route('/rawhtml',methods=['POST'])
def raw_html_view():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>this is raw html front end</h1>
</body>
</html>
"""    
#FORM DATA 
@app.route('/formdata',methods=['POST'])
def query_form_data_view():
    # #when know are there
    # name=request.form.get("name")
    # age=request.form.get("age")
    # return jsonify(msg=f"form data is {name} and {age}")
    
    ##When want to give more values 
    # name=request.form.getlist("name")
    # age=request.form.getlist("age")
    # return jsonify(msg=f"query params are {name} and {age}")
    
    ##When we dont know the keys we are expecting and when we have duplicate we use flat = false 
    data =request.form.to_dict(flat=False)
    print(data,type(data))
    return data

@app.route('/protected',methods=['GET'])
@jwt_required()

def prot_func():
    return jsonify(msg="This is protected page")


#registration block

@app.route('/register',methods=['POST'])
def register_fun():
    data1= request.get_json(silent=True)
    if not data1:
        return jsonify(msg="please provide the proper name and password"),400
    user_data= Employee.query.filter_by(emp_name=data1['user_emp_name']).first()
    if not user_data:
        db_user = Employee(
            emp_name=data1['user_emp_name'],
            username=data1['username'],        # Added username
            password=data1['user_password'],
            emp_age=data1.get('emp_age', 0)   # optional if default exists
        )
        db.session.add(db_user)
        db.session.commit()
        return jsonify(msg=f"user {data1['user_emp_name']} successfully registered")
    return jsonify(msg="user already exixts")

#login block
   
@app.route('/login', methods=['POST'])
def login_fun():
    data2 = request.get_json(silent=True)
    
    if not data2:
        return jsonify(msg="please provide the proper name and password"), 400
#	• “Left side is model field, right side is client input.”

    # Check user exists with given emp_name AND password
    user_data = Employee.query.filter_by(
        emp_name=data2['user_emp_name'], 
        password=data2['user_password']
    ).first()

    # If no user found, return invalid credentials
    if not user_data:
        return jsonify(msg="provide valid credentials"), 401
    acc_token = create_access_token(identity=data2['user_emp_name'])
    return jsonify(access_token=acc_token)

    # Success
    # print("user {data2['user_emp_name']} logged in successfully"), 200


@app.route('/basiclogin',methods=['GET'])
@auth.required
def basic_login_view():
    session['logged_in'] = True
    return jsonify(msg="user logged in")


@app.route('/logout',methods=["GET"])
def logout_view():
    val =session.pop("logged_in",None)
    if not val:
        return jsonify(msg="user need to login first to logout")
    return jsonify(msg = "user logged out successfully")

@app.route('/status',methods=['GET'])
def session_status():
    val = session.get('logged_in')
    if val:
        return jsonify(msg="user is logged in ")
    
    return jsonify(msg="user is not logged in ")

# this block is for cookie 
@app.route('/search/<item>',methods=['GET'])
def search_view(item):
    res = jsonify(msg=f"user is searching for {item}")
    res.set_cookie(key="unique_key",value =item)
    return res



@app.route('/getcookie', methods=['GET'])
def get_cookie():
    cookie_val = request.cookies.get("unique_key")
    if cookie_val:
        # return jsonify(msg=f"user searched for {cookie_val}")
        return jsonify(msg=f"user searched for {cookie_val}")
    return jsonify(msg=f"cookie not found")


#deleting the cookie 

@app.route('/deletecookie', methods=['GET'])
def del_cookie():
    cookie_val = request.cookies.get("unique_key")
    if cookie_val:
        # return jsonify(msg=f"user searched for {cookie_val}")
        res = jsonify(msg=f"user deleting this   {cookie_val}")
        res.delete_cookie("unique_key")
        return res
    return jsonify(msg=f"cookie not found")

#caching 



@app.route('/simplecache',methods=['GET'])
@cach.cached()
def simple_cache_func():
    time.sleep(5)
    return jsonify(msg="from a simple cache ")

@app.route('/filecache',methods=['GET'])
@cach.cached()
def filecache_func():
    time.sleep(5)
    print("!"*5)
    return jsonify(msg="from a file system  cache ")



if __name__ == '__main__': # if this is the main file 
    app.run(debug=True) # app is obj --> it contains attributes and methods ( run )





