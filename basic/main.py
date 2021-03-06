import os
import jinja2
import urllib
from google.appengine.ext import webapp
import cgi
import logging
import wordExtraction

from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

jinja_environment = jinja2.Environment(loader = 
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Struct(): pass
data = Struct()

	
class MainHandler(webapp.RequestHandler):
	def get(self):
		upload_url = blobstore.create_upload_url('/upload')
	
		template_values = {'upload_url' : upload_url}
		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))
	
	def post(self):
		uploaded_file = self.request.get("file")
		logging.info("hello")
		logging.debug(uploaded_file)
		print "pls?", uploaded_file
		self.redirect('/confirm')
		
class AboutHandler(webapp.RequestHandler):
        def get(self):
                template = jinja_environment.get_template('about.html')
		self.response.out.write(template.render())
                
class ConfirmHandler(webapp.RequestHandler):
	def post(self):
		fileitem = self.request.get('user_file')
		unicode_str = fileitem.decode('utf-8')
		logging.info("``````````````````````````")
		logging.debug(fileitem)
		(assignmentList,examList) = main(unicode_str)
		data.assignments = assignmentList
		data.exams = examList
		#logging.info(assignmentList[0])
		
		#assignmentList = unicode_str.split("\n")
		#logging.debug(assignmentList)
		##examList = []
		##logging.log(root,assignmentList[0][0])
		template_values = {'assignmentList': assignmentList,
				'exams': examList}
		template = jinja_environment.get_template('confirm_upload.html')
		self.response.out.write(template.render(template_values))

class CalendarHandler(webapp.RequestHandler):
	def post(self):
		#grab all the things in the form
		(num_assign, num_exam) = (len(data.assignments), len(data.exams))
		for i in range(num_assign):
			date = self.request.get("a_Date%d" % i)
			name = self.request.get("a_Description%d" % i)

		
		for i in range(num_exam):
			date = self.request.get("e_Date%d" % i)
			name = self.request.get("e_Description%d" % i)
		
		self.redirect('/success')
	
class SuccessHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		#a = wordExtraction.createics(data.assignments,data.exams)
		logging.info(add(2,3))
		print add(4,5)
		logout_url = users.create_logout_url('/')
		template_values = {'user': user, 'logout_url': logout_url,
		'assign':str(len(data.assignments)), 'exam':str(len(data.exams))}
	
		template = jinja_environment.get_template('success.html')
		self.response.out.write(template.render(template_values))
	
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
	
		#blob_info = upload_files[0]
		logging.debug(blob_info)
		self.redirect('/serve')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, resource):
		resource = str(urllib.unquote(resource))
		if not blobstore.get(resource):
			self.error(404)
		else:
			self.send_blob(blobstore.BlobInfo.get(resource), save_as=True)
	#blob_info = blobstore.BlobInfo.get(resource)
	#self.send_blob(blob_info)
	
		self.redirect('/confirm')

app = webapp.WSGIApplication(
[('/', MainHandler),
         ('/about', AboutHandler),
	('/confirm', ConfirmHandler),
	('/calendar', CalendarHandler),
	('/success', SuccessHandler),
	('/upload', UploadHandler),
	('/serve', ServeHandler),
],debug=True)
