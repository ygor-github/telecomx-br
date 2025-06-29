import streamlit as st
import pandas as pd
import plotly.express as px






# --- Configurações da Página ---
st.set_page_config(
    page_title="Dashboard de Análise de Churn de Telecom",
    page_icon="📊",
    layout="wide", # Permite que o conteúdo ocupe toda a largura da página
)

# --- Função Auxiliar para Plotar Gráficos de Categoria no Segmento ---
def plot_segment_category(df_segment, col_name):
    # Tratar colunas binárias para mostrar 'Sim'/'Não' se for o caso
    if df_segment[col_name].dtype in ['int64', 'float64'] and df_segment[col_name].nunique() <= 2:
        value_counts = df_segment[col_name].value_counts(normalize=True) * 100
        data_to_plot = pd.DataFrame({
            'Categoria': ['Não' if v == 0 else 'Sim' for v in value_counts.index],
            'Porcentagem': value_counts.values
        })
        title = f'Distribuição de {col_name.replace("_", " ")}'
        fig = px.bar(
            data_to_plot,
            x='Categoria',
            y='Porcentagem',
            title=title,
            labels={'Porcentagem': 'Porcentagem', 'Categoria': col_name.replace("_", " ")},
            template='plotly_white'
        )
    else: # Para colunas categóricas (object) com mais de 2 categorias
        value_counts = df_segment[col_name].value_counts(normalize=True) * 100
        data_to_plot = value_counts.reset_index()
        data_to_plot.columns = ['Categoria', 'Porcentagem']
        title = f'Distribuição de {col_name.replace("_", " ")}'
        fig = px.bar(
            data_to_plot,
            x='Categoria',
            y='Porcentagem',
            title=title,
            labels={'Porcentagem': 'Porcentagem', 'Categoria': col_name.replace("_", " ")},
            template='plotly_white'
        )
    st.plotly_chart(fig, use_container_width=True)       



# --- Carregamento dos Dados ---
@st.cache_data # Decorador para cachear os dados e evitar recarregamento a cada interação
def load_data():
    try:
        df = pd.read_parquet('telecom_churn_processed_data.parquet')
        return df
    except FileNotFoundError:
        st.error("Erro: O arquivo 'telecom_churn_processed_data.parquet' não foi encontrado. Certifique-se de que ele está na mesma pasta que este script.")
        st.stop() # Interrompe a execução do script se o arquivo não for encontrado

df = load_data()

# --- Título do Dashboard ---
st.title("📊 Análise Exploratória de Churn de Clientes de Telecom")
st.markdown("""
Este dashboard permite explorar a distribuição da variável Churn e sua relação com diversas características dos clientes.
""")


# Paleta de cores personalizada
paleta_cores = {
    'Sim': '#FF5A3C',      # rojo fuerte
    'Não': '#7079FF',      # azul vibrante
    '1': '#FF5A3C',
    '0': '#7079FF',
    'Feminino': '#FF5A3C',
    'Masculino': '#7079FF',
    'Yes': '#FF5A3C',
    'No': '#7079FF'
}


# --- 1. Visão Geral da Distribuição de Churn ---
st.header("1. Distribuição Geral do Churn")

# Calcular porcentagem de churn
churn_counts = df['Churn'].value_counts(normalize=True) * 100

# Traduzir 0 → Não, 1 → Sim
churn_data = pd.DataFrame({
    'Evasão': ['Não' if c == 0 else 'Sim' for c in churn_counts.index],
    'Porcentagem': churn_counts.values
})

# Criar gráfico de pizza com estilo
fig_churn_pie = px.pie(
    churn_data,
    values='Porcentagem',
    names='Evasão',
    title='Proporção de Clientes com Churn vs. Sem Churn',
    color='Evasão',
    color_discrete_map={
        'Sim': paleta_cores['Sim'],
        'Não': paleta_cores['Não']
    },
    hole=0  # sem donut
)

# Atualizar layout dos rótulos
fig_churn_pie.update_traces(
    textinfo='percent',
    textfont=dict(color='white', size=18, family='Arial'),
    insidetextfont=dict(color='white', size=18, family='Arial'),
    textposition='inside'
)

# Mostrar gráfico no Streamlit
st.plotly_chart(fig_churn_pie, use_container_width=True)

# Observação
st.markdown("""
**Observação:** A proporção de clientes que evadiram (`Churn = Sim`) em relação aos que permaneceram (`Churn = Não`) é um insight inicial crucial para entender a magnitude do problema de churn na base de clientes.
""")

# --- 2. Análise de Churn por Variáveis Categóricas ---
st.header("2. Churn por Variáveis Categóricas")

# Identificar colunas categóricas
categorical_cols = df.select_dtypes(include='object').columns.tolist()
all_binary_cols_names = [
    'Cliente_Senior', 'Tem_Parceiro', 'Tem_Dependentes', 'Servico_Telefone',
    'Multiplas_Linhas', 'Seguranca_Online', 'Backup_Online', 'Protecao_Dispositivo',
    'Suporte_Tecnico', 'Streaming_TV', 'Streaming_Filmes', 'Fatura_Digital'
]
categorical_cols_for_display = [col for col in df.columns if col in all_binary_cols_names + ['Genero', 'Servico_Internet', 'Tipo_Contrato', 'Metodo_Pagamento']]
categorical_cols_for_display = [col for col in categorical_cols_for_display if col not in ['ID_Cliente', 'Churn']]

selected_category = st.selectbox(
    "Selecione uma Variável Categórica para Analisar Churn:",
    options=categorical_cols_for_display
)

if selected_category:
    churn_by_category = df.groupby(selected_category)['Churn'].value_counts(normalize=True).unstack() * 100
    churn_by_category = churn_by_category.fillna(0)
    churn_by_category.columns = ['Não Churn', 'Sim Churn']
    churn_by_category = churn_by_category.reset_index()

    # Gráfico com Plotly
    fig_cat_churn = px.bar(
        churn_by_category,
        x=selected_category,
        y=['Não Churn', 'Sim Churn'],
        title=f'Proporção de Churn por {selected_category.replace("_", " ")}',
        labels={'value': 'Porcentagem de Clientes', 'variable': 'Evasão'},
        barmode='group',
        color_discrete_map={
            'Não Churn': paleta_cores['Não'],
            'Sim Churn': paleta_cores['Sim']
        }
    )

    # Estilo do texto das barras: branco, 18px, negrito
    fig_cat_churn.update_traces(
        texttemplate='%{y:.1f}%',
        textposition='outside',
        textfont=dict(
            color='white',
            size=18,
            family='Arial'
        )
    )

    # Layout escuro e sem grid
    fig_cat_churn.update_layout(
        yaxis_title='Porcentagem de Clientes',
        legend_title='Evasão',
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='white'),
        yaxis=dict(showgrid=False, color='white'),
        xaxis=dict(tickmode='linear', color='white'),
        title_font=dict(color='white')
    )

    fig_cat_churn.update_traces(
    texttemplate='%{y:.1f}%',
    textposition='inside',
    textfont=dict(
        color='white',
        size=18,
        family='Arial'
    )
)

    # Mostrar gráfico
    st.plotly_chart(fig_cat_churn, use_container_width=True)

    # Observação
    st.markdown(f"""
    **Insights para {selected_category.replace("_", " ")}:** Este gráfico de barras mostra como a proporção de churn (`Sim Churn`) varia entre as diferentes categorias de `{selected_category.replace("_", " ")}`. Permite identificar segmentos de clientes com maior ou menor propensão a evadir.
    """)

# --- 3. Análise de Churn por Variáveis Numéricas ---
st.header("3. Churn por Variáveis Numéricas")

numeric_cols = ['Meses_Contrato', 'Custo_Mensal', 'Custo_Total', 'Custo_Diario']

selected_numeric = st.selectbox(
    "Selecione uma Variável Numérica para Analisar Churn:",
    options=numeric_cols
)

if selected_numeric:
    fig_num_churn = px.histogram(
        df,
        x=selected_numeric,
        color='Churn',
        nbins=50,
        histnorm='percent',
        title=f'Distribuição de {selected_numeric.replace("_", " ")} por Churn',
        labels={selected_numeric: selected_numeric.replace("_", " "), 'count': 'Porcentagem de Clientes', 'Churn': 'Evasão'},
        template='plotly_white',
        barmode='overlay'
    )
    # Ajustar a legenda para 'Não' e 'Sim'
    fig_num_churn.for_each_trace(lambda t: t.update(name = "Sim" if t.name == "1" else "Não"))

    fig_num_churn.update_layout(
        yaxis_title='Porcentagem de Clientes',
        legend_title='Evasão',
        hovermode='x unified'
    )
    st.plotly_chart(fig_num_churn, use_container_width=True)

    st.markdown(f"""
    **Insights para {selected_numeric.replace("_", " ")}:** Este histograma mostra a distribuição de `{selected_numeric.replace("_", " ")}` para clientes que evadiram (`Sim`) e não evadiram (`Não`). Permite observar se há faixas de valores numéricos que estão mais associadas ao comportamento de churn.
    """)
    
    # --- 4. Análise de Causa Direta: Gráfico de Dispersão ---
    st.header("4. Análise de Dispersão (Potenciais Causas de Churn)")
    st.markdown("""
    Este gráfico de dispersão permite visualizar a relação entre duas variáveis numéricas e a evasão (Churn).
    Ao observar a distribuição dos pontos coloridos por Churn (0=Não, 1=Sim), é possível identificar clusters ou regiões onde a evasão é mais comum, sugerindo potenciais combinações de fatores que levam ao Churn.
    """)

    # Colunas numéricas disponíveis para os eixos X e Y
    scatter_numeric_cols = ['Meses_Contrato', 'Custo_Mensal', 'Custo_Total', 'Custo_Diario']

    col1, col2 = st.columns(2)

    with col1:
        x_axis_col = st.selectbox(
            "Selecione a Variável para o Eixo X:",
            options=scatter_numeric_cols,
            index=0 # Default para Meses_Contrato
        )
    with col2:
        y_axis_col = st.selectbox(
            "Selecione a Variável para o Eixo Y:",
            options=scatter_numeric_cols,
            index=1 # Default para Custo_Mensal
        )

    if x_axis_col and y_axis_col:
        fig_scatter = px.scatter(
            df,
            x=x_axis_col,
            y=y_axis_col,
            color='Churn',
            title=f'Dispersão de {x_axis_col.replace("_", " ")} vs. {y_axis_col.replace("_", " ")} por Churn',
            labels={
                x_axis_col: x_axis_col.replace("_", " "),
                y_axis_col: y_axis_col.replace("_", " ")
            },
            template='plotly_white',
            hover_data=['ID_Cliente'] # Opcional: Mostra o ID do cliente ao passar o mouse
        )
        # Ajustar a legenda para 'Não' e 'Sim'
        fig_scatter.for_each_trace(lambda t: t.update(name = "Sim" if t.name == "1" else "Não"))

        fig_scatter.update_layout(
            legend_title='Evasão',
            hovermode='closest' # Melhor para gráficos de dispersão
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown(f"""
        **Observações para a Dispersão de {x_axis_col.replace("_", " ")} vs. {y_axis_col.replace("_", " ")}:**
        * Observe a concentração dos pontos `Sim` (Evasão) em certas áreas do gráfico. Isso pode indicar combinações de `Meses_Contrato` e `Custo_Mensal` (ou outras variáveis) que são mais arriscadas.
        * Por exemplo, uma alta concentração de pontos `Sim` com `Meses_Contrato` baixo e `Custo_Mensal` alto sugere que clientes novos com altos gastos tendem a evadir.
        """)
 

import numpy as np
import plotly.express as px
from matplotlib.colors import to_rgb
import streamlit as st

# Paleta de cores personalizada
paleta_cores = {
    'Sim': '#FF5A3C',      # rojo fuerte
    'Não': '#7079FF',      # azul vibrante
    '1': '#FF5A3C',
    '0': '#7079FF',
    'Feminino': '#FF5A3C',
    'Masculino': '#7079FF',
    'Yes': '#FF5A3C',
    'No': '#7079FF'
}

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(
        int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
    )

def gerar_mapa_cores_degradado(df, coluna, paleta):
    prop = df[coluna].value_counts(normalize=True).sort_values(ascending=False)
    categorias_ordenadas = prop.index.tolist()

    cor_vermelha = np.array(to_rgb(paleta['Sim']))   # rojo puro
    cor_azul = np.array(to_rgb(paleta['Não']))       # azul puro
    n = len(categorias_ordenadas)
    if n > 1:
        degradado_rgb = [
            cor_vermelha + (cor_azul - cor_vermelha) * i/(n-1)
            for i in range(n)
        ]
    else:
        degradado_rgb = [cor_vermelha]

    degradado_hex = [rgb_to_hex(c) for c in degradado_rgb]
    return dict(zip(categorias_ordenadas, degradado_hex))

def plot_segment_category(df_segment, coluna):
    dados = df_segment.copy()

    valores_unicos = set(dados[coluna].dropna().unique())
    if valores_unicos <= {0, 1}:
        dados[coluna] = dados[coluna].map({1: 'Sim', 0: 'Não'})

    prop = dados[coluna].value_counts(normalize=True).reset_index()
    prop.columns = [coluna, 'Proporção']

    if coluna in ['Metodo_Pagamento', 'Tipo_Contrato', 'Servico_Internet']:
        color_map = gerar_mapa_cores_degradado(dados, coluna, paleta_cores)
    else:
        color_map = paleta_cores

    fig = px.bar(
        prop,
        x='Proporção',
        y=coluna,
        orientation='h',
        color=coluna,
        color_discrete_map=color_map,
        text='Proporção',
        template='plotly_white'
    )
    fig.update_layout(
        showlegend=False,
        height=300,
        margin=dict(l=40, r=10, t=30, b=30),
        xaxis_tickformat='.0%',
        xaxis_title=None
    )
    fig.update_traces(
        texttemplate='%{text:.0%}',
        textposition='inside',
        textfont=dict(color='white', size=16, family='Arial')
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 5. Análise de Segmento Específico: Clientes Novos com Alto Custo Mensal ---
st.header("5. Análise de Clientes Novos com Alto Custo Mensal")
st.markdown("""
Esta seção foca em um segmento de clientes particularmente propenso ao churn:  
**Clientes com `Meses_Contrato` baixo (<= 5 meses) e `Custo_Mensal` alto (>= 70 R$).**  
Vamos analisar as características comuns deste grupo.
""")

limite_meses_contrato_novo = 5
limite_custo_mensal_alto = 70

clientes_segmento_risco = df[
    (df['Meses_Contrato'] <= limite_meses_contrato_novo) &
    (df['Custo_Mensal'] >= limite_custo_mensal_alto)
]

if not clientes_segmento_risco.empty:
    st.subheader(f"Visão Geral do Segmento (N = {len(clientes_segmento_risco)} clientes)")
    st.write(f"**Taxa de Churn neste segmento:** {clientes_segmento_risco['Churn'].mean() * 100:.2f}%")
    st.write(f"**Custo Mensal Médio:** {clientes_segmento_risco['Custo_Mensal'].mean():.2f} R$")
    st.write(f"**Meses de Contrato Médio:** {clientes_segmento_risco['Meses_Contrato'].mean():.2f} meses")

    st.subheader("Distribuição de Características Categóricas no Segmento de Risco")

    categorical_cols_for_segment_analysis = [
        'Genero', 'Servico_Internet', 'Tipo_Contrato', 'Metodo_Pagamento',
        'Cliente_Senior', 'Tem_Parceiro', 'Tem_Dependentes', 'Servico_Telefone',
        'Multiplas_Linhas', 'Seguranca_Online', 'Backup_Online', 'Protecao_Dispositivo',
        'Suporte_Tecnico', 'Streaming_TV', 'Streaming_Filmes', 'Fatura_Digital'
    ]

    col_cat1, col_cat2 = st.columns(2)
    current_col = 0

    for col in categorical_cols_for_segment_analysis:
        if current_col % 2 == 0:
            with col_cat1:
                plot_segment_category(clientes_segmento_risco, col)
        else:
            with col_cat2:
                plot_segment_category(clientes_segmento_risco, col)
        current_col += 1

    st.markdown("""
    **Insights para o Segmento de Risco:** Os gráficos acima revelam as proporções de cada característica dentro do grupo de clientes novos com alto custo mensal. Observe quais categorias são mais prevalentes para entender melhor o perfil desses clientes de alto risco.
    """)
else:
    st.warning("Não há clientes que correspondam aos critérios de 'Novo com Alto Custo Mensal'. Ajuste os limites ou verifique os dados.")


# --- Rodapé ---
st.markdown("---")
st.markdown("Dashboard criado para análise exploratória de dados de Churn de Telecom.")