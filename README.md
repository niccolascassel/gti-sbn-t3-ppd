🎮 Steam Game Data Analysis & Visualization Tool

Este projeto oferece uma ferramenta para analisar e visualizar dados de jogos da plataforma Steam. Ele permite insights sobre a distribuição de jogos gratuitos vs. pagos, tendências de lançamento ao longo dos anos, e os gêneros de jogos com maior média de recomendações.

## ✨ Recursos

*   **Análise de Monetização:** Calcula e visualiza o percentual de jogos gratuitos e pagos.
*   **Tendência de Lançamentos:** Identifica o(s) ano(s) de pico no lançamento de novos jogos e gera um gráfico da contagem de jogos por ano.
*   **Top Gêneros por Recomendação:** Apresenta os 10 gêneros com as maiores médias de recomendações (filtradas por ano e número mínimo de reviews positivas), destacando visualmente o(s) gênero(s) com a maior média.
*   **Seleção Flexível de Dataset:** Permite escolher entre o dataset completo ou uma das amostras fornecidas via linha de comando.
*   **Geração de Gráficos:** Salva automaticamente os gráficos gerados em um diretório `data/plots/` para fácil incorporação em relatórios.

## 🚀 Primeiros Passos

Siga as instruções abaixo para configurar e executar o projeto em sua máquina local.

### 📋 Pré-requisitos

Certifique-se de ter o Python 3.x instalado em seu sistema. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).

### 📦 Instalação e Configuração

1.  **Clone o Repositório:**
    Comece clonando este repositório para a sua máquina local:

    ```bash
    git clone https://github.com/SeuUsuario/SeuRepositorio.git # Substitua pelo seu usuário e nome do repositório
    cd SeuRepositorio # Navegue até o diretório do projeto
    ```

2.  **Configuração dos Dados (Passo CRÍTICO!):**
    Devido ao limite de tamanho de arquivos do GitHub, o dataset completo `steam_games.csv` está compactado como `steam_games.zip` no diretório `data/dataset/`. **Você DEVE descompactá-lo antes de executar a análise.**

    *   **Local do Arquivo Compactado:** `data/dataset/steam_games.zip`
    *   **Local de Destino (onde o arquivo descompactado deve ficar):** `data/dataset/steam_games.csv`

    Você pode usar sua ferramenta de descompactação de preferência. Em sistemas baseados em Unix (Linux/macOS) ou Git Bash no Windows, você pode usar:

    ```bash
    unzip data/dataset/steam_games.zip -d data/dataset/
    ```

    No Windows, você pode descompactar manualmente usando o Explorador de Arquivos ou via PowerShell:

    ```powershell
    Expand-Archive -LiteralPath "data/dataset/steam_games.zip" -DestinationPath "data/dataset/"
    ```

    **Verifique se, após a descompactação, o arquivo `steam_games.csv` existe em `data/dataset/`**.

3.  **Instale as Dependências:**
    As bibliotecas Python necessárias são `matplotlib` (para geração de gráficos). É recomendado usar um ambiente virtual.

    ```bash
    # (Opcional) Crie e ative um ambiente virtual
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate

    # Instale as dependências
    pip install matplotlib
    ```

## ⚙️ Uso

Execute o script `main_analysis.py` a partir da linha de comando. Você pode especificar qual dataset usar:

### Opções de Execução:

*   **Analisar o dataset completo (`steam_games.csv`):**
    ```bash
    python main_analysis.py -s full
    # ou
    python main_analysis.py --sample full
    ```

*   **Analisar uma amostra específica (`steam_games_sample_XX.csv`):**
    Substitua `ID_DA_AMOSTRA` por um número de `1` a `10`. Por exemplo, para `steam_games_sample_05.csv`:
    ```bash
    python main_analysis.py -s 5
    # ou
    python main_analysis.py --sample 05
    ```

*   **Analisar o dataset completo (comportamento padrão):**
    Se nenhum argumento for fornecido, a análise será executada para o dataset completo.
    ```bash
    python main_analysis.py
    ```

*   **Mostrar Ajuda:**
    Para ver as opções de uso e uma descrição detalhada:
    ```bash
    python main_analysis.py -h
    # ou
    python main_analysis.py --help
    ```

### Exemplo de Saída dos Gráficos

Após a execução, os gráficos serão salvos no diretório `data/plots/` como arquivos `.png`. Você pode então copiá-los e utilizá-los em seus relatórios.

## 📁 Estrutura do Projeto
├── main_analysis.py # Script principal para executar análises e gerar gráficos
├── steam_analyzer.py # Classe para carregar, pré-processar e analisar dados
├── chart_generator.py # Classe para gerar e salvar os gráficos
├── data/
│ ├── dataset/
│ │ └── steam_games.csv # Dataset completo (descompacte steam_games.zip aqui)
│ │ └── steam_games.zip # Dataset completo compactado (no GitHub)
│ ├── samples/
│ │ ├── steam_games_sample_01.csv # Amostras de dataset
│ │ └── ... (até sample_10.csv)
│ └── plots/ # Diretório onde os gráficos gerados serão salvos
└── README.md # Este arquivo


---
