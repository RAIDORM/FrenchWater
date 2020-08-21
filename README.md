# FrenchWater

FrenchWater is an api written in python which helps you getting informations about the water near you

## Installation

With pip

```bash
pip install frenchwater
```

## Get your informations

|  parameter  |    type    |                                link                                 |
| :---------: | :--------: | :-----------------------------------------------------------------: |
|   region    | str or int | https://fr.wikipedia.org/wiki/Codes_g%C3%A9ographiques_de_la_France |
| departement |    str     | https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do  |
|   commune   |    str     | https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do  |
|   reseau    |    str     | https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do  |

## Usage

```python
from FrenchWater import FrenchWater

water = FrenchWater(region="93", departement="ALPES-DE-HAUTE-PROVENCE", commune="AIGLUN", reseau="AIGLUN VILLAGE")
```

```python
water.get_last_results()
# return the last results, it looks like this :
{'Entérocoques /100ml-MS': ['<1 n/(100mL)', '14/04/2020'], 'Bact. et spores sulfito-rédu./100ml': ['<1 n/(100mL)', '14/04/2020'], ...}
```

```python
water.get_last_x_results()
# Return latest result for every key, and it looks like this:
{'Entérocoques /100ml-MS': ['<1 n/(100mL)', '14/04/2020'], 'Bact. et spores sulfito-rédu./100ml': ['<1 n/(100mL)', '14/04/2020'], ...}
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
