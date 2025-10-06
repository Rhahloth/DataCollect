import os
from flask import Flask, session, redirect, url_for, request, render_template, flash
from config import DevelopmentConfig
from db import db, migrate
from werkzeug.security import generate_password_hash, check_password_hash

from routes import main, forms

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)  
    app.config.from_object(config_class)
    app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")  # required for sessions

    # Load login credentials from env
    APP_USERNAME = os.getenv("APP_USERNAME", "Jonathan")
    APP_PASSWORD = os.getenv("APP_PASSWORD", "Jonathan@123")
    PASSWORD_HASH = generate_password_hash(APP_PASSWORD)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from models import create_tables
        create_tables()

    # Register blueprints
    
    app.register_blueprint(main.bp)
    app.register_blueprint(forms.bp)

    #Add simple login routes
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if username == APP_USERNAME and check_password_hash(PASSWORD_HASH, password):
                session["logged_in"] = True
                return redirect(url_for("main.dashboard"))
            else:
                flash("Invalid credentials", "danger")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    #Protect all other routes
    @app.before_request
    def require_login():
        if request.endpoint not in ("login", "static") and not session.get("logged_in"):
            return redirect(url_for("login"))

    return app
