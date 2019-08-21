# pylot - Johnny Lee
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

# declear objects
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///licenses.db'
db = SQLAlchemy(app)

# for use with SQLAlchemy
app.secret_key = b'234@lk1ji123JnQ'

# declare table structure
class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.Text, nullable=False)
    purchase_date = db.Column(db.Integer, nullable=False)
    lic_num = db.Column(db.Text, nullable=False)
    user = db.Column(db.Text, nullable=True)
    expire_date = db.Column(db.Integer, nullable=True)
    lic_port = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"License('{self.app_name}', '{self.purchase_date}', '{self.lic_num}', '{self.user}', '{self.expire_date}'), '{self.lic_port}'))"

# function to insert to database
def add_lic(app_name1, purchase_date1, lic_num1, user1, expire_date1, lic_port1):
    # looping through if multiple licences need to be added
    for list_element in lic_num1:
        lic = License(app_name=app_name1, 
                        purchase_date=purchase_date1, 
                        lic_num=list_element, 
                        user=user1,
                        expire_date=expire_date1,
                        lic_port=lic_port1)
        db.session.add(lic)
        db.session.commit()
    return


# Ignore these weird notes
# app01 = Licenses(app_name='Sketch', lic_num='2342asf232', handle='johnnl', lic_port='No')
# db.session.add(app01)
# db.session.commit()
# license_data = Licenses.query.all()
# data = add_lic(app_name1='gibberish', lic_num1='23423', handle1='ADMIN', lic_port1='No')

# Currently testing only so clear the database and restart again
#db.drop_all()
#b.create_all()

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

    # get data from the forms
    getform_appname = request.form['appname']
    getform_purchase_date = request.form['purchase_date']
    getform_lic_num = request.form.getlist('lic_num')
    getform_user = request.form['user']
    getform_expire_date = request.form['expire_date']
    getform_lic_port = request.form['lic_port']
    
    # write to database
    add_lic(getform_appname, 
            getform_purchase_date, 
            getform_lic_num, 
            getform_user,
            getform_expire_date, 
            getform_lic_port)
    
    # clear data passed from (how_many)
    session.clear()
    return redirect(url_for('show_update_lic'))


@app.route('/show_lic')
def show_update_lic():
    license_list = License.query.all()
    return render_template('show_lic.html', license_list=license_list)

@app.route('/show_lic', methods=['GET', 'POST'])
def edit_lic():
    # declare var to pass by session - this var is ID numbrer of license
    session['get_lic_id'] = request.form['edit']
    return redirect(url_for('update_lic'))
    # below return statement will not work for passing vars thru sessions
    # return render_template('update_lic.html')

@app.route('/update_lic')
def update_lic():
    lic_id = session.get('get_lic_id')
    lic_list = License.query.get(lic_id)
    return render_template('update_lic.html', lic_list=lic_list)

@app.route('/update_lic', methods=['GET', 'POST'])
def submit_update():
    # get ID for correct row and udpate record in dbase with all values
    lic_id = session.get('get_lic_id')
    update_lic = License.query.get(lic_id)

    update_lic.app_name = request.form['appname']
    update_lic.purchase_date = request.form['purchase_date']
    update_lic.lic_num = request.form['lic_num']
    update_lic.user = request.form['user']
    update_lic.expire_date = request.form['expire_date']

    db.session.commit()

    updated_lic = License.query.get(lic_id)

    # clear data passed from edit_lic
    session.clear()
    return render_template('update_status.html', updated_lic=updated_lic)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)