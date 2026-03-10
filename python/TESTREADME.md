# Gilded Rose — Documentação dos Testes

## O que é o Gilded Rose?

O Gilded Rose é uma kata de refatoração clássica. O sistema gerencia o inventário de uma pousada, atualizando diariamente os atributos de cada item:

- **`sell_in`** — número de dias restantes para vender o item.
- **`quality`** — valor/qualidade do item (0 a 50, exceto Sulfuras).

A lógica está concentrada no método `update_quality()` da classe `GildedRose` em [gilded_rose.py](gilded_rose.py).

---

## Regras de negócio (resumo)

| Tipo de item | Comportamento |
|---|---|
| Item normal | `quality` -1/dia; -2/dia após `sell_in < 0`. Nunca negativa. |
| **Aged Brie** | `quality` +1/dia; +2/dia após `sell_in < 0`. Máximo 50. |
| **Sulfuras, Hand of Ragnaros** | `sell_in` e `quality` nunca mudam. `quality` = 80 fixo. |
| **Backstage passes** | +1 com `sell_in > 10`; +2 com `sell_in ≤ 10`; +3 com `sell_in ≤ 5`; `quality = 0` após o show. |
| **Conjured** (não implementado) | `quality` -2/dia; -4/dia após `sell_in < 0`. |

> **Nota sobre o `sell_in` e a degradação dupla:** a verificação `sell_in < 0` ocorre *após* o decremento do dia. Portanto, quando `sell_in` era `0` antes da atualização, ao final do dia `sell_in` vira `-1` e a degradação dupla é aplicada. O dia de `sell_in = 0` já conta como prazo expirado.

---

## Arquivo de testes

**[test_gilded_rose.py](test_gilded_rose.py)**

O arquivo está organizado em 7 classes de teste:

### `TestNormalItem` — 13 casos
Testa itens genéricos como `+5 Dexterity Vest` e `Elixir of the Mongoose`.

| Caso | O que verifica |
|---|---|
| `test_sell_in_decreases_by_one` | `sell_in` reduz 1 por dia |
| `test_quality_decreases_by_one_before_sell_date` | `quality` reduz 1 antes do vencimento |
| `test_quality_decreases_by_two_on_sell_date` | degradação dupla quando `sell_in=0` (prazo hoje) |
| `test_quality_degrades_twice_as_fast_past_sell_date` | degradação dupla com `sell_in` negativo |
| `test_quality_never_goes_below_zero` | `quality` não fica negativa |
| `test_quality_never_goes_below_zero_past_sell_date` | `quality` não fica negativa pós-prazo |
| `test_quality_at_one_degrades_to_zero_not_negative` | `quality=1` vai para 0, não -1 |
| `test_quality_at_one_past_sell_date_clamps_at_zero` | clamp em 0 pós-prazo |
| `test_sell_in_decreases_correctly_over_multiple_days` | `sell_in` ao longo de vários dias |
| `test_quality_over_multiple_days_before_sell_date` | `quality` ao longo de vários dias |
| `test_quality_degradation_accelerates_after_sell_date` | aceleração após prazo em simulação multi-dia |
| `test_quality_never_below_zero_over_many_days` | invariante ao longo de 20 dias |
| `test_sell_in_goes_negative` | `sell_in` vai para valores negativos corretamente |

---

### `TestAgedBrie` — 12 casos
Testa o item especial que envelhece bem.

| Caso | O que verifica |
|---|---|
| `test_sell_in_decreases_by_one` | `sell_in` reduz normalmente |
| `test_quality_increases_by_one_before_sell_date` | +1 antes do vencimento |
| `test_quality_increases_by_two_on_sell_date` | +2 quando `sell_in=0` (prazo expira hoje) |
| `test_quality_increases_by_two_past_sell_date` | +2 com `sell_in` negativo |
| `test_quality_never_exceeds_50` | máximo 50 |
| `test_quality_at_49_caps_at_50` | 49 → 50 (cap aplicado) |
| `test_quality_cap_past_sell_date_at_49` | cap mesmo com degradação dupla pós-prazo |
| `test_quality_cap_past_sell_date_at_50` | permanece em 50 pós-prazo |
| `test_quality_increases_from_zero` | sobe mesmo começando em 0 |
| `test_quality_over_multiple_days` | progressão ao longo de 3 dias |
| `test_quality_increases_faster_after_sell_date_over_multiple_days` | simulação multi-dia com aceleração |
| `test_quality_does_not_exceed_50_over_many_days` | cap invariante ao longo de 20 dias |

---

### `TestSulfuras` — 6 casos
Testa o item lendário imutável.

| Caso | O que verifica |
|---|---|
| `test_quality_never_changes` | `quality` permanece 80 |
| `test_sell_in_never_changes` | `sell_in` não muda |
| `test_sell_in_stays_at_negative_one` | `sell_in=-1` não muda |
| `test_quality_stays_at_80_with_negative_sell_in` | `quality` 80 com `sell_in` negativo |
| `test_unchanged_over_many_days` | inalterado após 100 dias |
| `test_positive_sell_in_never_changes` | `sell_in` positivo também não muda |

---

### `TestBackstagePasses` — 20 casos
Testa as três faixas de incremento e o colapso pós-show. Cobre todos os **valores de contorno** (`sell_in = 11, 10, 6, 5, 1, 0`).

| Caso | O que verifica |
|---|---|
| `test_sell_in_decreases_by_one` | `sell_in` reduz normalmente |
| `test_quality_increases_by_one_when_more_than_10_days` | +1 com `sell_in=15` |
| `test_quality_increases_by_one_at_sell_in_11` | limite superior da faixa +1 |
| `test_quality_increases_by_two_at_sell_in_10` | fronteira: 11→10, muda para +2 |
| `test_quality_increases_by_two_at_sell_in_9` | meio da faixa +2 |
| `test_quality_increases_by_two_at_sell_in_6` | limite inferior da faixa +2 |
| `test_quality_increases_by_three_at_sell_in_5` | fronteira: 6→5, muda para +3 |
| `test_quality_increases_by_three_at_sell_in_3` | meio da faixa +3 |
| `test_quality_increases_by_three_at_sell_in_1` | último dia antes do show |
| `test_quality_drops_to_zero_when_concert_day` | show hoje (`sell_in=0`): quality cai para 0 |
| `test_quality_stays_at_zero_past_concert` | pós-show: quality permanece 0 |
| `test_quality_never_exceeds_50_below_10_days` | cap 50 na faixa +2 |
| `test_quality_never_exceeds_50_at_50_below_10_days` | já em 50 na faixa +2 |
| `test_quality_never_exceeds_50_below_5_days` | cap 50 na faixa +3 |
| `test_quality_at_48_capped_when_5_days_remain` | 48 + 3 = 51, mas clampa em 50 |
| `test_quality_never_exceeds_50_far_from_concert` | já em 50 longe do show |
| `test_quality_progression_from_far_to_near` | simulação multi-dia cruzando faixas |
| `test_quality_drops_to_zero_after_concert_multi_day` | colapso após 3 dias partindo de `sell_in=2` |
| `test_sell_in_boundary_between_plus1_and_plus2` | compara `sell_in=11` (+1) com `sell_in=10` (+2) |
| `test_sell_in_boundary_between_plus2_and_plus3` | compara `sell_in=6` (+2) com `sell_in=5` (+3) |

---

### `TestConjured` — 5 casos (3 xfail + 2 pass)
Documenta o comportamento esperado de itens Conjurados conforme a spec.
Os casos marcados `xfail` **falham propositalmente** pois a funcionalidade ainda não foi implementada. Quando implementada, basta remover o `@pytest.mark.xfail`.

| Caso | Status | O que verifica |
|---|---|---|
| `test_quality_degrades_by_two_before_sell_date` | **xfail** | -2/dia (atualmente só -1) |
| `test_quality_degrades_by_four_past_sell_date` | **xfail** | -4/dia pós-prazo (atualmente só -2) |
| `test_quality_never_goes_below_zero` | pass | `quality` não fica negativa (comportamento já correto) |
| `test_sell_in_decreases_by_one` | pass | `sell_in` reduz normalmente (já correto) |
| `test_quality_clamps_at_zero_past_sell_date_low_quality` | **xfail** | clamp em 0 com degradação de -4 pós-prazo |

---

### `TestMultipleItems` — 5 casos
Garante que a lista de itens é processada corretamente.

| Caso | O que verifica |
|---|---|
| `test_items_are_processed_independently` | 3 itens de tipos diferentes processados sem interferência |
| `test_all_item_types_together` | simulação completa com todos os tipos |
| `test_empty_items_list` | lista vazia não lança exceção |
| `test_single_item_list` | lista com 1 item funciona |
| `test_many_normal_items` | 100 itens iguais processados corretamente |

---

### `TestQualityBoundaries` — 4 casos
Valida os invariantes globais de `quality`.

| Caso | O que verifica |
|---|---|
| `test_quality_maximum_is_50_for_normal_item` | parte de 50, reduz (não excede 50) |
| `test_quality_minimum_is_zero_for_normal_item` | parte de 0, não fica negativa |
| `test_quality_can_start_at_zero` | sem erro ao começar com quality=0 |
| `test_sell_in_can_go_deeply_negative` | `sell_in` e `quality` corretos após 100 dias |

---

### `TestItemClass` — 5 casos
Valida a classe `Item` em si.

| Caso | O que verifica |
|---|---|
| `test_item_repr` | `__repr__` retorna o formato correto |
| `test_item_stores_name` | atributo `name` armazenado |
| `test_item_stores_sell_in` | atributo `sell_in` armazenado |
| `test_item_stores_quality` | atributo `quality` armazenado |
| `test_gilded_rose_stores_items` | `GildedRose.items` referencia a lista original |

---

## Resumo dos resultados esperados

```
70 testes coletados
67 passam    (comportamento atual correto)
 3 xfailed   (Conjured não implementado — falha esperada e documentada)
 0 erros
```

---

## Como rodar os testes

### Pré-requisitos

```bash
pip install pytest
```

Ou instale todas as dependências do projeto:

```bash
pip install -r requirements.txt
```

### Executar todos os testes

```bash
cd GildedRose-Refactoring-Kata/python
python -m pytest test_gilded_rose.py
```

### Saída verbosa (ver nome de cada caso)

```bash
python -m pytest test_gilded_rose.py -v
```

### Rodar apenas uma classe

```bash
python -m pytest test_gilded_rose.py::TestBackstagePasses -v
```

### Rodar apenas um caso específico

```bash
python -m pytest test_gilded_rose.py::TestAgedBrie::test_quality_increases_by_two_on_sell_date -v
```

### Ver os xfail detalhados

```bash
python -m pytest test_gilded_rose.py -v -r xf
```

### Gerar relatório de cobertura (requer `coverage`)

```bash
pip install coverage
coverage run -m pytest test_gilded_rose.py
coverage report -m
coverage html   # gera htmlcov/index.html
```

---

## Descobertas importantes durante a análise

### 1. A verificação de `sell_in` usa o valor *antes* do decremento (para Backstage passes)
Os checks `sell_in < 11` e `sell_in < 6` são feitos **antes** de decrementar `sell_in`. Portanto:
- `sell_in=10` antes da atualização → entra na faixa `< 11` → +2.
- `sell_in=5` antes da atualização → entra na faixa `< 6` → +3.

### 2. O colapso do Backstage pass usa o valor *após* o decremento
A verificação `sell_in < 0` que zera a qualidade usa o valor **depois** do decremento. Logo:
- `sell_in=0` antes → `sell_in=-1` depois → `quality = 0`.
- `sell_in=1` antes → `sell_in=0` depois → **não** colapsa (show ainda não foi).

### 3. Conjured não está implementado
O item `Conjured Mana Cake` presente em `texttest_fixture.py` é tratado como item normal. Os testes `xfail` documentam a funcionalidade pendente.

### 4. Aged Brie com sell_in=0 aumenta 2 por dia
Por que +2? A lógica incrementa 1 no bloco principal e mais 1 no bloco de pós-prazo (`sell_in < 0` após decremento). Os testes `test_quality_increases_by_two_on_sell_date` e `test_quality_increases_by_two_past_sell_date` cobrem esse comportamento.
