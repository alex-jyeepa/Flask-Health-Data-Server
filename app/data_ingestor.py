"""ingestor to read csv and POST methods"""

import csv

class DataIngestor:
    #citim fisierul csv
    def __init__(self, csv_path: str):
        print(csv_path)
        with open (csv_path, 'r') as file:
            self.data = list(csv.DictReader(file))

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    #metodele de mai jos calculeaza raspunsurile la request-uri
    #ele intorc dictionare in format query : raspuns
    #statele sunt introduse in dictionar pe masura ce sunt gasite,
    #si un alt dictionar tine cont de numarul de aparitii pentru medie

    #calculeaza media tuturor valorilor
    def state_mean(self, state, question):
        mean = 0
        occurences = 0
        for row in self.data:
            if row['LocationDesc'] == state and row['Question'] == question:
                mean += float(row['Data_Value'])
                occurences += 1
        return {state: mean / occurences}

    #metoda ce, in functie de parametrul type, calculeaza
    #valorile primelor/ultimelor 5 state dupa data_value, sau toate statele
    def mean_best_worst(self, question, type):
        means = {}
        occurences = {}
        for row in self.data:
            if row['Question'] == question:
                if row['LocationDesc'] in means:
                    means[row['LocationDesc']] += float(row['Data_Value'])
                    occurences[row['LocationDesc']] += 1
                else:
                    means[row['LocationDesc']] = float(row['Data_Value'])
                    occurences[row['LocationDesc']] = 1
        for state in means:
            means[state] /= occurences[state]
        #in functie de tipul intrebarii, se sorteaza descrescator/crescator dictionarele
        if type == "mean":
            if question in self.questions_best_is_min:
                return dict(sorted(means.items(), key=lambda item: item[1]))
            return dict(sorted(means.items(), key=lambda item: item[1], reverse=True))
        if type == "best":
            if question in self.questions_best_is_min:
                return dict(list(sorted(means.items(), key=lambda item: item[1]))[:5])
            return dict(list(sorted(means.items(), key=lambda item: item[1], reverse=True))[:5])
        if question in self.questions_best_is_min:
            return dict(list(sorted(means.items(), key=lambda item: item[1], reverse=True))[:5])
        return dict(list(sorted(means.items(), key=lambda item: item[1]))[:5])

    #functia poate returna global_mean ca numar pentru calcule,
    #sau dictionar pentru raspuns la query
    def global_mean(self, question, n = "number"):
        mean = 0
        occurences = 0
        for row in self.data:
            if row['Question'] == question:
                mean += float(row['Data_Value'])
                occurences += 1
        if n == "number":
            return mean / occurences
        return {"global_mean": mean / occurences}

    def diff_from_mean(self, question):
        means = {}
        occurences = {}
        global_mean = self.global_mean(question)
        for row in self.data:
            if row['Question'] == question:
                if row['LocationDesc'] in means:
                    means[row['LocationDesc']] += float(row['Data_Value'])
                    occurences[row['LocationDesc']] += 1
                else:
                    means[row['LocationDesc']] = float(row['Data_Value'])
                    occurences[row['LocationDesc']] = 1
        for state in means:
            means[state] /= occurences[state]
            means[state] = global_mean - means[state]
        if question in self.questions_best_is_min:
            return dict(sorted(means.items(), key=lambda item: item[1], reverse=True))
        return dict(sorted(means.items(), key=lambda item: item[1]))

    def state_diff_from_mean(self, state, question):
        means = {}
        means[state] = 0
        occurences = 0
        global_mean = self.global_mean(question)
        for row in self.data:
            if row['LocationDesc'] == state and row['Question'] == question:
                means[state] += float(row['Data_Value'])
                occurences += 1
        means[state] /= occurences
        return {state: global_mean - means[state]}

    #campurile relevante sunt identificate printr-un dictionar tip tuplu : valoare,
    #tuplul contine statul, tipul de categorie si categoria
    def mean_by_category(self, question):
        means = {}
        occurences = {}
        for row in self.data:
            if row['Question'] == question and row['Stratification1'] != "" and row['StratificationCategory1'] != "":
                key = f"('{row['LocationDesc']}', '{row['StratificationCategory1']}', '{row['Stratification1']}')"
                if key in means:
                    means[key] += float(row['Data_Value'])
                    occurences[key] += 1
                else:
                    means[key] = float(row['Data_Value'])
                    occurences[key] = 1
        for key in means:
            means[key] /= occurences[key]
        return dict(sorted(means.items()))

    def state_mean_by_category(self, state, question):
        means = {}
        occurences = {}
        for row in self.data:
            if row['LocationDesc'] == state and row['Question'] == question and row['Stratification1'] != "" and row['StratificationCategory1'] != "":
                key = f"('{row['StratificationCategory1']}', '{row['Stratification1']}')"
                if key in means:
                    means[key] += float(row['Data_Value'])
                    occurences[key] += 1
                else:
                    means[key] = float(row['Data_Value'])
                    occurences[key] = 1
        for key in means:
            means[key] /= occurences[key]
        return {state : dict(sorted(means.items()))}
    