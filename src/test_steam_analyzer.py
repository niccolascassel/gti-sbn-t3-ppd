import unittest
import os
import json
from steam_analyzer import SteamDataAnalyzer

SAMPLES_DIR = 'data/samples'
ALL_EXPECTED_RESULTS_FILE = os.path.join(SAMPLES_DIR, 'all_expected_results.json')

class TestSteamDataAnalyzer(unittest.TestCase):
    """
    Classe de testes para a SteamDataAnalyzer, utilizando múltiplas amostras de dados
    e um único arquivo JSON para todos os resultados esperados.
    """

    @classmethod
    def setUpClass(cls):
        """
        Configura o ambiente de teste uma vez antes de todos os testes.
        Carrega o único arquivo JSON de resultados esperados e mapeia as amostras CSV.
        """
        cls.samples_config = []
        
        if not os.path.exists(SAMPLES_DIR):
            raise FileNotFoundError(f"O diretório de amostras '{SAMPLES_DIR}' não foi encontrado. "
                                    "Por favor, certifique-se de que ele foi criado e contém os arquivos de amostra e o JSON.")
        
        if not os.path.exists(ALL_EXPECTED_RESULTS_FILE):
            raise FileNotFoundError(f"O arquivo de resultados esperados '{ALL_EXPECTED_RESULTS_FILE}' não foi encontrado. "
                                    "Certifique-se de que ele foi criado e está no local correto.")
        
        try:
            with open(ALL_EXPECTED_RESULTS_FILE, 'r', encoding='utf-8') as f:
                cls.all_expected_results = json.load(f)
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar JSON de '{ALL_EXPECTED_RESULTS_FILE}': {e}. Verifique a sintaxe do JSON.")
        except Exception as e:
            raise Exception(f"Erro inesperado ao carregar '{ALL_EXPECTED_RESULTS_FILE}': {e}")

        for i in range(1, 11):
            sample_id_str = f"{i:02d}"
            filename = f'steam_games_sample_{sample_id_str}.csv'
            csv_path = os.path.join(SAMPLES_DIR, filename)
            
            if not os.path.exists(csv_path):
                print(f"Aviso: Arquivo de amostra '{csv_path}' não encontrado. Pulando esta amostra.")
                continue
            
            expected_data_for_this_sample = cls.all_expected_results.get(f'sample_{sample_id_str}')
            
            if expected_data_for_this_sample:
                cls.samples_config.append((sample_id_str, csv_path, expected_data_for_this_sample))
            else:
                print(f"Aviso: Resultados esperados para 'sample_{sample_id_str}' não encontrados em '{ALL_EXPECTED_RESULTS_FILE}'. Pulando esta amostra.")
        
        if not cls.samples_config:
            raise Exception(f"Nenhuma amostra de teste válida encontrada no diretório '{SAMPLES_DIR}'. "
                            "Verifique a nomeação (steam_games_sample_NN.csv) e se o JSON contém entradas correspondentes.")
        
        print(f"\nTotal de {len(cls.samples_config)} amostras carregadas para teste.")

    def test_q1_free_vs_paid_percentage(self):
        """
        Testa a função get_free_vs_paid_percentage para todas as amostras.
        """
        for sample_id, csv_path, expected_data in self.samples_config:
            with self.subTest(sample=sample_id):
                analyzer = SteamDataAnalyzer(csv_path)
                result = analyzer.get_free_vs_paid_percentage()
                expected_q1 = expected_data['q1_percentages']
                
                # print(f"\nDEBUG Teste Q1 para amostra {sample_id}:")
                # print(f"Valores esperados: {expected_q1}")
                # print(f"Resultado da função: {result}")
                
                self.assertAlmostEqual(result['gratuito_percentual'], expected_q1['gratuito_percentual'], places=2, 
                                     msg=f"Falha na Q1 para amostra {sample_id} - Percentual Gratuito")
                self.assertAlmostEqual(result['pago_percentual'], expected_q1['pago_percentual'], places=2,
                                     msg=f"Falha na Q1 para amostra {sample_id} - Percentual Pago")


    def test_q2_year_with_most_new_games(self):
        """
        Testa a função get_year_with_most_new_games para todas as amostras.
        Ajustado para o novo formato do JSON (sem 'max_games').
        """
        for sample_id, csv_path, expected_data in self.samples_config:
            with self.subTest(sample=sample_id):
                analyzer = SteamDataAnalyzer(csv_path)
                result = analyzer.get_year_with_most_new_games()
                expected_q2 = expected_data['q2_most_games_year']
                
                # print(f"\nDEBUG Teste Q2 para amostra {sample_id}:")
                # print(f"Valores esperados: {expected_q2}")
                # print(f"Resultado da função: {result}")
                
                self.assertListEqual(result['years'], expected_q2['years'], 
                     msg=f"Falha na Q2 para amostra {sample_id} - Anos com mais jogos")


    def test_q3_top_genre_by_avg_recommendations(self):
        """
        Testa a função get_top_genre_by_avg_recommendations para todas as amostras.
        Ajustado para o novo formato do JSON (genre sempre lista).
        """
        for sample_id, csv_path, expected_data in self.samples_config:
            with self.subTest(sample=sample_id):
                analyzer = SteamDataAnalyzer(csv_path)
                expected_q3 = expected_data['q3_top_genre']
                
                result = analyzer.get_top_genre_by_avg_recommendations(min_year=2015, min_positive_reviews=1000)
                
                # print(f"\nDEBUG Teste Q3 para amostra {sample_id}:")
                # print(f"Valores esperados: {expected_q3}")
                # print(f"Resultado da função: {result}")
                
                if result is None or 'genre' not in result or result['genre'] is None:
                    self.fail(f"Erro na Q3 para amostra {sample_id}: 'genre' no resultado da função é None ou não existe. Resultado completo: {result}")
                
                result_genres_sorted = sorted(result['genre'])
                expected_genres_sorted = sorted(expected_q3['genre'])

                self.assertListEqual(result_genres_sorted, expected_genres_sorted,
                                     msg=f"Falha na Q3 para amostra {sample_id} - Gênero(s)")

                self.assertAlmostEqual(result['average_recommendations'], expected_q3['average_recommendations'], places=2,
                                     msg=f"Falha na Q3 para amostra {sample_id} - Média de recomendações")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
