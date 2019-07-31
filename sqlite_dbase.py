"""
import sqlite3
from licenses import Applications
# create object
connect_object = sqlite3.connect(':memory:')

# create cursor
c = connect_object.cursor()

c.execute("""CREATE TABLE licenses (
            app_name text,
            lic_num text,
            handle text,
            lic_port text
) """)

def insert_license(app):
    with connect_object:
        c.execute("INSERT INTO licenses VALUES (?,?,?,?)", (app.app_name, app.lic_num, app.handle, app.lic_port))

def get_app_by_appname(app):
        c.execute("SELECT * FROM licenses WHERE app_name=?", (app,))
        return c.fetchall()

def show_all():
        c.execute("SELECT * FROM licenses")
        return c.fetchall()

def remove_license(handle):
    with connect_object:
        c.execute("DELETE FROM licenses WHERE handle=?", (handle,))

# define all data (create instances)
app01 = Applications('Sketch', 'w23423422111', 'tpuni', 'True')
app02 = Applications('Sketch', 'w3234wrfs', 'johnnl', 'True')
app03 = Applications('Admin', 'alasjfaksjfd', 'akabeer', 'True')

# run functions to assign input data
insert_license(app01)
insert_license(app02)
insert_license(app03)

lic_list = get_app_by_appname('Sketch')
show = show_all()

print(lic_list)
print(show)

remove_license('johnnl')
# re-query this and assign to show otherwies stale query still there
show = show_all()
print(show)

connect_object.close()

"""