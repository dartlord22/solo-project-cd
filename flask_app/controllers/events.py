from flask_app import app 
from flask_app.models.event import Event
from flask_app.models.user import User
import datetime
from flask import render_template, redirect, request, session

@app.route('/events')
def my_events():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('my_events.html', events = Event.get_all_for_user(session['user_id']), datetime=datetime, user_id=session['user_id'])

@app.route('/events/add', methods=['POST'])
def add_event():
    data = {
        'user_id': session['user_id'],
        'event_name': request.form['event_name'],
        'event_start': request.form['event_start'],
        'event_end': request.form['event_end'],
        'event_date': request.form['event_date'] 
    }
    Event.save(data)
    return redirect('/events')

@app.route('/events/all')
def posted_events():
    return render_template('posted_events.html', events=Event.get_all(), datetime=datetime, user_id=session['user_id'])

@app.route('/events/all/add/<int:event_id>', methods=['POST'])
def save_for_user(event_id):
    if 'user_id' not in session:
        return redirect('/login')
    Event.save_for_user(session['user_id'], event_id)
    return redirect('/events')

@app.route('/events/edit/<int:id>')
def edit_event(id):
    if 'user_id' not in session:
        return redirect('/login')
    data = {'id': id}
    return render_template('edit_event.html', event=Event.get_one(data))

@app.route('/events/edit/process/<int:id>', methods=['POST'])
def edit_event_process(id):
    if 'user_id' not in session:
        return redirect('/login')
    data ={ 
        'id': id,
        'event_name': request.form['event_name'],
        'event_start': request.form['event_start'],
        'event_end': request.form['event_end']  
    }
    
    Event.update(data)
    return redirect('/events')

@app.route('/events/delete/<int:id>')
def delete(id):
    data = {'id': id}
    
    Event.delete(data)
    return redirect('/events')