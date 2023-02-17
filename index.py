import dash
from dash import Dash,html, dcc, Input, Output, State, dash_table, no_update
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from base import app

#app = Dash(__name__)




navbar = dmc.Group([
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
])



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

# Callback in the future (with sqlAlchemy)

# To signup a new user

# To check if the email is already in the database

# To check if the password is correct




#if __name__ == '__main__':
 #   app.run_server(debug=True)