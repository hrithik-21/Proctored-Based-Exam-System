from flask import Flask, render_template, request, redirect, url_for,send_file
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import csv
import pandas as pd
from datetime import date,time,datetime
from flask_cors import CORS
import cv2 as cv
import time
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app, expose_headers=["x-suggested-filename"])

'''Here we have connected databases i.e mongodb'''

app.config['MONGODB_SETTINGS'] = {
    'db': 'proctored-exam-system',
    'host': 'mongodb+srv://hrithik:qwerty1234@cluster0.oolkd.mongodb.net'
}

db = MongoEngine(app)
app.config['SECRET_KEY'] = 'qwertyuiop'
app.config['UPLOAD_FOLDER'] = 'images\\'
app.config['MAX_CONTENT_PATH'] = '500'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

'''Here we have used different class which contains variables for different objects'''

class User(UserMixin, db.Document):
    meta = {'collection': 'teacher'}
    roll_id = db.StringField(max_length=30)
    test_id = db.StringField(max_length=30)
    password = db.StringField()
    name = db.StringField()
    department = db.StringField()
    ctime = db.StringField()



class tuser(UserMixin, db.Document):
    meta = {'collection': 'tapprove'}
    approve = db.StringField()
    test_id = db.StringField(max_length=30)
    password = db.StringField(max_length=30)
    name = db.StringField()
    department = db.StringField()

class admin(UserMixin, db.Document):
    meta = {'collection': 'inadm'}
    name = db.StringField()
    password = db.StringField()

class suser(UserMixin, db.Document):
    meta = {'collection': 'student'}
    roll = db.StringField()
    test_id = db.StringField()
    ctime = db.StringField()
    ltime = db.StringField()

class fstu(UserMixin, db.Document):
    meta = {'collection': 'final'}
    name = db.StringField()
    roll = db.StringField()
    test_id = db.StringField()
    tlogin = db.StringField()
    tlogout = db.StringField()
    score = db.StringField()

class sissue(UserMixin, db.Document):
    meta = {'collection': 'issue'}
    name = db.StringField()
    roll = db.StringField()
    test_id = db.StringField()
    email = db.StringField()
    issue = db.StringField()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class RegForm(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    department = StringField('department', validators=[InputRequired()])
    roll_id = StringField('roll_id') #,  validators=[InputRequired(), Length(2)])
    test_id = StringField('test_id', validators=[InputRequired(), Length(5)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=20)])

class LoginForm(FlaskForm):
    test_id = StringField('test_id', validators=[InputRequired(), Length(5)])
    roll_id = StringField('roll_id') #validators=[InputRequired(), Length(2)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=20)])
    name = StringField('name')#, validators=[InputRequired()])

class issueform(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    department = StringField('department', validators=[InputRequired()])
    roll_id = StringField('roll_id') 
    test_id = StringField('test_id', validators=[InputRequired(), Length(5)])
    email = StringField('email')
    issue = StringField('issue')
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=20)])

'''Here SAWO Api is integrated for user i.e teacher authentication'''
    
@app.route('/sawo', methods=['GET', 'POST'])
def sawo():
    return render_template("sawo.htm")

'''This is api for giving proof to student that they are cheating'''

@app.route('/proof/<string:tid>/<string:roll>', methods=['GET', 'POST'])
def images(tid,roll):
    path = "static/data/" + tid + "/capture/"
    list_img = os.listdir(path)
    base_img = []
    for i in list_img:
        # print(i)
        cur_img = cv.imread(f'{path}/{i}')
        # cur_img = fg.load_image_file(path + str(i))
        if(i.split("-")[0]==roll):
            base_img.append(i)
    print(base_img)
    final_list = []
    path = "data/" + tid + "/capture/"
    for i in base_img:
        final_list.append(path+str(i))
    print(final_list)
    return render_template("images.html",files=final_list,tid = tid)

''' This will save the issue in database raised by students '''

@app.route('/issue',methods=['GET', 'POST'])
def issue():
    form = issueform()
    if request.method == 'POST':
        sissue(name=form.name.data, roll= form.roll_id.data, test_id = form.test_id.data, email = form.email.data ,issue = form.issue.data).save()
    return render_template("issue.html")

''' This is end point for teacher registration '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(test_id=form.test_id.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                approve = "No"
                tuser(name=form.name.data, department= form.department.data, test_id = form.test_id.data, approve=approve).save()
                User(name=form.name.data, department= form.department.data, test_id = form.test_id.data, password = hashpass).save()
                path = "static/data/"
                parent = str(form.test_id.data)
                final_path = os.path.join(path,parent)
                os.mkdir(final_path)
                path_csv = os.path.join(final_path,"csv")
                os.mkdir(path_csv)
                path_img = os.path.join(final_path, "img")
                os.mkdir(path_img)
                path_img = os.path.join(final_path, "capture")
                os.mkdir(path_img)
                path_ques = os.path.join(final_path, "question")
                os.mkdir(path_ques)
                path_result = os.path.join(final_path, "result")
                os.mkdir(path_result)
                parent_dir = "static/data/" + str(form.test_id.data) + "/result/"
                file = "result" + ".csv"
                path = os.path.join(parent_dir, file)
                with open(path, 'w', newline='') as file:
                    csvwriter = csv.writer(file)
                    fields = ['Roll No', 'Name', 'Score', 'Status','Login Time','Logout Time']
                    csvwriter.writerow(fields, )
                message1 = "Registered Successfully !! You will able to upload questions when admin approves"
                return render_template('register.html', form=form, message1=message1)
            else:
                message = str(form.test_id.data)+" Already Exists"
                return render_template('register.html', form=form, message=message)
    return render_template('register.html', form=form)

'''This will redirect teacher from contactus page to homepage'''

@app.route('/direct')
def direct():
    return render_template("index.html", name=current_user.name)

@app.route('/seeissue/<string:test>')
def seeissue(test):
    teach = sissue.objects(test_id=test)
    files = []
    if teach is None:
        return render_template("seeissue.html", files=files)
    for x in teach:
        files.append({
            "name": x['name'],
            "roll": x['roll'],
            "tid": x['test_id'],
            "email": x['email'],
            "issue": x['issue'],
        })
    val="Yes"
    return render_template("seeissue.html", files=files, val=val)

'''This is end point for techer login'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(test_id=form.test_id.data).first()
            teach = tuser.objects(test_id=form.test_id.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    if teach['approve']=="Yes":
                        login_user(check_user)
                        return render_template("index.html",name=current_user.name, test = form.test_id.data)
                    else:
                        message = "Admin of your institution didn't approved yet"
                        return render_template("login.html", form=form, message=message)
                else:
                    message = "Invalid Password Or Test Id"
                    return render_template("login.html", form=form, message=message)
            else:
                message = "Invalid Password Or Test Id"
                return render_template("login.html", form=form, message=message)
    return render_template('login.html', form=form)

'''This is end point for student login'''

@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(test_id=form.test_id.data).first()
            if check_user:

                if check_password_hash(check_user['password'], form.password.data):
                    name = form.name.data
                    fpath = str(form.test_id.data)
                    path = "static/data/"
                    finalpath = os.path.join(path, fpath)
                    csv_path = os.path.join(finalpath, "csv")
                    filelist = os.listdir(csv_path)
                    if(len(filelist)==0):
                        message = "Quetion Is Not Uploaded By Teacher Yet"
                        return render_template("studentlogin.html", form=form, message=message)
                    fname = str(filelist[0])
                    finalpath = os.path.join(csv_path, fname)
                    df = pd.read_csv(finalpath)
                    data = df.loc[df['Name'] == name, 'Roll No']
                    if(len(data)!=0) :
                        roll = str(data.values[0])
                        if(roll==str(form.roll_id.data)):
                            today = date.today()
                            d = today.strftime("%d-%b")
                            data = df.loc[df['Name'] == name, 'Date']
                            if(d==data.values[0]):
                                cuser = fstu.objects(name=name,test_id=form.test_id.data).first()
                                if (cuser == None):
                                    login_user(check_user)
                                    # return redirect(url_for('dashboard'))
                                    # return render_template("dashboard.html", roll=roll,name=form.roll_id.data)
                                    now = datetime.now()
                                    current_time = now.strftime("%H:%M:%S")
                                    ltime = ''
                                    suser(test_id=form.test_id.data, roll=form.roll_id.data, ctime=current_time,
                                          ltime=ltime).save()

                                    return render_template("dashboard.html", name = form.name.data ,roll=form.roll_id.data ,test = form.test_id.data)
                                else:
                                    message = str(form.name.data)+(" you have already submitted your exam")
                                    return render_template("studentlogin.html", form=form,message=message)
                            else:
                                if(d<data.values[0]):
                                    message = "Sorry!!! Exam of test id "+str(form.test_id.data)+" is on " + str(data.values[0]) + "-2021"
                                else:
                                    message = "Sorry!!! Exam of test id " + str(form.test_id.data) + " was on " + str(data.values[0]) + "-2021"
                                return render_template("studentlogin.html", form=form, message=message)
                        else:
                            message = "Sorry!!! Your roll number or name does not exist please re-enter or contact your teacher"
                            return render_template("studentlogin.html", form=form, message=message)
                    else:
                        message = "Sorry!!! Your roll number or name does not exist please re-enter or contact your teacher"
                        return render_template("studentlogin.html", form=form, message=message)
                else:
                    message = "Invalid Password Or Test Id"
                    return render_template("studentlogin.html", form=form, message=message)
            else:
                message = "Invalid Password Or Test Id"
                return render_template("studentlogin.html", form=form, message=message)
    return render_template('studentlogin.html', form=form)

@app.route('/contactus')
def contact():
    return render_template("ContactUs.html",name=current_user.name)


@app.route('/action/<string:tid>/<string:name>')
def action(tid,name):
    teach = tuser.objects(test_id=tid,name=name,approve="No").first()
    # tuser.objects(test_i)
    # tteach = {"$set": {"approve": "Yes"}}
    # print(teach['name'])
    if(teach is None):
        files = []
        files.append({
            "name": "No Data",
            "dept": "No data",
            "tid": "No Data",
            "approve": "No Data",
        })
        return render_template("admin.html",files=files)

    tuser(name=str(teach['name']), department=str(teach['department']), test_id=str(teach['test_id']), approve="Yes").save()
    teach.delete()
    # tuser.objects.update(teach)
    # teach = tuser.objects()
    # print(len(teach))
    teach = tuser.objects()
    files = []
    for x in teach:
        if x['approve']=="No":
            files.append({
                "name": x['name'],
                "dept": x['department'],
                "tid": x['test_id'],
                "approve": x['approve'],
            })
    if(len(files)==0):
        files.append({
            "name": "No Data",
            "dept": "No data",
            "tid": "No Data",
            "approve": "No Data",
        })
        return render_template("admin.html", files=files)
    return render_template("admin.html", files=files,val="no")
    # return render_template("ContactUs.html",name=current_user.name)

@app.route('/admin')
def admin():
    teach = tuser.objects()
    print(len(teach))
    files = []
    for x in teach:
        if(x['approve']=="No"):
            files.append({
                "name": x['name'],
                "dept": x['department'],
                "tid": x['test_id'],
                "approve": x['approve'],
            })
    if (len(files) == 0):
        files.append({
            "name": "No Data",
            "dept": "No data",
            "tid": "No Data",
            "approve": "No Data",
        })
        return render_template("admin.html", files=files)
    return render_template("admin.html",files=files,val="No")


@app.route('/csvfile',methods=['GET','POST'])
def csvfile():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        if (files[0].filename == ''):
            valnn = "notdefined"
            message1 = "No File Selected"
            return render_template('index.html', message1=message1, valnn=valnn,name =current_user.name)
        else:
            valnnn = "defined"
            path = "static/data/"
            fpath = str(current_user.test_id)
            finalpath = os.path.join(path,fpath)
            csv_path = os.path.join(finalpath,"csv")
            for file in files:
                s = file.filename
                fname = s.split('.')
                l = len(fname)
                if (fname[l - 1] == "csv"):
                    csvpath = os.path.join(csv_path, file.filename)
                    file.save(csvpath)
                else:
                    msgval = "Defined"
                    message = "Upload file with extension .csv"
                    return render_template('index.html', message=message, msgval=msgval, name=current_user.name)
            message = "Uploaded Successfully"
            return render_template('index.html', message=message, valnnn=valnnn,name = current_user.name,test = current_user.test_id)
    return render_template("index.html")

@app.route('/image',methods=['GET','POST'])
def image():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        # file1 = request.files.getlist('file[]').read()
        if (files[0].filename == ''):
            val = "notdefined"
            message1 = "No File Selected"
            return render_template('index.html', message1=message1, val=val, name = current_user.name)

        else:
            path = "static/data/"
            fpath = str(current_user.test_id)
            finalpath = os.path.join(path, fpath)
            img_path = os.path.join(finalpath, "img")
            for file in files:
                valn = "defined"
                msg = file.filename
                fmsg = msg.split('.')
                l = len(fmsg)
                if (fmsg[l-1] == "jpeg" or fmsg[l-1] == "jpg"):
                    imgpath = os.path.join(img_path, file.filename)
                    file.save(imgpath)
                else:
                    fmsgval = "defined"
                    message1 = "Upload file with .jpg extension"
                    return render_template('index.html', message1=message1, fmsgval=fmsgval,name = current_user.name)
            message1 = "Uploaded Successfully"
            print(current_user.test_id)
            return render_template('index.html', message1=message1, valn=valn,name= current_user.name,test = current_user.test_id)


@app.route('/question',methods=['GET','POST'])
def question():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        if (files[0].filename == ''):
            valnn3 = "notdefined"
            message13 = "No File Selected"
            return render_template('index.html', message13=message13, valnn3=valnn3,name = current_user.name,test = current_user.test_id)
        else:
            valnnn3 = "defined"
            path = "static/data/"
            fpath = str(current_user.test_id)
            finalpath = os.path.join(path,fpath)
            que_path = os.path.join(finalpath,"question")
            for file in files:
                s = file.filename
                fname = s.split('.')
                l = len(fname)
                if (fname[l - 1] == "js"):
                    quepath = os.path.join(que_path, file.filename)
                    file.save(quepath)
                else:
                    msgval3 = "Defined"
                    message3 = "Upload file with extension .json"
                    return render_template('index.html', message3=message3, msgval3=msgval3,name= current_user.name)
            message3 = "Uploaded Successfully"
            return render_template('index.html', message3=message3, valnnn3=valnnn3,name= current_user.name,test = current_user.test_id)
    return render_template("index.html")



@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.test_id, roll=str(current_user.test_id))

@app.route('/tout', methods = ['GET'])
@login_required
def tout():
    logout_user()
    return redirect(url_for('login'))
    # return render_template('login.html')
@app.route('/logout/<string:name>/<string:tid>')
@login_required
def logout(name,tid):
    time.sleep(2)
    logout_user()
    # return redirect(url_for('studentlogin'))
    cuser = fstu.objects(name=name,test_id=tid).first()
    while(cuser==None):
        cuser = fstu.objects(name=name, test_id=tid).first()
    # print(cuser)
    return render_template('logout.html',score= cuser['score'], name=cuser['name'],roll=cuser['roll'],test=cuser['test_id'],tlogin=cuser['tlogin'],tlogout=cuser['tlogout'])

@app.route('/login.html/<string:name>/<string:tid>')
@login_required
def logouthtml(name,tid):
    logout_user()
    # return redirect(url_for('studentlogin'))
    time.sleep(2)
    cuser = fstu.objects(name=name,test_id=tid).first()
    # return {}
    while (cuser == None):
        cuser = fstu.objects(name=name, test_id=tid).first()
    return render_template('logout.html', score=cuser['score'], name=cuser['name'], roll=cuser['roll'],est=cuser['test_id'],tlogin=cuser['tlogin'],tlogout=cuser['tlogout'])

@app.route('/chart/<string:tid>')
def chart(tid):
    return render_template("plot.html",tid=tid)


@app.route('/', methods = ['GET'])
def root():
    return render_template('home.html')

@app.route('/result', methods = ['POST'])
def result():
    detected = request.form.get('detected')
    notdetected = request.form.get('not_detected')
    score = request.form.get('score')
    roll = request.form.get('roll')
    name = request.form.get('name')
    test = request.form.get('test')
    fpath = str(test)
    path = "static/data/"
    finalpath = os.path.join(path, fpath)
    res_path = os.path.join(finalpath, "result")
    filelist = os.listdir(res_path)
    fname = str(filelist[0])
    path = os.path.join(res_path, fname)
    towrite = []
    towrite.append(roll)
    towrite.append(name)
    towrite.append(score)
    if(int(notdetected)>=10):
        towrite.append("Cheated")
    else:
        towrite.append("Not Cheated")
    cuser = suser.objects(test_id=current_user.test_id, roll=roll).first()
    intime = cuser['ctime']
    towrite.append(intime)
    now = datetime.now()
    ctime = now.strftime("%H:%M:%S")
    towrite.append(ctime)

    with open(path, 'a', newline='') as file:
        csvwriter = csv.writer(file)
        # fields = ['Roll No', 'Name','Score','Status']
        # csvwriter.writerow(fields, )
        csvwriter.writerow(towrite, )
    # print(path)
    pcsv = "static/data/"+str(test)+"plot.png"
    csv_file = "static/data/"+str(test)+"/result/result.csv"
    data = pd.read_csv(csv_file)
    a = data["Name"]
    b = data["Score"]
    x = []
    y = []
    x = list(a)
    y = list(b)
    plt.bar(x, y)
    plt.savefig(pcsv, dpi=300, bbox_inches='tight')
    fstu(name=name,roll =roll, test_id = test, tlogin = intime, tlogout = ctime, score = score).save()
    # return {}
    return render_template('logout.html', score=score, name=name, roll=roll,
                           test=test, tlogin=intime, tlogout=ctime)



@app.route('/return_csv', methods = ['POST','GET'])
def return_csv():
    filepath = "static/sample/test.csv"
    name = "test.csv"
    res = send_file(filepath, mimetype='application/x-csv', as_attachment=True, conditional=False,attachment_filename=name)
    res.headers["x-suggested-filename"] = name
    return res
@app.route('/return_jquery', methods = ['POST','GET'])
def return_jquery():
    filepath = "static/sample/questions.js"
    name = "questions.js"
    res = send_file(filepath, mimetype='application/x-csv', as_attachment=True, conditional=False,attachment_filename=name)
    res.headers["x-suggested-filename"] = name
    return res

@app.route('/download/', methods = ['POST','GET'])
def return_result():
    # fpath = str(current_user.test_id)
    # path = "static/data/"
    # finalpath = os.path.join(path, fpath)
    # csv_path = os.path.join(finalpath, "csv")
    # filelist = os.listdir(csv_path)
    # fname = str(filelist[0])
    # finalpath = os.path.join(csv_path, fname)
    # df = pd.read_csv(finalpath)
    # data = df.loc[df['Name'] == name, 'Roll No']
    filepath = "static/data/" + current_user.test_id + "/result/result.csv"
    name = str(current_user.test_id) + ".csv"
    print(filepath)
    print(name)
    res = send_file(filepath, mimetype='application/x-csv', as_attachment=True, conditional=False, attachment_filename=name)
    res.headers["x-suggested-filename"] = name
    return res

@app.route('/adminauth',methods = ['POST','GET'])
def adminauth():
    form = RegForm()
    print(form.name.data)
    if (form.name.data == "hilag" and form.password.data == "hilag"):
        print("hi")
        return redirect(url_for("admin"))
    message="incorrect credentials"
    return render_template("adminlogin.html", form=form,message=message)
@app.route('/adminlogin')
def adminlogin():
    form = RegForm()
    # if request.method == 'POST':
    #     return render_template("adminlogin.html", form=form)

    return render_template("adminlogin.html",form=form)


if __name__ == "__main__":
    app.run(debug=True)
