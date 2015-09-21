import cgi
import webapp2
import time, datetime
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from webapp2_extras import sessions, auth, json
from basehandler import SessionHandler, login_required
from models import User, Profile, Request, Endorsement

class RequestsHandler(SessionHandler):
  ''' Views current requests from other users '''
  @login_required
  def get(self):
    user = self.user_model
    current_date = datetime.datetime.now() - datetime.timedelta(hours=7)
    available_requests = Request.query(Request.start_time > current_date).order(Request.start_time)
    dead_requests = Request.query(Request.start_time <= current_date).order(Request.start_time)
    
    my_requests = []
    empty_requests = []
    filled_requests = []
    # Append to master list or personal list
    for request in available_requests:
      if request.sender != user.key:
        if request.recipient is None:
          empty_requests.append(request)
        else:
          filled_requests.append(request)
      else:
        my_requests.append(request)
    self.response.out.write(template.render('views/requests.html',
                            {'user': user, 'my_requests': my_requests,
                            "all_requests": empty_requests, 'filled_requests': filled_requests,
                            'dead_requests':dead_requests}))


class CreateRequestHandler(SessionHandler):
  ''' Create request from html modal '''
  @login_required
  def post(self):
    user = self.user_model
    location = cgi.escape(self.request.get("location"))
    date = cgi.escape(self.request.get("date"))
    time = cgi.escape(self.request.get("time"))
    
    # Convert date and time to datetime
    format_date = str(date+ " " +time+":00.0")
    start_time = datetime.datetime.strptime(format_date, "%Y-%m-%d %H:%M:%S.%f")

    # Create request
    request = Request()
    request.sender = user.key
    request.sender_name = user.username
    request.location = location
    request.start_time = start_time
    request.creation_time = datetime.datetime.now() - datetime.timedelta(hours=7) #PST
    request.put()
    self.redirect('/')

class ApproveRequestHandler(SessionHandler):
  ''' Processes current requests and removes from database '''
  def post(self):
    receiver = User.query(User.username == cgi.escape(self.request.get('approver'))).get()
    request_key = self.request.get('request')
    # Get request
    request = ndb.Key(urlsafe=request_key).get()
    if request != None:
        # Remove request
        request.recipient = self.user_model.key
        request.recipient_name.append(self.user_model.username)
        request.put()
    self.redirect('/requests')

class DeleteRequestHandler(SessionHandler):
  ''' Removes request entirely '''
  def post(self):
    request_key = self.request.get('request')
    # Get request
    request = ndb.Key(urlsafe=request_key).get()
    if request:
      request.key.delete()
    else:
      print "Not in datastore"
