import mysql.connector
from flask import Flask, redirect, url_for, request,render_template,flash
from flask_table import Table, Col
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="SurgeryDepartment"
)
mycursor = mydb.cursor()
app = Flask(__name__)
app.secret_key= 'dont tell anyone'
@app.route('/')
def home():
	return render_template('home.html')
@app.route('/signin', methods=['POST','GET'])
def signin():
	if request.method == 'POST': 
		username = request.form['user_name']
		password = request.form['pass_word']
		if str(username)=='Ahmed' and password=='1234' :
			return render_template('index.html')
		else:	   
			mycursor.execute("SELECT * FROM Doctors WHERE user_name='" +username+ "' and pass_word='" +password+ "' ")
			data=mycursor.fetchone()
			if data is None:
				return render_template('sign-in.html', message="Username or Password may be wrong! ") 
			else:
				return render_template('doctors.html')
	else:
		return render_template('sign-in.html') 
@app.route('/addsurgeon' ,methods = ['POST', 'GET'])
def addsurgeon():
	if request.method == 'POST': 
		username = request.form['user_name']
		passwd = request.form['pass_word']
		name = request.form['name']
		id= request.form['D_id']
		age=request.form['age']
		gender=request.form['gender']
		stdate=request.form['start_date']
		degree=request.form['degree']
		department=request.form['department']
		phone=request.form['phone']
		mail=request.form['mail']
		sql = "INSERT INTO Doctors(user_name,pass_word,name ,D_id,age,gender,start_date,degree,department,phone,mail) VALUES (%s,%s,%s, %s ,%s ,%s,%s, %s ,%s,%s, %s )"
		val = (username,passwd,name,id,age,gender,stdate,degree,department,phone,mail)
		mycursor.execute(sql, val)
		mydb.commit()   
		return render_template('index.html')
	else:
		return render_template('add.html')
@app.route('/deletedoctor' , methods=['POST' ,'GET'])
def deletedoctor():
	if request.method=='POST':
		id=request.form['D_id']
		mycursor.execute("SELECT * FROM Doctors WHERE D_id='" +id+ "'")
		d=mycursor.fetchone()
		if d is None:
			return render_template('deletedoctor.html')
		else:
			mycursor.execute("DELETE FROM Doctors WHERE D_id ='" +id+"' ")
			mydb.commit()
			return render_template('index.html')
	else:
		return render_template('deletedoctor.html')
@app.route('/head')
def head():
	return render_template('index.html')
@app.route('/doctor')
def doctor():
	return render_template('doctors.html')

@app.route('/viewsurgeons',methods = ['POST', 'GET'])
def viewsurgeons():
	if request.method == 'POST':
		return render_template('index.html')
	else:
		mycursor.execute("SELECT * FROM Doctors")
		row_headers=[x[0] for x in mycursor.description] 
		myresult = mycursor.fetchall()
		data={
		'message':"data retrieved",
		'rec':myresult,
		'header':row_headers
		}
		return render_template('view.html',data=data)	     	      	
@app.route('/applyforsurgery' ,methods = ['POST', 'GET'])
def applyforsurgery():
	if request.method == 'POST': 
		name = request.form['name']
		pid = request.form['P_id']
		Did=request.form['d_id']
		age=request.form['age']
		gender=request.form['gender']
		VD=request.form['visit_date']
		SD=request.form['surgery_date']
		ST=request.form['surgery_time']
		urgency=request.form['urgency']
		OR=request.form['OR_Room']
		mycursor = mydb.cursor()
		mycursor.execute("SELECT surgery_date, surgery_time,OR_Room FROM Patients WHERE surgery_time= '" +ST+"' AND surgery_date = '" +SD+ "' AND OR_Room= '" +OR+"' " )
		myresult = mycursor.fetchall()
		for x in myresult:
			print(x)
		if myresult  :
			return render_template('doctors.html', message="room is already occupied! ") 
		else:
			sql = "INSERT INTO Patients(name, P_id ,d_id ,age,gender,visit_date,surgery_date,surgery_time,urgency,OR_Room) VALUES (%s,%s,%s, %s ,%s ,%s,%s, %s ,%s,%s )"
			val = (name,pid,Did,age,gender,VD,SD,ST,urgency,OR)
			mycursor.execute(sql, val)
			mydb.commit() 
			return render_template('doctors.html') 
	else:
			return render_template('apply_for_surgery.html')

@app.route('/patientinfo',methods = ['POST', 'GET'])
def patientinfo():
	if request.method == 'POST': 
		id=request.form['d_id']
		# print(id)
		mycursor.execute( "SELECT * FROM Patients WHERE D_id= '" +id+ "' ")
		row_headers=[x[0] for x in mycursor.description] 
		myresult = mycursor.fetchall()
		data={
		'message':"data retrieved",
		'rec':myresult,
		'header':row_headers
		}
		return render_template('patients_data.html',data=data)
	else:
		return render_template('patient_id.html')
@app.route('/findrooms',methods = ['POST', 'GET'])
def findrooms():
   if request.method == 'POST': 
      Room_ID = request.form['Room ID']
      Department_ID = request.form['Department ID']
      print(Room_ID, Department_ID )
      mycursor.execute( "SELECT * FROM OR_Rooms WHERE Room_id= '" +Room_ID+ "' AND Dep_id = '" +Department_ID+ "' ")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }
      return render_template('viewroom.html',data=data)
   else:
      return render_template('findroom.html')


@app.route('/statistic') 
def statisic():
	mycursor.execute("SELECT COUNT(Result) FROM Patients WHERE Result=1")
	count=mycursor.fetchone()
	mycursor.execute("SELECT COUNT(Result) FROM Patients ")
	count1=mycursor.fetchone()
	return render_template('statistics.html' ,message="surgerical statisics: "+str(count)+"sucess surgeries of "+str(count1))		
@app.route('/LogOut')
def LogOut():
	return render_template('/home.html')

if __name__ == '__main__':
	app.run(debug=True , port=7000)
