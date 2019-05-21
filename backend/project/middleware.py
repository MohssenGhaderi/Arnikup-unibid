from flask_login import current_user,login_required
from functools import wraps
from flask import render_template,abort
# from model.user import User

def role_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return render_template('site/login.html')
        found = False
        user = User.query.get(current_user.id)
        if(not has_role(user,"admin")):
            abort(400)
        # for role in current_user.roles:
        #     if( role.name == 'admin' ):
        #         found = True
        #         break
        # if not found :
        #     abort(400)
            # return render_template('site/401.html'), 401
        return f(*args, **kwargs)
    return decorated_function

def has_role(user,name):
    found = True
    for role in user.roles:
        if( role.name == name ):
            found = True
            break
    return found
