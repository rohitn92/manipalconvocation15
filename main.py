#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import smtplib
import shlex
import subprocess
import requests
import cgi
import os
import logging
import urllib
from google.appengine.ext import ndb
from google.appengine.api import users

mailinglist_key = ndb.Key('Mailinglist', 'default_mailinglist')



class Greeting(ndb.Model):
  student = ndb.TextProperty()
  address = ndb.TextProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):

        self.response.out.write('<html><head><script src="https://www.google.com/recaptcha/api.js"></script></head><body>')


        self.response.write('<h1>MU Convocation Mail Alert</h1><h2>Find out asap when the server comes back up!</h2>')

        if (self.request.get('CaptchaFail')=='True'):
            self.response.out.write("<h3 style='color:red'>Sign-up FAILED. Please enter Captcha before submit</h3>")
        self.response.out.write("""
          <form action="/sign" method="post">
            <div>NAME:<input type="text" name="stuname" required disabled></input><br \>EMAIL:<input type="email" name="stumail" required disabled></input></div>
            <div>Sorry, it's over now. Thanks for Visiting! If you wanna know how I coded this, tweet me @theRonnicle</div>
            <div class="g-recaptcha" data-sitekey="YOUR-SITE-PUBLIC-KEY"></div>
          </form>
        """)
        self.response.write('<h3>The following are already signed up</h3>')

        greetings = ndb.gql('SELECT * '
                      'FROM Greeting '
                      'WHERE ANCESTOR IS :1 ',
                      mailinglist_key)
        for greeting in greetings:
            self.response.out.write('%s<br \> ' % cgi.escape(greeting.student))
        self.response.out.write('</body></html>')


class Mailinglist(webapp2.RequestHandler):
  def post(self):
    remoteip  = self.request.remote_addr
    gresponse = self.request.get('g-recaptcha-response')
    captchaUrl = 'https://www.google.com/recaptcha/api/siteverify'
    data = urllib.urlencode({"secret":"YOUR-SITE-SECRET-KEY","response":gresponse,"remoteip":remoteip})
    cResponse = urllib.urlopen(captchaUrl,data)
    print remoteip
    verf =  cResponse.read()
    if "true" in verf and 'chutiya' not in self.request.get('stuname') and 'Chutiya' not in self.request.get('stuname'):
        greeting = Greeting(parent=mailinglist_key)
        greeting.student = self.request.get('stuname')
        greeting.address = self.request.get('stumail')
        greeting.put()
        self.redirect('/')
    else:
      self.redirect('/?CaptchaFail=True')




class CronTask(webapp2.RequestHandler):

    def  get(self):
        print 'Cron Run'
        FROMADDR = "YOUREMAILADDR@gmail.com"
        LOGIN    = FROMADDR
        PASSWORD = "EMAILPASSWORD"
        TOADDRS  = ["MAILS@SOMETHING.COM"]
        SUBJECT  = "SUBJECT FOR EMAIL"

        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
               % (FROMADDR, ", ".join(TOADDRS), SUBJECT) )
        msg += "Hi. \r\n YOUR MSG \r\n"


        resp = requests.head("http://google.com")
        status = resp.status_code

        #You can check for multiple URLs
        #resp2 = requests.head("http://google.com")
        #status2 = resp2.status_code

        print status
        print status2
        #and then check the response...
        if (status == 404 or status == 500):
          print 'Convocation Server is down!'
        #Can make conditions according to our needs
        #if (status == 404 or status == 500) and (status2 == 500 or status2 == 404) .. Can also check 200 or any other status code
        else:
          print 'is up!'
          greetings = ndb.gql('SELECT * '
                        'FROM Greeting '
                        'WHERE ANCESTOR IS :1',
                        mailinglist_key)
          for greeting in greetings:
              TOADDRS.append(str(cgi.escape(greeting.address)));

        #IMPORTANT --  Gmail does not allow more than 100 emails a day!!!!!!!!!!!!!!!!! You will be marked as spammer too
        #So use LIMIT and OFFSET in your query OR use multiple emails and send msgs in batches of < 100.
          server = smtplib.SMTP('smtp.gmail.com', 587)
          server.set_debuglevel(1)
          server.ehlo()
          server.starttls()
          server.login(LOGIN, PASSWORD)
          server.sendmail(FROMADDR, TOADDRS, msg)
          server.quit()


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/crontask', CronTask),
    ('/sign', Mailinglist)
], debug=True)
