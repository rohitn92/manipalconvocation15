<h1>App Engine Python Project</h1>

<h2> What does this project do? </h2>

<h3>This project does the following 3 things -</h3>
<ul>
<li>Repeatedly check the status of a URL using the <a href="http://www.python-requests.org/en/latest/">"Requests"</a> library a through a Cron job scheduler that runs a particular method in the python script </li>
<li>Send emails via GMAIL through python script using STMPLIB </li>
<li>Create an online mailing list through form submission that is verified using <a href="https://www.google.com/recaptcha/intro/index.html">Google's "Recaptcha"</a></li>
</ul>
<h4>What will you learn?</h4>
<ul type = "square">
<li>How to implement reCAPTCHA using python. The packages you will find online are quite redundant. You just need to send a POST request with certain parameters to google's verification. </li>
<li>Schedule tasks using cron on Google App Engine.</li>
<li>How to check the status of a URL using HTTP requests, since GAE doesn't support ICMP or telnet.</li>
<li>How to automate emails through you web application</li>
</ul>
<h5>NOTES</h5>
<ul type = "circle">
<li>The Requests library is included in my repository since it is not provided in Google Cloud's Runtime-Provided Libraries. So you will need to upload it with your application.</li>
<li>Emails will not be sent till you enable BILLING on your application which enables sockets.</li>
<li>You cannot send more than 100 emails a day via gmail. Also, you can be easily marked as a spammer for bulk mails. So use OFFSET, LIMIT and you judgement as to how you will handle sending over 100 mails, whether multiple IDs, breaking the emailing list into parts, etc. </li>
</ul>

<h4>MORE NOTES</h4>
App Engine does not have ICMP or Telnet Support. That is the reason we are using Requests library for its http request API call for external host communication. 

For a normal python script, something like the following would have worked as well - 

```python
cmd=shlex.split("ping -n 1 convocation.manipal.edu/registration/startup.aspx")
try:
   output = subprocess.check_output(cmd)
except subprocess.CalledProcessError,e:
   #Will print the command failed with its exit status
   print "The IP {0} is NotReacahble".format(cmd[-1])

else:
  print "The IP {0} is Reachable".format(cmd[-1])
```

For any more information, contact me <a href="http://www.twitter.com/theRonnicle" target="_blank"><h6>@theRonnicle</h6></a>
