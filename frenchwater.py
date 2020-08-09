import requests
from bs4 import BeautifulSoup


class FrenchWater:
    def __init__(self, region, departement, commune, reseau):
        self.region = region
        self.departement = departement
        self.commune = commune
        self.reseau = reseau

        self.session = requests.Session()
        self.session.get(
            "https://orobnat.sante.gouv.fr/orobnat/afficherPage.do?methode=menu&usd=AEP&idRegion=93"
        )
        self.cookie = self.session.cookies.get_dict()

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "TE": "Trailers",
        }

    def get_last_results(self):
        url = "https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do"

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

        water_headers = self.headers
        water_headers[
            "Referer"
        ] = "https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do"
        water_headers["Cookie"] = (
            "JSESSIONID="
            + self.cookie["JSESSIONID"]
            + ";BWFSESSID_vk35skh3d745n9jzlgg5lvcl2a="
            + self.cookie["BWFSESSID_vk35skh3d745n9jzlgg5lvcl2a"]
        )

        response = self.session.request(
            "POST", url, headers=water_headers, data=payload
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

    def get_last_x_results(self, result_size):
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
            water_headers = self.headers
            water_headers[
                "Referer"
            ] = "https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do"
            water_headers["Cookie"] = (
                "JSESSIONID="
                + self.cookie["JSESSIONID"]
                + ";BWFSESSID_vk35skh3d745n9jzlgg5lvcl2a="
                + self.cookie["BWFSESSID_vk35skh3d745n9jzlgg5lvcl2a"]
            )

            response = self.session.request(
                "POST", url, headers=water_headers, data=payload
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
