import dash
from dash import Dash,html, dcc, Input, Output, State, dash_table, no_update
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify



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
                                    dbc.Label("Email", html_for="example-email"),
                                    dbc.Input(type="email", id="example-email", placeholder="Enter your email"),
                                ],
                                id="email_input", className="mb-3"
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
                                    dbc.Input(type="text", id="username_signup", placeholder="Enter your username")
                                ],
                                id="username-signup-input",
                                className="mb-3"
                            ),
                            html.Div(
                                [
                                    dbc.Label("Email"),
                                    dbc.Input(type="email", id="email_signup", placeholder="Enter your email address")
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
            )
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


'''# To open the signup interface
@app.callback(
    Output("signup-page","children"),
    Input("email_signup","value"),
    Input("first_password_signup","value"),
    Input("second_password_signup","value"),
    Input("modal-signup-button","n_clicks"),
    prevent_initial_call=True,

)
def sign_me_up(email, pwd1, pwd2, n_clicks):
   # if email = text.with(""):
    #    return 

    # To check if the password is correct
    if pwd1 != pwd2:
        return dmc.Notification(
            title="Error",
            id="bad-signup-notify",
            action="show",
            message="Your first password does not match the second. Please try again",
            icon=DashIconify(icon="feather:info", color="red", width=30),
        )
    else:
        # enregistre dans la base


        return dmc.Notification(
            title="Welcome",
            id="good-signup-notify",
            action="show",
            message="You have been successfully registered",
            icon=DashIconify(icon="ic:round-celebration"),

        )
'''

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