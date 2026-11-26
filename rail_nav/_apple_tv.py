"""Estilo "apple_tv": vidro escuro em camadas, destaque em pílula clara que "cresce"
no hover, painel flutuante com cantos arredondados e animações suaves.

É aplicado POR CIMA do CSS padrão (mesma estrutura de trilho + painel).

Cores usadas neste estilo:
- cor_trilho         -> tom do vidro (trilho e painel)
- cor_trilho_ativo   -> página atual
- cor_destaque       -> pílula do item sob o mouse
- cor_texto_destaque -> texto/ícone sobre a pílula (padrão: cor_trilho)
- vidro_opacidade / vidro_desfoque -> quanto o vidro deixa ver e desfoca o fundo
As cores do painel do estilo padrão (cor_painel, cor_texto_painel, cor_titulo_painel,
cor_hover_link) não se aplicam aqui.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Tema

_ITENS = '[data-testid="stSidebarNavItems"]'
_SECAO = f"{_ITENS} > div"
_HEADER = '[data-testid="stNavSectionHeader"]'
_LINK = 'a[data-testid="stSidebarNavLink"]'
_EASE = "cubic-bezier(.2,.8,.2,1)"


def _rgba(hex_cor: str, alfa: float) -> str:
    h = hex_cor.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    try:
        r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return hex_cor
    return f"rgba({r},{g},{b},{alfa})"


def css_apple_tv(t: "Tema") -> str:
    op = max(0.0, min(1.0, t.vidro_opacidade))
    blur = max(0, int(t.vidro_desfoque))
    vidro_trilho = _rgba(t.cor_trilho, op)
    vidro_painel = _rgba(t.cor_trilho, min(1.0, op + 0.08))
    ativo = _rgba(t.cor_trilho_ativo, 0.75)
    destaque = t.cor_destaque
    texto_destaque = t.cor_texto_destaque or t.cor_trilho
    filtro = f"blur({blur}px) saturate(170%)"
    # "brilho" do vidro: reflexo suave no topo + filete claro na borda de cima
    reflexo = "linear-gradient(180deg, rgba(255,255,255,.07) 0%, rgba(255,255,255,.015) 38%, rgba(255,255,255,0) 100%)"
    filete = "inset 0 1px 0 rgba(255,255,255,.10), inset 0 0 0 1px rgba(255,255,255,.06)"
    return f"""
/* ================= estilo apple_tv ================= */
:root {{
  --atv-margem: 12px;
  --painel-top: calc({t.topo_painel}px + var(--atv-margem));
}}

/* --- Trilho: vidro (o blur fica num pseudo-elemento, para não impedir o blur
       do painel, que mora dentro da sidebar) --- */
section[data-testid="stSidebar"] {{
  background: transparent !important;
  border-right: 1px solid rgba(255,255,255,.06);
}}
section[data-testid="stSidebar"]::before {{
  content: "";
  position: absolute; inset: 0;
  background: {reflexo}, {vidro_trilho};
  -webkit-backdrop-filter: {filtro};
  backdrop-filter: {filtro};
  pointer-events: none;
}}
[data-testid="stSidebarContent"] {{ position: relative; }}

/* --- Itens do trilho --- */
{_HEADER}, {_ITENS} > li {_LINK} {{
  border-radius: 16px !important;
  transition: background-color 200ms {_EASE}, box-shadow 200ms {_EASE} !important;
}}
{_HEADER} p, {_ITENS} > li {_LINK} > span {{
  transition: transform 220ms {_EASE}, color 200ms {_EASE} !important;
}}
{_HEADER} p, {_ITENS} > li {_LINK} p {{
  color: rgba(255,255,255,.62) !important;
  font-size: 11px !important;
  letter-spacing: -.005em !important;
}}
{_HEADER} p span[role="img"], {_ITENS} > li {_LINK} [data-testid="stIconMaterial"] {{
  color: rgba(255,255,255,.92) !important;
}}
/* deixa o rótulo crescer sem ser cortado nas bordas do item */
{_HEADER}, {_HEADER} *, {_ITENS} > li {_LINK}, {_ITENS} > li {_LINK} * {{
  overflow: visible !important;
  text-overflow: clip !important;
}}

/* página atual: placa de vidro mais clara, com filete de luz */
{_SECAO}:has(a[aria-current="page"]) > {_HEADER},
{_ITENS} > li a[aria-current="page"] {{
  background: {reflexo}, {ativo} !important;
  box-shadow: {filete} !important;
}}
{_SECAO}:has(a[aria-current="page"]) > {_HEADER} p,
{_ITENS} > li a[aria-current="page"] p {{ color: rgba(255,255,255,.95) !important; }}

/* foco (hover): pílula clara que cresce, com sombra */
{_SECAO}:hover > {_HEADER},
{_ITENS} > li {_LINK}:hover {{
  background: {destaque} !important;
  box-shadow: 0 10px 28px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.6) !important;
}}
{_SECAO}:hover > {_HEADER} p,
{_ITENS} > li {_LINK}:hover > span {{
  transform: scale(1.05);
}}
{_SECAO}:hover > {_HEADER} p,
{_SECAO}:hover > {_HEADER} p span[role="img"],
{_ITENS} > li {_LINK}:hover p,
{_ITENS} > li {_LINK}:hover [data-testid="stIconMaterial"] {{
  color: {texto_destaque} !important;
}}

/* --- Painel: vidro flutuante, no formato dos cards --- */
{_SECAO}::after {{
  top: var(--painel-top) !important;
  bottom: var(--atv-margem) !important;
  left: calc(var(--rail-w) + 10px) !important;
  width: var(--painel-w) !important;
  border-radius: 22px;
  background: {reflexo}, {vidro_painel} !important;
  -webkit-backdrop-filter: blur({blur + 8}px) saturate(180%);
  backdrop-filter: blur({blur + 8}px) saturate(180%);
  border: 1px solid rgba(255,255,255,.08);
  box-shadow: 0 24px 64px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.10) !important;
  transform: translateX(-10px) scale(.98);
  transform-origin: left center;
}}
{_SECAO}:hover::after {{ transform: none; }}

/* animação de entrada: deslizar + aparecer (o atraso de abrir/fechar continua valendo) */
{_SECAO}::after, {_SECAO} > li, {_SECAO} > {_HEADER}::before {{
  transition: visibility 0s linear {t.atraso_fechar_ms}ms,
              opacity 160ms ease {max(t.atraso_fechar_ms - 160, 0)}ms,
              transform 260ms {_EASE} {max(t.atraso_fechar_ms - 160, 0)}ms !important;
}}
{_SECAO}:hover::after, {_SECAO}:hover > li, {_SECAO}:hover > {_HEADER}::before {{
  transition: visibility 0s linear {t.atraso_abrir_ms}ms,
              opacity 160ms ease {t.atraso_abrir_ms}ms,
              transform 260ms {_EASE} {t.atraso_abrir_ms}ms !important;
}}
{_SECAO} > li {{
  left: calc(var(--rail-w) + 22px) !important;
  width: calc(var(--painel-w) - 24px) !important;
  transform: translateX(-10px);
}}
{_SECAO}:hover > li {{ transform: none; }}

/* título do painel: rótulo pequeno, maiúsculo e espaçado (como os rótulos dos cards) */
{_SECAO} > {_HEADER}::before {{
  top: calc(var(--painel-top) + 24px) !important;
  left: calc(var(--rail-w) + 36px) !important;
  font-size: 11.5px !important;
  letter-spacing: .14em !important;
  text-transform: uppercase !important;
  color: rgba(255,255,255,.48) !important;
}}

/* links do painel: pílulas */
{_SECAO} > li {_LINK} {{
  height: 44px !important;
  border-radius: 999px !important;
  padding: 0 16px !important;
  transition: background-color 180ms {_EASE}, box-shadow 180ms {_EASE}, transform 200ms {_EASE} !important;
}}
{_SECAO} > li {_LINK} p,
{_SECAO} > li {_LINK} span {{
  color: rgba(255,255,255,.86) !important;
  transition: color 160ms {_EASE};
}}
{_SECAO} > li a[aria-current="page"] {{
  background: {reflexo}, {ativo} !important;
  box-shadow: {filete} !important;
}}
{_SECAO} > li a[aria-current="page"] p,
{_SECAO} > li a[aria-current="page"] span {{ color: #ffffff !important; }}
{_SECAO} > li {_LINK}:hover {{
  background: {destaque} !important;
  box-shadow: 0 8px 22px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.6) !important;
  transform: scale(1.03);
}}
{_SECAO} > li {_LINK}:hover p,
{_SECAO} > li {_LINK}:hover span {{ color: {texto_destaque} !important; }}

/* botões da sidebar (ex.: Logout): pílula de vidro */
[data-testid="stSidebarUserContent"] button {{
  border-radius: 999px !important;
  border: 1px solid rgba(255,255,255,.12) !important;
  background: {reflexo}, rgba(255,255,255,.06) !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.08);
  color: rgba(255,255,255,.85) !important;
  transition: background-color 180ms {_EASE}, color 180ms {_EASE};
}}
[data-testid="stSidebarUserContent"] button:hover {{
  background: {destaque} !important;
  color: {texto_destaque} !important;
}}
"""
