# models.py

from main_flask import db

# declare table structure
class Licenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.Text, nullable=False)
    purchase_date = db.Column(db.Integer, nullable=False)
    lic_num = db.Column(db.Text, nullable=False)
    user = db.Column(db.Text, nullable=True)
    expire_date = db.Column(db.Integer, nullable=True)
    lic_port = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Licenses('{self.app_name}', '{self.purchase_date}', '{self.lic_num}', '{self.user}', '{self.expire_date}'), '{self.lic_port}'))"


# Ignore these weird notes
# app01 = Licenses(app_name='Sketch', lic_num='2342asf232', handle='johnnl', lic_port='No')
# db.session.add(app01)
# db.session.commit()
# license_data = Licenses.query.all()
# data = add_lic(app_name1='gibberish', lic_num1='23423', handle1='ADMIN', lic_port1='No')

# Currently testing only so clear the database and restart again
db.drop_all()
db.create_all()