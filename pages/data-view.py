import streamlit as st
from data_tools import df_wind_turbine
import plotly.express as px

# BARRA LATERAL COM FILTROS E INSTRUÇÕES
st.sidebar.header("Filtros Interativos")
st.sidebar.info(
    """
    Use os filtros abaixo para explorar os dados em períodos específicos:
    1. **Selecione um Ano:** Escolha 'Todos' para ver o dataset completo ou um ano específico.
    2. **Selecione o(s) Mês(es):** Após escolher um ano, você pode selecionar um ou mais meses para detalhar a análise.
    """
)

# Criar lista de anos, incluindo uma opção para "Todos"
anos = ["Todos"] + sorted(df_wind_turbine.index.year.unique())
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", anos)

# Filtro de meses
meses_selecionados_nomes = []
if ano_selecionado != "Todos":
    meses_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    meses_selecionados_nomes = st.sidebar.multiselect("Selecione o(s) Mês(es)", meses_nomes)

# LÓGICA DE FILTRAGEM DO DATAFRAME
df_filtrado = df_wind_turbine.copy()

# 1. Aplica o filtro de ano
if ano_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado.index.year == ano_selecionado]
    periodo_texto = f"de {ano_selecionado}"
else:
    periodo_texto = "(2017-2022)"

# 2. Aplica o filtro de mês
if meses_selecionados_nomes:
    mapa_meses = {nome: i+1 for i, nome in enumerate(meses_nomes)}
    meses_selecionados_numeros = [mapa_meses[nome] for nome in meses_selecionados_nomes]
    df_filtrado = df_filtrado[df_filtrado.index.month.isin(meses_selecionados_numeros)]
    
    # Atualiza o texto do período
    meses_str = ", ".join(meses_selecionados_nomes)
    periodo_texto = f"de {meses_str} de {ano_selecionado}"


# SEÇÃO PRINCIPAL
st.header(f"Visão Geral do Desempenho {periodo_texto}")

# Verifica se o dataframe filtrado não está vazio antes de continuar
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para o período selecionado. Por favor, ajuste os filtros.")
else:
    st.markdown(
        """ 
        <div style="text-align: justify"> 
        Os números e gráficos a seguir refletem o período selecionado nos filtros. 
        Com mais de <strong>{count} registros</strong> neste período, temos uma visão clara do comportamento da turbina. 
        O <strong>percentual de anomalias<strong> indica a frequência de operações fora do padrão, enquanto os gráficos detalham a geração de energia e a distribuição dos estados operacionais.
        </div> 
        """.format(count=f"{df_filtrado.shape[0]:,}").replace(",", "."),
        unsafe_allow_html=True
    )

    kpi1, kpi2 = st.columns(2)

    total_registros = df_filtrado.shape[0]
    perc_anomalias = df_filtrado['failure'].mean() * 100

    kpi1.metric(
        label="Total de Registros (minutos)",
        value=f"{total_registros:,}".replace(",", ".")
    )

    kpi2.metric(
        label="Percentual de Anomalias (%)",
        value=f"{perc_anomalias:.2f}",
        delta=f"{perc_anomalias:.2f}% do tempo em estado não-ideal",
        delta_color="inverse",
        help="Percentual de registros onde a turbina, a rede ou o sistema não estavam em estado perfeitamente normal."
    )

    st.markdown("---")

    # --- Gráfico Principal ---
    st.subheader("Distribuição de Anomalias ao Longo do Tempo")

    # Resample por mês para visualização
    df_resampled = df_filtrado.resample('M')['failure'].value_counts().unstack(fill_value=0)
    df_resampled.rename(columns={0: 'Normal', 1: 'Anomalia'}, inplace=True)

    fig_anomalias_tempo = px.bar(
        df_resampled,
        x=df_resampled.index,
        y=['Normal', 'Anomalia'],
        title="Contagem de Registros Normais vs. Anômalos por Mês",
        labels={'value': 'Contagem de Registros', 'log_time': 'Data'},
        color_discrete_map={'Normal': '#1f77b4', 'Anomalia': '#ff7f0e'},
        template='plotly_white'
    )

    st.plotly_chart(fig_anomalias_tempo, use_container_width=True)

    st.markdown("""
    A análise revelou que a turbina opera em estado de anomalia na maior parte do tempo. 
    O gráfico acima mostra como essas ocorrências se distribuem, permitindo-nos identificar períodos 
    de maior instabilidade operacional.
    """)

    st.markdown("---")
    