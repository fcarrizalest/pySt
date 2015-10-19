from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware


from pySt import front,users,groups,wp,cv


application = DispatcherMiddleware(cv.create_app(),{ '/admin':front.create_app(), '/users': users.create_app() , '/groups': groups.create_app() , '/wp':wp.create_app()})
	
	
if __name__ == "__main__":
	run_simple('0.0.0.0', 5000, application, use_reloader=True, use_debugger=True)