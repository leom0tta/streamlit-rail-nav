# streamlit-rail-nav

Sidebar do Streamlit em formato **trilho + painel**: um trilho estreito com o ícone de cada categoria e, ao passar o mouse, um painel ao lado com as páginas daquela categoria, aberto por cima do conteúdo (relatórios e iframes não são empurrados).

A navegação continua sendo a nativa do `st.navigation`. O pacote só organiza as seções e aplica CSS.

## Instalação

No `requirements.txt` do app, travado numa versão:

```
streamlit-rail-nav @ git+https://github.com/<seu-usuario>/streamlit-rail-nav@v0.1.0
```

Ou localmente: `pip install -e .` na pasta deste repositório.

## Uso

```python
import streamlit as st
from rail_nav import rail_navigation

st.set_page_config(page_title="Meu app", layout="wide")

pagina = rail_navigation(
    inicio=st.Page("Home.py", title="Início", icon=":material/home:", default=True),
    secoes={
        ("Comercial", "groups"): [
            st.Page("pages/crm.py", title="CRM", icon=":material/contacts:"),
        ],
        ("Receita", "payments"): [
            st.Page("pages/receita_mes.py", title="Receita no Mês", icon=":material/calendar_month:"),
        ],
    },
    logo="logo.png",
)
pagina.run()
```

- Cada chave de `secoes` é `(título, ícone)`. O ícone é um nome do [Material Symbols](https://fonts.google.com/icons), como `groups` ou `payments`.
- Quando o app usa `st.navigation`, o Streamlit ignora a navegação automática da pasta `pages/`.
- Botões colocados com `st.sidebar.button(...)` (ex.: Logout) ficam no rodapé do trilho.

## Personalizar

```python
from rail_nav import Tema

tema = Tema(cor_trilho="#0b3d2e", cor_trilho_ativo="#145c45", atraso_fechar_ms=500)
pagina = rail_navigation(secoes=..., tema=tema)
```

| Campo | Padrão | O que faz |
|---|---|---|
| `largura_trilho` | 88 | largura do trilho (px) |
| `largura_painel` | 300 | largura do painel (px) |
| `topo_painel` | 0 | distância do topo da tela até o painel (px) |
| `cor_trilho` / `cor_trilho_ativo` | `#16324f` / `#24476b` | fundo do trilho / da categoria ativa |
| `cor_painel`, `cor_texto_painel`, `cor_titulo_painel`, `cor_hover_link` | tons claros | cores do painel |
| `atraso_abrir_ms` | 150 | tempo parado numa categoria antes de trocar o painel |
| `atraso_fechar_ms` | 350 | tolerância antes de fechar o painel quando o mouse sai |

Para montar o `st.navigation` por conta própria, use só o CSS com `aplicar_estilo(["Comercial", "Receita"], tema)`, passando os títulos na mesma ordem das seções.

## Limitações

- **Versão do Streamlit:** o CSS depende do HTML interno do Streamlit, por isso o pacote exige `streamlit>=1.67,<1.68`. Para liberar uma versão nova do Streamlit: testar o exemplo, ajustar o CSS se precisar, mudar o limite no `pyproject.toml` e criar uma tag nova.
- O painel abre ao passar o mouse, não ao clicar. Em telas de toque, o comportamento depende do navegador.
- Uma seção comporta até 20 páginas.

## Exemplo

```
pip install -e .
cd exemplo
streamlit run app.py
```
