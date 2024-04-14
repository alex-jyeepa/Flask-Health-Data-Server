"""custom tests"""

import unittest
import json
import sys
import os
class TestServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        import app.data_ingestor
        cls.data_ingestor = app.data_ingestor.DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

    def test_state_mean(self):
        data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)",
            "state": "Maine",
        }
        expected = {"Maine": 52.446666666666665}

        self.assertEqual(
            self.data_ingestor.state_mean(data["state"], data["question"]), expected
        )

    def test_states_mean(self):
        data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification"
        }
        expected = {
            "District of Columbia": 30.746875,
            "Missouri": 32.76268656716418,
            "Arkansas": 32.99516129032258,
            "Kentucky": 33.071641791044776,
            "Vermont": 33.11818181818182,
            "Louisiana": 33.1793103448276,
            "Ohio": 33.25753424657533,
            "South Carolina": 33.25909090909091,
            "Virgin Islands": 33.296875,
            "Illinois": 33.521874999999994,
            "Indiana": 33.58701298701301,
            "Michigan": 33.73734939759038,
            "West Virginia": 33.8611111111111,
            "Iowa": 33.96455696202532,
            "Washington": 33.96842105263158,
            "Hawaii": 34.00468750000001,
            "Kansas": 34.05625,
            "Oklahoma": 34.05833333333334,
            "Tennessee": 34.10945945945945,
            "Oregon": 34.1421875,
            "Alabama": 34.1551724137931,
            "Wisconsin": 34.15542168674699,
            "Utah": 34.195081967213106,
            "Florida": 34.27333333333333,
            "Georgia": 34.30126582278482,
            "Mississippi": 34.315625,
            "Maine": 34.31612903225807,
            "Texas": 34.37692307692308,
            "North Carolina": 34.377631578947366,
            "Virginia": 34.458823529411774,
            "Guam": 34.485454545454544,
            "Maryland": 34.528395061728396,
            "Pennsylvania": 34.54354838709677,
            "Massachusetts": 34.6203125,
            "Delaware": 34.673846153846156,
            "Colorado": 34.78536585365854,
            "New Hampshire": 34.84415584415584,
            "New York": 34.86,
            "North Dakota": 34.89166666666666,
            "National": 35.08593750000001,
            "Rhode Island": 35.17878787878787,
            "Idaho": 35.19090909090909,
            "South Dakota": 35.19565217391305,
            "Arizona": 35.404687500000016,
            "Wyoming": 35.5169014084507,
            "Minnesota": 35.54576271186441,
            "Nebraska": 35.69142857142857,
            "California": 35.72459016393442,
            "Connecticut": 35.75428571428572,
            "New Mexico": 35.86349206349206,
            "Alaska": 35.902777777777786,
            "New Jersey": 36.08059701492537,
            "Montana": 36.17826086956522,
            "Nevada": 36.358333333333334,
            "Puerto Rico": 36.98636363636363,
        }

        self.assertEqual(
            self.data_ingestor.mean_best_worst(data["question"], "mean"), expected
        )

    def test_best5(self):
        data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)"
        }
        expected = {
            "Idaho": 57.75333333333333,
            "Vermont": 57.48064516129032,
            "Oregon": 57.199999999999974,
            "Colorado": 56.77428571428571,
            "Hawaii": 56.76,
        }

        self.assertEqual(
            self.data_ingestor.mean_best_worst(data["question"], "best"), expected
        )

    def test_worst5(self):
        data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)"
        }
        expected = {
            "Puerto Rico": 37.32000000000001,
            "Mississippi": 42.52333333333332,
            "Tennessee": 42.82592592592592,
            "Alabama": 43.40357142857143,
            "Oklahoma": 43.7551724137931,
        }

        self.assertEqual(
            self.data_ingestor.mean_best_worst(data["question"], "worst"), expected
        )

    def test_global_mean(self):
        data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week"
        }
        expected = {"global_mean": 20.20445945945952}

        self.assertEqual(
            self.data_ingestor.global_mean(data["question"], "dictionary"), expected
        )

    def test_diff_from_mean(self):
        data = {
            # Add your test logic here
            "question": "Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)"
        }
        expected = {
            "Montana": -7.042887245012441,
            "Vermont": -6.49083596296116,
            "Colorado": -6.29852827065346,
            "California": -6.151458673583864,
            "Alaska": -6.106220578345759,
            "Oregon": -6.0501599722851545,
            "Hawaii": -5.621220578345767,
            "Wisconsin": -4.227649149774333,
            "Maine": -4.172220578345776,
            "New Mexico": -3.7312205783457593,
            "Washington": -3.5607660328912196,
            "New Hampshire": -3.449553911679107,
            "Idaho": -2.976808813639888,
            "Wyoming": -2.569264056606638,
            "Florida": -2.392584214709405,
            "Utah": -1.4862205783457618,
            "Minnesota": -1.2228872450124335,
            "Michigan": -1.1265909487161458,
            "Massachusetts": -1.1062205783457735,
            "Arizona": -0.881220578345765,
            "National": -0.8795539116790998,
            "Nevada": -0.49258421470941016,
            "District of Columbia": -0.2995539116791015,
            "Maryland": -0.07545134757653571,
            "Virgin Islands": 0.04377942165423221,
            "Virginia": 0.07454865242346642,
            "New Jersey": 0.14377942165423008,
            "Ohio": 0.24377942165423505,
            "Georgia": 0.41044608832090645,
            "Delaware": 0.5920552837232016,
            "South Carolina": 0.6473508502256635,
            "Pennsylvania": 0.7207024985773067,
            "Illinois": 0.8298905327653472,
            "West Virginia": 0.9322409601157666,
            "New York": 1.296160374035182,
            "South Dakota": 1.4472276975163005,
            "Guam": 1.712529421654235,
            "Kansas": 1.800301160784663,
            "Arkansas": 1.858065135939949,
            "Rhode Island": 1.8901208850688782,
            "Connecticut": 1.921904421654233,
            "Missouri": 2.0760374861703568,
            "Nebraska": 2.126388117306405,
            "Louisiana": 2.664469076826645,
            "Kentucky": 2.969705347580149,
            "North Carolina": 3.097112754987563,
            "Indiana": 3.343779421654233,
            "North Dakota": 3.347483125357936,
            "Iowa": 3.7307359433933627,
            "Tennessee": 4.449661774595398,
            "Alabama": 4.730143058017873,
            "Oklahoma": 5.972350850225663,
            "Texas": 6.03508376948032,
            "Mississippi": 7.311521357138105,
            "Puerto Rico": 13.268779421654234,
        }

        # Add your test logic here
        self.assertEqual(self.data_ingestor.diff_from_mean(data["question"]), expected)

    def test_state_diff_from_mean(self):
        data = {
            "question": "Percent of adults who report consuming vegetables less than one time daily",
            "state": "Texas",
        }
        expected = {"Texas": 0.034150827713080645}

        self.assertEqual(
            self.data_ingestor.state_diff_from_mean(data["state"], data["question"]),
            # Add your test logic here
            expected,
        )

    def test_mean_by_category(self):
        data = {
            "question": "Percent of adults who engage in no leisure-time physical activity"
        }
        with open("mean_by_category", "r") as file:
            expected = json.load(file)
        # Add your test logic here
        self.assertEqual(
            self.data_ingestor.mean_by_category(data["question"]), expected
        )

    def test_state_mean_by_category(self):
        data = {
            "question": "Percent of adults who engage in muscle-strengthening activities on 2 or more days a week",
            "state": "Connecticut",
        }
        with open("state_mean_by_category", "r") as file:
            expected = json.load(file)
        self.assertEqual(
            self.data_ingestor.state_mean_by_category(data["state"], data["question"]),
            expected,
        )
