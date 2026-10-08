# Laboratório Avaliado 3 — Projeto e Análise de Algoritmos I

**Tópicos:** Algoritmo de Dijkstra · Fila de Prioridade (Heap) · Reconstrução de Caminhos · Expansão do Espaço de Estados

---

## Contexto do Problema: os Buracos do Anel Viário

Quem chega ao Instituto de Informática pelo anel viário do Campus do Vale conhece bem o problema: a pista está cheia de buracos.

O anel é uma única estrada, mas isso não significa que exista um único caminho. Dependendo da **posição em que o carro navega dentro da pista**, ele acerta ou desvia de cada buraco. O anel tem **mão única (sentido horário)**: da entrada do campus, o carro sobe pela pista oeste, ao lado dos Setores 6 e 7, e percorre cerca de **800 m** até o INF (Bloco IV).

Para modelar isso, a pista foi discretizada em pontos:

- ao longo do anel há **estações** a cada ~2 m;
- em cada estação há **7 posições laterais**, a cada 1 m, da borda interna à borda externa da pista;
- de um ponto, o carro só pode ir para a **estação seguinte** (mão única), **mantendo a posição lateral ou desviando uma posição** para um dos lados. Portanto, o grafo é **dirigido**;
- o peso de cada aresta é a distância real percorrida, em centímetros. Desviar custa um pouco mais do que seguir reto, e o lado interno das curvas é mais curto que o externo.

```
     estação i            estação i+1

                          (i+1, j-1)
                        ↗
     (i, j)  ─────────▶   (i+1, j)
                        ↘
                          (i+1, j+1)
```

Alguns pontos têm **buracos**. O objetivo é sair da **entrada do campus** e chegar ao **INF** percorrendo a menor distância possível, **passando por no máximo 3 buracos**.

---

## Instruções

1. Faça o clone deste repositório:
   ```bash
   git clone https://github.com/PAA1/lab3-26-2.git
   cd lab3-26-2
   ```

2. Abra o arquivo `lab3.py` e complete as funções indicadas com `# TODO`.

3. Em cada função a ser implementada, **preencha a linha de complexidade assintótica**:
   ```python
   # Complexidade: O( )
   ```
   Utilize $n$ para o número de vértices ($|V|$), $m$ para o número de arestas ($|E|$) e $k$ para o número máximo de buracos.

4. Teste sua solução executando:
   ```bash
   python3 lab3.py
   ```
   Um `✓ OK` indica que o teste passou. Um `✗ FALHOU` indica erro.

5. **Visualização do Anel Viário:**
   Ao implementar as duas funções exigidas, o script executará a solução na pista do anel viário (~9.100 pontos, ~24.700 arestas e ~690 buracos) e gerará o arquivo:
   ```
   resultado_lab3.html
   ```
   Abra este arquivo em um navegador para comparar a rota que ignora os buracos com a rota que atinge no máximo $k$ buracos. Use o controle de $k$ para ver como a rota muda e a roda do mouse para aproximar a pista.

6. Ao terminar, **entregue o arquivo `lab3.py`** pela tarefa correspondente no Moodle.

---

## Visão Geral das Partes

| Parte | Função | Descrição |
|-------|--------|-----------|
| 1 | `dijkstra_caminho` | **A implementar.** Algoritmo de Dijkstra com fila de prioridade (`heapq`) e registro de antecessores (`parent`) para obter o caminho de menor custo. |
| 2 | `dijkstra_buracos` | **A implementar.** Adaptação do algoritmo de Dijkstra para encontrar o caminho de menor custo que passa por **no máximo $k$ vértices com buraco**. |
| Aux | `carregar_anel`, `construir_grafo` | *Já fornecidas.* Leem o arquivo da pista e constroem a lista de adjacência no formato `dict[vértice, list[tuple[vizinho, distância]]]`. |
| Aux | `contar_buracos` | *Já fornecida.* Conta quantos buracos um caminho atinge (a origem não conta). |
| Aux | `analise_anel` | *Já fornecida.* Integra as funções implementadas para comparar as duas rotas. |

---

## Dicas de Implementação

- **Fila de prioridade:** utilize o módulo `heapq` da biblioteca padrão, como na Aula 18:
  ```python
  import heapq
  heap = [(0, origem)]
  d, u = heapq.heappop(heap)        # extrai o par de menor distância
  heapq.heappush(heap, (novo, v))   # insere um novo par
  ```
  Um vértice pode aparecer no heap mais de uma vez. Ao extrair um par de um vértice já processado, descarte-o.

- **Reconstrução de caminho:** sempre que a distância de `v` melhorar através de `u`, registre `parent[v] = u`. Ao final, retroceda a partir do destino até a origem e inverta a lista, como no Laboratório 2.

- **Parte 2: por que `dist[v]` não basta?** No grafo `G_ARMADILHA` do arquivo, o caminho mais curto até `M` passa pelo buraco `H1`. Com $k = 1$, quem chega a `M` por ele não pode mais passar por `H2`, que é obrigatório para chegar a `T`. O caminho correto chega a `M` pela aresta mais longa, sem buracos. Ou seja, para cada vértice importa **quanto custou** chegar nele e também **quantos buracos** já foram atingidos.

- **Parte 2: espaço de estados.** Execute o algoritmo de Dijkstra sobre **estados** `(v, b)`, onde `b` é o número de buracos atingidos até chegar em `v`. As distâncias, os antecessores e o controle de processados passam a ser indexados pelo estado, e o heap guarda triplas `(dist, v, b)`. É a mesma ideia do problema clássico do *voo mais barato com no máximo $k$ escalas*.

---

## Observações

- Não utilize bibliotecas externas (como `networkx` ou `numpy`). Utilize apenas a biblioteca padrão do Python.
- Não altere as assinaturas das funções nem os blocos de teste.
- As justificativas de complexidade devem ser expressas em termos de $n$ (vértices), $m$ (arestas) e $k$ (máximo de buracos).
