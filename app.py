import login as log
import sqlite3 as sq
import os 
import io
import csv
from datetime import datetime as dt

from flask import Flask,render_template,redirect,session,make_response, send_file

from flask import request as rq

from flask import url_for
#Wrapper function to check if file exists
#We use a decorator

def db_file_check(func):
    def wrapper(*args, **kwargs):
        if not os.path.exists(Database.dbname):
            return redirect(rq.url)
        
        #*args = self and **kwargs is like a dict
        return func(*args, **kwargs)
    return wrapper
class Products:

    def __init__(self,db):

        self.dbname = db

        #create connection
        try:
            con = sq.connect(self.dbname)

            #create a cursor.

            cur = con.cursor()

            table = """

        create table if not exists Product(

        SR_no integer primary key AUTOINCREMENT,

        EntryDate date,

        Prod_ID int,

        Prod_Name text,

        Prod_Price double,

        Prod_Qtd int,

        Prod_Size_cms text,

        Total double,

        PaymentType text,

        OrderType text

        );"""

        #use cursor to execute

            cur.execute(table)

            print("Connection successful.")

        #Close once.

            con.close()
        except sq.OperationalError:
            return render_template("manipulator.html")
    
    def startConn(self):

        return sq.connect(self.dbname)
    
    #This is a decorator.
    @db_file_check
    def addEntry(self,ID,Name,Price,Qtd,Size,PaymentT,OrderT):

        con = self.startConn()

        cur = con.cursor()

        Today = dt.now().strftime("%d-%m-%Y")

        Total = (Price * Qtd)

        Query = """

        insert into Product(EntryDate,Prod_ID,Prod_Name,Prod_Price,Prod_Qtd,Prod_Size_cms,Total,PaymentType,OrderType) values

        (?,?,?,?,?,?,?,?,?);

        """
        cur.execute(Query, (Today, ID, Name, Price, Qtd, Size, Total, PaymentT, OrderT))

        con.commit()

        con.close()

    def getEntries(self):

        con = self.startConn()

        cur = con.cursor()

        data = cur.execute("select * from Product order by SR_no DESC;")

        entries = data.fetchall()

        con.close()

        return entries
    
    def deleteEntry(self,SR_no):
        con = self.startConn()
        cur = con.cursor()
        query = "delete from product where SR_no = ?;"
        cur.execute(query,(SR_no,))
        con.commit()
        con.close()
app = Flask(__name__)
app.secret_key = 'zVfkoY_E;(h[war'
Database = Products("Main.db")
Keys = log.login()

@app.route("/",methods=["GET","POST"])
def waitingroom():
    session.clear()
    error = None
    if rq.method == "POST":
        password = rq.form.get("password")
        
        if Keys.checkPassword(password=password):
            session['Logged_in'] = True
            session['Role'] = password
            return redirect(url_for('option'))
        else:
            error = "Error: Invalid password. Try again."
    return render_template("login.html",error=error)

@app.route("/index")
def index():
    try:
        if not session.get('Logged_in'):
            return redirect(url_for("Invalid"))
            #Use select * from
        
        if session.get('Logged_in'):
            entries = Database.getEntries()
            Entity = session.get('Role')

            #send data to html. Here, products is variable which i will use in html. entries is stored in products.

            #so, to use in html, use {product in products}

            return render_template("index.html",products=entries,Entity=Entity)
        else:
            return redirect(url_for("Invalid"))
    except Exception:

        return redirect(url_for("Invalid"))

@app.route("/option")
def option():
    if not session.get('Logged_in'):
        return redirect(url_for("waitingroom"))
    
    Role = session.get('Role')

    if Role == "member":
        Rights = False 
    else:
        Rights = True

    return render_template("option.html",ExtraRights=Rights)

@app.route("/Control",methods=["GET","POST"])
def Control():

    if session.get('Role') not in ["admin","co_admin"]:
                return redirect(url_for('Invalid', message="You do not have permission to access the Control Panel."))
                    
    if rq.method == "POST":
        try:  
                
            if not session.get('Logged_in'):
                return redirect(url_for("Invalid"))
            
            Prod_Name = rq.form.get("Item")
            Prod_Price = float(rq.form.get("Prod_price") or 0.0)
            Prod_Qtd = int(rq.form.get("Prod_qtd") or 0)
                
            PaymentType = rq.form.get("paymentType")
            OrderType = rq.form.get("orderType")
            Prod_id = 0
            Prod_size_cms = "Not found"

            #Fetch data
            entries = Database.getEntries()

            if Prod_Price < 0 or Prod_Qtd < 0 or PaymentType == "Payment type" or OrderType == "Order type" or Prod_Name=="ITEM":
                
                print("Missing fields")
                #Re-fresh page
                return render_template("manipulator.html", products=entries)
            
            if Prod_Name == "a":
                Prod_id = 1
                Prod_size_cms = "1 x 1"
            elif Prod_Name == "b":
                Prod_id = 2
                Prod_size_cms = "1 x 2"
            elif Prod_Name == "c":
                Prod_id = 3
                Prod_size_cms = "1 x 3"
            else:
                Prod_id = 0
                Prod_size_cms = "Not found"

            Entity = session.get('Role')
            Database.addEntry(Prod_id,Prod_Name,Prod_Price,Prod_Qtd,Prod_size_cms,PaymentType,OrderType)
                #This returns updated page.
            return redirect(url_for("Control",extra=True,Entity=Entity))

        except sq.OperationalError as err:
            print(err)
            return redirect(url_for("Invalid"))
        
    entries = Database.getEntries()
    return render_template("manipulator.html", products=entries,extra=True)

@app.route("/Control/<int:SR_no>/delete")
def DeletePage(SR_no):
    
        if not session.get('Logged_in'):
            return redirect(url_for("Invalid"))
        if session.get('Role') not in ["admin", "co_admin"]:
            return redirect(url_for('Invalid', message="You do not have permission to delete entries."))
        Database.deleteEntry(SR_no)
        return redirect(url_for("Control"))

@app.route("/download")
def download():
    # 1. Security Check: Ensure the user is logged in.
    if not session.get('Logged_in'):
        return redirect(url_for("Invalid"))

    # 2. Fetch the data from the database.
    entries = Database.getEntries()

    # 3. Create an in-memory text buffer. This acts like a temporary file
    #    that only exists in the computer's memory.
    output = io.StringIO()
    writer = csv.writer(output)

    # 4. Write the header row for the CSV file.
    header = ['SR_no', 'EntryDate', 'Prod_ID', 'Prod_Name', 'Prod_Price', 'Prod_Qtd', 'Prod_Size_cms', 'Total', 'PaymentType', 'OrderType']
    writer.writerow(header)

    # 5. Write all the data rows from the database into the buffer.
    writer.writerows(entries)

    # 6. Prepare the final response for the browser.
    response = make_response(output.getvalue())
    
    # 7. Set special HTTP headers. These are crucial instructions for the browser.
    #    - 'Content-Disposition' tells the browser to treat this as a downloadable file
    #      and suggests a filename.
    #    - 'Content-type' tells the browser the exact file format.
    response.headers["Content-Disposition"] = "attachment; filename=product_data.csv"
    response.headers["Content-type"] = "text/csv"

    # 8. Return the response to the user, triggering the download.
    return response

@app.route("/2025/credits")
def credits():
    # We use a <style> block to avoid quote issues and keep the HTML clean.
    credits_html = """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.7;
            color: #333;
            background-color: #f4f7f6;
            padding: 2em;
        }
        .credit-container {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 2em;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        h1, p, ul {
            margin-bottom: 1em;
        }
        li {
            list-style-type: square;
            margin-left: 20px;
        }
    </style>
    <div class="credit-container">
        <h1>Website Credits</h1>
        <p>This application was created by <b>Aziz shahiwala</b>.</p>
        <p><b>Front-end and Back-end by Aziz shahiwala.</b></p>
        <h2>Stack Used:</h2>
        <ul>
            <li>HTML5</li>
            <li>Python (Flask)</li>
            <li>CSS</li>
            <li>JavaScript</li>
            <li>SQLite</li>
            <li>Deployed on PythonAnywhere</li>
        </ul>    
    </div>
    """
    return credits_html

@app.route("/invalidroute")
def Invalid():
    # This route now displays the message we pass to it.
    message = rq.args.get('message', "An unknown error occurred.")
    return render_template("invalid.html", message=message)

if __name__ == "__main__":

    app.run()
    