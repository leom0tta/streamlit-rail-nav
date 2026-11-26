"""
rail_nav — sidebar do Streamlit em formato "trilho + painel".

Um trilho estreito com o ícone de cada categoria; ao passar o mouse, abre um
painel ao lado (por cima do conteúdo) com as páginas daquela categoria.
Funciona só com CSS sobre a navegação nativa do st.navigation.

Uso mínimo:

    import streamlit as st
    from rail_nav import rail_navigation

    st.set_page_config(page_title="Meu app", layout="wide")
    pagina = rail_navigation(
        secoes={
            ("Comercial", "groups"): [st.Page("pages/crm.py", title="CRM", icon=":material/contacts:")],
        },
        inicio=st.Page("Home.py", title="Início", icon=":material/home:", default=True),
        logo="logo.png",
    )
    pagina.run()
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional, Sequence

import streamlit as st

from ._css import montar_css

__all__ = ["Tema", "rail_navigation", "aplicar_estilo"]
__version__ = "0.1.4"


@dataclass(frozen=True)
class Tema:
    """Cores, tamanhos e tempos do trilho. Troque só o que precisar:
    Tema(cor_trilho="#0b3d2e")"""

    largura_trilho: int = 88          # px
    largura_painel: int = 300         # px
    topo_painel: int = 0              # px, distância do topo da tela até o painel
    cor_trilho: str = "#16324f"
    cor_trilho_ativo: str = "#24476b"  # categoria sob o mouse / da página atual
    cor_painel: str = "#ffffff"
    cor_texto_painel: str = "#1f2937"
    cor_titulo_painel: str = "#111827"
    cor_hover_link: str = "#eef2f7"
    atraso_abrir_ms: int = 150        # espera antes de trocar de categoria
    atraso_fechar_ms: int = 350       # tolerância antes de fechar o painel

    # Fonte e ícones
    fonte: Optional[str] = None       # família do Google Fonts, ex.: "Inter", "Nunito Sans".
                                      # None = fonte padrão do Streamlit (Source Sans)
    peso_texto: int = 400             # nomes no trilho e links do painel (300 = mais leve)
    peso_titulo: int = 600            # título do painel e página atual
    icones_negrito: bool = False      # False = traço fino (300); True = grosso (600)
    peso_icone: Optional[int] = None  # 100–700; se informado, ignora icones_negrito
    estilo_icone: str = "outlined"    # "outlined", "rounded" ou "sharp"
    carregar_google_fonts: bool = True  # False se o ambiente bloquear fonts.googleapis.com

    # Visual
    estilo: str = "padrao"            # "padrao" ou "apple_tv" (vidro escuro, pílula no hover)

    # Só para estilo="apple_tv"
    cor_destaque: str = "#f5f5f7"     # pílula do item sob o mouse
    cor_texto_destaque: Optional[str] = None  # texto sobre a pílula (None = cor_trilho)
    vidro_opacidade: float = 0.55     # 0 = vidro transparente, 1 = sólido
    vidro_desfoque: int = 32          # px de desfoque do que está atrás

    def com(self, **mudancas) -> "Tema":
        """Cópia do tema com alguns valores trocados."""
        return replace(self, **mudancas)


def rail_navigation(
    secoes: dict,
    inicio: Optional["st.Page"] = None,
    logo: Optional[str] = None,
    tema: Optional[Tema] = None,
):
    """Monta o st.navigation com as seções, aplica o estilo e devolve a página
    selecionada. Chame .run() no retorno.

    secoes: {("Título", "nome_do_icone_material"): [st.Page, ...], ...}
            O ícone é o nome do Material Symbols, ex.: "groups", "payments".
    inicio: página solta no topo do trilho (opcional).
    logo:   caminho/URL da imagem do topo do trilho (opcional).
    tema:   Tema(...) para trocar cores, larguras e tempos (opcional).
    """
    if not secoes:
        raise ValueError("Informe ao menos uma seção.")

    nav: dict[str, list] = {}
    if inicio is not None:
        nav[""] = [inicio]
    titulos: list[str] = []
    for chave, paginas in secoes.items():
        titulo, icone = _ler_chave(chave)
        rotulo = f":material/{icone}: {titulo}" if icone else titulo
        if rotulo in nav:
            raise ValueError(f"Seção repetida: {titulo!r}")
        nav[rotulo] = list(paginas)
        titulos.append(titulo)

    if logo:
        st.logo(logo, size="large")
    pagina = st.navigation(nav)
    aplicar_estilo(titulos, tema)
    return pagina


def aplicar_estilo(titulos_secoes: Sequence[str], tema: Optional[Tema] = None) -> None:
    """Só o CSS, para quem prefere montar o st.navigation por conta própria.
    titulos_secoes: títulos das seções na mesma ordem do dict do st.navigation
    (sem a seção vazia "")."""
    st.markdown(montar_css(tema or Tema(), list(titulos_secoes)), unsafe_allow_html=True)


def _ler_chave(chave) -> tuple[str, str]:
    if isinstance(chave, tuple) and len(chave) == 2:
        return str(chave[0]), str(chave[1] or "")
    if isinstance(chave, str):
        return chave, ""
    raise TypeError(
        "Cada chave de 'secoes' deve ser (título, ícone) ou só o título. "
        f"Recebido: {chave!r}"
    )
