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
