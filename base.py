from dash import Dash,html, dcc, Input, Output, State, dash_table, no_update
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from index import appFlask,app

# Create the Flask extension 
db = SQLAlchemy()
#create the app

db.init_app(appFlask)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)


with appFlask.app_context():
    db.create_all()


'''@appFlask.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    return render_template("user/list.py", users=users)'''


@app.callback(
    "/users",
    Output("page-content", "children"),
    Input("user-list", "n_clicks"),
)
def user_list():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    return render_template("user/list.py", users=users)

@app.callback(
    "/users/create",
    Output("page-content", "children"),
    Input("user-create", "n_clicks"),
    methods=["GET", "POST"],
)
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

@app.callback(
    "/user/<int:id>",
    Output("page-content", "children"),
    Input("user-detail", "n_clicks"),
)
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.py", user=user)

@app.callback("/user/<int:id>/delete",methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.py", user=user)
