# -*- coding: utf-8 -*-
"""
Comprehensive test suite for the Gilded Rose kata.

Covers all item types and edge cases based on the official requirements:
https://github.com/emilybache/GildedRose-Refactoring-Kata/blob/main/GildedRoseRequirements.md
"""

import pytest
from gilded_rose import GildedRose, Item


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def update(items, days=1):
    """Run update_quality for a given number of days and return items."""
    gr = GildedRose(items)
    for _ in range(days):
        gr.update_quality()
    return items


def make_item(name, sell_in, quality):
    return Item(name, sell_in, quality)


# ---------------------------------------------------------------------------
# Normal items  (e.g. "+5 Dexterity Vest", "Elixir of the Mongoose")
# ---------------------------------------------------------------------------

class TestNormalItem:

    def test_sell_in_decreases_by_one(self):
        item = make_item("+5 Dexterity Vest", sell_in=10, quality=20)
        update([item])
        assert item.sell_in == 9

    def test_quality_decreases_by_one_before_sell_date(self):
        item = make_item("+5 Dexterity Vest", sell_in=5, quality=10)
        update([item])
        assert item.quality == 9

    def test_quality_decreases_by_two_on_sell_date(self):
        # sell_in=0 means "today is the last day"; after update sell_in=-1
        # and quality degrades by 2 total
        item = make_item("+5 Dexterity Vest", sell_in=0, quality=10)
        update([item])
        assert item.quality == 8

    def test_quality_degrades_twice_as_fast_past_sell_date(self):
        item = make_item("+5 Dexterity Vest", sell_in=-1, quality=10)
        update([item])
        assert item.quality == 8

    def test_quality_never_goes_below_zero(self):
        item = make_item("+5 Dexterity Vest", sell_in=5, quality=0)
        update([item])
        assert item.quality == 0

    def test_quality_never_goes_below_zero_past_sell_date(self):
        item = make_item("+5 Dexterity Vest", sell_in=-1, quality=0)
        update([item])
        assert item.quality == 0

    def test_quality_at_one_degrades_to_zero_not_negative(self):
        item = make_item("+5 Dexterity Vest", sell_in=5, quality=1)
        update([item])
        assert item.quality == 0

    def test_quality_at_one_past_sell_date_clamps_at_zero(self):
        # quality would want to go to -1, but clamps at 0
        item = make_item("+5 Dexterity Vest", sell_in=-1, quality=1)
        update([item])
        assert item.quality == 0

    def test_sell_in_decreases_correctly_over_multiple_days(self):
        item = make_item("Elixir of the Mongoose", sell_in=5, quality=7)
        update([item], days=5)
        assert item.sell_in == 0

    def test_quality_over_multiple_days_before_sell_date(self):
        item = make_item("Elixir of the Mongoose", sell_in=5, quality=7)
        update([item], days=3)
        assert item.quality == 4

    def test_quality_degradation_accelerates_after_sell_date(self):
        # 3 days before sell date (quality -3) + 2 days after (+0 => 0, capped)
        item = make_item("Elixir of the Mongoose", sell_in=3, quality=10)
        update([item], days=5)
        # day 1: q=9, si=2
        # day 2: q=8, si=1
        # day 3: q=7, si=0
        # day 4: q=5, si=-1  (double degradation: sell_in became -1)
        # day 5: q=3, si=-2
        assert item.quality == 3
        assert item.sell_in == -2

    def test_quality_never_below_zero_over_many_days(self):
        item = make_item("+5 Dexterity Vest", sell_in=5, quality=3)
        update([item], days=20)
        assert item.quality == 0

    def test_sell_in_goes_negative(self):
        item = make_item("+5 Dexterity Vest", sell_in=1, quality=20)
        update([item], days=3)
        assert item.sell_in == -2


# ---------------------------------------------------------------------------
# Aged Brie
# ---------------------------------------------------------------------------

class TestAgedBrie:

    def test_sell_in_decreases_by_one(self):
        item = make_item("Aged Brie", sell_in=2, quality=0)
        update([item])
        assert item.sell_in == 1

    def test_quality_increases_by_one_before_sell_date(self):
        item = make_item("Aged Brie", sell_in=5, quality=10)
        update([item])
        assert item.quality == 11

    def test_quality_increases_by_two_on_sell_date(self):
        # sell_in=0 → after update sell_in=-1 (< 0), triggers extra +1
        item = make_item("Aged Brie", sell_in=0, quality=10)
        update([item])
        assert item.quality == 12

    def test_quality_increases_by_two_past_sell_date(self):
        item = make_item("Aged Brie", sell_in=-1, quality=10)
        update([item])
        assert item.quality == 12

    def test_quality_never_exceeds_50(self):
        item = make_item("Aged Brie", sell_in=5, quality=50)
        update([item])
        assert item.quality == 50

    def test_quality_at_49_caps_at_50(self):
        item = make_item("Aged Brie", sell_in=5, quality=49)
        update([item])
        assert item.quality == 50

    def test_quality_cap_past_sell_date_at_49(self):
        # Would want to increase by 2 but capped at 50
        item = make_item("Aged Brie", sell_in=-1, quality=49)
        update([item])
        assert item.quality == 50

    def test_quality_cap_past_sell_date_at_50(self):
        item = make_item("Aged Brie", sell_in=-1, quality=50)
        update([item])
        assert item.quality == 50

    def test_quality_increases_from_zero(self):
        item = make_item("Aged Brie", sell_in=2, quality=0)
        update([item])
        assert item.quality == 1

    def test_quality_over_multiple_days(self):
        item = make_item("Aged Brie", sell_in=3, quality=0)
        update([item], days=3)
        # day 1: q=1, si=2
        # day 2: q=2, si=1
        # day 3: q=3, si=0
        assert item.quality == 3

    def test_quality_increases_faster_after_sell_date_over_multiple_days(self):
        item = make_item("Aged Brie", sell_in=1, quality=0)
        update([item], days=3)
        # day 1: q=1,  si=0
        # day 2: q=3,  si=-1  (double: sell_in < 0)
        # day 3: q=5,  si=-2
        assert item.quality == 5

    def test_quality_does_not_exceed_50_over_many_days(self):
        item = make_item("Aged Brie", sell_in=1, quality=40)
        update([item], days=20)
        assert item.quality == 50


# ---------------------------------------------------------------------------
# Sulfuras, Hand of Ragnaros
# ---------------------------------------------------------------------------

class TestSulfuras:

    def test_quality_never_changes(self):
        item = make_item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)
        update([item])
        assert item.quality == 80

    def test_sell_in_never_changes(self):
        item = make_item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)
        update([item])
        assert item.sell_in == 0

    def test_sell_in_stays_at_negative_one(self):
        item = make_item("Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80)
        update([item])
        assert item.sell_in == -1

    def test_quality_stays_at_80_with_negative_sell_in(self):
        item = make_item("Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80)
        update([item])
        assert item.quality == 80

    def test_unchanged_over_many_days(self):
        item = make_item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)
        update([item], days=100)
        assert item.sell_in == 0
        assert item.quality == 80

    def test_positive_sell_in_never_changes(self):
        item = make_item("Sulfuras, Hand of Ragnaros", sell_in=10, quality=80)
        update([item])
        assert item.sell_in == 10
        assert item.quality == 80


# ---------------------------------------------------------------------------
# Backstage passes to a TAFKAL80ETC concert
# ---------------------------------------------------------------------------

PASS = "Backstage passes to a TAFKAL80ETC concert"


class TestBackstagePasses:

    # sell_in decrements normally
    def test_sell_in_decreases_by_one(self):
        item = make_item(PASS, sell_in=15, quality=20)
        update([item])
        assert item.sell_in == 14

    # sell_in > 10: quality +1
    def test_quality_increases_by_one_when_more_than_10_days(self):
        item = make_item(PASS, sell_in=15, quality=20)
        update([item])
        assert item.quality == 21

    def test_quality_increases_by_one_at_sell_in_11(self):
        item = make_item(PASS, sell_in=11, quality=20)
        update([item])
        assert item.quality == 21

    # sell_in <= 10 (≥ 6): quality +2
    def test_quality_increases_by_two_at_sell_in_10(self):
        item = make_item(PASS, sell_in=10, quality=20)
        update([item])
        assert item.quality == 22

    def test_quality_increases_by_two_at_sell_in_9(self):
        item = make_item(PASS, sell_in=9, quality=20)
        update([item])
        assert item.quality == 22

    def test_quality_increases_by_two_at_sell_in_6(self):
        item = make_item(PASS, sell_in=6, quality=20)
        update([item])
        assert item.quality == 22

    # sell_in <= 5 (≥ 1): quality +3
    def test_quality_increases_by_three_at_sell_in_5(self):
        item = make_item(PASS, sell_in=5, quality=20)
        update([item])
        assert item.quality == 23

    def test_quality_increases_by_three_at_sell_in_3(self):
        item = make_item(PASS, sell_in=3, quality=20)
        update([item])
        assert item.quality == 23

    def test_quality_increases_by_three_at_sell_in_1(self):
        item = make_item(PASS, sell_in=1, quality=20)
        update([item])
        assert item.quality == 23

    # Concert day (sell_in=0): quality drops to 0 after update
    def test_quality_drops_to_zero_when_concert_day(self):
        # sell_in=0 means "concert is today"; after update sell_in=-1 → quality=0
        item = make_item(PASS, sell_in=0, quality=20)
        update([item])
        assert item.quality == 0

    def test_quality_stays_at_zero_past_concert(self):
        item = make_item(PASS, sell_in=-1, quality=0)
        update([item])
        assert item.quality == 0

    # Quality cap at 50
    def test_quality_never_exceeds_50_below_10_days(self):
        item = make_item(PASS, sell_in=10, quality=49)
        update([item])
        assert item.quality == 50

    def test_quality_never_exceeds_50_at_50_below_10_days(self):
        item = make_item(PASS, sell_in=10, quality=50)
        update([item])
        assert item.quality == 50

    def test_quality_never_exceeds_50_below_5_days(self):
        item = make_item(PASS, sell_in=5, quality=49)
        update([item])
        assert item.quality == 50

    def test_quality_at_48_capped_when_5_days_remain(self):
        item = make_item(PASS, sell_in=5, quality=48)
        update([item])
        assert item.quality == 50  # would want +3 but capped at 50

    def test_quality_never_exceeds_50_far_from_concert(self):
        item = make_item(PASS, sell_in=20, quality=50)
        update([item])
        assert item.quality == 50

    # Multi-day scenarios
    def test_quality_progression_from_far_to_near(self):
        item = make_item(PASS, sell_in=13, quality=10)
        update([item], days=3)
        # day 1: sell_in=13 → +1, si=12, q=11
        # day 2: sell_in=12 → +1, si=11, q=12
        # day 3: sell_in=11 → sell_in < 11? NO → +1, si=10, q=13
        # The bonus triggers when sell_in < 11 (i.e., 10 or less) at time of check
        assert item.sell_in == 10
        assert item.quality == 13

    def test_quality_drops_to_zero_after_concert_multi_day(self):
        item = make_item(PASS, sell_in=2, quality=15)
        update([item], days=3)
        # day 1: si=1, q=18  (+3)
        # day 2: si=0, q=21  (+3)
        # day 3: si=-1, q=0  (concert passed)
        assert item.quality == 0

    def test_sell_in_boundary_between_plus1_and_plus2(self):
        """Crossing from sell_in=11 to sell_in=10 changes the increment."""
        item_a = make_item(PASS, sell_in=11, quality=20)
        item_b = make_item(PASS, sell_in=10, quality=20)
        update([item_a])
        update([item_b])
        assert item_a.quality == 21   # +1
        assert item_b.quality == 22   # +2

    def test_sell_in_boundary_between_plus2_and_plus3(self):
        """Crossing from sell_in=6 to sell_in=5 changes the increment."""
        item_a = make_item(PASS, sell_in=6, quality=20)
        item_b = make_item(PASS, sell_in=5, quality=20)
        update([item_a])
        update([item_b])
        assert item_a.quality == 22   # +2
        assert item_b.quality == 23   # +3


# ---------------------------------------------------------------------------
# Conjured items  (NOTE: not yet implemented in the current code)
# ---------------------------------------------------------------------------

class TestConjured:
    """
    These tests document the EXPECTED behaviour for Conjured items
    as described in the requirements. They will FAIL against the current
    implementation because conjured logic has not yet been added.
    Mark with pytest.mark.xfail to record the gap without breaking CI.
    """

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_quality_degrades_by_two_before_sell_date(self):
        item = make_item("Conjured Mana Cake", sell_in=5, quality=10)
        update([item])
        assert item.quality == 8   # degrades twice as fast as normal

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_quality_degrades_by_four_past_sell_date(self):
        item = make_item("Conjured Mana Cake", sell_in=-1, quality=10)
        update([item])
        assert item.quality == 6   # twice as fast, doubled after sell date

    def test_quality_never_goes_below_zero(self):
        # Even with double degradation, quality must not go negative.
        # With quality=1 before sell date the current code degrades by 1 → 0.
        # Once Conjured is implemented (degrade by 2), it should also clamp to 0.
        item = make_item("Conjured Mana Cake", sell_in=5, quality=1)
        update([item])
        assert item.quality == 0

    def test_sell_in_decreases_by_one(self):
        # Conjured items are still normal goods; sell_in decrements daily.
        item = make_item("Conjured Mana Cake", sell_in=3, quality=6)
        update([item])
        assert item.sell_in == 2

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_quality_clamps_at_zero_past_sell_date_low_quality(self):
        item = make_item("Conjured Mana Cake", sell_in=0, quality=3)
        update([item])
        assert item.quality == 0   # would degrade by 4, clamped at 0

    # --- Variações de quality inicial antes do vencimento ---

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_quality_at_3_decreases_to_1(self):
        # quality=3, degrade -2 → 1 (não -1 → 2)
        item = make_item("Conjured Mana Cake", sell_in=5, quality=3)
        update([item])
        assert item.quality == 1

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_quality_at_2_clamps_at_zero(self):
        # quality=2, degrade -2 → 0 (não -1 → 1)
        item = make_item("Conjured Mana Cake", sell_in=5, quality=2)
        update([item])
        assert item.quality == 0

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_quality_at_50_decreases_to_48(self):
        # quality máxima degrada -2 por dia
        item = make_item("Conjured Mana Cake", sell_in=10, quality=50)
        update([item])
        assert item.quality == 48

    # --- Último dia antes do vencimento (sell_in=1) ---

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_quality_degrades_by_two_at_last_sell_day(self):
        # sell_in=1: ainda não venceu, mas -2 já deve ser aplicado
        item = make_item("Conjured Mana Cake", sell_in=1, quality=10)
        update([item])
        assert item.quality == 8

    # --- sell_in exatamente no vencimento (sell_in=0) ---

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_quality_degrades_by_four_on_sell_date(self):
        # sell_in=0 → depois do update sell_in=-1 → degradação dupla = -4
        item = make_item("Conjured Mana Cake", sell_in=0, quality=20)
        update([item])
        assert item.quality == 16

    # --- Simulações multi-dia ---

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_quality_over_three_days_before_sell_date(self):
        # 3 dias com sell_in positivo: -2/dia → 10 - 6 = 4
        item = make_item("Conjured Mana Cake", sell_in=5, quality=10)
        update([item], days=3)
        assert item.quality == 4

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_quality_crossing_sell_date(self):
        # sell_in=2, quality=12
        # dia 1: si=1, q=10  (-2)
        # dia 2: si=0, q=8   (-2)
        # dia 3: si=-1, q=4  (-4, passou do vencimento)
        item = make_item("Conjured Mana Cake", sell_in=2, quality=12)
        update([item], days=3)
        assert item.quality == 4

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_quality_reaches_zero_faster_than_normal(self):
        # Com degradação -2/dia, quality=8 some em 4 dias (antes do vencimento).
        # O código atual (-1/dia) ainda teria quality=4 nesse ponto.
        item = make_item("Conjured Mana Cake", sell_in=10, quality=8)
        update([item], days=4)
        assert item.quality == 0   # atual: 8-4=4, esperado: 8-(4×2)=0

    # --- Comparação direta com item normal ---

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_degrades_twice_as_fast_as_normal_item(self):
        # Mesmos parâmetros: Conjured deve ter metade da quality do normal após 1 dia
        normal = make_item("Elixir of the Mongoose", sell_in=5, quality=10)
        conjured = make_item("Conjured Mana Cake", sell_in=5, quality=10)
        update([normal])
        update([conjured])
        # normal: 10-1=9 | conjured: 10-2=8
        assert conjured.quality == normal.quality - 1  # conjured perde 1 a mais

    @pytest.mark.xfail(reason="Conjured items not yet implemented", strict=True)
    def test_degrades_twice_as_fast_past_sell_date_vs_normal(self):
        # Pós-vencimento: normal -2/dia, conjured -4/dia
        normal = make_item("Elixir of the Mongoose", sell_in=-1, quality=20)
        conjured = make_item("Conjured Mana Cake", sell_in=-1, quality=20)
        update([normal])
        update([conjured])
        # normal: 20-2=18 | conjured: 20-4=16
        assert conjured.quality == normal.quality - 2  # conjured perde 2 a mais


# ---------------------------------------------------------------------------
# Ambiguidades de requisito — casos onde duas ou mais regras se intersectam
# sem resolução explícita na especificação.
#
# Usamos Decision Tables para identificar as lacunas:
#   pytest.mark.skip  → genuinamente ambíguo: múltiplas respostas válidas,
#                        cliente precisa decidir antes de implementar
#   pytest.mark.xfail → comportamento esperado claro, mas não implementado
# ---------------------------------------------------------------------------

# --- Aged Brie após o vencimento --------------------------------------------
# A implementação atual escolheu q+2 (ambas as regras se acumulam),
# já coberta em TestAgedBrie. As 3 alternativas abaixo estão em aberto.

class TestAgedBrieAmbiguity:
    """
    Interpretações alternativas para Aged Brie após vencimento.
    Implementação atual: q' = q+2. As outras possibilidades estão abaixo como skip.
    """

    @pytest.mark.skip(reason=(
        "AMBIGUIDADE: regra do Brie sobrescreve vencimento? "
        "Interpretação: q'=q+1. Requer decisão do cliente."
    ))
    def test_brie_overrides_sell_date_rule(self):
        item = make_item("Aged Brie", sell_in=-1, quality=10)
        update([item])
        assert item.quality == 11

    @pytest.mark.skip(reason=(
        "AMBIGUIDADE: vencimento sobrescreve regra do Brie? "
        "Interpretação: q'=q-2. Requer decisão do cliente."
    ))
    def test_sell_date_overrides_brie_rule(self):
        item = make_item("Aged Brie", sell_in=-1, quality=10)
        update([item])
        assert item.quality == 8

    @pytest.mark.skip(reason=(
        "AMBIGUIDADE: 'degrada um passo mais rápido' aplicado à direção oposta? "
        "Interpretação: q'=q (efeitos se cancelam). Requer decisão do cliente."
    ))
    def test_effects_cancel_each_other(self):
        item = make_item("Aged Brie", sell_in=-1, quality=10)
        update([item])
        assert item.quality == 10


# --- Conjured + Backstage pass -----------------------------------------------
# Combinar 'conjured' com Backstage pass abre múltiplas ambiguidades.
# O código atual trata "Conjured Backstage passes..." como item normal
# (nome não coincide exatamente com o pass).

CONJURED_PASS = "Conjured Backstage passes to a TAFKAL80ETC concert"


class TestConjuredBackstagePass:
    """
    Ambiguidades de ingresso conjurado: ganho por faixa de dias indefinido.
    Apenas o colapso após o show é inequívoco (xfail).
    """

    @pytest.mark.skip(reason=(
        "AMBIGUIDADE: ingresso conjurado com >10 dias — ainda ganha quality? "
        "Possibilidades: q+1 (bônus normal), q-2 (apenas conjurado), q-1 (conjurado "
        "dimina o ganho), q'=0 (ingresso falso não tem valor). Requer decisão do cliente."
    ))
    def test_conjured_pass_gains_quality_above_10_days(self):
        item = make_item(CONJURED_PASS, sell_in=15, quality=20)
        update([item])
        assert item.quality == 21  # ganho normal — uma das interpretações

    @pytest.mark.skip(reason=(
        "AMBIGUIDADE: ingresso conjurado 5-9 dias — bônus +2 se aplica? "
        "Possibilidades: q+2, q-2, q-4, q+1 (metade do bônus), etc. "
        "Requer decisão do cliente."
    ))
    def test_conjured_pass_5_to_9_days(self):
        item = make_item(CONJURED_PASS, sell_in=7, quality=20)
        update([item])
        assert item.quality == 22  # bônus normal — uma das interpretações

    @pytest.mark.skip(reason=(
        "AMBIGUIDADE: ingresso conjurado 0-4 dias — bônus +3 se aplica? "
        "Possibilidades: q+3, q-2, q-4, etc. Requer decisão do cliente."
    ))
    def test_conjured_pass_0_to_4_days(self):
        item = make_item(CONJURED_PASS, sell_in=3, quality=20)
        update([item])
        assert item.quality == 23  # bônus normal — uma das interpretações

    @pytest.mark.xfail(reason=(
        "Conjured não implementado + nome não coincide com Backstage pass. "
        "Após o show quality DEVE ser 0 — única interpretação razoável. "
        "Atualmente tratado como item normal: quality sofre degradação dupla mas não zera."
    ), strict=True)
    def test_conjured_pass_drops_to_zero_after_concert(self):
        item = make_item(CONJURED_PASS, sell_in=0, quality=20)
        update([item])
        assert item.quality == 0


# --- Conjured + Aged Brie ----------------------------------------------------
# Cruzar 'conjured' com Brie cria pelo menos 3 regras intersectando
# (brie +1, vencimento ×2, conjured ×2). Sem resolução explícita na spec.

CONJURED_BRIE = "Conjured Aged Brie"


class TestConjuredAgedBrie:
    """
    Ambiguidades de Aged Brie conjurado.
    Antes do vencimento: ganha ou perde quality? A que taxa?
    Após o vencimento: três regras em conflito sem resolução.
    """

    @pytest.mark.skip(reason=(
        "AMBIGUIDADE: Brie conjurado antes do vencimento — ganha ou perde quality? "
        "Possibilidades: q+1 (brie domina), q-2 (conjurado domina), q-1 (conjurado "
        "anula o ganho), q+2 (brie conjurado ganha duas vezes mais). "
        "Requer decisão do cliente."
    ))
    def test_conjured_brie_before_sell_date(self):
        item = make_item(CONJURED_BRIE, sell_in=5, quality=10)
        update([item])
        assert item.quality == 9  # conjurado anula ganho — uma das interpretações

    @pytest.mark.skip(reason=(
        "AMBIGUIDADE: Brie conjurado após vencimento — 3 regras em conflito: "
        "brie aumenta, vencimento dobra degradação, conjurado dobra degradação. "
        "Possibilidades: q+4, q+2, q+0, q-2, q-4, q-8, etc. "
        "Requer decisão do cliente."
    ))
    def test_conjured_brie_past_sell_date(self):
        item = make_item(CONJURED_BRIE, sell_in=-1, quality=10)
        update([item])
        # Sem asserção: qualquer valor seria uma escolha arbitrária de interpretação
        pass


# --- Conjured Misc após vencimento: multiplicar vs agregar ------------------
# Duas leituras válidas da spec para item vencido conjurado.

class TestConjuredPastSellDateInterpretations:
    """
    Duas interpretações para item Conjured após o vencimento:

    A — penalidades multiplicam: q' = q-4
        "conjured" = 2× mais rápido; "overdue" = 2× mais rápido → 2×2 = -4.
        Coberta pelo xfail existente (test_quality_degrades_by_four_past_sell_date).

    B — penalidades se acumulam (apply-then-aggregate): q' = q-3
        "overdue" aplica -2 total; "conjured" adiciona -1 extra → q-3.
        Ambas são válidas — requer decisão explícita do cliente.
    """

    @pytest.mark.skip(reason=(
        "AMBIGUIDADE: interpretação B — penalidades agregadas: q'=q-3. "
        "Implementação planeja q'=q-4 (interpretação A). "
        "Requer decisão explícita do cliente antes de implementar."
    ))
    def test_overdue_conjured_aggregate_interpretation(self):
        # Interpretação B: -2 (overdue normal) + -1 (extra conjurado) = -3
        item = make_item("Conjured Mana Cake", sell_in=-1, quality=10)
        update([item])
        assert item.quality == 7  # q-3

    @pytest.mark.xfail(reason=(
        "Conjured não implementado. "
        "Interpretação A (penalidades multiplicam): q'=q-4. "
        "Leitura mais natural de 'twice as fast' composto com overdue."
    ), strict=True)
    def test_overdue_conjured_multiply_interpretation(self):
        # Interpretação A: (-1 normal × 2 por vencimento) × 2 por conjurado = -4
        item = make_item("Conjured Mana Cake", sell_in=-1, quality=10)
        update([item])
        assert item.quality == 6  # q-4


# ---------------------------------------------------------------------------
# Multiple items processed together
# ---------------------------------------------------------------------------

class TestMultipleItems:

    def test_items_are_processed_independently(self):
        items = [
            make_item("+5 Dexterity Vest", sell_in=10, quality=20),
            make_item("Aged Brie", sell_in=2, quality=0),
            make_item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        ]
        update(items)
        vest, brie, sulfuras = items
        assert vest.quality == 19
        assert brie.quality == 1
        assert sulfuras.quality == 80

    def test_all_item_types_together(self):
        items = [
            make_item("+5 Dexterity Vest", sell_in=10, quality=20),
            make_item("Aged Brie", sell_in=2, quality=0),
            make_item("Elixir of the Mongoose", sell_in=5, quality=7),
            make_item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            make_item("Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
            make_item(PASS, sell_in=15, quality=20),
            make_item(PASS, sell_in=10, quality=49),
            make_item(PASS, sell_in=5, quality=49),
        ]
        update(items)
        assert items[0].quality == 19   # normal -1
        assert items[1].quality == 1    # brie +1
        assert items[2].quality == 6    # normal -1
        assert items[3].quality == 80   # sulfuras unchanged
        assert items[4].quality == 80   # sulfuras unchanged
        assert items[5].quality == 21   # pass +1 (sell_in=15 > 10)
        assert items[6].quality == 50   # pass +2 but capped at 50
        assert items[7].quality == 50   # pass +3 but capped at 50

    def test_empty_items_list(self):
        gr = GildedRose([])
        gr.update_quality()   # should not raise
        assert gr.items == []

    def test_single_item_list(self):
        items = [make_item("+5 Dexterity Vest", sell_in=5, quality=5)]
        update(items)
        assert items[0].quality == 4

    def test_many_normal_items(self):
        items = [make_item("Widget", sell_in=10, quality=10) for _ in range(100)]
        update(items)
        for item in items:
            assert item.quality == 9


# ---------------------------------------------------------------------------
# Quality boundary / invariant tests
# ---------------------------------------------------------------------------

class TestQualityBoundaries:

    def test_quality_maximum_is_50_for_normal_item(self):
        # Normal items start at max; should only decrease, never exceed 50
        item = make_item("Widget", sell_in=5, quality=50)
        update([item])
        assert item.quality == 49
        assert item.quality <= 50

    def test_quality_minimum_is_zero_for_normal_item(self):
        item = make_item("Widget", sell_in=5, quality=0)
        update([item])
        assert item.quality == 0
        assert item.quality >= 0

    def test_quality_can_start_at_zero(self):
        item = make_item("Widget", sell_in=5, quality=0)
        gr = GildedRose([item])
        gr.update_quality()
        assert item.quality >= 0

    def test_sell_in_can_go_deeply_negative(self):
        item = make_item("Widget", sell_in=1, quality=50)
        update([item], days=100)
        assert item.quality == 0
        assert item.sell_in == -99


# ---------------------------------------------------------------------------
# Item class tests
# ---------------------------------------------------------------------------

class TestItemClass:

    def test_item_repr(self):
        item = Item("Test Item", 10, 20)
        assert repr(item) == "Test Item, 10, 20"

    def test_item_stores_name(self):
        item = Item("Foo", 1, 1)
        assert item.name == "Foo"

    def test_item_stores_sell_in(self):
        item = Item("Foo", 7, 1)
        assert item.sell_in == 7

    def test_item_stores_quality(self):
        item = Item("Foo", 1, 42)
        assert item.quality == 42

    def test_gilded_rose_stores_items(self):
        items = [Item("Foo", 1, 1)]
        gr = GildedRose(items)
        assert gr.items is items
