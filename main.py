from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:Blogz@localhost:8889/Blogz'
#database conection string = 'mysqul+pymysql://user:password@location:port_number/db_name'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(139))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner
        
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True) 
    password = db.Column(db.String(12))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password



@app.route('/signup', methods = ['POST','GET'])
def signup():

    if request.method =='POST':
        username = request.form['new-user']
        #user_name_error = ''
        password = request.form['password']
        #password_error = ''
        confirm_password = request.form['confirm-password']
        #passmatch_error = ''
        email = request.form['email']
        #email_error = ''
        existing_user = User.query.filter_by(username=username).first()
        #print(existing_user)
        valid_new_user = User(username, password)
    
        if username == '':
            flash('please enter a user name')
            return render_template('signup.html',title="dont be shy",username =username, email=email)
        elif len(password) <= 3:
            flash('password is to short')
            return render_template('signup.html',title='wipe away your tears',username =username, email=email)
        elif password != confirm_password:
            flash('passwords do not match')
            return render_template('signup.html',title='wipe away your tears',username =username, email=email)
        #elif email == '':
            #return '<h1> Welcome, '+new_user+'</h1>'
        elif '@' not in email or '.' not in email or len(email) < 5 or len(email) > 20 or ' ' in email:    
            flash('Please enter a valid email') #a single @, a single ., contains no spaces, and is between 3 and 20 characters
            return render_template('signup.html',title='wipe away your tears',username =username, email=email)
        elif existing_user:
            flash('Pick a unique user name')
            return render_template('signup.html',title='you be you baby', email=email)
        else:
            db.session.add(valid_new_user)
            db.session.commit()
            return render_template('newpost.html',title='youre never alone... ever')

    return render_template('signup.html',title='wipe away your tears')

@app.route('/login', methods=['POST', 'GET'])
def login():
    #todo-add function to create users session containing email

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    entry_title = Blog.query.all()
    return render_template('login.html')

@app.route('/logout', methods = ['POST'])
def logout():
    #todo- delete username from session
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST':
        task_name = request.form['new_post']
        new_task = Blog(task_name)
        db.session.add(new_task)
        db.session.commit()

    entry_title = Blog.query.all()
    #entry = Blog.query.all()
    return render_template('display.html',title="Why am I always crying!", 
        entry_titles = entry_title)


@app.route('/newpost', methods=['POST','GET'])
def add_post():
    #todo-make sure post is bound to the user.id
    #owner = User.query.filter_by(['email']).first()

    if request.method == 'POST':    
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = Blog(post_title, post_content)

        if post_title == '':
            flash('Please title your troubles')
            return render_template('post.html',title='wipe away your tears', post_content=post_content, post_title=post_title)
        elif post_content == '':
            flash('Its ok tell me whats on your mind')
            return render_template('post.html',title='wipe away your tears', post_content=post_content, post_title=post_title)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
        #return render_template('display.html',title="Why am I always crying!", 
        #post_title = entry_title)
    #task_id = int(request.form['task-id'])
    #task = Task.query.get(task_id)
    #task.completed = True
    #db.session.add(task)
    #db.session.commit()

    return render_template('newpost.html',title='wipe away your tears')

@app.route('/view_post', methods=['POST','GET'])
def view_post():


    #entry_title = Blog.query.all()
    key = request.args.get('id')
    post_title = Blog.query.get(key).title
    body = Blog.query.get(key).body
        
    return render_template('view_post.html',title='wipe away your tears', post_title = post_title, body = body)
        
    #task_id = int(request.form['task-id'])
    #task = Task.query.get(task_id)
    #task.completed = True
    #db.session.add(task)
    #db.session.commit()



if __name__ == '__main__':
    app.run()


#python
#from main import db,Task
#db #will show the SQLAlchemy engine=
#db.create_all() #scans the classes and creates the associated tables in
                    #the database
#new_task = Task('finish ORM lesson 2')
#db.session.add(new_task)
#another_task = Task('post lesson video')
#db.session.add(another_task)
#db.session.commit() #sessions will not be added until you commit()
#Task.query.all() #select all query objects from the database
#tasks = Task.query.all()
#tasks #show objects hex number
#tasks[0].name #will display 'finish ORM lesson 2' 

#NEW COLMN WHEN CLASS CHANGES
#python
#from main import db,Task
#db.drop_all() #will destory all tables in database
#db.create_all() #will create new structure with new classes
                    #you would not want to do this if you wanted to
                    #keep all the data #flask-migrate docs can show you how to use this 

#FOR USER CLASS
#python
#import db,User
#db.create_all() #create the table structure in the database
#new_user = User('chris@launchcode.org', 'cheese')
#db.session.add(new_user)
#db.session.commit()