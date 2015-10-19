from flask import session,flash,url_for,redirect,request,Blueprint, render_template
from ..core import db
from . import route
from .models import Category

bp = Blueprint('dashboard', __name__)

@route(bp, '/',methods=('GET','POST'))
def index():
	cats = Category.query.all()
	return render_template('main.html', cats= cats )