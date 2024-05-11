from flask import Flask, render_template, request, redirect, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['expiration_time'] = datetime.now() + timedelta(minutes=0)
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.String(200))
    end_time = db.Column(db.String(200))

    def __repr__(self):
        return f"{self.sno} - {self.title}"
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        date_str = request.form['dt'] 
        date= datetime.strptime(date_str, '%Y-%m-%d')
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        todo = Todo(title=title, desc=desc, date=date, start_time=start_time, end_time=end_time)
        db.session.add(todo)
        db.session.commit()
        

    allTodo = Todo.query.all()
    name = "Chiranjit"

    return render_template('index.html', allTodo=allTodo, name=name)

@app.route('/page1')
def page1():
    return render_template('webApp.html')

@app.route('/delete/<int:sno>', methods=['GET', 'POST'])
def delete(sno):
    try:
        todo = Todo.query.filter_by(sno=sno).first()
        if todo:
            db.session.delete(todo)
            db.session.commit()
            return redirect('/')
        else:
            return "Todo item not found."
    except Exception as e:
        return str(e)

@app.route('/remaining_time')
def remaining_time():
    remaining_time_seconds = get_remaining_time()
    return jsonify({'remaining_time_in_sec': remaining_time_seconds})

@app.route('/reset',methods=['GET','POST'])
def reset():
    global expiration_time
    minutes = request.form.get('minutes')
    app.config['expiration_time'] = datetime.now() + timedelta(minutes=int(minutes))
    allTodo = Todo.query.all()
    name = "Chiranjit"
    return render_template('index.html',allTodo=allTodo, name=name)

@app.route('/stop', methods=['GET', 'POST'])
def stop():
    global expiration_time
    app.config['expiration_time'] = datetime.now()  # Stop the timer
    allTodo = Todo.query.all()
    name = "Chiranjit"
    return render_template('index.html',allTodo=allTodo, name=name)
@app.route('/about')
def about():
    return render_template('about.html')


def get_remaining_time():
    expiration_time = app.config['expiration_time']
    remaining_time = expiration_time - datetime.now()
    return remaining_time.total_seconds()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
