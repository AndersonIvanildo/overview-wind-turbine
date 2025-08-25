from pathlib import Path
import streamlit as st
import pandas as pd

# VARIÁVEIS ÚTEIS PARA A APLICAÇÃO
path_df_wind_turbine = Path.cwd() / "data" / "df_wind-turbine.parquet"

# CARREGAMENTO DOS DADOS
@st.cache_data
def carregar_dados(caminho_parquet):
    """
    Função para carregar os dados do arquivo Parquet, otimizada com cache.
    """
    df = pd.read_parquet(caminho_parquet)
    if not isinstance(df.index, pd.DatetimeIndex):
        if 'log_time' in df.columns:
            df['log_time'] = pd.to_datetime(df['log_time'])
            df.set_index('log_time', inplace=True)
    return df

df_wind_turbine = carregar_dados(path_df_wind_turbine)