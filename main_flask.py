# pylot - Johnny Lee
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from finger import finger

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
    jira = db.Column(db.Text, nullable=True)
    lic_num = db.Column(db.Text, nullable=False)
    user = db.Column(db.Text, nullable=True)
    expire_date = db.Column(db.Integer, nullable=True)
    lic_port = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"License('{self.app_name}', '{self.jira}', '{self.lic_num}', '{self.user}', '{self.expire_date}'), '{self.lic_port}'))"

# function to insert to database
def add_lic(app_name1, jira1, lic_num1, user1, expire_date1, lic_port1):
    # looping through if multiple licences need to be added
    for list_element in lic_num1:
        lic = License(app_name=app_name1, 
                        jira=jira1, 
                        lic_num=list_element, 
                        user=user1,
                        expire_date=expire_date1,
                        lic_port=lic_port1)
        db.session.add(lic)
        db.session.commit()
    return

# Currently testing only so clear the database and restart again
#db.drop_all()
#db.create_all()

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
    getform_jira = request.form['jira']
    getform_lic_num = request.form.getlist('lic_num')
    getform_user = request.form['user']
    getform_expire_date = request.form['expire_date']
    getform_lic_port = request.form['lic_port']
    
    # write to database
    add_lic(getform_appname, 
            getform_jira, 
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

    # Stats for top of the page
    license_count = License.query.count()
    lic_count_assigned = License.query.filter(License.user != '')
    lic_count_free = License.query.filter(License.user == '')

    finger_user = ''
    # Run a for loop to finger a username and check if they are active or seperated. Then update the database before displaying
    row_counter = 1
    for x in license_list:
        update_license = License.query.get(row_counter)
        finger_user = finger(x.user)
        if update_license.user == '':
            active_user = ''
        elif finger_user['disabled'] == True: 
            active_user = ''
        else:
            active_user = update_license.user
        update_license.user = active_user
        db.session.commit()
        row_counter += 1

    return render_template('show_lic.html', license_list=license_list, lic_count_assigned=lic_count_assigned, license_count=license_count, lic_count_free=lic_count_free)

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
    update_lic.jira = request.form['jira']
    update_lic.lic_num = request.form['lic_num']
    update_lic.user = request.form['user']
    update_lic.expire_date = request.form['expire_date']

    # commit to dbase
    db.session.commit()

    updated_lic = License.query.get(lic_id)

    # clear data passed from edit_lic session
    session.clear()
    return render_template('update_status.html', updated_lic=updated_lic)

@app.route('/test')
def test():
    
    active_user = ''
    finger_user = 'Johnny'
    finger_results = finger(finger_user)
    if finger_results['name'] == "Unknown": 
        active_user = 'No User'
    else:
        active_user = finger_user


    return render_template('test.html', finger_results=finger_results, active_user=active_user)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)