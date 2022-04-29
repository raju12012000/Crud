from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
conn = None

import psycopg2
from dbconfig import config
from parts import get_parts
import parts
import vendors


def vendor_report(id):
    sql = "SELECT vendors.vendor_id,vendors.vendor_name FROM vendors inner join vendor_parts on vendor_parts.vendor_id = vendors.vendor_id where vendor_parts.part_id=%s order by vendor_id"
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (id,))
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows


def product_report(id):
    sql = "SELECT * FROM parts where part_id=%s"
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (id,))
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows


def get_assign_vendors(part_id):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.callproc('get_vendor_by_parts', (part_id,))
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows


def Assign_vendor(part_id, vendor_list):
    assign_vendor = "INSERT INTO vendor_parts(vendor_id,part_id) VALUES(%s,%s)"
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for vendor_id in vendor_list:
            cur.execute(assign_vendor, (vendor_id, part_id))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def delete_vendors_availability(vendor_id, part_id):
    sql = """delete from vendor_parts where vendor_id = %s and part_id = %s;"""
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (vendor_id, part_id))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return 1


@app.route('/check_vendors/<int:id>')
def check_vendors(id):
    vrows = vendor_report(id)
    prows = product_report(id)
    return render_template('product_availability.html', prows=prows, vrows=vrows)



@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    rows = get_parts()
    return render_template('home.html', rows=rows)


@app.route('/assign_vendor/<int:pid>', methods=['GET', 'POST'])
def assign_vendor(pid):
    prows = product_report(pid)
    vrows = get_assign_vendors(pid)
    if request.method == 'POST':
        vid = request.form.getlist("vendors")
        Assign_vendor(pid, vid)
        return redirect(url_for('parts'))
    return render_template('assign_vendor.html', prows=prows, vrows=vrows)


@app.route('/delete_vendor_availability/<int:vid>/<int:pid>', methods=['GET', 'POST'])
def Delete_vendors_availability(vid, pid):
    delete_vendors_availability(vid, pid)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

