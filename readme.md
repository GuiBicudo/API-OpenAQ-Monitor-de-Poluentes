# Monitor de Poluentes

Este projeto Python coleta, processa e visualiza dados de qualidade do ar de diversas localizações, utilizando a API OpenAQ. Ele permite monitorar os níveis de poluentes em um raio definido a partir de coordenadas geográficas e apresenta as informações de forma gráfica.

## Funcionalidades

  * **Coleta de Dados:** Baixa medições de qualidade do ar de sensores próximos a uma localização configurada (por padrão, Copacabana) para os últimos 7 dias.
  * [cite\_start]**Processamento de Dados:** Limpa, organiza e traduz os nomes dos poluentes para uma melhor compreensão. [cite: 1]
  * [cite\_start]**Análise Descritiva:** Apresenta um resumo da quantidade de medições por tipo de poluente e o período de cobertura dos dados. [cite: 1]
  * [cite\_start]**Visualização Gráfica:** Gera dois tipos de gráficos para facilitar a interpretação: [cite: 1]
      * [cite\_start]Um gráfico de barras mostrando a quantidade de medições por poluente. [cite: 1]
      * [cite\_start]Gráficos de linha para cada poluente, exibindo a variação do nível ao longo do tempo. [cite: 1]

## Como Usar

Siga os passos abaixo para configurar e executar o projeto em sua máquina.

### Pré-requisitos

Python 3.x 

As bibliotecas Python necessárias estão no arquivo `requisitos.txt`.

### Instalação

1.  **Clone o Repositório (ou baixe os arquivos):**

    ```bash
    git clone https://github.com/GuiBicudo/API-OpenAQ-Monitor-de-Poluentes
    cd API-OpenAQ-Monitor-de-Poluentes
    ```

2.  **Instale as Dependências:**
    Navegue até o diretório do projeto no terminal e instale as bibliotecas necessárias usando pip:

    ```bash
    pip install -r requisitos.txt
    ```

### Configuração da API Key

Para acessar a API OpenAQ, você precisará de uma chave de API.

1.  **Obtenha sua API Key:**

      * Visite o site da OpenAQ: [https://openaq.org/](https://openaq.org/)
      * Crie uma conta.
      * No final do seu perfil é possível gerar uma API Key gratuitamente.

2.  **Crie um arquivo `.env`:**
    No diretório raiz do projeto, crie um arquivo chamado `.env`. Dentro dele, adicione sua chave de API da seguinte forma:

    ```
    API_KEY="SUBSTITUA_SUA_CHAVE_API"
    ```

### Execução do Programa

O projeto é dividido em três scripts principais:

1.  **Coleta de Dados (`coleta_dados.py`):**
    Este script é responsável por fazer as requisições à API OpenAQ e salvar os dados brutos em um arquivo CSV.

    Para executar:

    ```bash
    python coleta_dados.py
    ```

    Este comando irá gerar um arquivo chamado `medicoes_copacabana_7dias_raio.csv` no mesmo diretório. Você pode ajustar as coordenadas (`coordinates_copacabana`) e o raio de busca (`radius_meters`) dentro do arquivo `coleta_dados.py`, se desejar analisar outras regiões ou distâncias. Por padrão, ele busca dados dos últimos 7 dias em um raio de 25 km de Copacabana.

2.  **Análise e Geração de Gráficos (`analise_dados.py`):**
    [cite\_start]Este script lê o arquivo CSV gerado pelo `coleta_dados.py`, processa os dados, realiza a limpeza e gera os gráficos de visualização. [cite: 1]

    Para executar:

    ```bash
    python analise_dados.py
    ```

    [cite\_start]Este script exibirá no console informações sobre o DataFrame, a contagem de medições por poluente e o período de cobertura dos dados. [cite: 1] [cite\_start]Em seguida, ele gerará e exibirá os dois gráficos descritos nas funcionalidades. [cite: 1]

3.  **Listar Cidades/Localizações (`listar_cidades.py` - Opcional):**
    Este script pode ser útil para explorar outras cidades ou localizações disponíveis na API OpenAQ, listando seus IDs e nomes.

    Para executar:

    ```bash
    python listar_cidades.py
    ```

## Arquivos do Projeto

  * `coleta_dados.py`: Script Python para coletar dados de medição da qualidade do ar da API OpenAQ e salvá-los em um arquivo CSV.
  * [cite\_start]`analise_dados.py`: Script Python para ler o CSV, limpar e processar os dados, e gerar gráficos de visualização. [cite: 1]
  * `listar_cidades.py`: Script Python auxiliar para listar IDs e nomes de cidades/localizações disponíveis na API OpenAQ.
  * `medicoes_copacabana_7dias_raio.csv`: Arquivo CSV gerado pelo `coleta_dados.py` contendo os dados brutos das medições.
  * `requisitos.txt`: Lista das bibliotecas Python necessárias para o projeto.
  * `.env`: Arquivo para armazenar a chave da API (não deve ser commitado no GitHub).

## Visualização dos Dados

[cite\_start]Após executar `analise_dados.py`, dois gráficos serão exibidos: [cite: 1]

1.  [cite\_start]**Quantidade de Medições por Tipo de Poluente:** Um gráfico de barras que mostra a frequência de cada poluente medido na área de estudo. [cite: 1]
2.  **Nível de Poluente ao Longo do Tempo:** Para cada poluente encontrado nos dados, um gráfico de linha separado exibirá como o nível desse poluente variou ao longo do tempo. [cite\_start]As unidades de medição serão indicadas no eixo Y. [cite: 1]

## Tecnologias Utilizadas

  * Python 3.x
  * `pandas`: Para manipulação e análise de dados.
  * `requests`: Para fazer requisições HTTP à API OpenAQ.
  * `matplotlib`: Para a criação dos gráficos.
  * `python-dotenv`: Para carregar variáveis de ambiente do arquivo `.env`.

## Autor

Guilherme Bicudo
[LinkedIn](https://www.linkedin.com/in/guilherme-bicudo/)

-----
