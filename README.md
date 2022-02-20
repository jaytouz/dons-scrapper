# dons-scrapper

Scrapper donation for political entities in Quebec

# Installation

Pour le scrapper assurer vous d'avoir installer le driver de google chrome et qu'il soit visible dans les variables d'environnement de votre ordinateur. (guide https://selenium-python.readthedocs.io/installation.html)

# Exemple d'utilisation

Lancer à partir du main en indiquand le path de sortie et les paramètres de recherche. Par exemple, l'exemple suivant lance une recherche pour les dons des années 2019 à 2022 pour le parti concervateur du québec et du parti libéral du québec.

```py
import logging
from datetime import datetime

# local package
from src.runner.process import DonationScrapperRunner
from src.scrapper.enums import PoliticalPartiesValues, LeadershipCandidateValues


def main():
    outputDir = "../output/multiprocess/"
    now = datetime.now().strftime("%Y_%m_%d_%H_%M")
    logging.basicConfig(filename=outputDir + f"donation_scrapper_{now}.log",
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        encoding='utf-8', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    runner = DonationScrapperRunner(
        "../output/multiprocess/", years=["2022", "2021", "2020", "2019"], parties=[PoliticalPartiesValues.PCQ_CPQ, PoliticalPartiesValues.PLQ_QLP])
    runner.run(poolSize=4)


if __name__ == "__main__":
    main()
```

### WARNING

Utiliser un trop grand poolSize peut entraîner des erreurs dans l'extraction des données. Vérifier le log, des avertissements s'afficheront dans le cas où certaines informations n'ont pas été bien collecter. Si c'est le cas, essayer le même query avec moins
de process dans le pool.

Valider également les résultats avec l'outil de recherche des donateurs Québécois, le nombre de résultat devrait être similaire à N + nbr page. (ils comptent le premier et dernier résultat en double à chaque page.)
