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

    st.header("Capítulo 2: O Coração da Turbina - Performance")

    st.markdown("""
    A performance de uma turbina é medida por sua capacidade de converter a energia do vento em eletricidade. 
    As variáveis `power_out`, `rpm` e `windspeed_(ref)` são os indicadores mais diretos dessa eficiência.
    """)

    # --- Gráfico 1: Curva de Potência ---
    st.subheader("Curva de Potência: Velocidade do Vento vs. Energia Gerada")

    fig_power_curve = px.scatter(
        df_filtrado,
        x='windspeed_(ref)',
        y='power_out',
        title='Curva de Potência',
        labels={'windspeed_(ref)': 'Velocidade do Vento (m/s)', 'power_out': 'Potência de Saída (W)'},
        template='plotly_white',
        opacity=0.5
    )
    st.plotly_chart(fig_power_curve, use_container_width=True)
    st.markdown("""
    A curva de potência ilustra a relação entre a velocidade do vento e a energia gerada. 
    Pontos fora do padrão esperado podem indicar ineficiências ou falhas.
    """)


    # --- Gráfico 2: RPM vs. Tensão ---
    st.subheader("Relação entre RPM e Tensão de Entrada")

    fig_rpm_voltage = px.scatter(
        df_filtrado,
        x='rpm',
        y='voltage_in',
        title='Tensão Real vs. Tensão Mínima Esperada',
        labels={'rpm': 'Rotação por Minuto (RPM)', 'voltage_in': 'Tensão (V)'},
        opacity=0.3,
        template='plotly_white'
    )

    # Adicionando a curva de tensão mínima esperada
    fig_rpm_voltage.add_scatter(
        x=df_filtrado['rpm'],
        y=df_filtrado['min_v_from_rpm'],
        mode='markers',
        name='Tensão Mínima Esperada',
        marker=dict(color='orange', opacity=0.3)
    )

    st.plotly_chart(fig_rpm_voltage, use_container_width=True)
    st.markdown("""
    A tensão gerada (`voltage_in`, azul) deve ser superior a um mínimo esperado (`min_v_from_rpm`, laranja) 
    para uma dada rotação. Pontos azuis abaixo da curva laranja podem sinalizar problemas na geração de energia.
    """)