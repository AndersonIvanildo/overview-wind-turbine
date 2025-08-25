import streamlit as st
from data_tools import df_wind_turbine

# INÍCIO DA APLICAÇÃO

st.title("🌬️ Análise Interativa de Dados de Turbina Eólica Urbana")
st.markdown("---")
st.header("Sobre o Projeto e o Conjunto de Dados")

st.write("""
Esta aplicação apresenta uma análise exploratória e interativa dos dados operacionais de uma turbina eólica de pequeno porte, 
localizada em um ambiente urbano na cidade de São Paulo, Brasil. 
A análise foi originalmente realizada em um ambiente de notebook (Google Colab) e agora é apresentada de forma interativa com o Streamlit.
""")

st.subheader("Origem dos Dados")
st.info("""
Os dados, intitulados **"Operation SCADA Data of an Urban Small Wind Turbine in São Paulo, Brazil"**, foram coletados pelo 
Instituto de Energia e Ambiente da Universidade de São Paulo (IEE-USP). Eles representam registros do sistema SCADA 
(Supervisory Control and Data Acquisition) da turbina modelo Skystream 3.7, gravados a cada minuto entre os anos de 2017 e 2022.

**DOI do dataset original:** [10.5281/zenodo.7348454](https://doi.org/10.5281/zenodo.7348454)
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Processamento e Escopo")
    st.write("""
    O conjunto de dados inicial continha **1.443.381 registros** e **39 variáveis**. Após um rigoroso processo de pré-processamento, que incluiu:
    - Remoção de colunas constantes ou acumulativas.
    - Análise e tratamento de variáveis de status.
    - Engenharia de uma variável alvo (`failure`) para detecção de anomalias.
    
    O dataset final utilizado nesta análise foi consolidado em **24 variáveis preditoras** e **1 variável alvo**, mantendo todos os registros originais.
    """)

with col2:
    st.subheader("A Variável Alvo: `failure`")
    st.write("""
    Para treinar um modelo de detecção de anomalias, foi criada a coluna `failure`. Ela é definida com base nos códigos de status da turbina, da rede e do sistema:

    - **Normal (0):** A turbina, a rede e o sistema estão operando em seus estados normais.
    - **Anomalia (1):** Qualquer desvio em um desses status, indicando uma possível falha ou operação fora do padrão.
    
    Isso resultou em um dataset com aproximadamente **24%** de amostras normais e **76%** de anomalias.
    """)

st.markdown("---")

st.header("Pré-visualização dos Dados Finais")
st.write("Abaixo estão as primeiras linhas do dataset final, pronto para a modelagem e visualização.")
st.dataframe(df_wind_turbine.head())
st.page_link("pages/data-view.py", label="Ir para o Dashboard", icon="📊")