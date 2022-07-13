from flask import Flask, render_template
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy



#contains the name of the file between __
app = Flask(__name__)
proxied = FlaskBehindProxy(app) 
app.config['SECRET_KEY'] = 'f5f4cb779b6af997f5edab127e951f79'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"



# this is a deorator
# it is saying that in a url when theres just a slash 
# run this function 
@app.route("/")
def hello_world():
  return "<p>Hello Big Big World!</p>"

@app.route("/home")
def home_info():
  my_subtitle = "Home Page"
  my_text = 'This is the home page'
  return render_template('home.html', 
    text=my_text, 
    subtitle=my_subtitle)


@app.route("/about")
def about_info():
  #return "<h2> This is a wonderful program do demo Flask. </h2>"
  return render_template('about.html', subtitle="About This Demo")

@app.route("/second_page")
def second_page():
    return render_template('second_page.html', subtitle='Second Page', text='This is the second page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home_info')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)



if __name__ == "__main__":
  # 0.0.0.0 runs on any ip number
  #this requires you to rerun everychange
  # app.run(host="0.0.0.0")

  # This is so you dont have to rerun 
  # evertime you make changes
  app.run(debug=True, host="0.0.0.0")