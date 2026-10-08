"""
visualizador.py — Módulo de visualização para o Laboratório 3 (PAA 1).

Gera uma página HTML autossuficiente com Canvas 2D para visualização gráfica
da pista do anel viário, dos buracos e das rotas calculadas com o algoritmo
de Dijkstra (Parte 1) e com sua adaptação com limite de buracos (Parte 2).

Não requer bibliotecas externas.
"""

import json
import os


def _ler_extras(arquivo: str) -> dict:
    """
    Lê do arquivo do anel as linhas usadas apenas na visualização:
        #PISTA N W               estações e posições laterais da pista
        #RUA x1 y1 x2 y2 ...     ruas próximas (decoração)
        #PREDIO x y w h          prédios do campus (decoração)
        #ROTULO x y texto        rótulos do mapa
    """
    extras = {"pista": None, "ruas": [], "predios": [], "rotulos": []}
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.split()
            if not partes:
                continue
            if partes[0] == "#PISTA":
                extras["pista"] = (int(partes[1]), int(partes[2]))
            elif partes[0] == "#RUA":
                nums = list(map(float, partes[1:]))
                extras["ruas"].append([nums[i:i + 2] for i in range(0, len(nums), 2)])
            elif partes[0] == "#PREDIO":
                extras["predios"].append(list(map(float, partes[1:5])))
            elif partes[0] == "#ROTULO":
                extras["rotulos"].append([float(partes[1]), float(partes[2]), " ".join(partes[3:])])
    if extras["pista"] is None:
        raise ValueError("linha #PISTA não encontrada em " + arquivo)
    return extras


def gerar_visualizacao_html(
    coords: dict,
    buracos: set,
    origem: int,
    destino: int,
    rota_livre: tuple,
    rotas_por_k: dict,
    k_padrao: int = 3,
    arquivo_saida: str = "resultado_lab3.html",
    titulo: str = "Laboratório 3 — Anel Viário do Campus do Vale"
) -> str:
    """
    Gera um arquivo HTML com visualizador Canvas 2D.

    Parâmetros:
        coords        : dict mapeando id do ponto -> (x, y) em metros
        buracos       : conjunto de ids dos pontos com buraco
        origem        : id do ponto da entrada do campus
        destino       : id do ponto em frente ao INF
        rota_livre    : (custo_cm, caminho) da Parte 1 (ignorando buracos)
        rotas_por_k   : dict k -> (custo_cm, caminho) da Parte 2
        k_padrao      : valor de k exibido inicialmente
        arquivo_saida : nome do arquivo HTML a ser salvo
        titulo        : título exibido no cabeçalho da página
    """
    extras = _ler_extras(os.path.join(os.path.dirname(os.path.abspath(__file__)), "anel_viario.txt"))
    n_est, n_lat = extras["pista"]

    pts = [[round(coords[v][0], 2), round(coords[v][1], 2)] for v in range(n_est * n_lat)]

    def custo_json(c):
        return None if c == float('inf') else c

    livre = {"custo": custo_json(rota_livre[0]), "rota": list(rota_livre[1])}
    por_k = {str(k): {"custo": custo_json(c), "rota": list(r)} for k, (c, r) in sorted(rotas_por_k.items())}
    k_max = max(rotas_por_k) if rotas_por_k else 0

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>{titulo}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: #0f172a;
      color: #f1f5f9;
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }}
    header {{
      background: #1e293b;
      border-bottom: 1px solid #334155;
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    h1 {{ font-size: 1.1rem; font-weight: 600; color: #38bdf8; }}
    .subtitle {{ font-size: 0.8rem; color: #94a3b8; margin-top: 2px; }}
    .stats-bar {{ display: flex; gap: 10px; flex-wrap: wrap; }}
    .stat-chip {{
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 4px;
      padding: 4px 10px;
      font-size: 0.8rem;
    }}
    .stat-label {{ color: #94a3b8; margin-right: 4px; }}
    .stat-val {{ color: #f8fafc; font-weight: 600; font-variant-numeric: tabular-nums; }}
    .main-container {{ display: flex; flex: 1; overflow: hidden; }}
    .toolbar {{
      background: #1e293b;
      border-right: 1px solid #334155;
      width: 290px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      overflow-y: auto;
    }}
    .toolbar-section {{ display: flex; flex-direction: column; gap: 8px; }}
    .toolbar-title {{
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #94a3b8;
      font-weight: 700;
    }}
    .btn-group {{ display: flex; flex-direction: column; gap: 6px; }}
    button {{
      background: #334155;
      color: #f1f5f9;
      border: 1px solid #475569;
      border-radius: 4px;
      padding: 8px 12px;
      font-size: 0.85rem;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.15s ease;
      text-align: left;
    }}
    button:hover {{ background: #475569; border-color: #64748b; }}
    button.active {{ background: #0284c7; border-color: #38bdf8; color: #ffffff; }}
    .swatch {{ width: 14px; height: 4px; border-radius: 2px; flex-shrink: 0; }}
    .legend {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 4px;
      padding: 10px;
      font-size: 0.78rem;
    }}
    .legend-item {{ display: flex; align-items: center; gap: 8px; }}
    .legend-line {{ width: 18px; height: 4px; border-radius: 2px; }}
    .legend-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
    .slider-row {{ display: flex; align-items: center; gap: 10px; font-size: 0.85rem; }}
    input[type=range] {{ flex: 1; accent-color: #22d3ee; }}
    .hint {{ font-size: 0.78rem; color: #94a3b8; line-height: 1.4; }}
    table.tab-k {{ width: 100%; border-collapse: collapse; font-size: 0.78rem; font-variant-numeric: tabular-nums; }}
    table.tab-k td, table.tab-k th {{ padding: 3px 6px; border-bottom: 1px solid #334155; text-align: right; }}
    table.tab-k th {{ color: #94a3b8; font-weight: 600; }}
    table.tab-k tr.sel td {{ color: #22d3ee; font-weight: 700; }}
    table.tab-k tr {{ cursor: pointer; }}
    .canvas-wrapper {{
      flex: 1;
      position: relative;
      background: #efefef;
      overflow: hidden;
    }}
    canvas {{ position: absolute; inset: 0; cursor: grab; }}
    canvas.arrastando {{ cursor: grabbing; }}
    .coord-tip {{
      position: absolute;
      bottom: 12px;
      right: 12px;
      background: rgba(15, 23, 42, 0.92);
      border: 1px solid #334155;
      border-radius: 4px;
      padding: 4px 10px;
      font-size: 0.75rem;
      color: #94a3b8;
      font-family: monospace;
      pointer-events: none;
      max-width: calc(100% - 24px);
    }}
    .zoom-tip {{
      position: absolute;
      top: 12px;
      right: 12px;
      font-size: 0.75rem;
      color: #94a3b8;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid #334155;
      border-radius: 4px;
      padding: 4px 10px;
      pointer-events: none;
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>{titulo}</h1>
      <div class="subtitle">Projeto e Análise de Algoritmos I — Instituto de Informática — UFRGS</div>
    </div>
    <div class="stats-bar">
      <div class="stat-chip"><span class="stat-label">Pontos (|V|):</span><span class="stat-val">{len(coords)}</span></div>
      <div class="stat-chip"><span class="stat-label">Buracos:</span><span class="stat-val">{len(buracos)}</span></div>
      <div class="stat-chip"><span class="stat-label">Ignorando buracos:</span><span class="stat-val" id="chipLivre">—</span></div>
      <div class="stat-chip"><span class="stat-label" id="chipKLabel">No máx. k buracos:</span><span class="stat-val" id="chipK">—</span></div>
    </div>
  </header>

  <div class="main-container">
    <aside class="toolbar">
      <div class="toolbar-section">
        <div class="toolbar-title">Modos de visualização</div>
        <div class="btn-group">
          <button id="btn-k" class="active" onclick="setMode('k')">
            <span class="swatch" style="background:#22d3ee"></span>No máximo k buracos (Parte 2)
          </button>
          <button id="btn-livre" onclick="setMode('livre')">
            <span class="swatch" style="background:#f97316"></span>Ignorando buracos (Parte 1)
          </button>
          <button id="btn-ambas" onclick="setMode('ambas')">
            <span class="swatch" style="background:linear-gradient(90deg,#f97316,#22d3ee)"></span>Comparar rotas
          </button>
          <button id="btn-pista" onclick="setMode('pista')">
            <span class="swatch" style="background:#6e6e6e"></span>Somente a pista
          </button>
        </div>
      </div>

      <div class="toolbar-section">
        <div class="toolbar-title">Limite de buracos (k)</div>
        <div class="slider-row">
          <input type="range" id="kSlider" min="0" max="{k_max}" step="1" value="{k_padrao}" oninput="setK(this.value)">
          <span id="kVal" style="min-width:2em; text-align:right; font-weight:600;">{k_padrao}</span>
        </div>
        <table class="tab-k" id="tabK"></table>
      </div>

      <div class="toolbar-section">
        <div class="toolbar-title">Legenda</div>
        <div class="legend">
          <div class="legend-item"><div class="legend-line" style="background:#6e6e6e; height:10px"></div><span>Pista (largura exagerada)</span></div>
          <div class="legend-item"><div class="legend-line" style="background:#7c5cff; height:10px"></div><span>Prédios do campus</span></div>
          <div class="legend-item"><div class="legend-dot" style="background:#1c1917; border:2px solid #78716c"></div><span>Buraco</span></div>
          <div class="legend-item"><div class="legend-dot" style="background:transparent; border:2px solid #ef4444"></div><span>Buraco atingido pela rota</span></div>
          <div class="legend-item"><span style="width:18px; text-align:center; color:#94a3b8; font-weight:700">›</span><span>Sentido de circulação (mão única)</span></div>
          <div class="legend-item"><div class="legend-dot" style="background:#10b981"></div><span>Entrada do campus (origem)</span></div>
          <div class="legend-item"><div class="legend-dot" style="background:#f43f5e"></div><span>INF (destino)</span></div>
        </div>
      </div>

      <div class="toolbar-section" style="margin-top: auto;">
        <div class="toolbar-title">Instruções</div>
        <div class="hint">
          Use a roda do mouse para aproximar e arraste para mover o mapa. Clique duas vezes para
          voltar à visão inicial. Posicione o cursor sobre a pista para ver o ponto correspondente.
        </div>
      </div>
    </aside>

    <main class="canvas-wrapper" id="canvasWrapper">
      <canvas id="mapa"></canvas>
      <div class="zoom-tip" id="zoomTip">zoom 1.0×</div>
      <div class="coord-tip" id="coordTip">Passe o cursor sobre a pista</div>
    </main>
  </div>

  <script>
    const PTS = {json.dumps(pts)};
    const N_EST = {n_est}, N_LAT = {n_lat};
    const BURACOS = new Set({json.dumps(sorted(buracos))});
    const ORIGEM = {origem}, DESTINO = {destino};
    const LIVRE = {json.dumps(livre)};
    const POR_K = {json.dumps(por_k)};
    const RUAS = {json.dumps(extras["ruas"])};
    const PREDIOS = {json.dumps(extras["predios"])};
    const ROTULOS = {json.dumps(extras["rotulos"])};
    const EXAGERO = 5;   // a largura da pista é exagerada para ficar visível

    let modo = 'k';
    let kAtual = {k_padrao};
    let hover = -1;

    // Posições de desenho: centro da estação + deslocamento lateral exagerado
    const centros = [];
    for (let i = 0; i < N_EST; i++) {{
      let sx = 0, sy = 0;
      for (let j = 0; j < N_LAT; j++) {{ sx += PTS[i * N_LAT + j][0]; sy += PTS[i * N_LAT + j][1]; }}
      centros.push([sx / N_LAT, sy / N_LAT]);
    }}
    function desenhoLat(i, jFrac) {{
      // jFrac pode ser fracionário (bordas da pista)
      const c = centros[i];
      const a = PTS[i * N_LAT], b = PTS[i * N_LAT + N_LAT - 1];
      const t = (jFrac - (N_LAT - 1) / 2) / (N_LAT - 1);
      return [c[0] + EXAGERO * t * (b[0] - a[0]), c[1] + EXAGERO * t * (b[1] - a[1])];
    }}
    const POS = PTS.map((_, v) => desenhoLat(Math.floor(v / N_LAT), v % N_LAT));
    const passoLat = Math.hypot(POS[1][0] - POS[0][0], POS[1][1] - POS[0][1]);

    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const [x, y] of POS) {{
      minX = Math.min(minX, x); maxX = Math.max(maxX, x);
      minY = Math.min(minY, y); maxY = Math.max(maxY, y);
    }}
    const inclui = (x, y) => {{
      minX = Math.min(minX, x); maxX = Math.max(maxX, x);
      minY = Math.min(minY, y); maxY = Math.max(maxY, y);
    }};
    RUAS.forEach(r => r.forEach(([x, y]) => inclui(x, y)));
    PREDIOS.forEach(([x, y, w, h]) => {{ inclui(x, y); inclui(x + w, y + h); }});
    minY -= 30; maxY += 30; minX -= 30; maxX += 30;

    const canvas = document.getElementById('mapa');
    const ctx = canvas.getContext('2d');
    const wrapper = document.getElementById('canvasWrapper');
    const tip = document.getElementById('coordTip');
    let base = 1, zoom = 1, panX = 0, panY = 0, W = 0, H = 0;

    const COR_ASFALTO = '#6e6e6e';
    const tx = x => W / 2 + panX + (x - (minX + maxX) / 2) * base * zoom;
    const ty = y => H / 2 + panY + (y - (minY + maxY) / 2) * base * zoom;
    const s = () => base * zoom;

    function resize() {{
      const dpr = window.devicePixelRatio || 1;
      W = wrapper.clientWidth; H = wrapper.clientHeight;
      canvas.width = W * dpr; canvas.height = H * dpr;
      canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      base = Math.min(W / (maxX - minX), H / (maxY - minY));
      render();
    }}

    function borda(jFrac) {{
      const pts = [];
      for (let i = 0; i < N_EST; i++) pts.push(desenhoLat(i, jFrac));
      return pts;
    }}
    const BORDA_INT = borda(-0.6), BORDA_EXT = borda(N_LAT - 1 + 0.6), FAIXA = borda((N_LAT - 1) / 2);

    function caminhoFechado(pts) {{
      ctx.moveTo(tx(pts[0][0]), ty(pts[0][1]));
      for (let i = 1; i < pts.length; i++) ctx.lineTo(tx(pts[i][0]), ty(pts[i][1]));
      ctx.closePath();
    }}

    function rotaAtual(nome) {{
      if (nome === 'livre') return LIVRE;
      return POR_K[String(kAtual)] || {{ custo: null, rota: [] }};
    }}

    function desenhaRota(r, cor, largura) {{
      if (r.length < 2) return;
      ctx.strokeStyle = cor;
      ctx.lineWidth = largura;
      ctx.lineJoin = 'round'; ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(tx(POS[r[0]][0]), ty(POS[r[0]][1]));
      for (let i = 1; i < r.length; i++) ctx.lineTo(tx(POS[r[i]][0]), ty(POS[r[i]][1]));
      ctx.stroke();
    }}

    function marcaBuracosAtingidos(r, cor) {{
      ctx.strokeStyle = cor;
      ctx.lineWidth = Math.max(1.5, passoLat * s() * 0.18);
      for (let i = 1; i < r.length; i++) {{
        if (!BURACOS.has(r[i])) continue;
        ctx.beginPath();
        ctx.arc(tx(POS[r[i]][0]), ty(POS[r[i]][1]), Math.max(4, passoLat * s() * 0.75), 0, 2 * Math.PI);
        ctx.stroke();
      }}
    }}

    function marcador(v, cor, texto, lado) {{
      const x = tx(POS[v][0]), y = ty(POS[v][1]);
      ctx.fillStyle = cor;
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(x, y, 8, 0, 2 * Math.PI); ctx.fill(); ctx.stroke();
      ctx.font = '600 13px -apple-system, Segoe UI, Roboto, sans-serif';
      const w = ctx.measureText(texto).width + 12;
      const i = Math.floor(v / N_LAT);
      const fora = desenhoLat(i, lado > 0 ? N_LAT - 1 + 7 : -7);
      const lx = tx(fora[0]), ly = ty(fora[1]);
      ctx.fillStyle = 'rgba(15, 23, 42, 0.92)';
      ctx.strokeStyle = cor;
      ctx.lineWidth = 1.5;
      ctx.fillRect(lx - w / 2, ly - 11, w, 22);
      ctx.strokeRect(lx - w / 2, ly - 11, w, 22);
      ctx.fillStyle = '#f1f5f9';
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(texto, lx, ly);
    }}

    function render() {{
      ctx.clearRect(0, 0, W, H);
      const largPista = (N_LAT - 1 + 1.2) * EXAGERO * s();   // posições a 1 m, mais a margem das bordas

      // Ruas vizinhas (decoração)
      ctx.strokeStyle = COR_ASFALTO;
      ctx.lineWidth = largPista;
      ctx.lineJoin = 'round'; ctx.lineCap = 'butt';
      RUAS.forEach(r => {{
        ctx.beginPath();
        ctx.moveTo(tx(r[0][0]), ty(r[0][1]));
        for (let i = 1; i < r.length; i++) ctx.lineTo(tx(r[i][0]), ty(r[i][1]));
        ctx.stroke();
      }});

      // Prédios e rótulos
      ctx.fillStyle = '#7c5cff';
      PREDIOS.forEach(([x, y, w, h]) => ctx.fillRect(tx(x), ty(y), w * s(), h * s()));
      ctx.font = `500 ${{Math.max(11, Math.min(22, 16 * zoom))}}px -apple-system, Segoe UI, Roboto, sans-serif`;
      ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
      ctx.fillStyle = '#333333';
      ROTULOS.forEach(([x, y, t]) => ctx.fillText(t, tx(x), ty(y)));

      // Pista (asfalto)
      ctx.fillStyle = COR_ASFALTO;
      ctx.beginPath();
      caminhoFechado(BORDA_EXT);
      caminhoFechado([...BORDA_INT].reverse());
      ctx.fill('evenodd');
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.55)';
      ctx.lineWidth = 1.2;
      ctx.setLineDash([8, 8]);
      ctx.beginPath(); caminhoFechado(FAIXA); ctx.stroke();
      ctx.setLineDash([]);

      // Sentido de circulação (mão única, sentido horário)
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.85)';
      ctx.lineWidth = 2;
      ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      const passoSeta = Math.max(10, Math.round(50 / zoom));
      const tamSeta = Math.max(4, Math.min(12, largPista * 0.22));
      for (let i = Math.floor(passoSeta / 2); i < N_EST - 1; i += passoSeta) {{
        const x = tx(FAIXA[i][0]), y = ty(FAIXA[i][1]);
        const ang = Math.atan2(ty(FAIXA[i + 1][1]) - y, tx(FAIXA[i + 1][0]) - x);
        ctx.beginPath();
        ctx.moveTo(x - tamSeta * Math.cos(ang - 0.6), y - tamSeta * Math.sin(ang - 0.6));
        ctx.lineTo(x, y);
        ctx.lineTo(x - tamSeta * Math.cos(ang + 0.6), y - tamSeta * Math.sin(ang + 0.6));
        ctx.stroke();
      }}

      // Pontos da pista (visíveis apenas com zoom)
      const r = passoLat * s();
      if (r > 7) {{
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        POS.forEach(([x, y]) => {{
          ctx.beginPath(); ctx.arc(tx(x), ty(y), 1.5, 0, 2 * Math.PI); ctx.fill();
        }});
      }}

      // Buracos
      ctx.fillStyle = '#1c1917';
      ctx.strokeStyle = '#3f3a36';
      ctx.lineWidth = Math.max(0.5, r * 0.08);
      BURACOS.forEach(v => {{
        const x = tx(POS[v][0]), y = ty(POS[v][1]);
        const rr = Math.max(1.5, r * 0.42);
        ctx.beginPath();
        ctx.ellipse(x, y, rr * 1.15, rr * 0.85, (v * 0.7) % Math.PI, 0, 2 * Math.PI);
        ctx.fill(); ctx.stroke();
      }});

      // Rotas
      const larg = Math.max(2.5, r * 0.3);
      if (modo === 'livre' || modo === 'ambas') {{
        desenhaRota(LIVRE.rota, '#f97316', modo === 'ambas' ? larg * 1.8 : larg);
      }}
      if (modo === 'k' || modo === 'ambas') {{
        desenhaRota(rotaAtual('k').rota, '#22d3ee', larg);
      }}
      if (modo === 'livre') marcaBuracosAtingidos(LIVRE.rota, '#ef4444');
      if (modo === 'k' || modo === 'ambas') marcaBuracosAtingidos(rotaAtual('k').rota, '#ef4444');

      if (hover >= 0) {{
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(tx(POS[hover][0]), ty(POS[hover][1]), Math.max(5, r * 0.5), 0, 2 * Math.PI); ctx.stroke();
      }}

      marcador(ORIGEM, '#10b981', 'Entrada do Campus', 1);
      marcador(DESTINO, '#f43f5e', 'INF', -1);
      document.getElementById('zoomTip').textContent = 'zoom ' + zoom.toFixed(1) + '×';
    }}

    const contaBuracos = rota => rota.slice(1).filter(v => BURACOS.has(v)).length;
    const fmt = c => c === null ? 'sem rota' : (c / 100).toFixed(2) + ' m';

    function atualizaPainel() {{
      document.getElementById('chipLivre').textContent =
        fmt(LIVRE.custo) + (LIVRE.rota.length ? ' · ' + contaBuracos(LIVRE.rota) + ' buracos' : '');
      const rk = rotaAtual('k');
      document.getElementById('chipKLabel').textContent = 'No máx. ' + kAtual + ' buracos:';
      document.getElementById('chipK').textContent =
        fmt(rk.custo) + (rk.rota.length ? ' · ' + contaBuracos(rk.rota) + ' buracos' : '');
      let html = '<tr><th>k</th><th>distância</th><th>buracos</th></tr>';
      for (const k in POR_K) {{
        const e = POR_K[k];
        html += `<tr class="${{Number(k) === kAtual ? 'sel' : ''}}" onclick="setK(${{k}})">` +
                `<td>${{k}}</td><td>${{fmt(e.custo)}}</td><td>${{e.rota.length ? contaBuracos(e.rota) : '—'}}</td></tr>`;
      }}
      html += `<tr><td>∞</td><td>${{fmt(LIVRE.custo)}}</td><td>${{LIVRE.rota.length ? contaBuracos(LIVRE.rota) : '—'}}</td></tr>`;
      document.getElementById('tabK').innerHTML = html;
    }}

    function setMode(m) {{
      modo = m;
      ['k', 'livre', 'ambas', 'pista'].forEach(id =>
        document.getElementById('btn-' + id).classList.toggle('active', id === m));
      render();
    }}

    function setK(v) {{
      kAtual = Number(v);
      document.getElementById('kVal').textContent = kAtual;
      document.getElementById('kSlider').value = kAtual;
      atualizaPainel();
      render();
    }}

    // Zoom e arraste
    let arrasto = null;
    canvas.addEventListener('wheel', (e) => {{
      e.preventDefault();
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left - W / 2, my = e.clientY - rect.top - H / 2;
      const fator = Math.exp(-e.deltaY * 0.0015);
      const novo = Math.min(40, Math.max(1, zoom * fator));
      const f = novo / zoom;
      panX = mx - (mx - panX) * f;
      panY = my - (my - panY) * f;
      zoom = novo;
      render();
    }}, {{ passive: false }});
    canvas.addEventListener('mousedown', (e) => {{
      arrasto = {{ x: e.clientX, y: e.clientY, px: panX, py: panY }};
      canvas.classList.add('arrastando');
    }});
    window.addEventListener('mouseup', () => {{ arrasto = null; canvas.classList.remove('arrastando'); }});
    canvas.addEventListener('dblclick', () => {{ zoom = 1; panX = 0; panY = 0; render(); }});

    canvas.addEventListener('mousemove', (e) => {{
      if (arrasto) {{
        panX = arrasto.px + e.clientX - arrasto.x;
        panY = arrasto.py + e.clientY - arrasto.y;
        render();
        return;
      }}
      const rect = canvas.getBoundingClientRect();
      const px = e.clientX - rect.left, py = e.clientY - rect.top;
      let melhor = -1, melhorD = Math.max(6, passoLat * s() * 0.6);
      for (let v = 0; v < POS.length; v++) {{
        const d = Math.hypot(tx(POS[v][0]) - px, ty(POS[v][1]) - py);
        if (d < melhorD) {{ melhorD = d; melhor = v; }}
      }}
      if (melhor !== hover) {{ hover = melhor; render(); }}
      if (melhor < 0) {{ tip.textContent = 'Passe o cursor sobre a pista'; return; }}
      const i = Math.floor(melhor / N_LAT), j = melhor % N_LAT;
      const lado = j === 0 ? ' (borda interna)' : (j === N_LAT - 1 ? ' (borda externa)' : '');
      const naRota = [];
      if (LIVRE.rota.includes(melhor)) naRota.push('ignorando buracos');
      if (rotaAtual('k').rota.includes(melhor)) naRota.push('k = ' + kAtual);
      tip.textContent = `Ponto ${{melhor}} | estação ${{i}}, posição ${{j}}${{lado}}` +
        (BURACOS.has(melhor) ? ' | BURACO' : '') + (naRota.length ? ' | rotas: ' + naRota.join(', ') : '');
    }});
    canvas.addEventListener('mouseleave', () => {{ hover = -1; render(); }});

    window.addEventListener('resize', resize);
    atualizaPainel();
    resize();
  </script>
</body>
</html>
"""

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write(html)

    return arquivo_saida
