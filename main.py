import webapp2
import jinja2
import os

import re
import cgi

import urllib
import string

from google.appengine.ext import ndb
from google.appengine.api import users


template_dir = os.path.join(os.path.dirname(__file__), "templates")
#template librabry is used to build complicated strings. In web applications
# most of the times these strings are HTML.Jinja is one such library bult into 
# Google app engine.
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                extensions=['jinja2.ext.autoescape'],
                                autoescape=True)

Error = "error=1"
DEFAULT_HOLDER = 'default_comment'


def Comment_Key(comments_holder=DEFAULT_HOLDER):
# DEFAULT_HOLDER is the variable to assign key name to
#comments_holder.In case of no assignment from Handler function it will fall back to 'Commentblock' 
  return ndb.Key('Commentblock', comments_holder)

class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    location = ndb.StringProperty(indexed=False)

class Commentinfo(ndb.Model):
    """Main Model an individual  entry with an author,topic, content, and date."""
    author = ndb.StructuredProperty(Author)
    topic = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

def valid_name(name):
    if  len(name)<20:
        p = r"[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if re.search(p, name):
            return "invalid"
        else:
            return "valid"
    else:

        return "invalid"

def valid_id(email):
    if  len(email)<35:
        p = r"[@.]"
        if re.search(p, email):
            return "valid"
        else:
            return "invalid"
    else:
        return "invalid"

def blank_comments(mystring):
    if mystring:
        if not mystring.strip():
            return True 
        else:
            return False
    elif (mystring == ""):
        return True
    else:
        return False


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
#this function in the Parent class Handler only outputs what ever data
#is being sent to it. Additional parameters *a & **kw is mentioned in case
# there are extra parameters to be passed on.
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
# Inherited class MainPage is derived to have properties of parent class
# Handler such as its write function is used to render the form as shown 
# belowtemplate_values ={}
    def get(self):
        self.render('home.html')

class StageOne(Handler):
    def get(self):
        self.render('stage1.html')

class StageTwo(Handler):
    def get(self):
        self.render('stage2.html')

class StageThree(Handler):
    def get(self):
        self.render('stage3.html')

class StageFour(Handler):
    def get(self):
        self.render('stage4.html')

class StageFive(Handler):
    def get(self):
        self.render('stage5.html')

class ThanksHandler(Handler):
    
    def get(self):
        #Query DB to get last 10 entries
        comments_holder = self.request.get('comments_holder',DEFAULT_HOLDER)
        comments_query = Commentinfo.query(
           ancestor = Comment_Key(comments_holder)).order(Commentinfo.date)
        comments = comments_query.fetch(10)
        
        # once logged in the user has a log out option.
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        error_msg = ''
        error = self.request.get('error')
        if error=='1':
            error_msg = "Invalid Input"

        template_values = {'comments': comments, 'url': url, 
        'comments_holder':comments_holder,
        'error_msg' : error_msg, 'url_linktext': url_linktext}

        self.render('form.html', **(template_values))    

class FeedbackHandler(Handler):
    def write_form(self,nameerror,emailerror,locationerror,name,email,location):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {"nameerror":nameerror, "emailerror":emailerror,
                            "locationerror": locationerror,"name": name,
                            "email": email,"location": location,
                            'url': url,'url_linktext': url_linktext}
        self.render("form.html",**(template_values))

    def post(self):
        user_name = self.request.get('name')
        user_id = self.request.get('email')
        user_location = self.request.get('location')

        name = valid_name(user_name)
        email = valid_id(user_id)
        location = valid_name(user_location)

        if (name and email and location == "invalid"):
            self.write_form("Invalid name","Invalid email","Invalid location",user_name,user_id,user_location) 
        elif (name and email == "invalid"):
            self.write_form("Invalid name","Invalid email","",user_name,user_id,user_location) 
        elif (name and location == "invalid"):
            self.write_form("Invalid name","","Invalid location",user_name,user_id,user_location) 
        elif (email and location == "invalid"):
            self.write_form("","Invalid email","Invalid location",user_name,user_id,user_location) 
        elif (name == "invalid"):
            self.write_form("Invalid name","","",user_name,user_id,user_location)
        elif (email == "invalid"):
            self.write_form("","Invalid email","",user_name,user_id,user_location) 
        elif (location == "invalid"):
            self.write_form("","","Invalid location",user_name,user_id,user_location)
        else:
            comments_holder = self.request.get('comments_holder',DEFAULT_HOLDER)
            comment = Commentinfo(parent=Comment_Key(comments_holder))
            comment.author = Author(
                identity = user_name,
                email = user_id,
                location = user_location)

            comment.topic = self.request.get('topic')
            comment.content = self.request.get('content')

            blank_check = blank_comments(comment.content)
            if blank_check:
                self.redirect('/contact?' + Error)
            else: 
                comment.put()
                self.redirect('/contact?name='+user_name+urllib.urlencode({'comments_holder': comments_holder})) 
        #eg. self.redirect("/thanks?name="+user_name+"&email="+user_email+"&topic="+topic)                         
        

app = webapp2.WSGIApplication([('/', MainPage),("/stageone", StageOne),("/stagetwo", StageTwo),
                                ("/stagethree", StageThree),("/stagefour", StageFour),("/stagefive", StageFive),
                                ('/contact',ThanksHandler), ('/sign', FeedbackHandler)], debug=True)
