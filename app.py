from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
app.app_context().push()

class Employee(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    phone_no = db.Column(db.String(13),nullable = False)
    address = db.Column(db.String(), nullable = False)

    def __repr__(self):
        return f"{self.sno} - {self.name} "
    
with app.app_context():
    db.create_all()


@app.route("/",methods = ["GET","POST"])
def hello_world():
    if request.method == "POST":
       name = request.form["name"]
       email = request.form["email"]
       phone = request.form["phone"]
       address = request.form["address"]
       employee = Employee( name = name, address = address,phone_no = phone, email = email,)
       db.session.add(employee)
       db.session.commit()
    all_employee = Employee.query.all()
    return render_template("index.html",all_employee = all_employee)

@app.route("/about")
def about_page():
    return "<h3>Hello About page<h3>"

@app.route("/delete/<int:sno>")
def delete(sno):
    employee=Employee.query.filter_by(sno=sno).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)