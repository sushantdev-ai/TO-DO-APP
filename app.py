from flask import Flask,request,redirect
from flask import render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
db=SQLAlchemy(app)
class TODO(db.Model):
    num=db.Column(db.Integer,primary_key=True)
    todo=db.Column(db.Text,nullable=False)
    start=db.Column(db.Text,nullable=False,default=str(datetime.utcnow))
    end=db.Column(db.Text,nullable=False,default=str(datetime.utcnow))
    def __repr__(self):
        return "NUM : "+str(self.num)

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        post_todo=request.form['todo']
        post_start=request.form['start']
        post_end=request.form['end']
        db.session.add(TODO(todo=post_todo,start=post_start,end=post_end))
        db.session.commit()
        return redirect('/')
    else:
        todo1=TODO.query.all()
        return render_template('home.html',Todo=todo1)
@app.route('/delete/<int:num>')
def delete(num):
    post_delete=TODO.query.get_or_404(num)
    db.session.delete(post_delete)
    db.session.commit()
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)