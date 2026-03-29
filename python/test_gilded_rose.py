# -*- coding: utf-8 -*-
"""
Test suite for the Gilded Rose kata.

CT1–CT16 foram derivados a partir da cobertura de decisões (arestas) do
grafo de fluxo de controle de update_quality, garantindo 100% de cobertura
de todas as arestas do grafo.
"""

from gilded_rose import GildedRose, Item

NORMAL    = "Normal item"
SULFURAS  = "Sulfuras, Hand of Ragnaros"
AGED_BRIE = "Aged Brie"
BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"


def update(name, sell_in, quality):
    item = Item(name, sell_in, quality)
    GildedRose([item]).update_quality()
    return item


# CT1: Item normal com qualidade positiva antes do prazo
# Cobre: L10=False(esq), L11=True, L12=True, L13, L24=True, L25, L26=False
def test_CT1_normal_item_quality_decreases_before_sell_date():
    item = update(NORMAL, sell_in=10, quality=20)
    assert item.sell_in == 9
    assert item.quality == 19


# CT2: Item normal com qualidade zero antes do prazo
# Cobre: L10=False(esq), L11=False, L24=True, L25, L26=False
def test_CT2_normal_item_quality_zero_before_sell_date():
    item = update(NORMAL, sell_in=10, quality=0)
    assert item.sell_in == 9
    assert item.quality == 0


# CT3: Sulfuras com sell_in positivo
# Cobre: L10=False(esq), L11=True, L12=False, L24=False, L26=False
def test_CT3_sulfuras_positive_sell_in_unchanged():
    item = update(SULFURAS, sell_in=5, quality=80)
    assert item.sell_in == 5
    assert item.quality == 80


# CT4: Sulfuras com sell_in negativo
# Cobre: L24=False, L26=True, L27=True, L28=True, L29=True, L30=False
def test_CT4_sulfuras_negative_sell_in_unchanged():
    item = update(SULFURAS, sell_in=-1, quality=80)
    assert item.sell_in == -1
    assert item.quality == 80


# CT5: Aged Brie com qualidade abaixo de 50 antes do prazo
# Cobre: L10=True(direita), L15=True, L16, L17=False, L24=True, L25, L26=False
def test_CT5_aged_brie_quality_increases_before_sell_date():
    item = update(AGED_BRIE, sell_in=5, quality=10)
    assert item.sell_in == 4
    assert item.quality == 11


# CT6: Aged Brie com qualidade no teto (50) antes do prazo
# Cobre: L10=True(direita), L15=False, L17=False, L24=True, L25, L26=False
def test_CT6_aged_brie_quality_capped_before_sell_date():
    item = update(AGED_BRIE, sell_in=5, quality=50)
    assert item.sell_in == 4
    assert item.quality == 50


# CT7: Backstage pass com mais de 10 dias restantes
# Cobre: L10=True(direita), L15=True, L16, L17=True, L18=False, L21=False, L24=True, L25, L26=False
def test_CT7_backstage_more_than_10_days_quality_plus1():
    item = update(BACKSTAGE, sell_in=15, quality=20)
    assert item.sell_in == 14
    assert item.quality == 21


# CT8: Backstage pass com exatamente 10 dias restantes
# Cobre: L18=True, L19=True, L20, L21=False
def test_CT8_backstage_10_days_quality_plus2():
    item = update(BACKSTAGE, sell_in=10, quality=20)
    assert item.sell_in == 9
    assert item.quality == 22


# CT9: Backstage pass com exatamente 5 dias restantes
# Cobre: L18=True, L19=True, L20, L21=True, L22=True, L23
def test_CT9_backstage_5_days_quality_plus3():
    item = update(BACKSTAGE, sell_in=5, quality=20)
    assert item.sell_in == 4
    assert item.quality == 23


# CT10: Backstage pass com 10 dias e qualidade 49 (teto L19)
# Cobre: L18=True, L19=False, L21=False
def test_CT10_backstage_10_days_quality_capped_at_L19():
    item = update(BACKSTAGE, sell_in=10, quality=49)
    assert item.sell_in == 9
    assert item.quality == 50


# CT11: Backstage pass com 5 dias e qualidade 49 (teto L19 e L22)
# Cobre: L18=True, L19=False, L21=True, L22=False
def test_CT11_backstage_5_days_quality_capped_at_L22():
    item = update(BACKSTAGE, sell_in=5, quality=49)
    assert item.sell_in == 4
    assert item.quality == 50


# CT12: Item normal após o prazo com qualidade positiva
# Cobre: L26=True, L27=True, L28=True, L29=True, L30=True, L31
def test_CT12_normal_item_past_sell_date_quality_degrades_double():
    item = update(NORMAL, sell_in=0, quality=10)
    assert item.sell_in == -1
    assert item.quality == 8


# CT13: Item normal após o prazo com qualidade zero
# Cobre: L26=True, L27=True, L28=True, L29=False
def test_CT13_normal_item_past_sell_date_quality_zero():
    item = update(NORMAL, sell_in=0, quality=0)
    assert item.sell_in == -1
    assert item.quality == 0


# CT14: Backstage pass após o concerto (sell_in=0 → vira -1)
# Cobre: L26=True, L27=True, L28=False, L33 (quality = 0)
def test_CT14_backstage_after_concert_quality_zero():
    item = update(BACKSTAGE, sell_in=0, quality=20)
    assert item.sell_in == -1
    assert item.quality == 0


# CT15: Aged Brie após o prazo com qualidade abaixo de 50
# Cobre: L26=True, L27=False, L35=True, L36
def test_CT15_aged_brie_past_sell_date_quality_increases():
    item = update(AGED_BRIE, sell_in=0, quality=10)
    assert item.sell_in == -1
    assert item.quality == 12


# CT16: Aged Brie após o prazo com qualidade no teto (50)
# Cobre: L26=True, L27=False, L35=False
def test_CT16_aged_brie_past_sell_date_quality_capped():
    item = update(AGED_BRIE, sell_in=0, quality=50)
    assert item.sell_in == -1
    assert item.quality == 50
