import bottle
import zlib
import base64
import uuid
import urllib

from signxml import XMLVerifier
from base64 import b64decode

from datetime import datetime

from lxml import etree 

from lxml.builder import ElementMaker
import xmltodict
import json
import requests
import random
from datetime import datetime




class SAML_Request:
    def GetSAMLRequest(strACSUrl = None, strIssuer = None):
        print("hola saml request")
        xSAMLPNode = ElementMaker(namespace='urn:oasis:names:tc:SAML:2.0:protocol', nsmap=dict(saml2p='urn:oasis:names:tc:SAML:2.0:protocol'))
        xSAMLNode = ElementMaker(namespace='urn:oasis:names:tc:SAML:2.0:assertion', nsmap=dict(saml2='urn:oasis:names:tc:SAML:2.0:assertion'))

        dCurrentTime = datetime.utcnow()

        xAuthnRequestNode = xSAMLPNode.AuthnRequest(ProtocolBinding='urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST', Version='2.0', IssueInstant= dCurrentTime.replace(microsecond=0).isoformat() + ".46Z", ID=uuid.uuid4().hex, AssertionConsumerServiceURL=strACSUrl)

        xIssuerNode = xSAMLNode.Issuer()
        xIssuerNode.text = strIssuer
        xAuthnRequestNode.append(xIssuerNode)

        xNameIDNode = xSAMLPNode.NameIDPolicy('urn:oasis:names:tc:SAML:2.0:nameid-format:unspecified',AllowCreate='true')
        xAuthnRequestNode.append(xNameIDNode)

        xAuthnContextNode = xSAMLPNode.RequestedAuthnContext(Comparison='exact')
        xAuthnRequestNode.append(xAuthnContextNode)
        xAuthnContextClassRef = xSAMLNode.AuthnContextClassRef()
        xAuthnContextClassRef.text = 'urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport'
        xAuthnContextNode.append(xAuthnContextClassRef)

        strBase64Request = base64.b64encode(etree.tostring(xAuthnRequestNode))
        strUrlParams = urllib.parse.urlencode([('SAMLRequest', strBase64Request)])
  
        return strUrlParams
      
class SAML_Response:
    def ParseSAMLResponse(strACSUrl, strEncodedSAMLResponse):
        cert = open("static/certificates/SignCertFromIdaptive.cer").read()
        strDecodedSAMLResponse = b64decode(strEncodedSAMLResponse)
        XMLVerifier().verify(strDecodedSAMLResponse, x509_cert=cert)
            
       
        #print(json.loads(stringroot)) 
        try:
            XMLVerifier().verify(strDecodedSAMLResponse, x509_cert=cert)
            print("entre al metodo post")
            root = etree.fromstring(b64decode(strEncodedSAMLResponse))
            byteroot=etree.tostring(root)
            stringroot=byteroot.decode("utf-8") 
            xmlresponsedirect=xmltodict.parse(stringroot)
            datadumps=json.dumps(xmlresponsedirect)
            datajson=json.loads(datadumps)
            data=datajson['saml2p:Response']['Assertion']['AttributeStatement']['Attribute']
            dataUser=list()
            now = datetime.now()
            hour=now.strftime('%H:%M:%S')
            datetoday=datetime.today().strftime('%Y-%m-%d')
            numeros=list()
            for i in range(6):
              numeros.append(str(random.randrange(5, 100)))
     
            token=numeros[0]+numeros[1]+numeros[2]+numeros[3]+numeros[4]+numeros[5]+str(now).replace(" ","").replace(".","").replace(("-"), "").replace(":", "")     
            
            for d in data:
             dataUser.append({
                       "type":d["@Name"],
                       "value":d["AttributeValue"],
                       
                    })
            dataUser.append(
                
                {"type": "token",
                  "value":token 
                  }
            )
            dataUser.append(
                
                {"type": "fecha",
                  "value":datetoday 
                  }
            ) 
             
            dataUser.append(
                
                {"type": "hora",
                  "value":hour 
                  }
            ) 
            
            headersEnvio = {'Content-Type': 'application/json', 'Accept':'application/json'}    
            rest=requests.post("https://script.google.com/macros/s/AKfycbxj59wtJBvZF9qKqDAd392GAiiNVYMeF8LaFDxGIOPT--VVcc1wJiZDLKXgEyxh4xQ/exec", json=dataUser, headers=headersEnvio)
            print("respuesta",rest.text)
            print("token", token)
        except:
             dataUser.append(False)
             
        return token
