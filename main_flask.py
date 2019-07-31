# pylot - Johnny Lee
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# declear objects
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///licenses.db'
db = SQLAlchemy(app)

# for use with SQLAlchemy
app.secret_key = b'234@lk1ji123JnQ'

# declare table structure
class Licenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.Text, nullable=False)
    lic_date = db.Column(db.Integer, nullable=False)
    lic_num = db.Column(db.Text, nullable=False)
    handle = db.Column(db.Text, nullable=True)
    lic_port = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"Licenses('{self.app_name}', '{self.lic_date}', '{self.lic_num}', '{self.handle}', '{self.lic_port}')"

# function to write to database
def add_lic(app_name1, lic_date1, lic_num1, handle1, lic_port1):
    lic = Licenses(app_name=app_name1, 
                    lic_date=lic_date1, 
                    lic_num=lic_num1, 
                    handle=handle1, 
                    lic_port=lic_port1)
    db.session.add(lic)
    db.session.commit()
    results = Licenses.query.all()
    return results

# Ignore these weird notes
# app01 = Licenses(app_name='Sketch', lic_num='2342asf232', handle='johnnl', lic_port='No')
# db.session.add(app01)
# db.session.commit()
# license_data = Licenses.query.all()
# data = add_lic(app_name1='gibberish', lic_num1='23423', handle1='ADMIN', lic_port1='No')

# Currently testing only so clear the database and restart again
db.drop_all()
db.create_all()

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/how_many')
def ask_how_many():
    return render_template('how_many.html')

@app.route('/how_many', methods=['GET', 'POST'])
def enter_mult_lic():
    session['num_of_lic'] = request.form['num_of_lic']
    return redirect(url_for('enter_lic'))

@app.route('/enter_lic')
def enter_lic():
    tmp_num_lic = session.get('num_of_lic')
    # incrase by one to accurately print out number of licences in for range
    passed_num_lic = int(tmp_num_lic) + 1
    return render_template('enter_lic.html', passed_num_lic=passed_num_lic)

@app.route('/enter_lic', methods=['GET', 'POST'])
def add_lic_page_post():
    # Get data passed from previous session (how_many)
    # passpass = session.get('num_of_lic')
    # lic_list = request.form.getlist('lic_num')
    
    # get data from the forms
    getform_appname = request.form['appname']
    getform_lic_date = request.form['lic_date']
    getform_lic_num = request.form['lic_num']
    getform_handle = request.form['handle']
    getform_lic_port = request.form['lic_port']
    
    
    # write to database
    add_lic(getform_appname, 
            getform_lic_date, 
            getform_lic_num, 
            getform_handle, 
            getform_lic_port)
    
    # clear data passed from (how_many)
    session.clear()
    return render_template(
                            'enter_lic_success.html', 
                            getform_appname=getform_appname, 
                            getform_lic_date=getform_lic_date, 
                            getform_lic_num=getform_lic_num, 
                            getform_handle=getform_handle, 
                            getform_lic_port=getform_lic_port
                            )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)


# ============================================================
# @app.route('/', methods = ['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         date = request.form.get('date')
#         return redirect(url_for('booking', date=date))
#     return render_template('main/index.html')
# @app.route('/booking')
# def booking():
#     date = request.args.get('date', None)
#     return render_template('main/booking.html', date=date)    

# if __name__ == '__main__':
#     app.run(debug=True)