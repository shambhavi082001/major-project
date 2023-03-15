from flask import Flask,render_template,Response,session,flash,redirect,url_for,request
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine
from utils import *
from project_orm import User, Quiz
import cvzone
from cvzone.HandTrackingModule import HandDetector
import csv
import time
from sqlalchemy.orm import scoped_session

app=Flask(__name__)
app.secret_key = "the basics of life with python"

def get_db():
    engine = create_engine('sqlite:///quiz.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    return Session()


camera=cv2.VideoCapture(0)
camera.set(3,1280)
camera.set(4,720)
detector = HandDetector(detectionCon=0.8)

class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = data[5]

        self.userAns = None

    def update(self,image, cursor,bboxs):
        for x, bbox in enumerate(bboxs):
            x1,y1,x2,y2 = bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.userAns = self.answer
                print('image')
                cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), cv2.FILLED)


mcqList = []
# create object for each MCQ

qNo = 0
qTotal = 0  



def generate_frames():
    global qNo, qTotal, mcqList
    qNo= 0
    while camera.isOpened():
                
        # read the camera frame
        success,image=camera.read()
        image = cv2.flip(image, 1)
        if not success:
            print("Ignoring empty camera frame.")
            continue
        hands, image = detector.findHands(image, flipType=False)

        print("Total MCQ objects created:", len(mcqList))

        if qNo<qTotal:
            mcq = mcqList[qNo]
            image, bbox = cvzone.putTextRect(image, mcq.question, [100,100], 2, 2, offset=50 ,border=5)
            image, bbox1 = cvzone.putTextRect(image, mcq.choice1, [100,250], 2, 2, offset=50 ,border=5)
            image, bbox2 = cvzone.putTextRect(image, mcq.choice2, [400,250], 2, 2, offset=50 ,border=5)
            image, bbox3 = cvzone.putTextRect(image, mcq.choice3, [100,400], 2, 2, offset=50 ,border=5)
            image, bbox4 = cvzone.putTextRect(image, mcq.choice4, [400,400], 2, 2, offset=50 ,border=5)

            if hands:
                lmList = hands[0]['lmList']
                cursor = lmList[8]
                length, info = detector.findDistance(lmList[8][:2],lmList[12][:2])
                if length < 60:
                    mcq.update(image,cursor,[bbox1,bbox2,bbox3,bbox4])
                    print(mcq.userAns)
                    if mcq.userAns is not None:
                        time.sleep(0.3)
                        qNo += 1
        else:
            score = 0
            for mcq in mcqList:
                if mcq.answer == mcq.userAns:
                    score += 1
            score =  round((score/qTotal)*100,2)     
            image, _ = cvzone.putTextRect(image, "Quiz Completed", [250,300], 2, 2, offset=50, border=5)
            image, _ = cvzone.putTextRect(image, f'your score: {score}%', [700,300], 2, 2, offset=50, border=5)



        # draw progress bar
        barValue = 150+(950//qTotal)*qNo
        cv2.rectangle(image,(150,600),(barValue,650),(0,255,0),cv2.FILLED)
        cv2.rectangle(image,(150,600),(1100,650),(255,0,255),5)
        img, _ = cvzone.putTextRect(image, f'{round((qNo/qTotal)*100)}%', [1130,635], 2, 2, offset=16)

        if not success:
            yield(b'')
        else:
            ret,buffer=cv2.imencode('.jpg',image)
            frame=buffer.tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' b'\r\n')


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and check(email):
            if password and len(password)>=6:
                try:
                    sess = get_db()
                    user = sess.query(User).filter_by(email=email,password=password).first()
                    if user:
                        session['isauth'] = True
                        session['email'] = user.email
                        session['id'] = user.id
                        session['name'] = user.name
                        del sess
                        flash('login successfull','success')
                        return redirect('/home')
                    else:
                        flash('email or password is wrong','danger')
                except Exception as e:
                    flash(e,'danger')
            else:
                flash("password do not match", 'danger')
        else:
            flash('email is not valid', 'danger')
    return render_template('index.html',title='login')
    

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        if name and len(name) >= 3:
            if email  and check(email):
                if password and len(password)>=6:
                    if cpassword and cpassword == password:
                        try:
                            sess = get_db()
                            newuser = User(name=name,email=email,password=password)
                            sess.add(newuser)
                            sess.commit()
                            flash('registration successfull','success')
                            return redirect('/')
                        except:
                            flash('email account already exist','danger')
                    else:
                        flash('confirm password does not match','danger')
                else:
                    flash('password must be of 6 or more characters','danger')    
            else:
                flash('invalis email','danger')
        else:
            flash('invalid name, must be 3 or more characters','danger')


    return render_template('signup.html',title='register')

@app.route('/forgot',methods=['GET','POST'])
def forgot():
    return render_template('forgot.html',title='frogot password')

@app.route('/home',methods=['GET','POST'])
def home():
    if session.get('isauth'):
        username = session.get('name')
        return render_template('home.html',title=f'Home|{username}')
    flash('please login to continue','warning')
    return redirect('/')
    

@app.route('/video')
def video():
    global qTotal
    sess = get_db()
    questions = sess.query(Quiz).all()
    qTotal = len(questions)
    mcqList.clear()
    for q in questions:
        mcqList.append(MCQ(
            [q.question,
            q.a,
            q.b,
            q.c,
            q.d,
            q.answer,]
        ))
    print('total questions', qTotal)
    try:
        res =  Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')   
        return res    
    except Exception as e:
        print(e) 
        return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html',title='About Us')

@app.route('/logout')
def logout():
    def logout():
     if session.get('isauth'):
        session.clear()
        flash('you have been logged out','warning')
    return redirect('/')
    


@app.route('/admin',methods=['GET','POST'])
def admin():
    if session['email'] != 'jenny12@gmail.com':
        flash('login as admin','error')
        return redirect('/')
    if request.method == 'POST':
        question = request.form.get('question')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        answer = request.form.get('answer')
        sess = get_db()
        quiz = Quiz(question=question, a=option1, b=option2, c=option3, d=option4,answer=answer)
        sess.add(quiz)
        sess.commit()
        sess.close()
        flash('Question Added','success')
        return redirect('/admin')


    return render_template('admin.html',title='admin')



if __name__=="__main__":
    app.run(debug=True)


