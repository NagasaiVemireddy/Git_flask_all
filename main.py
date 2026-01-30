from flask import Flask ,jsonify,request
from config import ConfigClass
from models import db



app = Flask(__name__)
app.config.from_object(ConfigClass) # here we are loading the config class 
db.init_app(app) # its going to make connection between flask and mysql ( before the database engine)


#here we are creating the table 
with app.app_context():
    db.create_all()

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

if __name__ == '__main__': # if this is the main file 
    app.run(debug=True) # app is obj --> it contains attributes and methods ( run )

    
