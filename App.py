from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
import mysql.connector
mysql.connector.connect()
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

            bot_response = 'Hope to see you soon' + '<a href="/">Exit</a>'

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
        username = request.form['uname']
        password = request.form['password']

        # Use 'and' to ensure both username and password match
        if username == 'admin' and password == 'admin':
            try:
                conn = mysql.connector.connect(
                    host="sql100.infinityfree.com",
                    user="if0_39648553",
                    password="Rithik002",
                    database="if0_39648553_2chatbotdb",
                    port=3306
                )
                cur = conn.cursor()
                cur.execute("SELECT * FROM register")
                data = cur.fetchall()
                conn.close()
                return render_template('AdminHome.html', data=data)
            except mysql.connector.Error as err:
                error = f"Database error: {err}"
                return render_template('index.html', error=error)
        else:
            error = "Invalid admin credentials."
            return render_template('index.html', error=error)
    else:
        return render_template('AdminLogin.html')  # For GET request



@app.route("/reg", methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        rollno = request.form.get('rollno')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('PhoneNo')
        department = request.form.get('department')
        section = request.form.get('section')
        uname = request.form.get('uname')
        password = request.form.get('psw')

        try:
            conn = mysql.connector.connect(
                host="sql100.infinityfree.com",
                user="if0_39648553",
                password="Rithik002",
                database="if0_39648553_2chatbotdb",
                port=3306
            )
            cursor = conn.cursor()

            query = """
                INSERT INTO register 
                (rollno, name, email, phone, department, section, uname, psw) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (rollno, name, email, phone, department, section, uname, password)

            cursor.execute(query, values)
            conn.commit()
            return render_template('UserLogin.html')

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return "Registration failed. Please try again later."

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()




@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(
            host="sql100.infinityfree.com",
            user="if0_39648553",
            password="Rithik002",
            database="if0_39648553_2chatbotdb",
            port=3306
        )
        cursor = conn.cursor(dictionary=True)

        # Use parameterized query to prevent SQL injection
        cursor.execute("SELECT * FROM register WHERE uname = %s AND psw = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user is None:
            error = "Username or Password is incorrect"
            return render_template('UserLogin.html', error=error)
        else:
            # Save user info in session
            session['uname'] = user['uname']
            session['uid'] = user['id']  # assuming 'id' is the primary key column

            return render_template('UserHome.html', data=[user])



@app.route("/newquery", methods=['GET', 'POST'])
def newquery():
    if request.method == 'POST':
        uname = session.get('uname')
        query_type = request.form['Qtype']
        query_text = request.form['query']
        date = request.form['date']

        # Connect to production DB (InfinityFree)
        try:
            conn = mysql.connector.connect(
                host="sql100.infinityfree.com",
                user="if0_39648553",
                password="Rithik002",
                database="if0_39648553_2chatbotdb",
                port=3306
            )
            cursor = conn.cursor()

            # Parameterized insert query
            insert_query = """
                INSERT INTO Querytb (UserName, Qtype, query, date, Answer, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (uname, query_type, query_text, date, '', 'waiting'))
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print("Database error:", e)
            return "Error submitting query", 500

        # Fetch user queries with status='waiting'
        try:
            conn2 = mysql.connector.connect(
                host="sql100.infinityfree.com",
                user="if0_39648553",
                password="Rithik002",
                database="if0_39648553_2chatbotdb",
                port=3306
            )
            cur = conn2.cursor()
            cur.execute("SELECT * FROM Querytb WHERE UserName = %s AND status = %s", (uname, 'waiting'))
            data = cur.fetchall()
            cur.close()
            conn2.close()
        except mysql.connector.Error as e:
            print("Database error:", e)
            return "Error fetching query data", 500

        return render_template('UserQueryInfo.html', data=data)



@app.route("/UQueryandAns")
def UQueryandAns():
    uname = session.get('uname')

    if not uname:
        return redirect(url_for('UserLogin'))  # Redirect to login if session expired

    try:
        conn = mysql.connector.connect(
            host="sql100.infinityfree.com",
            user="if0_39648553",
            password="Rithik002",
            database="if0_39648553_2chatbotdb",
            port=3306
        )
        cur = conn.cursor()

        # Fetch waiting queries
        cur.execute("SELECT * FROM Querytb WHERE UserName = %s AND status = %s", (uname, 'waiting'))
        waiting_queries = cur.fetchall()

        # Fetch answered queries
        cur.execute("SELECT * FROM Querytb WHERE UserName = %s AND status = %s", (uname, 'Answer'))
        answered_queries = cur.fetchall()

        return render_template('UserQueryAnswerinfo.html', wait=waiting_queries, answ=answered_queries)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "An error occurred while fetching your queries. Please try again later."

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()



@app.route("/AdminQinfo")
def AdminQinfo():
    try:
        # Establish a database connection
        conn = mysql.connector.connect(
            host="sql100.infinityfree.com",
            user="if0_39648553",
            password="Rithik002",
            database="if0_39648553_2chatbotdb",
            port=3306
        )

        # Use a cursor to execute the query
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True for better readability in Jinja templates
        cursor.execute("SELECT * FROM Querytb WHERE status = %s", ('waiting',))
        data = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        data = []  # Return empty data in case of failure

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    # Render the template with the data
    return render_template('AdminQueryInfo.html', data=data)



@app.route("/answer", methods=['GET', 'POST'])
def answer():
    if request.method == 'POST':
        answer_text = request.form['AAnswer']
        query_id = request.form['id']
        uname = request.form['uname']

        print(f"Answer: {answer_text}")
        print(f"Query ID: {query_id}")

        # --- Update the query with the answer ---
        try:
            conn = mysql.connector.connect(
                host="sql100.infinityfree.com",
                user="if0_39648553",
                password="Rithik002",
                database="if0_39648553_2chatbotdb",
                port=3306
            )
            cursor = conn.cursor()
            update_query = "UPDATE Querytb SET status = %s, Answer = %s WHERE id = %s"
            cursor.execute(update_query, ('Answer', answer_text, query_id))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error updating query answer: {e}")
            return "Error occurred while updating the answer", 500

        # --- Get user's phone number ---
        try:
            conn = mysql.connector.connect(
                host="sql100.infinityfree.com",
                user="if0_39648553",
                password="Rithik002",
                database="if0_39648553_2chatbotdb",
                port=3306
            )
            cur = conn.cursor()
            cur.execute("SELECT PhoneNo FROM register WHERE uname = %s", (uname,))
            data = cur.fetchone()
            if data:
                phnumber = data[0]
                print(f"Sending SMS to: {phnumber}")
                sendmsg(phnumber, "Your Query Answer updated!")
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error sending SMS: {e}")

        # --- Get all answered queries of the user ---
        try:
            conn = mysql.connector.connect(
                host="sql100.infinityfree.com",
                user="if0_39648553",
                password="Rithik002",
                database="if0_39648553_2chatbotdb",
                port=3306
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM Querytb WHERE UserName = %s AND status != %s", (uname, 'waiting'))
            data = cur.fetchall()
            cur.close()
            conn.close()
            return render_template('AdminAnswer.html', data=data)
        except Exception as e:
            print(f"Error fetching updated queries: {e}")
            return "Error occurred while fetching updated data", 500



@app.route("/AdminAinfo")
def AdminAinfo():
    try:
        conn = mysql.connector.connect(
            host="sql100.infinityfree.com",
            user="if0_39648553",
            password="Rithik002",
            database="if0_39648553_2chatbotdb",
            port=3306
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM Querytb WHERE status != %s", ('waiting',))
        data = cur.fetchall()
        return render_template('AdminAnswer.html', data=data)
    except mysql.connector.Error as err:
        print("Database error:", err)
        return "An error occurred while fetching data."
    finally:
        if conn.is_connected():
            cur.close()
            conn.close()



def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://smsserver9.creativepoint.in/api.php?username=fantasy&password=596692&to=" + targetno + "&from=FSSMSS&message=Dear user  your msg is " + message + " Sent By FSMSG FSSMSS&PEID=1501563800000030506&templateid=1507162882948811640")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
