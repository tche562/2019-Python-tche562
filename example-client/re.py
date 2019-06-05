import cherrypy
import access
import db_setup
import threadcon
import threading
import time

class receiver(object):

    cp_config = {'tools.encode.on': True, 
                  'tools.encode.encoding': 'utf-8',
                  'tools.sessions.on' : 'True',
                } 

    # If they try somewhere we don't know, catch it here and send them to the right place.
    @cherrypy.expose
    def default(self, *args, **kwargs):
        """The default page, given when we don't recognise where the request is for."""
        Page = startHTML + "I don't know where you're trying to go, so have a 404 Error."
        cherrypy.response.status = 404
        return Page


    @cherrypy.expose
    @cherrypy.tools.json_in(force=False)
    def rx_broadcast(self):
        JSON_object = cherrypy.request.json
        print(JSON_object)


    