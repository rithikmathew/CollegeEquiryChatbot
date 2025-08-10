from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
import mysql.connector
import smtplib
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os
from flask import Flask, render_template, request, jsonify

english_bot = ChatBot('Bot',
                      storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch'
                          },

                      ],
                      trainer='chatterbot.trainers.ListTrainer')
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

app.config['DEBUG']



@app.route("/ask", methods=['GET', 'POST'])
def ask():
    message = str(request.form['messageText'])
    bott = ''
    bott1 = ''
    sresult1 = ''

    bot_response = english_bot.get_response(message)

    print(bot_response)

    while True:

        if bot_response.confidence > 0.5:

            bot_response = str(bot_response)
            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

        elif message == ("bye") or message == ("exit"):

            bot_response = 'Hope to see you soon' + '<a href="http://127.0.0.1:5000">Exit</a>'

            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

            break



        else:

            try:
                url = "https://en.wikipedia.org/wiki/" + message
                page = get(url).text
                soup = BeautifulSoup(page, "html.parser")
                p = soup.find_all("p")
                return jsonify({'status': 'OK', 'answer': p[1].text})



            except IndexError as error:

                bot_response = 'Sorry i have no idea about that.'

                print(bot_response)
                return jsonify({'status': 'OK', 'answer': bot_response})

@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Chat")
def Chat():
    return render_template('chat.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/UserHome")
def UserHome():
    return render_template('UserHome.html')


@app.route("/AdminHome")
def AdminHome():
    return render_template('AdminHome.html')


@app.route("/NewQuery1")
def NewQuery1():
    return render_template('NewQueryReg.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' or request.form['password'] == 'admin':
            conn = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
            cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM register")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)

        else:
            return render_template('index.html', error=error)


@app.route("/reg", methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        rollno = request.form['rollno']
        n = request.form['name']

        email = request.form['email']
        p = request.form['PhoneNo']
        department = request.form['department']
        section = request.form['section']

        uname = request.form['uname']
        password = request.form['psw']
        conn = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO register VALUES ('','" + rollno + "','" + n + "','" + email + "','" + p + "','" + department + "','" + section + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'
        return render_template('UserLogin.html')



@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from register where uname='" + username + "' and psw='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            return render_template('index.html')
            return 'Username or Password is wrong'
        else:
            print(data[0])
            session['uid'] = data[0]
            conn = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM register where uname='" + username + "' and psw='" + password + "'")
            data = cur.fetchall()

            return render_template('UserHome.html', data=data)


@app.route("/newquery", methods=['GET', 'POST'])
def newquery():
    if request.method == 'POST':
        uname = session['uname']
        type = request.form['Qtype']

        query = request.form['query']
        date = request.form['date']

        conn = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Querytb VALUES ('','" + uname + "','" + type + "','" + query + "','" + date + "','','waiting')")
        conn.commit()
        conn.close()
        # return 'file register successfully'
        conn = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' and status='waiting '")
        data = cur.fetchall()
        return render_template('UserQueryInfo.html', data=data)


@app.route("/UQueryandAns")
def UQueryandAns():
    uname = session['uname']

    conn = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' and status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' and status='Answer'")
    data1 = cur.fetchall()

    return render_template('UserQueryAnswerinfo.html', wait=data, answ=data1)


@app.route("/AdminQinfo")
def AdminQinfo():
    # uname = session['uname']

    conn = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where  status='waiting'")
    data = cur.fetchall()

    return render_template('AdminQueryInfo.html', data=data)


@app.route("/answer", methods=['GET', 'POST'])
def answer():
    if request.method == 'POST':
        Answer = request.form['AAnswer']
        id = request.form['id']
        uname = request.form['uname']

        print(Answer)
        print(id)

        conn = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
        cursor = conn.cursor()
        cursor.execute(
            "update Querytb set status='Answer',Answer='" + Answer + "' where id='" + str(id) + "' ")
        conn.commit()
        conn.close()

        conn3 = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
        cur3 = conn3.cursor()
        cur3.execute("SELECT * FROM register where 	uname='" + str(uname) + "'")
        data3 = cur3.fetchone()
        if data3:
            phnumber = data3[4]
            print(phnumber)
            sendmsg(phnumber, "Your Query Answer updated!")

        # return 'file register successfully'
        conn = mysql.connector.connec(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' and status !='waiting '")
        data = cur.fetchall()
        return render_template('AdminAnswer.html', data=data)


@app.route("/AdminAinfo")
def AdminAinfo():
    conn = mysql.connector.connect(user='Mathew002', password='Sqlrithik@002', host='Mathew002.mysql.pythonanywhere-services.com', database='Mathew002$2chatbotdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where  status !='waiting'")
    data = cur.fetchall()

    return render_template('AdminAnswer.html', data=data)


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://smsserver9.creativepoint.in/api.php?username=fantasy&password=596692&to=" + targetno + "&from=FSSMSS&message=Dear user  your msg is " + message + " Sent By FSMSG FSSMSS&PEID=1501563800000030506&templateid=1507162882948811640")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
