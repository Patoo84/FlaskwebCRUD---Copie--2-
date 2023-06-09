from flask import Flask, render_template,request,redirect,url_for,flash
from google.cloud import bigquery
from google.cloud.bigquery import dbapi
from datetime import datetime, timezone
import uuid
from uuid import uuid1
import unicodedata
project_id = 'ep-divabox-div2110184207'
client = bigquery.Client(project=project_id)


app = Flask(__name__)
app.secret_key='SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'bigquery://ep-divabox-div2110184207.DIVABOX_DATASTUDIO_EXTERNAL'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
@app.route("/")
def index():
    
    conn = dbapi.Connection(client)
    curr = conn.cursor()

    query = """
        SELECT * FROM `ep-divabox-div2110184207.DIVABOX_DATASTUDIO_EXTERNAL.SECURITY`
         
 
  
           """
    curr.execute(query)
    list_users = curr.fetchall()
    query_marque ="""
        SELECT distinct marque FROM `ep-divabox-div2110184207.DTS_DIVABOX_DMART.ref_article` order by  marque asc
         
 
  
           """
    curr.execute(query_marque)
    list_marque = curr.fetchall()
    return render_template("index.html",list_users=list_users,list_marque=list_marque)
@app.route('/insert',methods =['POST'])
def insert():
    if request.method=='POST':
        flash("Data Inserted Successfully")
        ID =  str(uuid.uuid1())
        email = request.form['Email']
        Marque = request.form['comp_select']
        conn = dbapi.Connection(client)
        curr = conn.cursor()
        '''curr.execute("SELECT * FROM ep-divabox-div2110184207.DIVABOX_DATASTUDIO_EXTERNAL.SECURITY WHERE email=%s", (email,)) 
        existingInfo = curr.fetchone()
        if existingInfo is not None:
         return "Error: email is already registered"
        curr.execute("SELECT * FROM ep-divabox-div2110184207.DIVABOX_DATASTUDIO_EXTERNAL.SECURITY WHERE Marque=%s", (Marque,))
        existingMarque = curr.fetchone() 
        if existingMarque is not None :
         return "Error: Marque is already registered"
        else :'''
        Marque_strim = Marque.replace(" ", "")
        Marque_quote = Marque_strim.replace("'","")
        Marque_accent = unicodedata.normalize('NFKD',Marque_quote).encode('ascii', 'ignore').decode("utf-8")
        Url = "https://storage.cloud.google.com/divabox_datastudio_images/Logos_marque/"+Marque_accent+".png?authuser=0"
        utc = timezone.utc
        created_at = datetime.now(utc)
        curr.execute("INSERT INTO ep-divabox-div2110184207.DIVABOX_DATASTUDIO_EXTERNAL.SECURITY(ID,email,Marque,Url,created_at)VALUES(%s,%s,%s,%s,%s)",(ID,email,Marque,Url,created_at))
        conn.commit()
        return redirect(url_for('index'))
    

@app.route('/update',methods=['POST','GET'])
def update():
        
    if request.method == 'POST':
        
        id_data = request.form['ID']
        #email = request.form['Email']
        Marque = request.form['comp_select']
       
        conn = dbapi.Connection(client)
        curr = conn.cursor()
        '''curr.execute("SELECT * FROM ep-divabox-div2110184207.DIVABOX_DATASTUDIO_EXTERNAL.SECURITY WHERE Marque=%s", (Marque,))
        existingInfo = curr.fetchone()
        if existingInfo is not None:
         return "Error: Marque is already registered"
        else :'''
        Marque_strim = Marque.replace(" ", "")
        Url = "https://storage.cloud.google.com/divabox_datastudio_images/Logos_marque/"+Marque_strim+".png?authuser=0"
        curr.execute("""
               UPDATE ep-divabox-div2110184207.DIVABOX_DATASTUDIO_EXTERNAL.SECURITY
               SET Marque=%s, Url=%s
               WHERE ID=%s
            """, (Marque, Url, id_data))
        flash("Data Updated Successfully")
        conn.commit()
        return redirect(url_for('index'))
    

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    conn = dbapi.Connection(client)
    curr = conn.cursor()
    curr.execute("DELETE FROM ep-divabox-div2110184207.DIVABOX_DATASTUDIO_EXTERNAL.SECURITY WHERE ID=%s", (id_data,))
    conn.commit()
    return redirect(url_for('index'))     
  
if __name__ == "__main__":
    app.run(debug=True)
    