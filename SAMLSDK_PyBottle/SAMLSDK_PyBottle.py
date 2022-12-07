#Main Application

import bottle
import os
import sys
import SAML_Interface
import uuid
import requests
from bottle import Bottle, route, view, run, redirect, request, response, ServerAdapter, jinja2_view
from datetime import datetime
from paste import httpserver
from beaker.middleware import SessionMiddleware



if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    bottle.debug(True)

def wsgi_app():
    #Returns the application to make available through wfastcgi. This is used when the site is published to Microsoft Azure.
    return bottle.default_app()

if __name__ == '__main__':
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    HOST =  '35.188.52.49'
    PORT = 80
    session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
    }
    app = SessionMiddleware(bottle.app(), session_opts)
    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        #Handler for static files, used with the development server. When running under a production server such as IIS or Apache, the server should be configured to serve the static files.
        return bottle.static_file(filepath, root=STATIC_ROOT)

#Http Routing

    #Default
    @route('/')
    @route('/default')
    @view('default')
    def default(): 
        url="https://script.google.com/macros/s/AKfycbxj59wtJBvZF9qKqDAd392GAiiNVYMeF8LaFDxGIOPT--VVcc1wJiZDLKXgEyxh4xQ/exec"
        res=requests.get(url)
        resserver=res.json()
        headersServer=resserver["schema"]["fields"] 
        rowsServer=resserver['rows'][0]['f']
        valuesJson=list()

        for i,v in enumerate(headersServer):
          valuesJson.append( rowsServer[i]['v'])    
        return dict(
        mensajeBienvenida=valuesJson[0],
        TituloMenu=valuesJson[1],
        SubtituloMensaje=valuesJson[2],
        IDConfiguracion=valuesJson[3],
        ImagenLogin=valuesJson[4],
        IconoLogin=valuesJson[5],
        year=datetime.now().year
        )
    #ACS
    @route('/acs', method=['GET','POST'])
    @view('acs')
    def acs():
        samlResponse = request.forms['SAMLResponse']
        #ACS URL listed here:
        strAcsUrl = 'http://portalanalitico.gruponutresa.com/acs'
        data=SAML_Interface.SAML_Response.ParseSAMLResponse(strAcsUrl,samlResponse)
        print(data,"response")
        if data[0]:
           return({"token":data}
          )   
        
        else:
           return({
              "token":data})
    #Logout
    @route('/logout', method=['GET','POST'])
    @view('logout')
    def logout():
        #Sign Out URL listed here:
        strIdentityProviderSignOutURL = 'https://aaj0709.my.idaptive.app/applogout/appkey/fdd6c5c3-1082-4fbf-b28f-18967a6fb049/customerid/AAJ0709'          
        bottle.redirect('{uIDPUrl}?{bParams}'.format(uIDPUrl = strIdentityProviderSignOutURL, bParams = ''))
    #Login
    @route('/login', method=['GET','POST'])
    @view('login')
    def login():
        strAcsUrl = 'http://portalanalitico.gruponutresa.com/acs'
        #Issuer URL listed here:
        strIssuer = 'https://aaj0709.my.idaptive.app/fdd6c5c3-1082-4fbf-b28f-18967a6fb049'
        #Sign In URL listed here:
        strSingleSignOnURL = 'https://aaj0709.my.idaptive.app/applogin/appKey/fdd6c5c3-1082-4fbf-b28f-18967a6fb049/customerId/AAJ0709'  
        bottle.redirect('{uIDPUrl}?{bParams}'.format(uIDPUrl = strSingleSignOnURL, bParams = SAML_Interface.SAML_Request.GetSAMLRequest(strAcsUrl, strIssuer)))
   
   # Starts a local test server.
    #bottle.run(host='10.128.0.3', port=PORT)
    #httpserver.serve(wsgi_app(), host='SSSPOR013CLOUD', port=443)
    bottle.run(host='SSSPOR013CLOUD', port=PORT, debug=False)
