import cherrypy
import access
import db_setup
import threadcon
import threading
import time
import verify
import communication
import sqlite3

startHTML = ("<!DOCTYPE HTML><html><head><title>CS302</title><!-- Custom Theme files -->"
                +"<link href='/static/style.css' rel='stylesheet' type='text/css' media='all'/>"
                +"<!-- Custom Theme files -->"
                +"<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />"
                +"<meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1'>"
                +"<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />"
                +"<meta name='keywords' content='Login form web template, Sign up Web Templates, Flat Web Templates, Login signup Responsive web template, Smartphone Compatible web template, free webdesigns for Nokia, Samsung, LG, SonyErricsson, Motorola web design' />"
                +"<!--Google Fonts-->"
                +"<link href='http://fonts.useso.com/css?family=Roboto:500,900italic,900,400italic,100,700italic,300,700,500italic,100italic,300italic,400' rel='stylesheet' type='text/css'>"
                +"<link href='http://fonts.useso.com/css?family=Droid+Serif:400,700,400italic,700italic' rel='stylesheet' type='text/css'>"
                +"<!--Google Fonts-->"
                +"</head>"
                +"<body>")

class MainApp(object):

    def __init__(self):
        self.dthread = threadcon.Downthread()
        self.current_username = ''

	#CherryPy Configuration
    _cp_config = {'tools.encode.on': True, 
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


    # PAGES (which return HTML that can be viewed in browser)    
    @cherrypy.expose
    def index(self):
        Page = startHTML
        
        try:
            username = cherrypy.session['username']
            Page += "<div class='status'><h3>Choose your status here : &nbsp;<a href='Online'>Online</a>" 
            Page += "&nbsp;<a href='Busy'>Busy</a> &nbsp;<a href='Away'>Away</a> </h3></div>"
            Page += "<div class='login'><h2>Compsys 302</h2>"
            Page += "<div class='login-top'><p>Hello " + username + "!<br/>Welcome To Home Page</br>"
            Page += "<a href='/signout'>Sign out</a></body></html></p></div>"
            Page += "<div class='login-bottom'><h3><a href='privatemessage'>Privatemessage</a> &nbsp;"
            Page += "&nbsp; <a href='broadcast'>Broadcast</a></h3></div></div></body></html>"

        except KeyError: #There is no username
            
            
            Page += "<div class='login'><h2>Compsys 302</h2>"
            Page += "<div class='login-top'><p>Click here to <a href='login'>login</a></p></div>"
            Page += "<div class='login-bottom'></div></div></body></html>"

        return Page

    @cherrypy.expose
    def privatemessage(self,user = None,message = None):
        Page = startHTML
        access.list_user(self.current_username)
        username,pubkey,address,status = db_setup.get_chatmate_info()
        Page += "<div class='status'><h3> &nbsp;<a href='index'>Home</a>" 
        Page += "&nbsp;<a href='message_send'>Refresh</a> &nbsp;<a href='broadcast'>Broadcast</a> </h3></div>"
        Page += "<div class='frame'>"
        Page += "<h2> Message </h2><div class='list'><p>"
        for index in range(len(username)):
            p_username = username[index]
            p_pubkey = pubkey[index]
            p_address = address[index]
            p_status = status[index]
            Page += "<a href='/privatemessage?user="+ p_username +"'>" + p_username + "</a> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;" + p_status + " </br>"
        Page += "</p></div>"

        if user != None :
            sender,ts,content,receiver,_ = db_setup.get_chat_record()
            Page += "<div class='chatwindow'>"
            for index in range(len(ts)):
                p_sender = sender[index]
                p_ts = ts[index]
                p_content = content[index]
                p_receiver = receiver[index]
                p_datetime = communication.trans_time(p_ts)
                if p_sender == self.current_username and p_receiver == user:
                    Page += "<div class = 'time'><p>"+p_datetime+"</p></div>"
                    Page += "<div class = 'girl'><p>"+p_content+"</p></div>"
                elif p_sender == user and p_receiver == self.current_username:
                    Page += "<div class = 'time'><p>"+p_datetime+"</p></div>"
                    Page += "<div class = 'boy'><p>"+p_content+"</p></div>"
            Page += "</div><form action='/privatemessage?user="+ user +"' method='post' enctype='multipart/form-data'>"
            Page += "<div class='chatwindow_bottom'>"
            Page +="<textarea name = 'message' cols = '60' row = '5' ></textarea></div><input type='submit' value='send' ></form></div>"
            if message != None :
                communication.privatemessage(self.current_username,user,message)
                raise cherrypy.HTTPRedirect("/message_send?user="+ user)

        return Page


    @cherrypy.expose
    def message_send(self,user=None):
        if user != None:
            raise cherrypy.HTTPRedirect("/privatemessage?user="+ user)
        else:
            raise cherrypy.HTTPRedirect("/privatemessage")


    @cherrypy.expose
    def broadcast(self,message=None):
        Page = startHTML
        access.list_user(self.current_username)
        Page += "<div class='status'><h3> &nbsp;<a href='index'>Home</a>" 
        Page += "&nbsp;<a href='broadcast_send'>Refresh</a> &nbsp;<a href='privatemessage'>Privatemessage</a> </h3></div>"
        Page += "<div class='frame'>"
        Page += "<h2> Broadcast </h2><div class='Board'>"
        broadcaster,ts,content = db_setup.get_broadcast_record()
        for index in range(len(ts)):
            p_broadcaster = broadcaster[index]
            p_ts = ts[index]
            p_content = content[index]
            p_datetime = communication.trans_time(p_ts)
            Page += "<div class = 'time'><p>"+p_datetime+"</p></div>"
            Page += "<div class = 'cube'><h1>"+p_broadcaster+":</h1></br><p>"+p_content+"</p></div>"
        Page += "</div><form action='/broadcast' method='post' enctype='multipart/form-data'>"
        Page += "<div class='chatwindow_bottom'>"
        Page +="<textarea name = 'message' cols = '60' row = '5' ></textarea></div><input type='submit' value='send' ></form></div>"
        if message != None:
            communication.broadcast(self.current_username,message)
            raise cherrypy.HTTPRedirect("/broadcast_send")

        return Page

    @cherrypy.expose
    def broadcast_send(self):
        raise cherrypy.HTTPRedirect("/broadcast")





    
    @cherrypy.expose
    def Busy(self):

        Page = startHTML
        status = "busy"
        username = cherrypy.session['username']
        self.dthread.threadset(username,status)

        Page += "<div class='login'><h2>Compsys 302</h2>"
        Page += "<div class='login-top'><p>You are Busy now <br/>"
        Page += "Click here back to <a href='index'>Home</a></p></div>"
        Page += "<div class='login-bottom'></div></div></body></html>"
        return Page

    @cherrypy.expose
    def Away(self):

        Page = startHTML
        status = "away"
        username = cherrypy.session['username']
        self.dthread.threadset(username,status)

        Page += "<div class='login'><h2>Compsys 302</h2>"
        Page += "<div class='login-top'><p>You are Away now <br/>"
        Page += "Click here back to <a href='index'>Home</a></p></div>"
        Page += "<div class='login-bottom'></div></div></body></html>"
        return Page

    @cherrypy.expose
    def Online(self):

        Page = startHTML
        status = "online"
        username = cherrypy.session['username']
        self.dthread.threadset(username,status)

        Page += "<div class='login'><h2>Compsys 302</h2>"
        Page += "<div class='login-top'><p>You are Online now <br/>"
        Page += "Click here back to <a href='index'>Home</a></p></div>"
        Page += "<div class='login-bottom'></div></div></body></html>"
        return Page


    @cherrypy.expose
    def login(self, bad_attempt = 0):
        Page = startHTML 
        if bad_attempt != 0:
            Page += "<font color='red'>Invalid username/password!</font>"
            
        Page += '<form action="/signin" method="post" enctype="multipart/form-data">'
        
        Page += '<div class="login"><h2>Compsys 302</h2>'
        Page += '<div class="login-top"><h1>LOGIN</h1>'
        Page += "<form><input type='text' name='username'><input type='text' name ='password' ></form>"
        Page += '<div class="forgot"><a href="#">forgot Password</a><input type="submit" value="Login" ></div></div>'
        Page += '<div class="login-bottom">'
        Page += '</div></div><div class="copyright"><p>Copyright &copy; 2015.Tianhang chen All rights reserved.</p></div></body></html>'
        return Page
    
    @cherrypy.expose    
    def sum(self, a=0, b=0): #All inputs are strings by default
        output = int(a)+int(b)
        return str(output)
        
    # LOGGING IN AND OUT
    @cherrypy.expose
    def signin(self, username=None, password=None):
        """Check their name and password and send them either to the main page, or back to the main login screen."""
        autherisedping = access.ping(username, password)
        if autherisedping['authentication'] == "basic":
            cherrypy.session['username'] = username
            db_setup.delete_db("user_info")
            db_setup.generate_k(username,password)
            access.addpubkey(username)
            access.keytest(username)
            self.current_username = username
            raise cherrypy.HTTPRedirect('/')
        else:
            raise cherrypy.HTTPRedirect('/login?bad_attempt=1')

    @cherrypy.expose
    def signout(self):
        """Logs the current user out, expires their session"""
        username = cherrypy.session.get('username')
        if username is None:
            pass
        else:
            cherrypy.lib.sessions.expire()
            self.dthread.terminate()
            offline_user = self.current_username
            status = "offline"
            access.report(offline_user,status)
            fl_ts = time.time()
            db_setup.update_outtime(offline_user,fl_ts)
            print("you are offline----------------------")
        raise cherrypy.HTTPRedirect('/')
    
    def get_username(self):
        username = self.current_username
        print(username)
        return username




###
### Functions only after here
###

def authoriseUserLogin(username, password):
    print("Log on attempt from {0}:{1}".format(username, password))
    if (username.lower() == "tche562") and (password.lower() == "hdlmap456"):
        print("Success")
        return 0
    else:
        print("Failure")
        return 1















class receiver(object):

    def __init__(self,MainApp):
        self.new_mainapp = MainApp    

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
        try: 
            verify.veri_broadcast(JSON_object)
            log_rec = JSON_object["loginserver_record"]
            recordpart = log_rec.split(',')
            broadcaster = recordpart[0]
            message =  JSON_object['message']
            ts = JSON_object['sender_created_at']

            con = sqlite3.connect('database.db')
            c = con.cursor()
            cursor = c.execute("INSERT INTO BROADCAST_RECORD(broadcaster,time,content)\
                VALUES('"+broadcaster+"',"+ts+",'"+message+"')")
            con.commit()
            con.close()

            return "{'respons' : 'ok'}"
        except:
            return "{'respons' : 'broadcast error'}"

    @cherrypy.expose
    @cherrypy.tools.json_in(force=False)
    def rx_privatemessage(self):
        JSON_object = cherrypy.request.json
        print(JSON_object)
        username = self.new_mainapp.get_username()
        try: 
            sender = verify.veri_privatemessage(JSON_object)


            ts = JSON_object['sender_created_at']
            message = communication.decrypt_privatemessage(JSON_object,username)
            

            print(message)
            con = sqlite3.connect('database.db')
            c = con.cursor()
            cursor = c.execute("INSERT INTO CHAT_RECORD(sender,time,content,receiver)\
                VALUES('"+sender+"',"+ts+",'"+message+"','"+username+"')")
            con.commit()
            con.close()
            return "{'respons' : 'ok'}"
        except:
            return "{'respons' : 'privatemessage error'}"

    # @cherrypy.expose
    # @cherrypy.tools.json_in(force=False)
    # def checkmessage(self):
        
    
        





