# -*- coding: utf-8 -*-
#
# @see      Flask WebServer Example
# @author   ben
#
# pyright: reportMissingImports=false
import flask

def route(regex, **kwds):
    def decorator(func):
        func.web_route = regex
        func.web_args = kwds
        return func
    return decorator

def errorhandler(regex, **kwds):
    def decorator(func):
        func.web_errorhandler = regex
        func.web_args = kwds
        return func
    return decorator

# Generic class, import flask and add decorators over it (see flaskApp class)
class webserver(object):
    def __init__(self, import_name, static_url_path=None, static_folder="static", static_host=None,
                       host_matching=False, subdomain_matching=False, template_folder="templates",
                       instance_path=None, instance_relative_config=False, root_path=None):
        self.app = flask.Flask(import_name=import_name,         static_url_path=static_url_path,
                               static_folder=static_folder,     static_host=static_host,
                               host_matching=host_matching,     subdomain_matching=subdomain_matching,
                               template_folder=template_folder, instance_path=instance_path,
                               instance_relative_config=instance_relative_config, root_path=root_path)
        for name in dir(self):
            method = self.__getattribute__(name)
            try:    # Applying route, if any
                route = method.web_route
                args = method.web_args
                self.app.route(route, **args)(method)
            except AttributeError:
                pass
            try:    # Applying errorhandler, if any
                errorhandler = method.web_errorhandler
                args = method.web_args
                self.app.errorhandler(errorhandler, **args)(method)
            except AttributeError:
                pass
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        self.app.run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)     # Run this webservice

class flaskApp(webserver):
    def __init__(self):
        super().__init__(import_name=__name__)
    def run(self, host='localhost', port=8888):
        super().run(host=host, port=port)

    # Just add other hooks here with leading decorator as shown
    #       @route('/api/<myVar>/abc')    def method(self,myVar)
    @route('/<path:path>')
    def index(self, path):
        message = f'Request : {flask.request.method} {flask.request.url}\nPath    : {path}\nParams  : {flask.request.args}\n'
        # page = request.args.get('page', default = 1, type = int)      # Sample querystring params with defaults and type, if needed
        return message      # To client


if __name__ == '__main__':
    myApplication = flaskApp()
    myApplication.run(host='localhost', port=8888)
