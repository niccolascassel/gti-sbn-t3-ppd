import csv
from datetime import datetime
import collections

class SteamDataAnalyzer:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = []
        self._load_data()

    
    def _load_data(self):
        """
        Carrega os dados do arquivo CSV e pré-processa-os.
        """
        try:
            with open(self.filepath, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                self.fieldnames = [field for field in reader.fieldnames if field is not None]

                for i, row in enumerate(reader):
                    cleaned_row = {}
                    for key, value in row.items():
                        if key is None:
                            continue 
                        
                        cleaned_key = key.strip().replace(' ', '_').replace('.', '').replace('-', '_').lower()
                        
                        if cleaned_key == 'release_date':
                            try:
                                dt_object = datetime.strptime(value, '%b %d, %Y')
                                cleaned_row[cleaned_key] = dt_object.year
                            except ValueError:
                                cleaned_row[cleaned_key] = None 
                        elif cleaned_key == 'price':
                            try:
                                cleaned_row[cleaned_key] = float(value)
                            except (ValueError, TypeError):
                                cleaned_row[cleaned_key] = 0.0
                        elif cleaned_key in ['estimated_owners', 'peak_ccu', 'dlc_count', 'reviews', 'positive', 'negative', 'achievements', 'recommendations', 'average_playtime_forever', 'average_playtime_two_weeks', 'median_playtime_forever', 'median_playtime_two_weeks']:
                            numeric_value = "".join(filter(str.isdigit, value)) if isinstance(value, str) and value.strip() else '0'
                            try:
                                cleaned_row[cleaned_key] = int(numeric_value)
                            except ValueError:
                                cleaned_row[cleaned_key] = 0
                        elif cleaned_key in ['windows', 'mac', 'linux']:
                            cleaned_row[cleaned_key] = value.lower() == 'true'
                        elif cleaned_key in ['genres', 'categories', 'tags']:
                            if isinstance(value, str) and value.strip():
                                cleaned_row[cleaned_key] = [item.strip() for item in value.split(',') if item.strip()]
                            else:
                                cleaned_row[cleaned_key] = []
                        else:
                            cleaned_row[cleaned_key] = value.strip() if isinstance(value, str) else value
                    self.data.append(cleaned_row)
            
            print(f"Dados de '{self.filepath}' carregados e pré-processados. Total de registros: {len(self.data)}")
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Erro: Arquivo '{self.filepath}' não encontrado.")
        
        except Exception as e:
            raise Exception(f"Erro ao carregar ou processar os dados do CSV: {e}")

    
    def get_free_vs_paid_percentage(self):
        """
        Calcula a porcentagem de jogos gratuitos vs. pagos.
        """
        free_games = 0
        paid_games = 0
        
        for game in self.data:
            price = game.get('price')
            if price is not None:
                if price == 0.0:
                    free_games += 1
                else:
                    paid_games += 1
        
        total_games = free_games + paid_games
        if total_games == 0:
            return {"gratuito_percentual": 0.0, "pago_percentual": 0.0}
        
        free_percentage = (free_games / total_games) * 100
        paid_percentage = (paid_games / total_games) * 100
        
        return {
            "gratuito_percentual": round(free_percentage, 2),
            "pago_percentual": round(paid_percentage, 2)
        }

    
    def get_year_with_most_new_games(self):
        """
        Identifica o(s) ano(s) com o maior número de lançamentos de jogos.
        """
        year_counts = {}
        for game in self.data:
            release_year = game.get('release_date')
            if release_year is not None:
                year_counts[release_year] = year_counts.get(release_year, 0) + 1
        
        if not year_counts:
            return {"years": [], "max_games": 0}
        
        max_games = 0
        for count in year_counts.values():
            if count > max_games:
                max_games = count
        
        years_with_most_games = []
        for year, count in year_counts.items():
            if count == max_games:
                years_with_most_games.append(year)
        
        years_with_most_games.sort()
        
        return {
            "years": years_with_most_games,
            "max_games": max_games
        }

    
    def get_top_genre_by_avg_recommendations(self, min_year=2015, min_positive_reviews=1000, top_n=10):
        """
        Encontra os top N gêneros com a maior média de recomendações positivas,
        filtrando por ano de lançamento e mínimo de reviews.
        Retorna uma lista de dicionários, ordenada alfabeticamente por gênero.
        """
        genre_recommendations_sum = collections.defaultdict(float)
        genre_game_count = collections.defaultdict(int)

        for game in self.data:
            release_year = game.get('release_date')
            genres = game.get('genres')
            recommendations_value = game.get('recommendations') 
            positive_reviews = game.get('positive')
            
            if (release_year is None or not isinstance(release_year, int) or release_year < min_year or
                genres is None or not isinstance(genres, list) or not genres or
                positive_reviews is None or not isinstance(positive_reviews, int) or positive_reviews < min_positive_reviews or
                recommendations_value is None):
                continue

            for genre in genres:
                normalized_genre = genre.strip()
                if normalized_genre:
                    genre_recommendations_sum[normalized_genre] += recommendations_value
                    genre_game_count[normalized_genre] += 1
        
        genre_averages_list = []
        for genre, total_recs in genre_recommendations_sum.items():
            count = genre_game_count[genre]
            if count > 0:
                avg_recs = total_recs / count
                genre_averages_list.append({'genre': genre, 'average_recommendations': round(avg_recs, 2)})
        
        sorted_by_avg_then_alpha = sorted(
            genre_averages_list,
            key=lambda x: (-x['average_recommendations'], x['genre'])
        )
        
        top_n_genres = sorted_by_avg_then_alpha[:top_n]
        
        final_sorted_genres_for_display = sorted(top_n_genres, key=lambda x: x['genre'])

        return final_sorted_genres_for_display
        
    
    def get_all_release_year_counts(self):
        """
        Retorna um dicionário com a contagem de jogos lançados por ano.
        A data de lançamento já é pré-processada como ano inteiro no _load_data.
        """
        year_counts = collections.defaultdict(int)
        for game in self.data:
            release_year = game.get('release_date')
            if release_year is not None:
                year_counts[release_year] += 1
        return dict(year_counts)
