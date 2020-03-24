from flask import Flask,request,redirect
from flask import render_template
from datetime import datetime
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
app.config['SECRET_KEY']='thisismysecretkey'
app.config['SQLALCHEMY_BINDS']={
    'login':'sqlite:///login.db',
}
db=SQLAlchemy(app)
class User(UserMixin,db.Model):
    __bind_key__='login'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def get(id):
    return User.query.get(id)
class BlogPost(db.Model):
    num=db.Column(db.Integer,primary_key=True)
    blog=db.Column(db.Text,nullable=False)
    author=db.Column(db.Text,nullable=False)
    published=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    def __repr__(self):
        return "NUM : "+str(self.num)

@app.route('/',methods=['GET'])
def home():
    post=BlogPost.query.all()
    return render_template('home.html',Post=post)
@app.route('/delete/<int:num>')
@login_required
def delete(num):
    post_delete=BlogPost.query.get_or_404(num)
    db.session.delete(post_delete)
    db.session.commit()
    return redirect('/admin')
@app.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    edit=BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        edit.blog=request.form['post']
        edit.author=request.form['author']
        db.session.commit()
        return redirect('/admin')
    else:
        return render_template('edit.html',Edit=edit)
@app.route('/admin',methods=['GET','POST'])
@login_required
def admin():
    if request.method == 'POST':
        post_blog=request.form['post']
        post_author=request.form['author']
        db.session.add(BlogPost(blog=post_blog,author=post_author))
        db.session.commit()
        return redirect('/admin')
    else:
        post=BlogPost.query.all()
        return render_template('admin.html',Post=post)
@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html')
@app.route('/login',methods=['POST'])
def login_post():
    username=request.form['username']
    password=request.form['password']
    user=User.query.filter_by(username=username).first()
    login_user(user)
    return redirect('/admin')
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
if __name__ == "__main__":
    app.run(debug=True)