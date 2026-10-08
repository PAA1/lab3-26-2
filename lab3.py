# ============================================================
# Laboratório Avaliado 3 — Projeto e Análise de Algoritmos I
# UFRGS — Instituto de Informática
# ============================================================
# Nome: ______________________________________________________
# Cartão: ____________________________________________________
# ============================================================
#
# Instruções:
#   - Complete as funções indicadas com "# TODO".
#   - As funções de leitura da pista (carregar_anel, construir_grafo),
#     a função auxiliar (contar_buracos) e a função de integração
#     (analise_anel) já são fornecidas prontas.
#   - Após cada função a ser implementada, indique a complexidade
#     no comentário marcado com "# Complexidade: O( )".
#     Use n para |V| (número de vértices), m para |E| (número de arestas)
#     e k para o número máximo de buracos permitido.
#   - Execute com: python3 lab3.py
#   - Ao implementar as funções, o script executará os testes e
#     avaliará o desempenho na pista do anel viário (~9.100 vértices),
#     gerando o arquivo "resultado_lab3.html" para inspeção visual.
#
# Regras:
#   - Não altere as assinaturas das funções nem as funções fornecidas.
#   - Utilize apenas a biblioteca padrão do Python (ex: heapq).
#     Não utilize bibliotecas externas como networkx ou numpy.
# ============================================================

import heapq
import time
import os

# Módulo visualizador auxiliar fornecido
try:
    from visualizador import gerar_visualizacao_html
except ImportError:
    gerar_visualizacao_html = None


# ============================================================
# Grafos didáticos usados nos exemplos e testes iniciais
# ============================================================
#
#  G_AULA — grafo da Aula 18:
#
#            A ----5---- D
#          1/  \4      4/  \2
#          S     \    /     E          F (isolado)
#          3\     \  /     /6
#            B ----1---- C
#
#        (arestas: S-A 1, S-B 3, A-D 5, A-C 4, B-D 4, B-C 1,
#                  C-E 6, D-E 2)
#
#  G_RUA — vértices marcados com * têm buraco:
#
#             X* ---1--- Y*
#           1/             \1
#          S ---2--- A* ---2--- T
#           2\                 /2
#             D ---2------ E
#
#  G_ARMADILHA — vértices marcados com * têm buraco:
#
#          S ---1--- H1* ---1--- M ---1--- H2* ---1--- T
#           \                   /
#            `-------5---------'
#
# ============================================================

G_AULA = {
    'S': [('A', 1), ('B', 3)],
    'A': [('S', 1), ('D', 5), ('C', 4)],
    'B': [('S', 3), ('D', 4), ('C', 1)],
    'C': [('B', 1), ('A', 4), ('E', 6)],
    'D': [('A', 5), ('B', 4), ('E', 2)],
    'E': [('D', 2), ('C', 6)],
    'F': [],
}

G_RUA = {
    'S': [('X', 1), ('A', 2), ('D', 2)],
    'X': [('S', 1), ('Y', 1)],
    'Y': [('X', 1), ('T', 1)],
    'A': [('S', 2), ('T', 2)],
    'D': [('S', 2), ('E', 2)],
    'E': [('D', 2), ('T', 2)],
    'T': [('Y', 1), ('A', 2), ('E', 2)],
}
BURACOS_RUA = {'X', 'Y', 'A'}

G_ARMADILHA = {
    'S':  [('H1', 1), ('M', 5)],
    'H1': [('S', 1), ('M', 1)],
    'M':  [('H1', 1), ('S', 5), ('H2', 1)],
    'H2': [('M', 1), ('T', 1)],
    'T':  [('H2', 1)],
}
BURACOS_ARMADILHA = {'H1', 'H2'}


# ============================================================
# Parte 1 — Dijkstra com Reconstrução do Caminho
# ============================================================

def dijkstra_caminho(grafo: dict, origem, destino) -> tuple[float, list]:
    """
    Encontra o caminho de menor custo total entre 'origem' e 'destino'
    em um grafo com pesos não-negativos, utilizando o algoritmo de Dijkstra
    com fila de prioridade (heapq), como visto na Aula 18.

    Conceito da Aula 18:
      - dist[v] guarda a menor distância conhecida de 'origem' até v.
      - O heap guarda pares (dist, v). Ao extrair um par de um vértice
        já processado, o par é obsoleto e deve ser descartado.
      - Ao relaxar uma aresta (u, v) com sucesso, registre o antecessor
        de v: parent[v] = u.
      - Para reconstruir o caminho, retroceda a partir de 'destino' pelos
        antecessores até 'origem' e inverta a lista obtida.

    Parâmetros:
        grafo   : dict mapeando vértice -> lista de pares (vizinho, peso)
        origem  : vértice de partida
        destino : vértice de chegada

    Retorna:
        tuple[float, list] : (custo, caminho)
            - custo  : soma dos pesos do caminho mínimo
                       (float('inf') se 'destino' é inalcançável)
            - caminho: lista de vértices de 'origem' até 'destino'
                       ([] se inalcançável).
                       Se origem == destino, o custo é 0 e o caminho é [origem].

    Exemplos:
        dijkstra_caminho(G_AULA, 'S', 'E') -> (8, ['S', 'A', 'D', 'E'])
        dijkstra_caminho(G_AULA, 'S', 'S') -> (0, ['S'])
        dijkstra_caminho(G_AULA, 'S', 'F') -> (inf, [])
    """
    # TODO: implemente esta função usando heapq e um dicionário de antecessores.
    return (float('inf'), [])

    # Complexidade: O( )


print("=" * 60)
print("  Parte 1 — Dijkstra com Reconstrução do Caminho")
print("=" * 60)
print()
print("dijkstra_caminho(G_AULA, 'S', 'E'):")
print("  obtido  :", dijkstra_caminho(G_AULA, 'S', 'E'))
print("  esperado: (8, ['S', 'A', 'D', 'E'])")
print()
print("dijkstra_caminho(G_RUA, 'S', 'T'):")
print("  obtido  :", dijkstra_caminho(G_RUA, 'S', 'T'))
print("  esperado: (3, ['S', 'X', 'Y', 'T'])")
print()


# ============================================================
# Parte 2 — Caminho Mínimo com no Máximo k Buracos
# ============================================================

def dijkstra_buracos(grafo: dict, buracos: set, origem, destino, k: int) -> tuple[float, list]:
    """
    Encontra o caminho de menor custo total entre 'origem' e 'destino'
    que passa por NO MÁXIMO k vértices com buraco.

    Cada vértice do caminho que pertence ao conjunto 'buracos' conta como
    um buraco atingido, exceto a própria 'origem' (o carro já está nela).

    Adapte o algoritmo de Dijkstra da Parte 1:
      - Guardar apenas dist[v] não é suficiente: chegar em v mais rápido,
        mas tendo atingido mais buracos, pode impedir que o resto do
        caminho seja feito sem ultrapassar o limite k.
      - Considere como "estado" o par (v, b): estar no vértice v tendo
        atingido b buracos até agora, com 0 <= b <= k. Execute o algoritmo
        de Dijkstra sobre esses estados.
      - Pense em: (i) qual é o estado inicial; (ii) para qual estado se vai
        ao percorrer a aresta (u, v) a partir do estado (u, b); (iii) quais
        transições devem ser descartadas; e (iv) quais estados representam
        a chegada ao destino.
      - Para reconstruir o caminho, guarde o antecessor de cada ESTADO.

    Parâmetros:
        grafo   : dict mapeando vértice -> lista de pares (vizinho, peso)
        buracos : conjunto de vértices que têm buraco
        origem  : vértice de partida
        destino : vértice de chegada
        k       : número máximo de buracos que o caminho pode atingir

    Retorna:
        tuple[float, list] : (custo, caminho)
            - custo  : soma dos pesos do melhor caminho com no máximo k buracos
                       (float('inf') se não existe tal caminho)
            - caminho: lista de vértices de 'origem' até 'destino'
                       ([] se não existe tal caminho).
                       Se origem == destino, o custo é 0 e o caminho é [origem].

    Exemplos:
        dijkstra_buracos(G_RUA, BURACOS_RUA, 'S', 'T', 0) -> (6, ['S', 'D', 'E', 'T'])
        dijkstra_buracos(G_RUA, BURACOS_RUA, 'S', 'T', 1) -> (4, ['S', 'A', 'T'])
        dijkstra_buracos(G_RUA, BURACOS_RUA, 'S', 'T', 2) -> (3, ['S', 'X', 'Y', 'T'])
    """
    inicio = (origem, 0)
    dist = {inicio: 0}
    parent = {inicio: None}
    processado = set()
    heap = [(0, origem, 0)]
 

 
    # TODO: implemente esta função adaptando o algoritmo de Dijkstra.


    return (float('inf'), [])

    # Complexidade: O( )


print("=" * 60)
print("  Parte 2 — Caminho Mínimo com no Máximo k Buracos")
print("=" * 60)
print()
for _k, _esp in [(0, "(6, ['S', 'D', 'E', 'T'])"), (1, "(4, ['S', 'A', 'T'])"),
                 (2, "(3, ['S', 'X', 'Y', 'T'])")]:
    print(f"dijkstra_buracos(G_RUA, BURACOS_RUA, 'S', 'T', {_k}):")
    print("  obtido  :", dijkstra_buracos(G_RUA, BURACOS_RUA, 'S', 'T', _k))
    print("  esperado:", _esp)
    print()


# ============================================================
# Funções Auxiliares Fornecidas
# (Não é necessário editar este bloco)
# ============================================================

def carregar_anel(caminho_arquivo: str) -> tuple[dict, set, list, int, int]:
    """
    Lê o arquivo da pista do anel viário.
    Função auxiliar fornecida.

    Formato (linhas iniciadas por '#' são comentários):
        n m origem destino
        n linhas: id x y buraco(0/1)
        m linhas: u v distancia_cm      (aresta dirigida de u para v)

    Retorna:
        tuple[coords, buracos, vias, origem, destino]:
            - coords : dict mapeando id -> (x, y) em metros, usado na visualização
            - buracos: conjunto de ids dos pontos com buraco
            - vias   : lista de tuplas (u, v, distancia_cm): deslocamento de u para v
                       (o anel tem mão única, então as arestas são dirigidas)
            - origem : id do ponto da entrada do campus
            - destino: id do ponto em frente ao INF
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        linhas = [l.split() for l in f if l.strip() and not l.startswith('#')]

    n, m, origem, destino = map(int, linhas[0])
    coords, buracos = {}, set()
    for partes in linhas[1:1 + n]:
        v = int(partes[0])
        coords[v] = (float(partes[1]), float(partes[2]))
        if partes[3] == '1':
            buracos.add(v)
    vias = [tuple(map(int, partes)) for partes in linhas[1 + n:1 + n + m]]
    return (coords, buracos, vias, origem, destino)


def construir_grafo(vertices, vias: list) -> dict:
    """
    Constrói a lista de adjacência (dirigida):
        vértice -> lista de (vizinho, distância em cm)
    """
    grafo = {v: [] for v in vertices}
    for u, v, cm in vias:
        grafo[u].append((v, cm))
    return grafo


def contar_buracos(caminho: list, buracos: set) -> int:
    """Conta os buracos atingidos ao longo de 'caminho' (a origem não conta)."""
    return sum(1 for v in caminho[1:] if v in buracos)


def analise_anel(vertices, vias: list, buracos: set, origem, destino, k: int) -> dict:
    """
    Integra as funções implementadas:
      1. caminho mais curto ignorando os buracos (Parte 1);
      2. caminho mais curto atingindo no máximo k buracos (Parte 2).
    """
    grafo = construir_grafo(vertices, vias)

    custo_livre, rota_livre = dijkstra_caminho(grafo, origem, destino)
    custo_k, rota_k = dijkstra_buracos(grafo, buracos, origem, destino, k)

    return {
        "custo_livre": custo_livre,
        "rota_livre": rota_livre,
        "buracos_livre": contar_buracos(rota_livre, buracos),
        "custo_k": custo_k,
        "rota_k": rota_k,
        "buracos_k": contar_buracos(rota_k, buracos),
    }


def _fmt_metros(cm: float) -> str:
    if cm == float('inf'):
        return "sem rota"
    return f"{cm / 100:.2f} m"


# ============================================================
# ==================== TESTES FINAIS =========================
# ============================================================

def _titulo(s):
    print(f"\n{'='*60}")
    print(f"  {s}")
    print('='*60)

def _ok(descricao, obtido, esperado):
    status = "✓ OK" if obtido == esperado else "✗ FALHOU"
    print(f"  [{status}] {descricao}")
    if obtido != esperado:
        print(f"          esperado : {esperado}")
        print(f"          obtido   : {obtido}")

def _custo_caminho(grafo, caminho):
    """Soma dos pesos de 'caminho', ou None se ele usa uma aresta inexistente."""
    total = 0
    for u, v in zip(caminho, caminho[1:]):
        pesos = [p for (w, p) in grafo[u] if w == v]
        if not pesos:
            return None
        total += min(pesos)
    return total


_titulo("Testes Finais — Parte 1 (Dijkstra com Caminho)")
_ok("dijkstra_caminho(G_AULA, 'S', 'E')", dijkstra_caminho(G_AULA, 'S', 'E'), (8, ['S', 'A', 'D', 'E']))
_ok("dijkstra_caminho(G_AULA, 'S', 'C')", dijkstra_caminho(G_AULA, 'S', 'C'), (4, ['S', 'B', 'C']))
_ok("dijkstra_caminho(G_AULA, 'E', 'B')", dijkstra_caminho(G_AULA, 'E', 'B'), (6, ['E', 'D', 'B']))
_ok("dijkstra_caminho(G_AULA, 'S', 'S') - mesmo vértice", dijkstra_caminho(G_AULA, 'S', 'S'), (0, ['S']))
_ok("dijkstra_caminho(G_AULA, 'S', 'F') - inalcançável", dijkstra_caminho(G_AULA, 'S', 'F'), (float('inf'), []))
_ok("dijkstra_caminho(G_RUA, 'S', 'T') - ignora buracos", dijkstra_caminho(G_RUA, 'S', 'T'), (3, ['S', 'X', 'Y', 'T']))


_titulo("Testes Finais — Parte 2 (no Máximo k Buracos)")
_ok("dijkstra_buracos(G_RUA, 'S', 'T', k=0)", dijkstra_buracos(G_RUA, BURACOS_RUA, 'S', 'T', 0), (6, ['S', 'D', 'E', 'T']))
_ok("dijkstra_buracos(G_RUA, 'S', 'T', k=1)", dijkstra_buracos(G_RUA, BURACOS_RUA, 'S', 'T', 1), (4, ['S', 'A', 'T']))
_ok("dijkstra_buracos(G_RUA, 'S', 'T', k=2)", dijkstra_buracos(G_RUA, BURACOS_RUA, 'S', 'T', 2), (3, ['S', 'X', 'Y', 'T']))
_ok("dijkstra_buracos(G_RUA, 'S', 'T', k=5)", dijkstra_buracos(G_RUA, BURACOS_RUA, 'S', 'T', 5), (3, ['S', 'X', 'Y', 'T']))
_ok("dijkstra_buracos(G_RUA, 'S', 'S', k=0) - mesmo vértice", dijkstra_buracos(G_RUA, BURACOS_RUA, 'S', 'S', 0), (0, ['S']))
_ok("dijkstra_buracos(G_RUA, 'X', 'T', k=1) - origem com buraco não conta",
    dijkstra_buracos(G_RUA, BURACOS_RUA, 'X', 'T', 1), (2, ['X', 'Y', 'T']))
_ok("dijkstra_buracos(G_ARMADILHA, 'S', 'T', k=1)",
    dijkstra_buracos(G_ARMADILHA, BURACOS_ARMADILHA, 'S', 'T', 1), (7, ['S', 'M', 'H2', 'T']))
_ok("dijkstra_buracos(G_ARMADILHA, 'S', 'T', k=2)",
    dijkstra_buracos(G_ARMADILHA, BURACOS_ARMADILHA, 'S', 'T', 2), (4, ['S', 'H1', 'M', 'H2', 'T']))
_ok("dijkstra_buracos(G_ARMADILHA, 'S', 'T', k=0) - sem caminho",
    dijkstra_buracos(G_ARMADILHA, BURACOS_ARMADILHA, 'S', 'T', 0), (float('inf'), []))


_titulo("Testes Finais — Integração (Rede Didática)")
VIAS_MINI = [(0, 1, 100), (1, 2, 100), (2, 3, 100), (0, 4, 150), (4, 5, 150), (5, 3, 150)]
BURACOS_MINI = {1, 2}
mini = analise_anel(range(6), VIAS_MINI, BURACOS_MINI, 0, 3, 1)
_ok("analise_anel(mini) - custo ignorando buracos", mini["custo_livre"], 300)
_ok("analise_anel(mini) - buracos ignorando buracos", mini["buracos_livre"], 2)
_ok("analise_anel(mini) - custo com no máximo 1 buraco", mini["custo_k"], 450)
_ok("analise_anel(mini) - rota com no máximo 1 buraco", mini["rota_k"], [0, 4, 5, 3])


# ============================================================
# EXECUÇÃO NO ANEL VIÁRIO (~9.100 vértices)
# ============================================================

_titulo("Execução no Anel Viário do Campus do Vale")

K_BURACOS = 3
caminho_anel = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anel_viario.txt")
if os.path.exists(caminho_anel):
    coords, buracos, vias, origem, destino = carregar_anel(caminho_anel)
    print(f"  Pista carregada: |V| = {len(coords)} pontos, |E| = {len(vias)} deslocamentos,"
          f" {len(buracos)} buracos")

    t0 = time.perf_counter()
    res = analise_anel(coords.keys(), vias, buracos, origem, destino, K_BURACOS)
    tempo_total = (time.perf_counter() - t0) * 1000

    if res["rota_livre"] or res["rota_k"]:
        grafo = construir_grafo(coords.keys(), vias)
        print(f"  Tempo de processamento: {tempo_total:.2f} ms")
        print()
        print(f"  Ignorando os buracos           : {_fmt_metros(res['custo_livre'])},"
              f" {res['buracos_livre']} buracos")
        print(f"  Com no máximo {K_BURACOS} buracos         : {_fmt_metros(res['custo_k'])},"
              f" {res['buracos_k']} buracos")

        rotas_por_k = {}
        print()
        print("  Distância mínima por limite de buracos:")
        for kk in range(0, 7):
            c, r = dijkstra_buracos(grafo, buracos, origem, destino, kk)
            rotas_por_k[kk] = (c, r)
            print(f"    k = {kk}: {_fmt_metros(c)}")
        print()

        _ok("distância ignorando os buracos", res["custo_livre"], 78927)
        _ok("distância com no máximo 3 buracos", res["custo_k"], 81639)
        _ok("rota com no máximo 3 buracos é um caminho válido de mesmo custo",
            _custo_caminho(grafo, res["rota_k"]) == res["custo_k"]
            and res["rota_k"][:1] == [origem] and res["rota_k"][-1:] == [destino], True)
        _ok("rota com no máximo 3 buracos atinge no máximo 3 buracos", res["buracos_k"] <= K_BURACOS, True)

        if gerar_visualizacao_html is not None:
            arquivo_html = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultado_lab3.html")
            gerar_visualizacao_html(
                coords=coords,
                buracos=buracos,
                origem=origem,
                destino=destino,
                rota_livre=(res["custo_livre"], res["rota_livre"]),
                rotas_por_k=rotas_por_k,
                k_padrao=K_BURACOS,
                arquivo_saida=arquivo_html
            )
            print()
            print(f"  Visualização gerada em: {arquivo_html}")
    else:
        print()
        print("  Implemente as funções das Partes 1 e 2 para executar o teste")
        print("  no anel viário e gerar a visualização correspondente.")
else:
    print(f"  Arquivo {caminho_anel} não encontrado.")
print()
