"""CSS do trilho + painel. Gerado a partir do Tema; não edite as cores aqui."""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Tema


def montar_css(t: "Tema", titulos_secoes: list[str]) -> str:
    titulos = "".join(
        f'[data-testid="stSidebarNavItems"] > div:nth-of-type({i}) > '
        f'[data-testid="stNavSectionHeader"]::before {{ content: "{_escapar(s.upper())}"; }}\n'
        for i, s in enumerate(titulos_secoes, start=1)
    )
    return _css_base(t).replace("</style>", titulos + "</style>")


def _escapar(texto: str) -> str:
    return texto.replace("\\", "\\\\").replace('"', '\\"')


def _css_base(t: "Tema") -> str:
    return f"""
<style>
:root {{
  --rail-w: {t.largura_trilho}px;
  --painel-w: {t.largura_painel}px;
  --painel-top: {t.topo_painel}px;
}}

/* ===== 1. Trilho fixo, estreito, sem botão de recolher/redimensionar ===== */
section[data-testid="stSidebar"] {{
  width: var(--rail-w) !important;
  min-width: var(--rail-w) !important;
  max-width: var(--rail-w) !important;
  transform: none !important;           /* senão o position:fixed do painel quebra */
  background: {t.cor_trilho} !important;
  z-index: 1000001 !important;   /* acima do header do Streamlit */
}}
section[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {{
  overflow: visible !important;         /* deixa o painel "vazar" para a direita */
  background: transparent !important;
}}
[data-testid="stSidebarContent"] {{ padding: 0 !important; }}
[data-testid="stSidebarNav"], [data-testid="stSidebarNavItems"] {{ width: 100% !important; }}
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarResizeHandle"],
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapsedControl"] {{
  display: none !important;
}}
[data-testid="stSidebarHeader"] {{
  padding: 14px 8px 6px !important;
  justify-content: center;
}}
[data-testid="stSidebarHeader"] img {{ max-width: 64px; height: auto; }}

/* Conteúdo principal começa depois do trilho */
[data-testid="stMain"], .main {{
  margin-left: 0 !important;
}}

/* ===== 2. Categorias viram "botões" do trilho ===== */
[data-testid="stSidebarNav"] {{ padding-top: 4px; }}
[data-testid="stSidebarNavItems"] {{
  padding: 0 !important;
  max-height: none !important;
  overflow: visible !important;
}}
[data-testid="stSidebarNavItems"] > div,      /* wrapper de cada seção */
[data-testid="stSidebarNavItems"] > li {{
  position: static;
  margin: 0 !important;
  padding: 3px 8px;    /* sem "buracos": o mouse vai do ícone ao painel sem perder o hover */
}}
[data-testid="stNavSectionHeader"] {{
  display: flex !important;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  width: 100%;
  padding: 10px 2px !important;
  margin: 0 !important;
  border-radius: 10px;
  cursor: default;
  pointer-events: none;                  /* não deixa o clique recolher a seção */
  text-align: center;
}}
[data-testid="stNavSectionHeader"] p {{
  color: #d6e2ef !important;
  font-size: 11.5px !important;
  font-weight: 500 !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  white-space: normal !important;
  line-height: 1.15 !important;
  display: flex; flex-direction: column; align-items: center; gap: 5px;
}}
[data-testid="stNavSectionHeader"] [data-testid="stMarkdownContainer"] {{
  overflow: visible !important;
  text-overflow: clip !important;
}}
[data-testid="stNavSectionHeader"] p span[role="img"] {{
  font-size: 24px !important;
  color: #ffffff !important;
}}
[data-testid="stNavSectionHeader"] > div:last-child {{ display: none !important; }} /* setinha */

[data-testid="stSidebarNavItems"] > div:hover > [data-testid="stNavSectionHeader"],
[data-testid="stSidebarNavItems"] > div:has(a[aria-current="page"]) > [data-testid="stNavSectionHeader"] {{
  background: {t.cor_trilho_ativo};
}}
[data-testid="stSidebarNavItems"] > div:has(a[aria-current="page"]) > [data-testid="stNavSectionHeader"] {{
  box-shadow: inset 3px 0 0 #ffffff;
}}

/* Páginas soltas (sem seção, ex.: Início) também viram ícone do trilho */
[data-testid="stSidebarNavItems"] > li a[data-testid="stSidebarNavLink"] {{
  flex-direction: column; justify-content: center; align-items: center;
  height: auto; padding: 10px 2px; gap: 4px; border-radius: 10px;
}}
[data-testid="stSidebarNavItems"] > li a[data-testid="stSidebarNavLink"] > span {{ margin: 0 !important; }}
[data-testid="stSidebarNavItems"] > li a[data-testid="stSidebarNavLink"] [data-testid="stIconMaterial"] {{
  font-size: 24px !important; color: #fff !important;
}}
[data-testid="stSidebarNavItems"] > li a[data-testid="stSidebarNavLink"] p {{
  font-size: 11.5px !important; color: #d6e2ef !important;
}}
[data-testid="stSidebarNavItems"] > li a[data-testid="stSidebarNavLink"]:hover,
[data-testid="stSidebarNavItems"] > li a[aria-current="page"] {{
  background: {t.cor_trilho_ativo} !important;
}}

/* ===== 3. Painel (flyout) ===== */
/* Abrir/fechar com atraso (estilo "mega menu"):
   - fecha só t.atraso_fechar_ms depois que o mouse sai -> dá tempo de chegar no painel
   - abre outra categoria só após t.atraso_abrir_ms -> atravessar outra categoria na
     diagonal a caminho do painel não troca o painel aberto                     */
[data-testid="stSidebarNavItems"] > div::after,
[data-testid="stSidebarNavItems"] > div > li,
[data-testid="stSidebarNavItems"] > div > [data-testid="stNavSectionHeader"]::before {{
  visibility: hidden;
  opacity: 0;
  transition: visibility 0s linear {t.atraso_fechar_ms}ms, opacity 120ms ease {t.atraso_fechar_ms - 120}ms;
}}
[data-testid="stSidebarNavItems"] > div:hover::after,
[data-testid="stSidebarNavItems"] > div:hover > li,
[data-testid="stSidebarNavItems"] > div:hover > [data-testid="stNavSectionHeader"]::before {{
  visibility: visible;
  opacity: 1;
  transition: visibility 0s linear {t.atraso_abrir_ms}ms, opacity 120ms ease {t.atraso_abrir_ms}ms;
}}

/* Fundo do painel: um pseudo-elemento fixo ao lado do trilho */
[data-testid="stSidebarNavItems"] > div::after {{
  content: "";
  position: fixed;
  top: var(--painel-top); bottom: 0;
  left: calc(var(--rail-w) - 2px);       /* encosta 2px no trilho: sem fresta */
  width: calc(var(--painel-w) + 2px);
  background: {t.cor_painel};
  box-shadow: 8px 0 24px rgba(0,0,0,.25);
  z-index: 1;
}}

/* Os links da seção: aparecem empilhados dentro do painel */
[data-testid="stSidebarNavItems"] > div > li {{
  display: block;
  position: fixed;
  left: calc(var(--rail-w) + 16px);
  width: calc(var(--painel-w) - 32px);
  z-index: 2;
}}

/* Título da categoria dentro do painel (texto injetado pelo Python) */
[data-testid="stSidebarNavItems"] > div > [data-testid="stNavSectionHeader"]::before {{
  position: fixed;
  display: block;
  top: calc(var(--painel-top) + 26px);
  left: calc(var(--rail-w) + 28px);
  z-index: 3;
  font-size: 12.5px; font-weight: 700; letter-spacing: .12em;
  color: {t.cor_titulo_painel};
}}

/* O painel da categoria sob o mouse fica sempre por cima do que está fechando */
[data-testid="stSidebarNavItems"] > div:hover::after {{ z-index: 11; }}
[data-testid="stSidebarNavItems"] > div:hover > li {{ z-index: 12; }}
[data-testid="stSidebarNavItems"] > div:hover > [data-testid="stNavSectionHeader"]::before {{ z-index: 13; }}

/* posição vertical de cada link (48px por linha, começa abaixo do título) */
{''.join(
    f'[data-testid="stSidebarNavItems"] > div > li:nth-of-type({i}) {{ top: calc(var(--painel-top) + 64px + {(i-1)*46}px); }}'
    for i in range(1, 21)
)}

[data-testid="stSidebarNavItems"] > div > li a[data-testid="stSidebarNavLink"] {{
  background: transparent !important;
  border-radius: 8px;
  height: 42px;
  padding: 0 12px;
}}
[data-testid="stSidebarNavItems"] > div > li a[data-testid="stSidebarNavLink"] p,
[data-testid="stSidebarNavItems"] > div > li a[data-testid="stSidebarNavLink"] span {{
  color: {t.cor_texto_painel} !important;
  font-size: 15px !important;
}}
[data-testid="stSidebarNavItems"] > div > li a[data-testid="stSidebarNavLink"]:hover {{
  background: {t.cor_hover_link} !important;
}}
[data-testid="stSidebarNavItems"] > div > li a[aria-current="page"] {{
  background: {t.cor_hover_link} !important;
  box-shadow: inset 3px 0 0 {t.cor_trilho};
}}
[data-testid="stSidebarNavItems"] > div > li a[aria-current="page"] p {{ font-weight: 600 !important; }}

/* "Ver mais" do Streamlit (aparece com muitas páginas) – não faz sentido aqui */
[data-testid="stSidebarNavViewButton"], [data-testid="stSidebarNavSeparator"] {{ display: none !important; }}

/* Conteúdo extra da sidebar (botões etc.) fica no rodapé do trilho */
[data-testid="stSidebarUserContent"] {{
  position: absolute; bottom: 12px; left: 0; right: 0;
  padding: 0 8px !important;
}}
[data-testid="stSidebarUserContent"] [data-testid="stButton"],
[data-testid="stSidebarUserContent"] [data-testid="stButton"] > div,
[data-testid="stSidebarUserContent"] [data-testid="stElementContainer"] {{ width: 100% !important; }}
[data-testid="stSidebarUserContent"] button {{
  width: 100%; padding: 4px 0; font-size: 11px;
  background: transparent; color: #d6e2ef; border-color: #3b5a7c;
}}
</style>
"""
