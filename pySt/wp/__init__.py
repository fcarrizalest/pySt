from functools import wraps
from flask import render_template
from .. import factory


def create_app(settings_override=None):
	"""Returns the  dashboard application instance"""
	app = factory.create_app(__name__, __path__, settings_override)

	# Init assets
	#assets.init_app(app)

	# Register custom error handlers
	if not app.debug:
		for e in [500, 404]:
			app.errorhandler(e)(handle_error)

	return app

def handle_error(e):
	return render_template('../front/errors/%s.html' % e.code), e.code


def route(bp, *args, **kwargs):
	def decorator(f):
		@bp.route(*args, **kwargs)
		@wraps(f)
		def wrapper(*args, **kwargs):
			return f(*args, **kwargs)
		return f

	return decorator