from flask import render_template, request, redirect, url_for
from app import app
import psycopg2
from dbconfig import config

conn = None


def get_parts():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT part_id, part_name FROM parts ORDER BY part_id")
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows


def insert_parts(part_name):
    sql = """INSERT INTO parts(part_name)
             VALUES(%s) RETURNING parts_id;"""
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (part_name,))
        part_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return part_id


def delete_parts(part_id):
    sql = """delete from parts where part_id = %s;"""
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (part_id,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return 1


def update_parts(part_name, part_id):
    sql = """update parts set part_name = %s where part_id = %s;"""
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (part_name, part_id))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return 1


def search_parts(id):
    sql = "select * from parts where part_id =%s"
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


@app.route('/parts', methods=['GET', 'POST'])
def parts():
    rows = get_parts()
    return render_template('parts.html', rows=rows)


@app.route('/new_part', methods=['GET', 'POST'])
def New_part():
    name = request.form.get("pname")
    if request.method == 'POST':
        insert_parts(name)
        return render_template('alert.html', p_message="created successfully")
    return render_template('new_part.html')


@app.route('/delete_part/<int:id>', methods=['GET', 'POST'])
def delete_part(id):
    delete_parts(id)
    return render_template('alert.html', p_message="deleted successfully")


@app.route('/update_part/<int:id>', methods=['GET', 'POST'])
def update_part(id):
    rows = search_parts(id)
    if request.method == 'POST':
        name = request.form.get("pname")
        update_parts(name, id)
        return render_template('alert.html', p_message="updated successfully")
    return render_template('update_part.html', rows=rows)