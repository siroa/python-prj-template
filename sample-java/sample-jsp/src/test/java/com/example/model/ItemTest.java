package com.example.model;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ItemTest {

    @Test
    @DisplayName("コンストラクタとGetterが正しく値を返すこと")
    void testConstructorAndGetter() {
        Item item = new Item(1, "テストアイテム");

        assertEquals(1, item.getId());
        assertEquals("テストアイテム", item.getName());
    }

    @Test
    @DisplayName("Setterで値の更新ができること")
    void testSetter() {
        Item item = new Item();
        item.setId(2);
        item.setName("更新後アイテム");

        assertEquals(2, item.getId());
        assertEquals("更新後アイテム", item.getName());
    }
}