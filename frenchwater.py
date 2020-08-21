import requests
from bs4 import BeautifulSoup


class FrenchWater:
    def __init__(self, region: str, departement: str, commune: str, reseau: str):
        # define self parameters

        self.region = str(region)
        self.departement = str(departement)
        self.commune = str(commune)
        self.reseau = str(reseau)
        self.url = "https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do"

        self.__get_cookie()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Referer": "https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "TE": "Trailers",
            "Cookie": "JSESSIONID="
            + self.cookie["JSESSIONID"]
            + ";BWFSESSID_vk35skh3d745n9jzlgg5lvcl2a="
            + self.cookie["BWFSESSID_vk35skh3d745n9jzlgg5lvcl2a"],
        }
        self.__get_departement_id()
        self.__get_commune_id()
        self.__get_reseau_id()

    def __get_departement_id(self):
        get_reseau_payload = "methode=changerDepartement&idRegion=" + self.region

        response = requests.request(
            "POST", self.url, headers=self.headers, data=get_reseau_payload
        )
        soup = BeautifulSoup(response.content, "lxml")
        soupSelect = soup.select(
            ".block-content > form:nth-child(2) > p:nth-child(6) > select:nth-child(2) > option"
        )
        if not soupSelect:
            raise Exception(
                "Departement not found please make sure your region id is correct")
        for i in soupSelect:
            if self.departement == i.text:
                self.departement = i["value"]
        return

    def __get_commune_id(self):
        get_reseau_payload = (
            "methode=changerCommune&idRegion="
            + self.region
            + "&usd=AEP&posPLV=0&departement="
            + self.departement
        )

        response = requests.request(
            "POST", self.url, headers=self.headers, data=get_reseau_payload
        )
        soup = BeautifulSoup(response.content, "lxml")
        soupSelect = soup.select(
            ".block-content > form:nth-child(2) > p:nth-child(7) > select:nth-child(2) > option"
        )
        if not soupSelect:
            raise Exception(
                "commune not found please make sure your departement name is correct and your departement name is correct")
        for i in soupSelect:
            if self.commune == i.text:
                self.commune = i["value"]
        return

    def __get_reseau_id(self):
        get_reseau_payload = (
            "methode=changerReseau&idRegion="
            + self.region
            + "&usd=AEP&posPLV=0&departement="
            + self.departement
            + "&communeDepartement="
            + self.commune
        )

        response = requests.request(
            "POST", self.url, headers=self.headers, data=get_reseau_payload
        )
        soup = BeautifulSoup(response.content, "lxml")
        soupSelect = soup.select(
            ".block-content > form:nth-child(2) > p:nth-child(8) > select:nth-child(2) > option"
        )
        if not soupSelect:
            raise Exception(
                "reseau not found please make sure your commune name is correct and your reseau name is correct")
        for i in soupSelect:
            if self.reseau == i.text:
                self.reseau = i["value"]
        return

    def __get_cookie(self):
        self.session = requests.Session()
        self.session.get(
            "https://orobnat.sante.gouv.fr/orobnat/afficherPage.do?methode=menu&usd=AEP&idRegion=93"
        )
        self.cookie = self.session.cookies.get_dict()
        return

    def get_last_results(self) -> (dict):

        payload = (
            "methode=rechercher&idRegion="
            + self.region
            + "&usd=AEP&posPLV=0&departement="
            + self.departement
            + "&communeDepartement="
            + self.commune
            + "&reseau="
            + self.reseau
        )

        response = self.session.request(
            "POST", url, headers=self.headers, data=payload
        )
        if response.status_code != 200:
            raise ConnectionError(f"Error code {response.status_code}")
        soup = BeautifulSoup(response.content, "lxml")
        date = soup.select_one(
            "div.block-content:nth-child(8) > table:nth-child(2) > tr > td"
        ).text[0:10]
        tr = soup.select(
            "div.block-content:nth-child(13) > table:nth-child(2) > tr")
        dic = {}
        for element in tr:
            for key in element.select("td:nth-child(1) > b"):
                for value in element.select("td:nth-child(2)"):
                    dic[key.text] = [value.text, date]
        return dic

    def get_last_x_results(self, result_size: int) -> (dict):
        dic = {}
        for i in range(0, result_size):
            url = "https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do"

            payload = (
                "methode=rechercher&idRegion="
                + self.region
                + "&usd=AEP&posPLV="
                + str(result_size - i)
                + "&departement="
                + self.departement
                + "&communeDepartement="
                + self.commune
                + "&reseau="
                + self.reseau
            )

            response = self.session.request(
                "POST", url, headers=self.headers, data=payload
            )
            if response.status_code != 200:
                raise ConnectionError(f"Error code {response.status_code}")
            soup = BeautifulSoup(response.content, "lxml")
            date = soup.select_one(
                "div.block-content:nth-child(8) > table:nth-child(2) > tr > td"
            ).text[0:10]
            tr = soup.select(
                "div.block-content:nth-child(13) > table:nth-child(2) > tr"
            )
            for element in tr:
                for key in element.select("td:nth-child(1) > b"):
                    for value in element.select("td:nth-child(2)"):
                        dic[key.text] = [value.text, date]
        return dic
