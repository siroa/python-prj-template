<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>アイテム一覧 (Spring Boot + JDK8)</title>
    <style>
        body { font-family: sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 400px; margin-top: 16px; }
        th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
        th { background-color: #f2f2f2; }
        .form-group { margin-bottom: 20px; }
        input[type="text"] { padding: 6px; width: 250px; }
        button { padding: 6px 12px; cursor: pointer; }
    </style>
</head>
<body>

    <h2>アイテム登録</h2>
    <form action="${pageContext.request.contextPath}/items" method="post" class="form-group">
        <input type="text" name="name" placeholder="新しいアイテム名を入力" required>
        <button type="submit">追加</button>
    </form>

    <h2>登録済みアイテム一覧</h2>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>名前</th>
            </tr>
        </thead>
        <tbody>
            <c:choose>
                <c:when test="${not empty items}">
                    <c:forEach var="item" items="${items}">
                        <tr>
                            <td><c:out value="${item.id}" /></td>
                            <td><c:out value="${item.name}" /></td>
                        </tr>
                    </c:forEach>
                </c:when>
                <c:otherwise>
                    <tr>
                        <td colspan="2">アイテムが登録されていません。</td>
                    </tr>
                </c:otherwise>
            </c:choose>
        </tbody>
    </table>

</body>
</html>