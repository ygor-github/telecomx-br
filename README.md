# Análise e Previsão de Churn de Clientes em Empresa de Telecomunicações

## Visão Geral do Projeto

Este repositório contém o projeto de Análise Exploratória de Dados (EDA) e pré-processamento para prever o *churn* (evasão) de clientes em uma empresa de telecomunicações. O objetivo é identificar os fatores que levam os clientes a cancelar seus serviços e preparar os dados para a construção de um modelo preditivo.

O projeto foi desenvolvido em um ambiente de Jupyter Notebook e conta com um dashboard interativo construído com Streamlit para facilitar a exploração dos dados e a comunicação dos insights.

## Sobre o Projeto

Este projeto é parte de um **desafio de aprendizado** proposto pela [Alura](https://cursos.alura.com.br/), uma plataforma de cursos online focada em tecnologia. O desafio visa aplicar conhecimentos em análise de dados, pré-processamento e visualização para resolver um problema de negócio real.

**Propriedade da Informação Analisada:** É importante notar que os dados utilizados neste projeto são de natureza fictícia ou pública, fornecidos para fins educacionais e de aprendizado. Não representam dados reais de clientes de nenhuma empresa específica.

## Contexto de Negócio

Empresas de telecomunicações enfrentam o desafio constante de reter seus clientes. O *churn* de clientes é um problema crítico que afeta a receita e a sustentabilidade do negócio. Compreender os motivos por trás da evasão e ser capaz de prever quais clientes estão em risco é fundamental para implementar estratégias de retenção eficazes.

## Objetivo

* Realizar uma Análise Exploratória de Dados (EDA) detalhada para entender o perfil dos clientes e os padrões de churn.
* Pré-processar e transformar os dados brutos para torná-los adequados para a modelagem preditiva.
* Identificar as principais variáveis que impactam a decisão de churn dos clientes.
* Desenvolver um dashboard interativo para visualização e exploração dos dados e insights.

## Estrutura do Repositório


* `telecomx-br.ipynb`: Notebook Jupyter principal contendo todo o fluxo de trabalho de EDA e pré-processamento.
* `dashboard_churn.py`: Script Python para o dashboard interativo construído com Streamlit.
* `telecom_churn_processed_data.parquet`: Dataset processado e salvo, pronto para ser utilizado pelo dashboard e por futuras etapas de modelagem.
* `requirements.txt`: Contém os pacotes necessários para o deploy do dashboard.
* `graficos_interativos/`: Contém os arquivos dos gráficos interativos em formato `.html`.
* `imagens/`: Pasta para armazenar quaisquer imagens de gráficos estáticos ou capturas de tela.


## Análise Exploratória de Dados (EDA)

O Jupyter Notebook `telecomx-br.ipynb` detalha os seguintes passos:

1.  **Carregamento e Inspeção Inicial dos Dados:**
    * Verificação de tipos de dados, valores nulos e estatísticas descritivas básicas.
    * Identificação e tratamento inicial de valores ausentes (`Charges.Total`).
2.  **Engenharia de Features:**
    * Criação de novas variáveis como `Contas_Diarias` (custo diário do serviço).
3.  **Padronização e Transformação de Dados:**
    * Renomeação de colunas para nomes mais intuitivos (ex: `Meses_Contrato`, `Custo_Mensal`).
    * Conversão de variáveis categóricas binárias ('Yes'/'No') para numéricas (1/0).
    * Tratamento de categorias inconsistentes (ex: 'No internet service' mapeado para 'No').
    * Geração de um dicionário de dados detalhado.
4.  **Análise Descritiva Aprofundada:**
    * Visualização da distribuição das variáveis numéricas (histogramas, box plots).
    * Análise da proporção de churn geral.
    * Exploração da relação entre churn e variáveis categóricas (proporções).
    * Exploração da relação entre churn e variáveis numéricas (dispersão, sobreposição de histogramas).
    * Análise focada em segmentos de alto risco (ex: clientes novos com alto custo mensal).

## Dashboard Interativo (Streamlit)

 [Dashboard](https://telecomx.streamlit.app/)
 
O dashboard `dashboard_churn.py` permite uma exploração dinâmica dos insights gerados na EDA. Ele inclui:

* Visão geral da proporção de churn.
* Análise de churn por variáveis categóricas (seleção dinâmica).
* Análise de churn por variáveis numéricas (seleção dinâmica, histogramas sobrepostos).
* Gráfico de dispersão para identificar padrões de churn entre duas variáveis numéricas.
* Seção dedicada à análise de um segmento de alto risco pré-definido (clientes novos com alto custo mensal).

### Como Rodar o Dashboard

1.  **Clone este repositório:**
    ```bash
    git clone [LINK PARA O REPOSITÓRIO]
    cd nome-do-seu-repositorio
    ```
2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install pandas numpy streamlit plotly
    ```
4.  **Execute o dashboard:**
    ```bash
    streamlit run dashboard_churn.py
    ```
    Isso abrirá o dashboard automaticamente no seu navegador padrão.

## Próximos Passos (Desenvolvimento Futuro)

* Modelagem preditiva de Churn (algoritmos de Machine Learning).
* Otimização de hiperparâmetros e avaliação do modelo.
* Implantação do modelo.
* Criação de um pipeline de dados automatizado.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Autor

Ygor A. Rodríguez H.

---