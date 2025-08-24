import os
import matplotlib.pyplot as plt

class ChartGenerator:
    """
    Classe responsável por gerar e salvar gráficos para as análises de dados.
    """
    def __init__(self, output_dir='plots'):
        """
        Inicializa o gerador de gráficos.
        Cria o diretório de saída se ele não existir.
        """
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        plt.rcParams.update({'font.size': 10})

    def _save_plot(self, filename):
        """
        Salva o gráfico atual e fecha a figura para liberar memória.
        """
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()

    def generate_q1_pie_chart(self, free_percentage, paid_percentage, title_suffix, filename_suffix):
        """
        Gera e salva um gráfico de pizza para o percentual de jogos gratuitos vs. pagos.

        Args:
            free_percentage (float): Percentual de jogos gratuitos.
            paid_percentage (float): Percentual de jogos pagos.
            title_suffix (str): Sufixo para o título do gráfico (ex: 'Dataset Completo').
            filename_suffix (str): Sufixo para o nome do arquivo (ex: 'full').
        """
        labels = ['Gratuitos', 'Pagos']
        sizes = [free_percentage, paid_percentage]
        colors = ['#66b3ff', '#99ff99']
        explode = (0.1, 0)

        fig1, ax1 = plt.subplots(figsize=(8, 6))
        wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                           colors=colors, shadow=True, startangle=90)
        ax1.axis('equal')
        plt.title(f'Percentual de Jogos Gratuitos vs. Pagos - {title_suffix}', fontsize=14)
        plt.setp(autotexts, size=10, weight='bold', color='black')
        plt.setp(texts, size=10, color='black')
        self._save_plot(f'q1_{filename_suffix}.png')

    def generate_q2_bar_chart(self, year_counts, max_years, title_suffix, filename_suffix):
        """
        Gera e salva um gráfico de barras para o número de jogos lançados por ano,
        destacando o(s) ano(s) com mais lançamentos.

        Args:
            year_counts (dict): Dicionário {ano: contagem_de_jogos}.
            max_years (list): Lista de anos com o maior número de lançamentos.
            title_suffix (str): Sufixo para o título do gráfico (ex: 'Dataset Completo').
            filename_suffix (str): Sufixo para o nome do arquivo (ex: 'full').
        """
        if not year_counts:
            print(f"Não há dados de anos para plotar para Q2 - {title_suffix}.")
            return

        years = sorted(year_counts.keys())
        counts = [year_counts[year] for year in years]

        plt.figure(figsize=(12, 7))
        bars = plt.bar(years, counts, color='skyblue')
        
        for i, year in enumerate(years):
            if year in max_years:
                bars[i].set_color('red')

        plt.xlabel('Ano de Lançamento', fontsize=12)
        plt.ylabel('Número de Jogos', fontsize=12)
        plt.title(f'Número de Jogos Lançados por Ano - {title_suffix}', fontsize=14)
        plt.xticks(years, rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        self._save_plot(f'q2_{filename_suffix}.png')

    def generate_q3_bar_chart(self, top_genres_data, title_suffix, filename_suffix):
        """
        Gera e salva um gráfico de barras para os top N gêneros com a maior média de recomendações,
        destacando o(s) gênero(s) com a maior média.

        Args:
            top_genres_data (list): Lista de dicionários, e.g.,
                                   [{'genre': 'Action', 'average_recommendations': 1831.0}, ...]
                                   Esta lista já deve estar ordenada alfabeticamente por gênero.
            title_suffix (str): Sufixo para o título do gráfico (ex: 'Dataset Completo').
            filename_suffix (str): Sufixo para o nome do arquivo (ex: 'full').
        """
        if not top_genres_data:
            print(f"Não há dados de gênero para plotar para Q3 - {title_suffix}.")
            return

        # Extrair nomes dos gêneros e médias de recomendações
        genres = [item['genre'] for item in top_genres_data]
        avg_recommendations_values = [item['average_recommendations'] for item in top_genres_data]

        # Encontrar a maior média de recomendações na lista para destaque
        max_avg_value = 0.0
        if avg_recommendations_values: # Garante que a lista não está vazia
            max_avg_value = max(avg_recommendations_values)

        plt.figure(figsize=(12, 7))
        # Gera o gráfico de barras. 'bars' é uma lista de objetos Rectangle (as barras)
        bars = plt.bar(genres, avg_recommendations_values, color='lightgreen') # Cor padrão

        # Percorre as barras para aplicar a cor de destaque
        for i, bar in enumerate(bars):
            if avg_recommendations_values[i] == max_avg_value:
                bar.set_color('red') # Cor de destaque para o(s) gênero(s) com a maior média

        plt.xlabel('Gênero', fontsize=12)
        plt.ylabel('Média de Recomendações', fontsize=12)
        plt.title(f'Top {len(genres)} Gêneros por Média de Recomendações (Filtrado) - {title_suffix}', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        self._save_plot(f'q3_{filename_suffix}.png')
