package com.example.servlet;

import com.example.model.Item;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicInteger;

@WebServlet("/items")
public class ItemServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    private final List<Item> itemList = new CopyOnWriteArrayList<>();
    private final AtomicInteger idCounter = new AtomicInteger(1);

    @Override
    public void init() throws ServletException {
        itemList.add(new Item(idCounter.getAndIncrement(), "JDK8環境の検証"));
        itemList.add(new Item(idCounter.getAndIncrement(), "JSP/Servletレガシー保守"));
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        req.setAttribute("items", itemList);
        req.getRequestDispatcher("/WEB-INF/views/items.jsp").forward(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) 
            throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        String itemName = req.getParameter("name");

        if (itemName != null && !itemName.trim().isEmpty()) {
            itemList.add(new Item(idCounter.getAndIncrement(), itemName.trim()));
        }

        resp.sendRedirect(req.getContextPath() + "/items");
    }
}