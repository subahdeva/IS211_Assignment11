from flask import Flask, render_template, request, redirect
import re
import pickle
__author__ = 'subahdeva'


todo = Flask(__name__)

db = 'todo.pkl'

tasklist = []

errors = []

count = 0


def dump_list(dbfile, data):
    try:
        with open(dbfile, 'wb') as datafile:
            pickle.dump(data, datafile)
            return True
    except IOError:
        errors.append('Could not save data')
    return False


def load_list(dbfile):
    try:
        with open(dbfile, 'rb') as datafile:
            data = pickle.load(datafile)
            return data
    except IOError:
        errors.append('Could not load data')
    return []


@todo.route('/')
def tasks():
    """
    Todo list entry and display
    """
    app_title = 'To Do List'
    app_entry = 'Create a new task'
    app_display = 'To Do List'
    tasklist = load_list(db)
    return render_template('index.html',
                           app_title=app_title,
                           app_entry=app_entry,
                           app_display=app_display,
                           tasks=tasklist,
                           errors=errors)


@todo.route('/submit', methods=['POST'])
def submit():
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    task = request.form['taskName'].strip()
    email = request.form['emailAdd'].strip()
    priority = request.form['priority'].strip()

    if task == '':
        errors.append('No task defined')
    elif not re.search(pattern, email):
        errors.append('Bad email address format')

    else:
        if len(errors) > 0:
            del errors[:]

        tasklist.append((task, email, priority))
        dump_list(db, tasklist)

    return redirect('/')


@todo.route('/clear', methods=['POST'])
def clear():
    if len(errors) > 0:
        del errors[:]

    cmd = request.form['clear'].lower().strip()
    idx = int(cmd) - 1
    if idx == -1:
        if len(tasklist) > 0:
            del tasklist[:]

    elif 0 <= idx < len(tasklist):
        tasklist.pop(idx)

    dump_list(db, tasklist)

    return redirect('/')


if __name__ == '__main__':
    todo.run()