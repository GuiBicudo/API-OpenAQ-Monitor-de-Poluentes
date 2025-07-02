import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ast

csv_file = "medicoes_copacabana_7dias_raio.csv"

df = pd.read_csv(csv_file, header=0)

df.rename(columns={
    'flagInfo': 'flags_raw',
    'parameter': 'parameter_raw',
    'date': 'date_info_raw_old',
    'period': 'period_raw',
    'coordinates': 'empty1',
    'summary': 'empty2',
    'coverage': 'meta_info_raw'
}, inplace=True)

print("--- Primeiras 5 linhas do DataFrame (após ler com cabeçalho e renomear) ---")
print(df.head())
print("\n--- Nomes das colunas ---")
print(df.columns)
print("\n--- Informações do DataFrame (tipos de dados e nulos) ---")
print(df.info())

def clean_string_dict(s):
    if pd.isna(s):
        return s
    if isinstance(s, str):
        if s.startswith('"') and s.endswith('"') and s.count('"') > 1: 
             s = s[1:-1]
        s = s.replace('""', '"') 
    return s

if 'parameter_raw' in df.columns:
    df['parameter_raw_cleaned'] = df['parameter_raw'].apply(clean_string_dict)
if 'period_raw' in df.columns:
    df['date_info_raw_cleaned'] = df['period_raw'].apply(clean_string_dict)
if 'flags_raw' in df.columns:
    df['flags_raw_cleaned'] = df['flags_raw'].apply(clean_string_dict)
if 'meta_info_raw' in df.columns:
    df['meta_info_raw_cleaned'] = df['meta_info_raw'].apply(clean_string_dict)

if 'parameter_raw_cleaned' in df.columns and not df['parameter_raw_cleaned'].empty:
    df['parameter_dict'] = df['parameter_raw_cleaned'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.strip().startswith('{') else None # strip() para remover espaços em branco
    )
    df["poluente_name_raw"] = df['parameter_dict'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
    df["unit"] = df['parameter_dict'].apply(lambda x: x.get('units') if isinstance(x, dict) else None)
else:
    df["poluente_name_raw"] = None
    df["unit"] = None

if 'date_info_raw_cleaned' in df.columns and not df['date_info_raw_cleaned'].empty:
    df['date_info_dict'] = df['date_info_raw_cleaned'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.strip().startswith('{') else None
    )
    df['utc_time'] = df['date_info_dict'].apply(lambda x: x.get('datetimeFrom', {}).get('utc') if isinstance(x, dict) else None)
else:
    df['utc_time'] = None

df["utc_time"] = pd.to_datetime(df["utc_time"], errors='coerce')

traducao = {
    "pm25": "Material Particulado Fino (PM2.5)",
    "pm10": "Material Particulado Grosso (PM10)",
    "so2": "Dióxido de Enxofre (SO₂)",
    "o3": "Ozônio (O3)",
    "co": "Monóxido de Carbono (CO)",
    "no": "Óxido Nítrico (NO)",
    "no2": "Dióxido de Nitrogênio (NO2)",
    "nox": "Óxidos de Nitrogênio (NOx)"
}

df["poluente_nome"] = df["poluente_name_raw"].map(traducao).fillna(df["poluente_name_raw"])

df['value'] = pd.to_numeric(df['value'], errors='coerce')

df.dropna(subset=['utc_time', 'value', 'poluente_nome'], inplace=True)


print("\n--- Contagem de medições por tipo de poluente (nomes traduzidos) ---")
print(df["poluente_nome"].value_counts())

print("\n--- Período de cobertura dos dados (usando utc_time) ---")
print(f"Início dos dados: {df['utc_time'].min()}")
print(f"Fim dos dados: {df['utc_time'].max()}")

if df.empty:
    print("\n--- ERRO: DataFrame VAZIO após a limpeza dos dados. Não é possível gerar gráficos. ---")
    print("Isso pode indicar que não há dados válidos no CSV, ou que o parser falhou para todas as linhas.")
    exit()

# Gráficos

# Gráfico 1
plt.figure(figsize=(10, 6))
df["poluente_nome"].value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Quantidade de Medições por Tipo de Poluente em Copacabana (Últimos 7 Dias)", fontsize=16)
plt.xlabel("Poluente", fontsize=14)
plt.ylabel("Quantidade de Medições", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# Gráfico 2
if not df.empty and 'utc_time' in df.columns:
    poluentes_unicos = df["poluente_nome"].unique()

    poluentes_para_plotar = [p for p in poluentes_unicos if not df[df["poluente_nome"] == p]['value'].isnull().all()]

    if len(poluentes_para_plotar) > 0:
        num_poluentes = len(poluentes_para_plotar)
        fig, axes = plt.subplots(num_poluentes, 1, figsize=(13, 5 * num_poluentes), sharex=True, squeeze=False)

        for i, poluente in enumerate(poluentes_para_plotar):
            df_poluente = df[df["poluente_nome"] == poluente].sort_values(by="utc_time")

            current_unit = df_poluente['unit'].iloc[0] if not df_poluente['unit'].empty else 'N/A'

            axes[i, 0].plot(df_poluente["utc_time"], df_poluente["value"], marker='.', linestyle='-', markersize=2, alpha=0.7)
            axes[i, 0].set_title(f"Nível de {poluente} ao longo do Tempo", fontsize=10)
            axes[i, 0].set_ylabel(f"Nível ({current_unit})", fontsize=8)

            axes[i, 0].xaxis.set_major_locator(mdates.AutoDateLocator())
            axes[i, 0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            axes[i, 0].grid(True, linestyle='--', alpha=0.6)

        fig.autofmt_xdate(rotation=45)
        plt.xlabel("Data e Hora (UTC)", fontsize=10)
        plt.tight_layout()
        plt.show()

    else:
        print("Nenhum poluente com dados válidos para plotar séries temporais após a limpeza.")
else:
    print("Não foi possível gerar gráficos de série temporal sem dados válidos ou coluna 'utc_time'.")

print("\nAnálise e geração de gráficos concluídas.")