from flask import Flask,render_template,request,session,redirect,url_for,Response,flash
from datetime import datetime
from flask_mysqldb import MySQL


# first - option login
# home=srch by bld form
# index1=hosp login form
# index2-bbman login form
# table-table to display of particular bank

app=Flask(__name__)
app.secret_key='thisisverysuperkey'
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="Giri200**"
app.config['MYSQL_DB']="bbms"
  
mysql=MySQL(app)


@app.route('/',methods=['GET','POST'])
def index():
	return render_template('first.html')

@app.route("/login",methods=['GET','POST'])
def login():
	msg=''
	if request.method=="POST":
		h_id=request.form['h_id']
		password=request.form['password']
		cur=mysql.connection.cursor()
		cur.execute("SELECT * FROM hosp_info WHERE h_id=%s AND password=%s",(h_id,password))
		record=cur.fetchone()
		if record:
			session['loggedin']=True
			session['h_id']=record[0]
			return redirect(url_for('home'))
		else:
			flash("Icorrect id/password")
	return render_template('index1.html',msg=msg)

@app.route('/home')
def home():
	return render_template('home.html',h_id=session['h_id'])

@app.route("/hospital-requesting-form",methods=['GET','POST'])
def hosprequest():
	cur=mysql.connection.cursor()
	if request.method=="POST":
		# s_no=request.form['s_no']
		bld_grp=request.form['bld_grp']
		bld_qty=request.form['bld_qty']
		m_id=request.form['m_id']
		# status='n'
		h_id=session['h_id']
		cur.execute("SELECT h_name,city_id,h_phno,password FROM hospr WHERE h_id=%s",[h_id])
		hospinfo=cur.fetchone()
		h_name=hospinfo[0]
		city_id=hospinfo[1]
		h_phno=hospinfo[2]
		password=hospinfo[3]
		# date=hospinfo[1]
		# now=datetime.now()
    	# date=now.strftime("%Y-%m-%d %H:%M:%S")
    	

		cur.execute("INSERT INTO hosp_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,now())",(h_id,h_name,bld_grp,bld_qty,h_phno,city_id,m_id,password))
		mysql.connection.commit()


	return render_template("hospreq.html",h_id=session['h_id'])

@app.route("/bbmanlogin",methods=['GET','POST'])
def bblogin():
	msg=''
	if request.method=="POST":
		m_id=request.form['m_id']
		global manager_id
		manager_id=m_id
		
		password=request.form['password']
		cur=mysql.connection.cursor()
		cur.execute("SELECT * FROM bb_man WHERE m_id=%s AND password=%s",(m_id,password))
		record=cur.fetchone()
		if record:
			session['loggedin']=True
			session['m_id']=record[0]
			return redirect(url_for('after_login'))
		else:
			flash("Icorrect id/password")
			msg="Incorrect password !!"
	return render_template('index2.html',msg=msg)


@app.route("/insert-to-bank-by-bbman",methods=['GET','POST'])
def inserting():
	cur=mysql.connection.cursor()
	if request.method=="POST":
		# s_no=request.form['s_no']
		bld_grp=request.form['bld_grp']
		bld_qty=request.form['bld_qty']
		d_id=request.form['d_id']
		status='n'
		m_id=session['m_id']
		# m_id=manager_id
		cur.execute("INSERT INTO bld_sp(bld_grp,bld_qty,status,m_id,d_id) VALUES(%s,%s,%s,%s,%s)",(bld_grp,bld_qty,status,m_id,d_id))
		mysql.connection.commit()


	return render_template('insert.html')



@app.route("/searchbyhosp",methods=['GET','POST'])
def search():
	msg=''
	if request.method=="POST":
		bld_grp=request.form['bld_grp']
		# city_id=request.form['city_id']
		cur=mysql.connection.cursor()
		cur.execute("SELECT bld_sp.bld_grp,bb_man.m_city_id,count(*),bld_sp.m_id,bb_man.m_name,bb_man.m_email,bb_man.m_phno from bld_sp inner join bb_man on bld_sp.m_id=bb_man.m_id and bld_sp.bld_grp=%s group by bb_man.m_city_id,bld_sp.bld_grp order by count(*) desc",[bld_grp])
		recording=cur.fetchall()
		if recording:
			return render_template('table.html',recording=recording)
		else:
		# 	msg='No Records found!!'
			return render_template('table.html',recording=recording)
	return render_template('home.html')



@app.route("/bbman-after-login",methods=['GET','POST'])
def after_login():
	return render_template("bbmanoption.html")

@app.route("/requests")
def requesting():
	#request is a view of hosp_info table
	cur=mysql.connection.cursor()
	m_id=session['m_id']
	cur.execute("SELECT * FROM request1 WHERE m_id=%s ORDER BY req_date",[str(m_id)])
	recording=cur.fetchall()
	if recording:
		return render_template('requests.html',recording=recording)
	else:
		# 	msg='No Records found!!'
		return render_template('requests.html',recording=recording)

@app.route("/total-data-in-database",methods=['GET','POST'])
def totalbldspce():
	cur=mysql.connection.cursor()
	m_id=session['m_id']
	cur.execute("SELECT s_no,bld_grp,bld_qty,m_id,d_id FROM bld_sp WHERE m_id=%s AND status='n' ORDER BY bld_grp",[str(m_id)])
	recording=cur.fetchall()
	cur.execute("SELECT bld_grp,count(*) from bld_sp WHERE m_id=%s AND status='n' GROUP BY bld_grp ORDER BY bld_grp",[str(m_id)])
	recording_cnt=cur.fetchall()
	if recording:
		return render_template('totalblds.html',recording=recording,recording_cnt=recording_cnt)
	else:
		# 	msg='No Records found!!'
		return render_template('totalblds.html',recording=recording,recording_cnt=recording_cnt)

@app.route("/delete/<int:s_no>",methods=['GET','POST'] )
def deletebld(s_no):
	cur=mysql.connection.cursor()
	cur.execute("DELETE FROM bld_sp WHERE s_no=%s", [str(s_no)])
	mysql.connection.commit()

	return redirect(url_for('totalbldspce'))



from flaskext.mysql import MySQL #pip install flask-mysql
import pymysql
from fpdf import FPDF #pip install fpdf 

Mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Giri200**'
app.config['MYSQL_DATABASE_DB'] = 'bbms'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
Mysql.init_app(app)
@app.route('/download/report/pdf')
def download_report():
    
    
    conn = Mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
     
    #select city.city_name,bb_man.m_city_id,bld_sp.m_id,bld_sp.bld_grp,count(*) from bld_sp 
    #inner join bb_man on bb_man.m_id=bld_sp.m_id inner join city on city.city_id=bb_man.m_city_id group by bb_man.m_city_id,bld_sp.bld_grp,bld_sp.m_id order by city.city_name,bld_sp.bld_grp;

    cursor.execute("SELECT * FROM report1")
    result = cursor.fetchall()
 
    pdf = FPDF()
    pdf.add_page()
     
    page_width = pdf.w - 2 * pdf.l_margin
     
    pdf.set_font('Times','B',14.0) 
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y  %H:%M:%S")
    pdf.image("D:/PROGRAMMING/dbpro/govt.png", x = 100, y = 0, w = 15, h = 15, type = 'png', link = '')
    pdf.ln(10)
    pdf.cell(page_width, 0.0, 'GOVERNMENT OF KARNATAKA', align='C')
    pdf.ln(10)
   
    pdf.cell(page_width, 0.0, 'DAILY REPORT', align='C')
    pdf.ln(10)
    pdf.cell(page_width, 0.0,f'DATE TIME : {dt_string}' ,align='R')
    pdf.ln(10)

    pdf.set_font('Times', 'B', 12)
    pdf.cell(page_width, 0.0,'CITY NAME         CITY ID                 MAN ID         BLD GRP         COUNT',align='L')     
    col_width = page_width/5.2
         
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
             
    th = pdf.font_size
         
    for row in result:
        pdf.cell(col_width,th,str(row['city_name']),border=1)
        pdf.cell(col_width,th,str(row['m_city_id']),border=1)
        pdf.cell(col_width/2,th,str(row['m_id']),border=1)
        pdf.cell(col_width,th,str(row['bld_grp']),border=1)
        pdf.cell(col_width,th,str(row['count(*)']),border=1)
       
        pdf.ln(th)
         
    pdf.ln(5)
         
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
         
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=total_report.pdf'})

@app.route('/download/request-report/pdf')
def request_report():
    
    
    conn = Mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    m_id=session['m_id']     
    cursor.execute("SELECT * FROM request1 WHERE m_id=%s",str(m_id))
    result = cursor.fetchall()
 
    pdf = FPDF('L','mm','A4')
    pdf.add_page()
     
    page_width = pdf.w - 2 * pdf.l_margin
     
    pdf.set_font('Times','B',14) 
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y  %H:%M:%S")
    pdf.ln(10)
    

    pdf.cell(page_width, 0.0, 'REQUEST FORMS', align='C')
    pdf.ln(10)
    pdf.image("D:/PROGRAMMING/dbpro/logo1.jpg", x = 140, y = 0, w = 15, h = 15, type = 'jpg', link = '')
    pdf.ln(10)
    pdf.cell(page_width, 0.0,f'DATE TIME : {dt_string}' ,align='R')
    pdf.ln(10)
    pdf.cell(page_width, 0.0,'  HOSP ID       HOSP NAME          BLD GRP  PACKETS  PH NO              CITY ID    M ID          DATE',align='L')
    pdf.set_font('Times', '', 12)
         
    col_width = page_width/6
         
    pdf.ln(10)
         
    th = pdf.font_size
         
    for row in result:
        pdf.cell(col_width/2,th,str(row['h_id']),border=1)
        pdf.cell(col_width+2,th,str(row['h_name']),border=1)
        pdf.cell(col_width/3,th,str(row['h_need_bld_grp']),border=1)
        pdf.cell(col_width/2,th,str(row['h_need_qty']),border=1)
        pdf.cell(col_width,th,str(row['h_phno']),border=1)
        pdf.cell(col_width/2,th,str(row['city_id']),border=1)
        pdf.cell(col_width/2,th,str(row['m_id']),border=1)
        pdf.cell(col_width+4,th,str(row['req_date']),border=1)
       
        pdf.ln(th)
         
    pdf.ln(10)
         
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, 'Signature of Blood Bank Manager', align='L')
    pdf.ln(10)
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
         
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=request.pdf'})



if __name__=="__main__":
	app.run(debug=True)