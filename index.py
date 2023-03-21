import dash
from dash import Dash,html, dcc, Input, Output, State, dash_table, no_update
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash.exceptions import PreventUpdate
#from base import db,User
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select





navbar = dmc.Header(
    height=55,
    fixed=True,
    p=0,
    m=0,
    style={'background-image': 'linear-gradient(rgba(255,255,255,0.3), rgba(255,255,255,0.3)), url(/assets/background.png)', 'background-size': 'cover'},
    children=[
	    dmc.Space(h=10),
        dmc.Group([
            dmc.Modal(
                title="Sign In",
                id = "modal-simple-login",
                children=[
                    dmc.Space(h=10),
                    dmc.Group(
                        [
                            html.Div(
                                [
                                    dbc.Label("Name", html_for="example-name"),
                                    dbc.Input(type="name", id="example-name", placeholder="Enter your name"),
                                ],
                                id="name_input", className="mb-3"
                            ),

                            html.Div(
                                [
                                    dbc.Label("Password", html_for="example-password"),
                                    dbc.Input(
                                        type="password",
                                        id="example-password",
                                        placeholder="Enter your password",
                                    ),
                                ],
                                id="password_input",
                                className="mb-3",
                            ),
                            html.Div(
                                [
                                    dmc.Group(
                                        [
                                            dmc.Button("Submit", id="modal-submit-button",size="lg" ,radius="xl"),
                                            dmc.Button("I forgot my password", id="pwd-lost", color="red",size="xs", radius="xl", variant="outline"),
                                        ],
                                        spacing="md"
                                    ),
                                    
                                ],
                            )
                        ],
                        position="center"
                    )

                ]
            ),
            dmc.Modal(
                title="Sign Up",
                id="modal-simple-signup",
                children=[
                    dmc.Space(h=10),
                    dmc.Group(
                        [
                            html.Div(
                                [
                                    dbc.Label("Username"),
                                    dbc.Input(type="text", id="username_signup", placeholder="Enter your username", name="username_signup")
                                ],
                                id="username-signup-input",
                                className="mb-3"
                            ),
                            html.Div(
                                [
                                    dbc.Label("Email"),
                                    dbc.Input(type="email", id="email_signup", placeholder="Enter your email address", name="email_signup")
                                ],
                                id="email-signup-input",
                                className="mb-3"
                            ),
                            html.Div(
                                [
                                    dbc.Label("Password"),
                                    dbc.Input(
                                        type="password",
                                        id="first_password_signup",
                                        placeholder="Create your password",
                                    ),
                                    dmc.Space(h=10),
                                    dbc.Input(
                                        type="password",
                                        id="second_password_signup",
                                        placeholder="Validate your password",
                                    )
                                ],
                                id="password-signup-input",
                                className="mb-3",
                            ),
                            html.Div(
                                [
                                    dmc.Group(
                                        [
                                            dmc.Button("Sign Up", id="modal-signup-button", radius="xl"),
                                        ],
                                        spacing="md"
                                    ),
                                    
                                ],
                            )
                        ],
                        position="center"
                    )
                ]
            ),
        dmc.Group(
                [
                    dmc.Button("Log In", id="login",size="md", radius="xl"),
                    dmc.Button("Sign Up", id="sign-up", size="md", radius="xl", color="green")
                ],
                position="right",
                spacing="md"
            ),
        html.Div(
            id="signup-page"
        ),
        html.Div(
            id="login-page"
        ),
        dmc.NotificationsProvider([
                # children
            ])  
    ])
])

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

# Create the Flask extension 
db = SQLAlchemy()
#create the app

db.init_app(appFlask)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

with appFlask.app_context():
    db.create_all()

# To open & close the login modal
@app.callback(
    Output("modal-simple-login", "opened"),
    Input("login", "n_clicks"),
    Input("modal-submit-button", "n_clicks"),
    Input("pwd-lost", "n_clicks"),
    State("modal-simple-login", "opened"),
    prevent_initial_call=True,
)
def modal_demo_login(nc1, nc2, nc3, is_open):
    return not is_open

#To open the login interface
@app.callback(
    Output("login-page","children"),
    Input("example-name","value"),
    Input("example-password","value"),
    Input("modal-submit-button","n_clicks"),
    #State("modal-simple-login", "opened"),
    prevent_initial_call=True,

)
def sign_me_in(name, pwd, nc):
    if name is not None and pwd is not None:
        user = User.query.filter_by(name=name).first()
        if user is not None and user.password == pwd:
            return html.Div("Welcome {}".format(name))
        else:
            return html.Div("Wrong username or password")
    else:
        return html.Div("Please enter your username and password")

# To open & close the signup modal
@app.callback(
    Output("modal-simple-signup", "opened"),
    Input("sign-up", "n_clicks"),
    Input("modal-signup-button","n_clicks"),
    State("modal-simple-signup", "opened"),
    prevent_initial_call=True,
)
def modal_demo_signup(nc1, nc2, is_open):
    return not is_open


# To open the signup interface
@app.callback(
    Output("signup-page","children"),
    Input("username_signup","value"),
    Input("email_signup","value"),
    Input("first_password_signup","value"),
    Input("second_password_signup","value"),
    Input("modal-signup-button","n_clicks"),
    #State("modal-simple-signup", "opened"),
    prevent_initial_call=True,

)
def sign_me_up(name, email, pwd1, pwd2, n_clicks ):
   # if email = text.with(""):
    #    return 
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(dash.callback_context.triggered)
    print(changed_id)
    if changed_id != 'modal-signup-button.n_clicks':
        raise PreventUpdate

    # To check if the password is correct
    if pwd1 != pwd2:
        
        return dmc.Notification(
            title="Error",
            id="bad-signup-notify",
            action="show",
            message="Your first password does not match the second. Please try again",
            icon=[DashIconify(icon="feather:info", color="red", width=30)],
        )
    else:
        # enregistre dans la base
        #if request.method == "POST":
        user = User(
            name=name,
            email=email,
            password=pwd1
        )
        namecheck = db.session.execute(
            select(User).where(User.name == name)
        )
        emailcheck = db.session.execute(
            select(User).where(User.email == email)
        )
        print(list(namecheck))
        if list(namecheck) !=[] or list(emailcheck) !=[]:
            return dmc.Notification(
                title="Error",
                id="bad-signup-notify",
                action="show",
                message="This email or name already exists",
                icon=[DashIconify(icon="feather:info", color="red", width=30)],
            )



        db.session.add(user)
        db.session.commit()
        print(user)

        return dmc.Notification(
            title="Welcome",
            id="good-signup-notify",
            action="show",
            message="You have been successfully registered",
            icon=[DashIconify(icon="ic:round-celebration")],
        )
    

'''
db.session.get(name)'''


# Callback in the future (with sqlAlchemy)

#


# # To signup a new user
# @app.callback(
#     Output(""),
#     Input("modal-signup-button", "n_clicks"),
#     State("email_signup", "value"),
#     State("first_password_signup", "value")
# )
# def signup_user(nc, email, password):
#     return 

# To check if the email is already in the database
  # @loginRequired


if __name__ == "__main__":
    app.run_server(debug=True)



#if __name__ == '__main__':
 #   app.run_server(debug=True)