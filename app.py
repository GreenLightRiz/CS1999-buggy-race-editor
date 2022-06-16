from flask import Flask, render_template, request, jsonify
import os
import sqlite3 as sql

from numpy import record

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "https://rhul.buggyrace.net"
#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone(); 
        return render_template("buggy-form.html", buggy = None) 

    elif request.method == 'POST':
        msg=""
        violations = ""
        cost = ""
        buggy_id = request.form['id']         
        
        qty_wheels = request.form['qty_wheels']        
        if not qty_wheels.isdigit():
            msg = f"Error: Data entry for qty_wheels is not a number! You wrote: {qty_wheels}"
            return render_template("updated.html", msg = msg, violations = violations)
        elif int(qty_wheels) % 2 != 0:
            msg = f"ERROR! Your vehicle cannot have an odd number of wheels! You wrote: {qty_wheels} "
            return render_template("updated.html", msg = msg, violations = violations)
        elif int(qty_wheels) < 4:
            violations = f"ERROR! too few wheels; minimum is 4"
            return render_template("updated.html", msg = msg, violations = violations)             

        
        tyreNo = request.form['tyreNo']
        if not tyreNo.isdigit():
            violations = f"Error: Data entry for tyreNo is not a number! You wrote: {tyreNo}"
            return render_template("updated.html", msg = msg, violations = violations)       
        if int(tyreNo) % 2 != 0:
            violations = f"ERROR! Your vehicle cannot have an odd number of tyres! You wrote: {tyreNo} "
            return render_template("updated.html", msg = msg, violations = violations) 
        elif int(tyreNo) < 4:
            violations = f"ERROR! too few tyres; minimum is 4"
            return render_template("updated.html", msg = msg, violations = violations) 

            
        total_cost = 0
        
        flag_color = request.form['flag_color']
        if flag_color == "select":
            violations = f"Error: you did not select anything for one of the options! Please try again"
            return render_template("updated.html", msg = msg, violations = violations)       
            
                
        flag_color_secondary = request.form['flag_color_secondary'] 
        if flag_color_secondary == "select":
            violations = f"Error: you did not select anything for one of the options! Please try again"
            return render_template("updated.html", msg = msg, violations = violations)             
        
        flag_pattern = request.form['flag_pattern']  
        if flag_pattern == "select":
            violations = f"Error: you did not select anything for one of the options! Please try again"
            return render_template("updated.html", msg = msg, violations = violations)             
        
        tyres = request.form['tyres']
        if tyres == "knobbly":
            total_cost += 15
        elif tyres == "slick":
            total_cost += 10
        elif tyres == "steelband":
            total_cost += 20
        elif tyres == "reactive":
            total_cost += 40
        elif tyres == "maglev":
            total_cost += 50
        if tyres == "select":
            violations = f"Error: you did not select anything for one of the options! Please try again"
            return render_template("updated.html", msg = msg, violations = violations)                          


        power_type = request.form['power_type']
        if power_type == "petrol":
            total_cost = total_cost + 4
        elif power_type == "fusion":
            total_cost = total_cost + 400
        elif power_type == "steam":
            total_cost = total_cost + 3
        elif power_type == "bio":
            total_cost = total_cost + 5
        elif power_type == "electric":
            total_cost = total_cost + 20
        elif power_type == "rocket":
            total_cost = total_cost + 16
        elif power_type == "hamster": 
            total_cost = total_cost + 3       
        elif power_type == "thermo":
            total_cost = total_cost + 300
        elif power_type == "solar":
            total_cost = total_cost + 40
        elif power_type == "wind":
            total_cost = total_cost + 20    
        elif power_type == "select":
            violations = f"Error: you did not select anything for one of the options! Please try again"
            return render_template("updated.html", msg = msg, violations = violations)                       

        armour = request.form['armour']        
        if armour == "none":
            total_cost += 0
        elif armour == "wood":
            total_cost += 40
        elif armour == "aluminium":
            total_cost += 200
        elif armour == "thinsteel":
            total_cost += 100
        elif armour == "thicksteel": 
            total_cost += 200
        elif armour == "titanium":
            total_cost += 290
        elif armour == "select":
            violations = f"Error: you did not select anything for one of the options! Please try again"
            return render_template("updated.html", msg = msg, violations = violations)                 

                                                  

        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                if buggy_id:
                    cur.execute(
                        "UPDATE buggies set qty_wheels=? WHERE id=?",
                        (qty_wheels, buggy_id)
                    )
                    cur.execute(
                        "UPDATE buggies set flag_color=? WHERE id=?",
                        (flag_color, buggy_id)
                    )
                    cur.execute(
                        "UPDATE buggies set flag_color_secondary=? WHERE id=?",
                        (flag_color_secondary, buggy_id)
                    )
                    cur.execute(
                        "UPDATE buggies set flag_pattern=? WHERE id=?",
                        (flag_pattern, buggy_id)
                    )
                    cur.execute(
                        "UPDATE buggies set tyres=? WHERE id=?",
                        (tyres, buggy_id)
                    )
                    cur.execute(
                        "UPDATE buggies set tyreNo=? WHERE id=?",
                        (tyreNo, buggy_id)
                    )
                    cur.execute(
                        "UPDATE buggies set power_type=? WHERE id=?",
                        (power_type, buggy_id)
                    )
                    cur.execute(
                        "UPDATE buggies set armour=? WHERE id=?",
                        (armour, buggy_id)
                    )
                    cur.execute(
                        "UPDATE buggies set total_cost=? WHERE id=?",
                        (total_cost, buggy_id)
                    )
                    

                else:
                    cur.execute(
                        "INSERT INTO buggies (qty_wheels, flag_color, flag_color_secondary, flag_pattern, tyres, tyreNo, power_type, armour, total_cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (qty_wheels, flag_color, flag_color_secondary, flag_pattern, tyres, tyreNo, power_type, armour, total_cost)
                    )                                                             
                    con.commit() 

                msg = (f'''Record successfully saved.

                The total cost is: {total_cost}
                    ''')                      
        except:
            con.rollback() 
            msg = "error in update operation"
        finally:
            con.close()
        return render_template("updated.html", msg = msg, violations = violations, cost = cost)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchall();  
    return render_template("buggy.html", buggies = record)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
    print (f"I want to edit buggy #{buggy_id}")
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row 
    cur = con.cursor() 
    cur.execute("SELECT * FROM buggies WHERE id=?", (buggy_id,))
    record = cur.fetchone();  
    return render_template("buggy-form.html", buggy = record)

#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items() 
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })

@app.route('/info')
def info():
    return render_template('/info.html')

@app.route('/poster')
def poster():
    return render_template('/poster.html')    



# You shouldn't need to add anything below this!
if __name__ == '__main__':
    alloc_port = os.environ['CS1999_PORT']
    app.run(debug=True, host="0.0.0.0", port=alloc_port) 
