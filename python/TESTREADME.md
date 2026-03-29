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
| Item normal | `quality` −1/dia; −2/dia após `sell_in < 0`. Nunca negativa. |
| **Aged Brie** | `quality` +1/dia; +2/dia após `sell_in < 0`. Máximo 50. |
| **Sulfuras, Hand of Ragnaros** | `sell_in` e `quality` nunca mudam. `quality` = 80 fixo. |
| **Backstage passes** | +1 com `sell_in > 10`; +2 com `sell_in ≤ 10`; +3 com `sell_in ≤ 5`; `quality = 0` após o show. |

> **Nota sobre a degradação dupla:** a verificação `sell_in < 0` ocorre *após* o decremento do dia. Portanto, quando `sell_in` era `0` antes da atualização, ao final do dia `sell_in` vira `−1` e a regra pós-prazo é aplicada.

---

## Estratégia de teste: Cobertura de Decisões (Edge Coverage)

Os testes foram derivados a partir do **grafo de fluxo de controle (CFG)** do método `update_quality()`. Cada nó do grafo corresponde a uma linha ou bloco do código; cada aresta corresponde a uma transição entre decisões (verdadeiro/falso de cada `if`).

A suite cobre **100% das arestas do grafo**, garantindo que toda decisão do código é exercitada em ambas as direções (Cobertura de Decisões).

O total de casos necessários para essa cobertura é **16 (CT1–CT16)**.

---

## Arquivo de testes

**[test_gilded_rose.py](test_gilded_rose.py)**

### Função auxiliar

```python
def update(name, sell_in, quality):
    item = Item(name, sell_in, quality)
    GildedRose([item]).update_quality()
    return item
```

Cria um item, executa um dia de atualização e retorna o item com os valores finais.

---

## Casos de Teste (CT1–CT16)

### Itens Normais

| CT | `sell_in` | `quality` | Arestas cobertas | `sell_in` esperado | `quality` esperada |
|---|---|---|---|---|---|
| **CT1** | 10 | 20 | `quality > 0` ✓, não Sulfuras ✓, `sell_in < 0` ✗ | 9 | 19 |
| **CT2** | 10 | 0  | `quality > 0` ✗, `sell_in < 0` ✗ | 9 | 0  |
| **CT12** | 0 | 10 | `sell_in < 0` ✓, não Backstage ✓, `quality > 0` ✓, não Sulfuras ✓ | −1 | 8  |
| **CT13** | 0 | 0  | `sell_in < 0` ✓, não Backstage ✓, `quality > 0` ✗ | −1 | 0  |

### Sulfuras, Hand of Ragnaros

| CT | `sell_in` | `quality` | Arestas cobertas | `sell_in` esperado | `quality` esperada |
|---|---|---|---|---|---|
| **CT3** | 5  | 80 | não Sulfuras (L12) ✗, não Sulfuras (L24) ✗, `sell_in < 0` ✗ | 5  | 80 |
| **CT4** | −1 | 80 | `sell_in < 0` ✓, não Backstage ✓, `quality > 0` ✓, não Sulfuras (L30) ✗ | −1 | 80 |

### Aged Brie

| CT | `sell_in` | `quality` | Arestas cobertas | `sell_in` esperado | `quality` esperada |
|---|---|---|---|---|---|
| **CT5**  | 5 | 10 | `quality < 50` (L15) ✓, não Backstage ✗, `sell_in < 0` ✗ | 4  | 11 |
| **CT6**  | 5 | 50 | `quality < 50` (L15) ✗, `sell_in < 0` ✗ | 4  | 50 |
| **CT15** | 0 | 10 | `sell_in < 0` ✓, não Aged Brie ✗, `quality < 50` (L35) ✓ | −1 | 12 |
| **CT16** | 0 | 50 | `sell_in < 0` ✓, não Aged Brie ✗, `quality < 50` (L35) ✗ | −1 | 50 |

### Backstage passes to a TAFKAL80ETC concert

| CT | `sell_in` | `quality` | Arestas cobertas | `sell_in` esperado | `quality` esperada |
|---|---|---|---|---|---|
| **CT7**  | 15 | 20 | `sell_in < 11` ✗, `sell_in < 6` ✗ | 14 | 21 |
| **CT8**  | 10 | 20 | `sell_in < 11` ✓, `quality < 50` (L19) ✓, `sell_in < 6` ✗ | 9  | 22 |
| **CT9**  | 5  | 20 | `sell_in < 11` ✓, `quality < 50` (L19) ✓, `sell_in < 6` ✓, `quality < 50` (L22) ✓ | 4  | 23 |
| **CT10** | 10 | 49 | `sell_in < 11` ✓, `quality < 50` (L19) ✗, `sell_in < 6` ✗ | 9  | 50 |
| **CT11** | 5  | 49 | `sell_in < 11` ✓, `quality < 50` (L19) ✗, `sell_in < 6` ✓, `quality < 50` (L22) ✗ | 4  | 50 |
| **CT14** | 0  | 20 | `sell_in < 0` ✓, não Backstage (L28) ✗ → `quality = 0` | −1 | 0  |

---

## Como rodar os testes

### Pré-requisito

```bash
pip install pytest
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

### Rodar um caso específico

```bash
python -m pytest test_gilded_rose.py::test_CT9_backstage_5_days_quality_plus3 -v
```

### Rodar todos os CTs de um tipo de item

```bash
# Backstage passes (CT7–CT11 e CT14)
python -m pytest test_gilded_rose.py -k "backstage" -v

# Aged Brie (CT5, CT6, CT15, CT16)
python -m pytest test_gilded_rose.py -k "aged_brie" -v

# Sulfuras (CT3, CT4)
python -m pytest test_gilded_rose.py -k "sulfuras" -v

# Normais (CT1, CT2, CT12, CT13)
python -m pytest test_gilded_rose.py -k "normal_item" -v
```

### Gerar relatório de cobertura de linha (requer `coverage`)

```bash
pip install coverage
coverage run -m pytest test_gilded_rose.py
coverage report -m
coverage html   # gera htmlcov/index.html
```

---

## Resultado esperado

```
16 passed in 0.xx s
```

Todos os 16 casos devem passar sem erros, xfails ou skips.

---

## Observações sobre o grafo

### Decisão `sell_in < 11` vs `sell_in < 6` (Backstage)
Os checks são feitos com o valor de `sell_in` **antes** do decremento. Portanto:
- `sell_in = 10` antes → entra em `< 11` → incremento extra de +1.
- `sell_in = 5` antes → entra também em `< 6` → mais um incremento de +1.

### Colapso do Backstage após o show
A zeragem da qualidade ocorre no bloco `sell_in < 0`, avaliado **após** o decremento. Logo:
- `sell_in = 0` antes → `sell_in = −1` depois → `quality = 0` (CT14).
- `sell_in = 1` antes → `sell_in = 0` depois → não colapsa, pois `0 < 0` é falso.

### Aged Brie pós-prazo aumenta 2 por dia
A lógica soma +1 no bloco principal (`quality < 50` em L15) e mais +1 no bloco pós-prazo (`quality < 50` em L35), resultando em +2 total — coberto por CT15.
