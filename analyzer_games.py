import csv

class SteamGameDataset:
    def __init__(self, filepath, separator=','):
        """Inicializa o conjunto de dados a partir de um arquivo CSV."""
        self.filepath = filepath
        self.data = []
        self.separator = separator
        self._load_data()

    def _load_data(self):
        """Carrega os dados do arquivo CSV para uma lista de dicionários."""
        try:
            csv.register_dialect('unixpwd', delimiter=self.separator, quoting=csv.QUOTE_NONE)
            with open(self.filepath, mode='r', encoding='latin-1') as file:
                reader = csv.DictReader(file)
                self.data = [dict(list(row.items())[:-1]) for row in reader]
        except FileNotFoundError:
            raise FileNotFoundError(f"O arquivo {self.filepath} não foi encontrado.")
        except Exception as e:
            raise Exception(f"Erro ao carregar os dados: {e}")

    def write_list(self, data):
        """Escreve cada item da lista de dados."""
        for item in data:
            print(item)
        return item

    def calculate_price_percentages(self):
        """Calcula o percentual de jogos gratuitos e pagos na plataforma."""
        total_games = len(self.data)
        if total_games == 0:
            return {'Free': 0, 'Paid': 0}

        free_games = sum(1 for game in self.data if game['Price'] == '0.0')
        paid_games = total_games - free_games

        free_percentage = (free_games / total_games) * 100
        paid_percentage = (paid_games / total_games) * 100

        return {
            'Free': free_percentage,
            'Paid': paid_percentage
        }

    def get_year_with_most_games(self):
        """Encontra o ano com mais lançamentos de jogos. Em caso de empate, retorna uma lista com os anos empatados."""
        year_count = {}
        for game in self.data:
            release_date = game['Release date']
            release_year = self._extract_year(release_date)
            if release_year:
                year_count[release_year] = year_count.get(release_year, 0) + 1

        if not year_count:
            return []

        max_count = max(year_count.values())
        years_with_max_count = [year for year, count in year_count.items() if count == max_count]

        return years_with_max_count if len(years_with_max_count) > 1 else years_with_max_count[0]

    def _extract_year(self, release_date):
        """Extrai o ano da data de lançamento, lidando com diferentes formatos."""
        try:
            # Verifica se a data está no formato "Jan 4, 2019"
            if "," in release_date:
                return release_date.split()[-1]
            # Verifica se a data está no formato "mar/17"
            elif "/" in release_date:
                return "20" + release_date.split("/")[-1]
            else:
                return None
        except Exception as e:
            print(f"Erro ao processar a data de lançamento '{release_date}': {e}")
            return None
        
    def get_game_with_most_positive_reviews(self):
        """Encontra o jogo com o maior número de avaliações positivas."""
        most_positive_reviews = 0
        game_with_most_positive = None

        for game in self.data:
            positive_reviews = game.get('Positive')
            if positive_reviews and positive_reviews.isdigit():
                positive_reviews = int(positive_reviews)
                if positive_reviews > most_positive_reviews:
                    most_positive_reviews = positive_reviews
                    game_with_most_positive = game['Name']

        return game_with_most_positive

if __name__ == '__main__':

    # Exemplo de uso:
    dataset = SteamGameDataset('steam_games.csv')

    # Calcular e imprimir o percentual de jogos gratuitos e pagos
    percentages = dataset.calculate_price_percentages()
    print(f"Percentual de jogos gratuitos: {percentages['Free']:.2f}%")
    print(f"Percentual de jogos pagos: {percentages['Paid']:.2f}%")

    # Obter e imprimir o(s) ano(s) com o maior número de novos jogos
    years_with_most_games = dataset.get_year_with_most_games()
    print(f"Ano(s) com o maior número de novos jogos: {years_with_most_games}")

    # Obter e imprimir o jogo com mais avaliações positivas
    game_with_most_positive_reviews = dataset.get_game_with_most_positive_reviews()
    print(f"O jogo com mais avaliações positivas é: {game_with_most_positive_reviews}")
