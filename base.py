from dash import Dash,html, dcc
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from index import navbar

# Create the Flask extension 
db = SQLAlchemy()
#create the app

app = Dash(__name__)

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content'),
    html.Div(children=False, id='is-mobile', hidden=True),
])

appFlask = app.server

#configure the SQLite database relative to the app instance folder
appFlask.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/stagiaire/Documents/Python/quentinvm/project.db'
#initialize the app with the extension
db.init_app(appFlask)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)


with appFlask.app_context():
    db.create_all()


@appFlask.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    return render_template("user/list.py", users=users)

@appFlask.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            name=request.form["name"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.py")

@appFlask.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.py", user=user)

@appFlask.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.py", user=user)


if __name__ == "__main__":
    app.run(debug=True)