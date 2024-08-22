import unittest
from openpyxl import load_workbook
from analyzer_games import SteamGameDataset

def test_methods():
    # Inicializa o dataset com o novo arquivo CSV
    dataset = SteamGameDataset('steam_games_teste.csv', separator=',')

    # Calcular o percentual de jogos gratuitos e pagos
    percentages = dataset.calculate_price_percentages()
    print(f"Percentual de jogos gratuitos: {percentages['Free']:.2f}%")
    print(f"Percentual de jogos pagos: {percentages['Paid']:.2f}%")

    # Obter o(s) ano(s) com o maior número de novos jogos
    years_with_most_games = dataset.get_year_with_most_games()
    print(f"Ano(s) com o maior número de novos jogos: {years_with_most_games}")

    # Obter o jogo com mais avaliações positivas
    game_with_most_positive_reviews = dataset.get_game_with_most_positive_reviews()
    print(f"O jogo com mais avaliações positivas é: {game_with_most_positive_reviews}")

    return {
        "percentages": percentages,
        "years_with_most_games": years_with_most_games,
        "game_with_most_positive_reviews": game_with_most_positive_reviews,
    }

class TestSteamGameDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Executa o test_methods uma vez e armazena os resultados
        cls.results = test_methods()
        
        # Carrega os resultados manuais da segunda sheet 'CALC'
        workbook = load_workbook(filename='steam_games_teste_estatistica.xlsx')
        sheet = workbook['calc']
        
        # Extraindo e convertendo os valores manuais
        cls.manual_percentual_free = sheet['D2'].value * 100  # Convertendo para o mesmo formato percentual
        cls.manual_percentual_paid = sheet['E2'].value * 100  # Convertendo para o mesmo formato percentual
        cls.manual_years_with_most_games = str(sheet['F2'].value)  # Convertendo o ano para string
        cls.manual_game_with_most_positive_reviews = sheet['G2'].value

    def test_percentual_free(self):
        self.assertAlmostEqual(self.results["percentages"]['Free'], self.manual_percentual_free, places=2, 
                               msg="Percentual de jogos gratuitos não confere!")

    def test_percentual_paid(self):
        self.assertAlmostEqual(self.results["percentages"]['Paid'], self.manual_percentual_paid, places=2, 
                               msg="Percentual de jogos pagos não confere!")

    def test_years_with_most_games(self):
        self.assertEqual(self.results["years_with_most_games"], self.manual_years_with_most_games, 
                         msg="Ano(s) com o maior número de novos jogos não confere(m)!")

    def test_game_with_most_positive_reviews(self):
        self.assertEqual(self.results["game_with_most_positive_reviews"], self.manual_game_with_most_positive_reviews, 
                         msg="O jogo com mais avaliações positivas não confere!")

if __name__ == "__main__":
    unittest.main()


