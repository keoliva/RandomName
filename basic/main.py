# #!/usr/bin/env python
# #
# # Copyright 2007 Google Inc.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
# #
# import webapp2
# from google.appengine.ext import ndb


# class ImageData(ndb.Model):
#      name = ndb.StringProperty(indexed=False)
#      image = ndb.BlobProperty()

# class AddProduct(webapp2.RequestHandler):
#     def post(self):
#         imagedata = ImageData(parent=image_key(image_name))
#         imagedata.name = self.request.get('name')
#         imagedata.image = self.request.get('image')
#         imagedata.put()

# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         self.response.write('Hello world!')




# app = webapp2.WSGIApplication([
#     ('/', MainHandler)
# ], debug=True)



# from __future__ import with_statement
# import os
# import urllib
# import webapp2



# import cloudstorage as gcs
# import main
# import webapp2

# from google.appengine.ext import blobstore
# from google.appengine.ext.webapp import blobstore_handlers

# import google.appengine.api.app_identity



# # from google.appengine.ext import blobstore
# # from google.appengine.ext.webapp import blobstore_handlers

# class MainHandler(webapp2.RequestHandler):
#   def get(self):
#     upload_url = blobstore.create_upload_url('/upload')
#     self.response.out.write('<html><body>')
#     self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
#     self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
#         name="submit" value="Submit"> </form></body></html>""")

# class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
#   def post(self):
#     upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
#     blob_info = upload_files[0]
#     self.redirect('/serve/%s' % blob_info.key())

# class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
#   def get(self, resource):
#     resource = str(urllib.unquote(resource))
#     blob_info = blobstore.BlobInfo.get(resource)
#     self.send_blob(blob_info)



# def CreateFile(filename):
#   """Create a GCS file with GCS client lib.

#   Args:
#     filename: GCS filename.

#   Returns:
#     The corresponding string blobkey for this GCS file.
#   """
#   # Create a GCS file with GCS client.
#   with gcs.open(filename, 'w') as f:
#     f.write('abcde\n')

#   # Blobstore API requires extra /gs to distinguish against blobstore files.
#   blobstore_filename = '/gs' + filename
#   # This blob_key works with blobstore APIs that do not expect a
#   # corresponding BlobInfo in datastore.
#   return blobstore.create_gs_key(blobstore_filename)


# class GCSHandler(webapp2.RequestHandler):

#   def get(self):
#     self.response.headers['Content-Type'] = 'text/plain'
#     gcs_filename = google.appengine.api.app_identity.get_default_gcs_bucket_name()  + '/blobstore_demo'
#     blob_key = CreateFile(gcs_filename)

#     # Fetch data.
#     self.response.write('Fetched data %s\n' %
#                         blobstore.fetch_data(blob_key, 0, 2))

#     # Delete files.
#     blobstore.delete(blob_key)


# class GCSServingHandler(blobstore_handlers.BlobstoreDownloadHandler):

#   def get(self):
#     blob_key = CreateFile(main.BUCKET + '/blobstore_serving_demo')
#     self.send_blob(blob_key)

# # app = webapp2.WSGIApplication([
# #                               debug=True)

# app = webapp2.WSGIApplication([('/', MainHandler),
#                                ('/upload', UploadHandler),
#                                ('/serve/([^/]+)?', ServeHandler),
# 								('/blobstore/ops', GCSHandler),
#                                ('/blobstore/serve', GCSServingHandler)],
#                               debug=True)





import os
import urllib
import jinja2
import wordExtraction

from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

jinja_environment = jinja2.Environment(loader = 
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Struct():
    pass
data = Struct()

class MainHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')

        template_values = {'upload_url' : upload_url}
        template = jinja_environment.get_template('home.html')
        self.response.out.write(template.render(template_values))
        
        #self.response.out.write('<html><body>')
        #self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        #self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit" name="submit" value="Submit"> </form></body></html>""")

    def post(self):
        #upload_files = self.get_uploads('file')
        #blob_info = upload_files[0]
        self.redirect('/upload')
    
        #b = blobstore.BlobInfo.all()[0]
        #Allows you to download the file you just uploaded
        #self.response.out.write('<li><a href="/serve/%s' % str(b.key()) + '">' + str(b.filename) + '</a>')

        #if ".txt" in b.filename:
            # location = "/serve/" + str(b.key)
            #blob_reader = blobstore.BlobReader(str(b.key()))
            #A HUGE STRING REPRESENTING THE SYLLABUS
            #txt_file_text = blob_reader.read()
            #data.text_file = txt_file_text
            #self.response.out.write('<li>' + value)

            #template_values = {'txt_file_text' : txt_file_text}
            #template = jinja_environment.get_template('confirm_upload.html')
            #self.response.out.write(template.render(template_values))
        
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        b = blobstore.BlobInfo.all()[0]
        #Allows you to download the file you just uploaded
        #self.response.out.write('<li><a href="/serve/%s' % str(b.key()) + '">' + str(b.filename) + '</a>')

        if ".txt" in b.filename:
            # location = "/serve/" + str(b.key)
            blob_reader = blobstore.BlobReader(str(b.key()))
            #A HUGE STRING REPRESENTING THE SYLLABUS
            txt_file_text = blob_reader.read()
            #data.text_file = txt_file_text
            #self.response.out.write('<li>' + value)
            (assignmentList, ExamsList) = wordExtraction.main(txt_file_text)
            template_values = {"assigmentList":assignmentList, "ExamsList":ExamsList}

            template = jinja_environment.get_template('confirm_upload.html')
            self.response.out.write(template.render(template_values))
            
    def post(self):
        #login handler code
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, blob_key):
        blob_key = str(urllib.unquote(blob_key))
        if not blobstore.get(blob_key):
            self.error(404)
        else:
            self.send_blob(blobstore.BlobInfo.get(blob_key), save_as=True)


app = webapp.WSGIApplication(
      [('/', MainHandler),
       ('/upload', UploadHandler),
       ('/serve/([^/]+)?', ServeHandler),
      ], debug=True)

