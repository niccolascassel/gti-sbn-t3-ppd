import os
import sys
import argparse

from steam_analyzer import SteamDataAnalyzer
from chart_generator import ChartGenerator

FULL_DATA_PATH = 'data/dataset/steam_games.csv'
SAMPLE_PATH_TEMPLATE = 'data/samples/steam_games_sample_{:02d}.csv'
PLOTS_DIR = 'data/plots'

chart_generator = ChartGenerator(output_dir=PLOTS_DIR)

CUSTOM_HELP_MESSAGE = """
Como utilizar o main_analysis.py:

python main_analysis.py [OPÇÕES]

Opções:
  -s DATASET_ID, --s DATASET_ID, -sample DATASET_ID, --sample DATASET_ID
                        Define qual dataset será analisado.
                        Pode ser um número de 1 a 10 para usar uma amostra
                        (e.g., '1' para sample_01, '10' para sample_10),
                        ou 'full' para usar o dataset completo.
                        Se esta opção não for especificada ou for vazia/inválida,
                        a análise será executada para o dataset COMPLETO por padrão.
  -h, --help, --h, -help
                        Mostra esta mensagem de ajuda e sai.

Exemplos de uso:
  - Analisar a amostra 'sample_05':
    python main_analysis.py -s 5

  - Analisar o dataset completo:
    python main_analysis.py --sample full

  - Analisar o dataset completo (comportamento padrão, sem opções):
    python main_analysis.py
"""

def print_custom_help():
    """Imprime a mensagem de ajuda personalizada no console e sai."""
    print(CUSTOM_HELP_MESSAGE)
    sys.exit(0)

def run_analysis(file_path, data_type_label, filename_prefix):
    """
    Executa a análise completa dos dados de jogos Steam, imprime os resultados
    e gera os gráficos correspondentes.

    Args:
        file_path (str): Caminho para o arquivo CSV a ser analisado.
        data_type_label (str): Rótulo para identificação no título dos gráficos
                                (e.g., "Dataset Completo", "Amostra (Sample 01)").
        filename_prefix (str): Prefixo para o nome dos arquivos de gráficos salvos
                               (e.g., "full", "sample_01").
    """
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo de dados '{file_path}' não foi encontrado.")
        print("Por favor, verifique se o arquivo está no diretório correto ou atualize o caminho.")
        return

    try:
        print(f"Carregando dados de: {file_path}...")
        analyzer = SteamDataAnalyzer(file_path)
        
        print(f"Dados carregados com sucesso! Total de jogos: {len(analyzer.data)}\n")
        
        print("---------------------------------------------")
        print("--- Percentual de Jogos Gratuitos e Pagos ---")
        print("---------------------------------------------")
        
        percentages = analyzer.get_free_vs_paid_percentage()
        
        print(f"Jogos Gratuitos: {percentages['gratuito_percentual']:.2f}%")
        print(f"Jogos Pagos: {percentages['pago_percentual']:.2f}%")
        
        chart_generator.generate_q1_pie_chart(
            percentages['gratuito_percentual'],
            percentages['pago_percentual'],
            data_type_label,
            f'{filename_prefix}_free_paid'
        )

        print("\nAnálise:")
        print("Este resultado nos mostra a distribuição do modelo de monetização na plataforma Steam.")
        print(f"Aproximadamente {percentages['gratuito_percentual']:.2f}% dos jogos são gratuitos. Isso pode incluir títulos Free-to-Play, demos, ou jogos que foram temporariamente gratuitos.")
        print(f"A maioria esmagadora, {percentages['pago_percentual']:.2f}%, são jogos pagos, indicando que a venda direta de licenças ainda é o principal modelo de negócio para os desenvolvedores na Steam.")
        print("Para a Fun Corp., isso sugere que, embora o mercado de jogos pagos seja dominante e provavelmente o mais lucrativo, há também espaço para explorar o modelo gratuito como forma de engajamento e potencial monetização através de DLCs ou itens no futuro.")
        print("-" * 70 + "\n")
        
        print("-------------------------------------------")
        print("--- Ano com Maior Número de Novos Jogos ---")
        print("-------------------------------------------")
        
        most_games_year = analyzer.get_year_with_most_new_games()
        
        if most_games_year['years']:
            print(f"O ano(s) com o maior número de jogos lançados é/são: {most_games_year['years']} com {most_games_year['max_games']} jogos.")
        else:
            print("Não foi possível determinar o ano com maior número de jogos (dados insuficientes ou inválidos).")
        
        all_year_counts = analyzer.get_all_release_year_counts()
        
        chart_generator.generate_q2_bar_chart(
            all_year_counts,
            most_games_year['years'],
            data_type_label,
            f'{filename_prefix}_new_games_year'
        )
        
        print("\nAnálise:")
        print("A identificação do ano com o pico de lançamentos é crucial para entender a evolução do mercado de jogos digitais.")
        
        if most_games_year['years']:
            print(f"O(s) ano(s) de destaque, {most_games_year['years']}, pode(m) indicar períodos de grande expansão da plataforma Steam ou de alta atividade de desenvolvimento na indústria.")
            print("Para a Fun Corp., isso significa que a concorrência pode ter sido mais acirrada nesses períodos, exigindo estratégias de marketing e diferenciação mais robustas.")
            print("-" * 70 + "\n")
        else:
            print("A ausência de dados para esta análise pode indicar problemas no formato das datas de lançamento ou uma base de dados muito pequena para identificar tendências anuais.")
            print("-" * 70 + "\n")
        
        print("-----------------------------------------------------------")
        print("--- Top 10 Gêneros por Média de Recomendações (Autoral) ---")
        print("-----------------------------------------------------------")
        
        top_genres_data_for_display = analyzer.get_top_genre_by_avg_recommendations(min_year=2015, min_positive_reviews=1000, top_n=10)
        
        if top_genres_data_for_display:
            
            print(f"Os {len(top_genres_data_for_display)} principais gênero(s) com a maior média de recomendações (filtrado) são:")
            
            for item in top_genres_data_for_display:
                print(f"- {item['genre']} (Média: {item['average_recommendations']:.2f})")
            
            max_avg_in_list = 0.0
            
            if top_genres_data_for_display:
                max_avg_in_list = max(item['average_recommendations'] for item in top_genres_data_for_display)
            
            highest_avg_genre_names = [item['genre'] for item in top_genres_data_for_display if item['average_recommendations'] == max_avg_in_list]
            highest_avg_genre_names.sort()
            highest_avg_genre_str = ', '.join(highest_avg_genre_names)

        else:
            print("Não foi possível determinar os principais gêneros com maior média de recomendações (dados insuficientes ou critérios de filtro muito restritivos).")
            
            highest_avg_genre_str = "nenhum gênero"
            max_avg_in_list = 0.0
        
        if top_genres_data_for_display:
            
            chart_generator.generate_q3_bar_chart(
                top_genres_data_for_display, 
                data_type_label,
                f'{filename_prefix}_top_10_genre_recommendations'
            )
        
        print("\nAnálise:")
        print("Esta análise mais aprofundada nos permite identificar nichos de mercado com alto potencial de engajamento e satisfação do cliente.")
        
        if top_genres_data_for_display:
            
            print(f"A análise dos principais gêneros revela que {highest_avg_genre_str} se destaca(m) com uma média de {max_avg_in_list:.2f} recomendações. Isso sugere que jogos bem-sucedidos nessas categorias tendem a gerar grande satisfação e a serem altamente indicados pelos usuários, o que é um fator crucial para o sucesso em um mercado digital.")
            print("Para a Fun Corp., focar em gêneros com alta recomendação pode ser uma estratégia valiosa para garantir não apenas vendas, mas também a viralidade e a construção de uma comunidade leal.")
        
        else:
            
            print("A ausência de gêneros de destaque sob estes critérios específicos pode significar que os jogos que atendem aos filtros são muito diversos, ou que a base de dados não contém exemplos suficientes para uma tendência clara.")
        
        print("-" * 70 + "\n")

    except FileNotFoundError as e:
        print(f"Erro: {e}")
        print("Certifique-se de que o arquivo CSV está no local correto.")
    
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a análise: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if any(arg in ['-h', '--h', '-help', '--help'] for arg in sys.argv[1:]):
        print_custom_help()
    
    parser = argparse.ArgumentParser(
        description="Script para análise de dados de jogos Steam e geração de gráficos.",
        add_help=False
    )
    
    parser.add_argument(
        '-s', '--s', '-sample', '--sample',
        dest='dataset_id',
        type=str,
        default='full',
        help="ID do dataset a ser analisado (1-10 para samples, 'full' para o dataset completo)."
    )

    args = parser.parse_args()

    selected_id = args.dataset_id
    file_to_analyze = FULL_DATA_PATH
    data_label = 'Dataset Completo'
    file_prefix = 'full'
    
    if isinstance(selected_id, str):
        if selected_id.isdigit():
            
            sample_num = int(selected_id)
            
            if 1 <= sample_num <= 10:
                file_to_analyze = SAMPLE_PATH_TEMPLATE.format(sample_num)
                data_label = f'Amostra (Sample {sample_num:02d})'
                file_prefix = f'sample_{sample_num:02d}'
            else:
                print(f"Aviso: ID de amostra '{selected_id}' fora do intervalo (1-10). Analisando o dataset COMPLETO por padrão.")
        
        elif selected_id.lower() == 'full':
            pass
        
        else:
            print(f"Aviso: Parâmetro '{selected_id}' inválido para a opção -s/--sample. Analisando o dataset COMPLETO por padrão.")

    print(f"\n--- Executando Análise para: {data_label} ---")
    run_analysis(file_to_analyze, data_label, file_prefix)