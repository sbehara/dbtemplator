Copyright Satya Behara 2023

import os, os.path
import random
import string

import cherrypy
import templatron

class TemplateOperator(object):
	def templatize(self, sqlscript='', comments='', dbName='', schemaName='', objName='', scriptName='', jiraTkt='', objType=''):
		#templated_script = "this is templated to: " + sqlscript + " : " + comments + " : " + dbName + " : " + schemaName + " : " + objName + " : " + scriptName + " : " + jiraTkt + " : " + objType
		templated_script = templatron.generateTemplate(sqlscript, comments, dbName, schemaName, objName, scriptName, jiraTkt, objType)
		return templated_script
				
class TemplateGenerator(object):
   @cherrypy.expose
   def index(self):
       return open('index.html')

class TemplateGeneratorWebService(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']

    def POST(self, sqlscript='', commentsection='', dbname='', schemaname='', objname='', scriptname='', jiratkt='', objecttype=''):        
        templateOp = TemplateOperator()
        some_string = templateOp.templatize(sqlscript, commentsection, dbname, schemaname, objname, scriptname, jiratkt, objecttype)        
        cherrypy.session['mystring'] = some_string
        return some_string

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    def DELETE(self):
        cherrypy.session.pop('mystring', None)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = TemplateGenerator()
    webapp.generator = TemplateGeneratorWebService()
    cherrypy.quickstart(webapp, '/', conf)
