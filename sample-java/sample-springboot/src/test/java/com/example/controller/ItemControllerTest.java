package com.example.controller;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ItemController.class)
class ItemControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    @DisplayName("GET /items: 一覧画面のJSPと初期データを返却すること")
    void testListItems() throws Exception {
        mockMvc.perform(get("/items"))
                .andExpect(status().isOk())
                .andExpect(view().name("items"))
                .andExpect(model().attributeExists("items"))
                .andExpect(model().attribute("items", hasSize(2)));
    }

    @Test
    @DisplayName("POST /items: パラメータを送信すると /items へリダイレクトすること")
    void testAddItem_Success() throws Exception {
        mockMvc.perform(post("/items").param("name", "新規テスト"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/items"));
    }
}