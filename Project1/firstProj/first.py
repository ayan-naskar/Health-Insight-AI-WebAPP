# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

import os
from flask import Flask , redirect , url_for, render_template, request, jsonify
import isvalid as iv
import init_db as idb
import addOperations as ao
from werkzeug.utils import secure_filename
from PIL import Image
import model 
import time
import contactUs as cu

app = Flask(__name__, static_url_path='/static')
curr_user={
    "email": "",
    "isLoggedIn": False
}
isModelLoaded = False
upload_folder="/images/Diseases"
allowed_extensions={
    'jpg','jpeg','png'
}
app.config['UPLOAD_FOLDER']=upload_folder

@app.route('/')
def index():
    return render_template('/index.html', isLoggedIn=curr_user["isLoggedIn"], email=curr_user["email"])

@app.route('/load_models')
def load_models():
    global isModelLoaded

    if not isModelLoaded:
        model.loadModels()
        isModelLoaded = True

    return jsonify({'status': 'success'})

# @app.route('/')
# def welcome():
#     return 'welcome to the first project'

# @app.route('/next')
# def nextpage():
#     return '<h1>Welcome to the next page!</h1>'

@app.route('/hello/<name>')
def helloName(name):
    return '<h1>Hello '+name+' !! </h1>'

# @app.route('/user/<name>')
# def userName(name):
#     if name == 'admin':
#         return redirect(url_for('helloName',name='Administrator'))
#     else:
#         return redirect(url_for('helloName', name=name))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    errormessage=''
    if request.method=='POST':
        uemail=request.form['email']
        upassword=request.form['password']

        user=iv.checkLogin(uemail)
        if user!=None and user[1]==upassword:
            curr_user["isLoggedIn"]=True
            curr_user["email"]=uemail
            return render_template("index.html", isLoggedIn=curr_user["isLoggedIn"], email=curr_user["email"])
        else:
            errormessage='Invalid User.'
        

    return render_template("login.html", errormessage=errormessage)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method=='POST':
        uemail=request.form['email']
        upassword=request.form['password']
        cpassword=request.form['confirm_password']
        pnumber=request.form['phone']

        user=iv.checkLogin(uemail)
        if user!=None:
            return render_template("login.html", errormessage='Existing User, Please Login.')
        elif upassword!=cpassword:
            return render_template("registration.html", errormessage='The passwords are not same.')
        else:
            isCommited=ao.addUser((uemail, pnumber, upassword))
            if isCommited==0:
                return render_template("registration.html", errormessage='Something Went wrong.')
            else:
                return render_template("login.html", errormessage='Successfully Registered, Please Login.')
        
    return render_template("registration.html", errormessage='')

@app.route('/logout')
def logout():
    curr_user["isLoggedIn"]=False
    curr_user['email']=""
    return render_template('/index.html', isLoggedIn=curr_user["isLoggedIn"], email=curr_user["email"])

@app.route('/services')
def services():
    return render_template('/services.html', isLoggedIn=curr_user["isLoggedIn"], email=curr_user["email"])

@app.route('/findDoctor')
def findDoctor():
    return render_template('/findDoctor.html', isLoggedIn=curr_user["isLoggedIn"], email=curr_user["email"])

@app.route('/detectdisease')
def detectdisease():    
    print(curr_user["isLoggedIn"])
    return render_template('/detectdisease.html', message='', isLoggedIn=curr_user["isLoggedIn"], email=curr_user["email"], isModelLoaded=isModelLoaded)

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    global isModelLoaded

    while not isModelLoaded:
        time.sleep(10)

    if 'image' not in request.files:
        return "No image uploaded.", 400

    image = request.files['image']
    if image.filename == '':
        return "No image selected.", 400

    image.save('Project1\\firstProj\\uploads\\' + image.filename) # type: ignore

    img=Image.open('Project1\\firstProj\\uploads\\' + image.filename) # type: ignore

    # print("here: image=", img, "here")
    result = model.detectDisease(image.filename)
    print(result)

    ao.addImageUpload((curr_user['email'], image.filename, img.tobytes(), result['class']))

    return jsonify(result)

@app.route('/submit', methods=['POST'])
def submit_question():
    if request.method == 'POST':
        question = request.form['question']
        description = request.form['description']

        # Perform any validation or data processing here if needed

        # Call the insert_question function to insert data into the database
        
        if not curr_user["isLoggedIn"]:
            return render_template('/index.html', isLoggedIn=curr_user["isLoggedIn"], email=curr_user["email"], err_message="Please login to send message.")
        cu.insert_question(curr_user["email"], question, description)
        print("data entered.")

    return render_template('/index.html', isLoggedIn=curr_user["isLoggedIn"], email=curr_user["email"])

if __name__ == '__main__':
    app.run(debug=True)