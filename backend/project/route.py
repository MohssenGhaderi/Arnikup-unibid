from flask import url_for, redirect, render_template, request, abort ,redirect, session,jsonify
from datetime import timedelta
from flask_login import current_user,login_required,logout_user
from .model import *
from . import app,login_manager,verify_required,iverify_required,mail
from definitions import *
import time
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from sqlalchemy import or_
from flask_mail import Message

class Route():

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def site():
        return render_template('site/login.html')

    @app.route('/login/')
    def account_login():
        if current_user.is_authenticated:
            return redirect('/')

        next = request.args.get('next')

        if next and ( "participate" in next or "instantview" in next):
            return render_template('site/iframes/ilogin.html', next=next)
        return render_template('site/login.html',next=next)

    @app.route('/verify')
    def account_verify():
        if current_user.is_authenticated:
            return redirect('/')
        if not "username" in session:
            return redirect('/login')
        next = request.args.get('next')
        return render_template('site/verify.html',next=next)

    @app.route('/forgotpassword')
    def account_forgot():
        if current_user.is_authenticated:
            return redirect('/')

        next = request.args.get('next')
        return render_template('site/forgot.html',next=next)

    @app.route('/register/')
    def account_register():
        if current_user.is_authenticated:
            return redirect('/')
        next = request.args.get('next')
        if next:
            return render_template('site/register.html',next=next)

        return render_template('site/register.html')

    @app.route("/logout")
    def logout():
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        logout_user()
        return redirect('/')

    # @app.route("/admin/")
    # @login_required
    # def admin():
    #     return redirect('/admin/')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('site/404.html'), 404

    @app.errorhandler(403)
    def page_not_found(e):
        next_url = request.url
        login_url = '%s?next=%s' % (url_for('account_login'), next_url)
        return redirect(login_url)
        # return render_template('site/403.html'), 403

route = Route()
