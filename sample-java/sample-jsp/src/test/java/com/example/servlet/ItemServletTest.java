package com.example.servlet;


import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ItemServletTest {

    private ItemServlet servlet;

    @Mock
    private HttpServletRequest request;

    @Mock
    private HttpServletResponse response;

    @Mock
    private RequestDispatcher dispatcher;

    @BeforeEach
    void setUp() throws ServletException {
        servlet = new ItemServlet();
        servlet.init(); // 初期データ投入
    }

    @Test
    @DisplayName("doGet: リクエストスコープにitemsを設定し、JSPへフォワードすること")
    void testDoGet() throws ServletException, IOException {
        when(request.getRequestDispatcher("/WEB-INF/views/items.jsp")).thenReturn(dispatcher);

        servlet.doGet(request, response);

        // リクエストスコープにリストがセットされたことを検証
        verify(request).setAttribute(eq("items"), any(List.class));

        // JSPへフォワードされたことを検証
        verify(dispatcher).forward(request, response);
    }

    @Test
    @DisplayName("doPost: 値が入力された場合、登録して/itemsへリダイレクトすること")
    void testDoPost_Success() throws ServletException, IOException {
        when(request.getParameter("name")).thenReturn("追加テスト");
        when(request.getContextPath()).thenReturn("/sample");

        servlet.doPost(request, response);

        // 文字エンコーディングがUTF-8に指定されたこと
        verify(request).setCharacterEncoding("UTF-8");

        // 二重送信防止のためのリダイレクト先URLを検証
        verify(response).sendRedirect("/sample/items");
    }

    @Test
    @DisplayName("doPost: 入力値が空白またはnullの場合でもリダイレクトすること")
    void testDoPost_EmptyName() throws ServletException, IOException {
        when(request.getParameter("name")).thenReturn("   ");
        when(request.getContextPath()).thenReturn("");

        servlet.doPost(request, response);

        verify(response).sendRedirect("/items");
    }
}