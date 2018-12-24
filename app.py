from flask import Flask, request, jsonify, make_response
import datetime
import jwt


app=Flask(__name__)
app.config['SECRET_KEY']= 'johnishere'
users= []

@app.route('/add', methods=['POST'])
def create_user():
    name = request.get_json()["Username"]
    email= request.get_json()["email"]
    password= request.get_json()["password"]
    user={}

    if not name or not email or not password:
        return jsonify({'Message':"All fields are required"}), 404
    new_user= verify_email(email)
    if new_user == "User email already taken":
        return jsonify({"Message":"The email is already in use"}), 400

    user_id= len(users)+1
    user ={
    'name':name,
    'email':email,
    'password':password,
    'id':user_id
    }
    users.append(user)

    return jsonify({'Message':'User has been registered'}), 201

def verify_email(email):

    for user in users:
        if email in user.values():
            return "User email already taken"
    return "new user"


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({"Users":users})

@app.route('/login', methods=['POST'])
def login():
    email= request.get_json()['email']
    password=request.get_json()['password']

    if not email or not password:
        return jsonify({"Error":"Fields are required"}), 404
    verified= verify_record(email, password)

    if verified == "Does not exist":
        return jsonify({"Error":"Please register first"}), 404
    for user in users:
        id=user['id']

    # token= jwt.encode({"user_id":id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'],algorithm= 'HS256')
    #
    # return jsonify({'token': token.decode('UTF-8')})
    return "loged in successful"

def verify_record(email, password):
    for user in users:
        if password in user.values() and email in user.values():
            return "Exists"
    return "Does not exist"



if __name__ == '__main__':
    app.run(debug=True)
