"""Estilo "apple_tv": vidro escuro, destaque em pílula clara que "cresce" no hover,
painel flutuante com cantos arredondados e animações suaves.

É aplicado POR CIMA do CSS padrão (mesma estrutura de trilho + painel).
Usa cor_trilho e cor_trilho_ativo como tom do vidro e destaque; as cores do painel
(cor_painel, cor_texto_painel, cor_titulo_painel, cor_hover_link) não se aplicam.
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
    h = hex_cor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    try:
        r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return hex_cor
    return f"rgba({r},{g},{b},{alfa})"


def css_apple_tv(t: "Tema") -> str:
    vidro_trilho = _rgba(t.cor_trilho, 0.55)
    ativo = _rgba(t.cor_trilho_ativo, 0.85)
    texto_pilula = t.cor_trilho  # texto/ícone escuro sobre a pílula clara
    return f"""
/* ================= estilo apple_tv ================= */
:root {{
  --atv-margem: 12px;
  --painel-top: calc({t.topo_painel}px + var(--atv-margem));
}}

/* --- Trilho: vidro escuro tingido de azul (blur num pseudo-elemento, para não
       impedir o blur do painel, que fica dentro da sidebar) --- */
section[data-testid="stSidebar"] {{
  background: transparent !important;
  border-right: 1px solid rgba(255,255,255,.06);
}}
section[data-testid="stSidebar"]::before {{
  content: "";
  position: absolute; inset: 0;
  background: {vidro_trilho};
  -webkit-backdrop-filter: blur(30px) saturate(160%);
  backdrop-filter: blur(30px) saturate(160%);
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
}}
{_HEADER} p span[role="img"], {_ITENS} > li {_LINK} [data-testid="stIconMaterial"] {{
  color: rgba(255,255,255,.92) !important;
}}

/* página atual: vidro azul mais forte, sem barrinha lateral */
{_SECAO}:has(a[aria-current="page"]) > {_HEADER},
{_ITENS} > li a[aria-current="page"] {{
  background: {ativo} !important;
  box-shadow: none !important;
}}

/* foco (hover): pílula clara que cresce, com sombra */
{_SECAO}:hover > {_HEADER},
{_ITENS} > li {_LINK}:hover {{
  background: rgba(255,255,255,.94) !important;
  box-shadow: 0 10px 28px rgba(0,0,0,.45) !important;
}}
{_SECAO}:hover > {_HEADER} p,
{_ITENS} > li {_LINK}:hover > span {{
  transform: scale(1.05);
}}
/* deixa o rótulo crescer sem ser cortado nas bordas do item */
{_HEADER}, {_HEADER} *, {_ITENS} > li {_LINK}, {_ITENS} > li {_LINK} * {{
  overflow: visible !important;
  text-overflow: clip !important;
}}
{_SECAO}:hover > {_HEADER} p,
{_SECAO}:hover > {_HEADER} p span[role="img"],
{_ITENS} > li {_LINK}:hover p,
{_ITENS} > li {_LINK}:hover [data-testid="stIconMaterial"] {{
  color: {texto_pilula} !important;
}}

/* --- Painel: vidro escuro flutuante --- */
{_SECAO}::after {{
  top: var(--painel-top) !important;
  bottom: var(--atv-margem) !important;
  left: calc(var(--rail-w) + 10px) !important;
  width: var(--painel-w) !important;
  border-radius: 24px;
  background: rgba(24,26,32,.62) !important;
  -webkit-backdrop-filter: blur(40px) saturate(180%);
  backdrop-filter: blur(40px) saturate(180%);
  border: 1px solid rgba(255,255,255,.09);
  box-shadow: 0 24px 64px rgba(0,0,0,.55) !important;
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

/* título do painel: grande, em caixa normal, como no tvOS */
{_SECAO} > {_HEADER}::before {{
  top: calc(var(--painel-top) + 20px) !important;
  left: calc(var(--rail-w) + 34px) !important;
  font-size: 22px !important;
  letter-spacing: -.01em !important;
  text-transform: none !important;
  color: rgba(255,255,255,.96) !important;
}}

/* links do painel */
{_SECAO} > li {_LINK} {{
  height: 44px !important;
  border-radius: 12px !important;
  transition: background-color 180ms {_EASE}, box-shadow 180ms {_EASE}, transform 200ms {_EASE} !important;
}}
{_SECAO} > li {_LINK} p,
{_SECAO} > li {_LINK} span {{
  color: rgba(255,255,255,.86) !important;
  transition: color 160ms {_EASE};
}}
{_SECAO} > li a[aria-current="page"] {{
  background: {ativo} !important;
  box-shadow: none !important;
}}
{_SECAO} > li a[aria-current="page"] p,
{_SECAO} > li a[aria-current="page"] span {{ color: #ffffff !important; }}
{_SECAO} > li {_LINK}:hover {{
  background: rgba(255,255,255,.94) !important;
  box-shadow: 0 8px 22px rgba(0,0,0,.4) !important;
  transform: scale(1.03);
}}
{_SECAO} > li {_LINK}:hover p,
{_SECAO} > li {_LINK}:hover span {{ color: {texto_pilula} !important; }}

/* botões da sidebar (ex.: Logout): pílula de vidro */
[data-testid="stSidebarUserContent"] button {{
  border-radius: 999px !important;
  border: 1px solid rgba(255,255,255,.14) !important;
  background: rgba(255,255,255,.08) !important;
  color: rgba(255,255,255,.85) !important;
  transition: background-color 180ms {_EASE}, color 180ms {_EASE};
}}
[data-testid="stSidebarUserContent"] button:hover {{
  background: rgba(255,255,255,.94) !important;
  color: {texto_pilula} !important;
}}
"""
