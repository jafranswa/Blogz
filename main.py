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
        self.owner = owner

        
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True) 
    password = db.Column(db.String(12))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'home']
    if request.endpoint not in allowed_routes and'user' not in session:
        return redirect('/login')



@app.route('/signup', methods = ['POST','GET'])
def signup():

    if request.method =='POST':
        username = request.form['new-user']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        email = request.form['email']
        existing_user = User.query.filter_by(username=username).first()
        valid_new_user = User(username, password)
#todo- *optional* figure out something with a continue type statement
        if username == '':
            flash('please enter a user name')
            return render_template('signup.html',title="dont be shy",username =username, email=email)
        elif existing_user:
            flash('Im afraid that user name has been claimed')
            return render_template('signup.html', title='highlight your rarity', email=email)
        elif len(password) <= 3:
            flash('password is to short')
            return render_template('signup.html',title='wipe away your tears',username =username, email=email)
        elif password != confirm_password:
            flash('passwords do not match')
            return render_template('signup.html',title='wipe away your tears',username =username, email=email)
        elif '@' not in email or '.' not in email or len(email) < 5 or len(email) > 20 or ' ' in email:    
            flash('Please enter a valid email') 
            return render_template('signup.html',title='wipe away your tears',username =username, email=email)
        else:
            db.session.add(valid_new_user)
            db.session.commit()
            session['user'] = username
            print(session)
            return render_template('newpost.html',title='youre never alone... ever')

    return render_template('signup.html',title='wipe away your tears')

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        user_login = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=user_login).first()

        if user_login == '':
            flash('Please enter a user name')
            return render_template('login.html', username=user_login)
        #elif password == '' or len(password) < 3:
            #flash('Please enter a valid password')
            #return render_template('login.html', username=username)
        elif user_login and existing_user.password != password:
            flash('Password is incorrect, pull it together')
            return render_template('login.html', username=user_login)
        elif not existing_user:
            flash('username does not exist. please signup with the link above')
        elif user_login and existing_user.password == password:
            session['user'] = user_login
            print('test session', session)
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('all validation checks failed back to the drawing board')
            return render_template('login.html', username=user_login)

    return render_template('login.html')

@app.route('/logout', methods = ['GET'])
def logout():
    del session['user']
    flash('Logged out')
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():
    
    #if request.method == 'POST':
        #task_name = request.form['new_post']
        #new_task = Blog(task_name)
        #db.session.add(new_task)
        #db.session.commit()

    user_table = User.query.all() #pulls user table contents
    user_name_list= []            #list of user names in order of db
    for user in user_table:
        user_name_list.append(user.username)  #appends usernames from user_table

    blog_table = Blog.query.all() #pulls blog table contents
    blog_id_list = []             #list of id=primeKey in order of db

    for user in blog_table:
        blog_id_list.append(user.owner)  #appends id from blog_table
    #flash(blog_id_list)
    #for index in blog_id_list:
     #   author
    entry_title = Blog.query.all()
    return render_template('display.html',title="Why am I always crying!", 
        entry_titles = entry_title, user_name_list = user_name_list, blog_id_list = blog_id_list)


@app.route('/newpost', methods=['POST','GET'])
def add_post():

    if request.method == 'POST':    
        post_title = request.form['title']
        post_content = request.form['content']
        owner = User.query.filter_by(username=session['user']).first()
        new_post = Blog(post_title, post_content, owner)

        if post_title == '':
            flash('Please title your troubles')
            return render_template('post.html',title='wipe away your tears', post_content=post_content, post_title=post_title)
        elif post_content == '':
            flash('Its ok tell me whats on your mind')
            return render_template('post.html',title='wipe away your tears', post_content=post_content, post_title=post_title)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

    return render_template('newpost.html',title='wipe away your tears')

@app.route('/view_post', methods=['POST','GET'])
def view_post():

    key = request.args.get('id')
    #blog_table = Blog.query.all()
    blog_table = Blog.query.filter_by(id = key).first()
    post_title = Blog.query.get(key).title
    body = Blog.query.get(key).body
        
    return render_template('view_post.html',title='wipe away your tears', post_title = post_title, body = body, blog_table = blog_table)

@app.route('/home')
def home():

    user_table = User.query.all()
    #user_name_list= []

    #for user in user_table:
        #user_name_list.append(user.username)
    return render_template('index.html', title='Sad doesnt mean lonley', user_table = user_table)

@app.route('/blog')
def blog():

    key = request.args.get('id')
    posts = Blog.query.filter_by(owner_id = key).all()
    user = User.query.filter_by(id = key).first()
    # posts = Blog.query.get(key)
    #post_title = Blog.query.get(key).title
    #body = Blog.query.get(key).body
    
    return render_template('singleUser.html',title='wipe away your tears', posts=posts, user=user)

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