import os
import jinja2
import urllib
from google.appengine.ext import webapp
import cgi
import logging
import wordExtraction

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
		template = jinja_environment.get_template('home.html')
		self.response.out.write(template.render(template_values))
	
	def post(self):
		uploaded_file = self.request.get("file")
		logging.info("hello")
		logging.debug(uploaded_file)
		print "pls?", uploaded_file
		self.redirect('/confirm')
		
class ConfirmHandler(webapp.RequestHandler):
	def post(self):
		fileitem = self.request.get('user_file')
		unicode_str = fileitem.decode('utf-8')
		#(assignmentList,examList) = wordExtraction.main(fileitem)
		assignmentList = unicode_str.split("\n")
		logging.debug(assignmentList)
		examList = []
		##logging.log(root,assignmentList[0][0])
		template_values = {'assignmentList': assignmentList,
							'exams': examList}
		template = jinja_environment.get_template('confirm_upload.html')
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
	('/confirm', ConfirmHandler),
	('/upload', UploadHandler),
	('/serve', ServeHandler),
],debug=True)