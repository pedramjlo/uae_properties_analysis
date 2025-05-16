"""
This file contains information about the United Arab Emirates
which can be used in analysing process of the data for fature engineering and etc.
"""


class UAEInfo:

    def uae_cities():
        uae_cities = [
        "Dubai",
        "Abu Dhabi",
        "Sharjah",
        "Al Ain",
        "Ajman",
        "Ras Al Khaimah",
        "Fujairah",
        "Umm Al Quwain",
        "Kalba",
        "Dibba Al-Fujairah",
        "Madinat Zayed",
        "Khor Fakkan",
        "Al Dhannah",
        "Ghayathi",
        "Dhaid",
        "Jebel Ali",
        "Liwa Oasis",
        "Hatta",
        "Ar-Rams",
        "Dibba Al-Hisn",
        "Al Jazirah Al Hamra",
        "Al Mirfa",
        "Masfut",
        "Masafi",
        "Al Madam",
        "Al Manama",
        "Al Khawaneej",
        "Al Awir",
        "Al Faqa",
        "Al Lisaili",
        "Sweihan",
        "Dalma",
        "Falaj Al Mualla",
        "Sila",
        "Al Badiyah",
        "Al Jeer",
        "Al Hamriyah",
        "Al Ajban",
        "Al Yahar",
        "Al Bataeh",
        "Al Ruwayyah",
        "Al Nakhil",
        "Al Nuaimia",
        "Al Gharbia",
        "Al Aryam",
        "Al Qusaidat",
        "Al Qor",
        "Al Salamah",
        "Al Shuwaib",
        "Al Rafaah",
        "Al Rashidya",
        "Asimah",
        "Dadna",
        "Digdaga",
        "Ghalilah",
        "Ghayl",
        "Ghub",
        "Habshan",
        "Huwaylat",
        "Khatt",
        "Khor Khwair",
        "Lahbab",
        "Manama",
        "Marawah",
        "Mirbah",
        "Mleiha",
        "Nahil",
        "Qidfa",
        "Sha'am",
        "Wadi Shah",
        "Zubarah"
    ]
        return uae_cities

import requests

url = 'https://releaseeuaestat.fcsc.gov.ae/rest/data/FCSA,DF_NA_COMP_CUR,3.4.0/.A.............?startPeriod=2015&dimensionAtObservation=AllDimensions'

params = {
    "city": "Dubai"
}

print(requests.get(url, params=None).json)