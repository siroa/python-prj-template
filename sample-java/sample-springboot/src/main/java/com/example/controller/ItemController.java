package com.example.controller;

import com.example.model.Item;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import javax.annotation.PostConstruct;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicInteger;

@Controller
@RequestMapping("/items")
public class ItemController {

    private final List<Item> itemList = new CopyOnWriteArrayList<>();
    private final AtomicInteger idCounter = new AtomicInteger(1);

    @PostConstruct
    public void init() {
        itemList.add(new Item(idCounter.getAndIncrement(), "Spring Boot学習"));
        itemList.add(new Item(idCounter.getAndIncrement(), "JDK8保守開発"));
    }

    @GetMapping
    public String listItems(Model model) {
        model.addAttribute("items", itemList);
        return "items"; // /WEB-INF/views/items.jsp を解決
    }

    @PostMapping
    public String addItem(@RequestParam(value = "name", required = false) String name) {
        if (name != null && !name.trim().isEmpty()) {
            itemList.add(new Item(idCounter.getAndIncrement(), name.trim()));
        }
        return "redirect:/items"; // 二重送信防止（PRGパターン）
    }
}