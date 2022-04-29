from flask import render_template, request, redirect, url_for
from app import app
import psycopg2
from dbconfig import config

conn = None


def get_vendors():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_id")
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows


def insert_vendors(vendor_name):
    sql = """INSERT INTO vendors(vendor_name)
             VALUES(%s) RETURNING vendor_id;"""
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (vendor_name,))
        vendor_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return "inserted"


def delete_vendors(vendor_id):
    sql = """delete from vendors where vendor_id = %s;"""
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (vendor_id,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return 1


def update_vendors(vendor_name, vendor_id):
    sql = """update vendors set vendor_name = %s where vendor_id = %s;"""
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (vendor_name, vendor_id))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return 1


def search_vendors(id):
    sql = "select * from vendors where vendor_id =%s"
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



@app.route('/vendor')
def vendors():
    rows = get_vendors()
    return render_template('vendors.html', rows=rows)


@app.route('/new_vendor', methods=['GET', 'POST'])
def New_vendor():
    name = request.form.get("pname")
    if request.method == 'POST':
        insert_vendors(name)
        return render_template('alert.html', v_message="created successfully")
    return render_template('new_vendor.html')


@app.route('/delete_vendor/<int:id>', methods=['GET', 'POST'])
def delete_vendor(id):
    delete_vendors(id)
    return render_template('alert.html', v_message="deleted successfully")


@app.route('/update_vendor/<int:id>', methods=['GET', 'POST'])
def update_vendor(id):
    rows = search_vendors(id)
    if request.method == 'POST':
        name = request.form.get("pname")
        update_vendors(name, id)
        return render_template('alert.html', v_message="updated successfully")
    return render_template('update_vendor.html', rows=rows)