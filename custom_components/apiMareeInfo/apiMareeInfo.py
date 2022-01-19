from datetime import datetime
import json
import logging
import requests

_LOGGER = logging.getLogger(__name__)


def getjson(url):
    try:
        session = requests.Session()
        response = session.post(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        response = {"error": "UNKERROR_001"}
        return response
    except requests.exceptions.HTTPError:
        return response.json()
    pass


class ListePorts:
    def getlisteport(self, nomport):
        url = f"http://webservices.meteoconsult.fr/meteoconsultmarine/android/100/fr/v20/recherche.php?rech={nomport}&type=48"
        ret = getjson(url)

        for x in ret["contenu"]:
            print(x["id"], x["nom"], x["lat"], x["lon"])
        return ret


class ApiMareeInfo:
    def __init__(self):
        self._donnees = {}
        self._nomDuPort = None
        self._dateCourante = None
        self._lat = None
        self._lng = None

    def setport(self, lat, lng):
        self._lat = lat
        self._lng = lng
        self._url = f"http://webservices.meteoconsult.fr/meteoconsultmarine/androidtab/115/fr/v20/previsionsSpot.php?lat={lat}&lon={lng}"
        """ autre url possible
        self._url = \
        #    "http://webservices.meteoconsult.fr/meteoconsultmarine/android/100/fr/v20/previsionsSpot.php?lat=%s&lon=%s" % (
        #    lat, lng)
        #print(self._url)
        """

    def getinformationport(self, jsondata=None, outfile=None):
        if jsondata is None:
            jsondata = getjson(self._url)

        if outfile is not None:
            with open("port.json", "w") as outfile:
                json.dump(jsondata, outfile)

        self._nomDuPort = jsondata["contenu"]["marees"][0]["lieu"]
        self._dateCourante = jsondata["contenu"]["marees"][0]["datetime"]

        myMarees = {}
        j = 0
        for maree in jsondata["contenu"]["marees"][:6]:
            i = 0
            for ele in maree["etales"]:
                dateComplete = datetime.fromisoformat(ele["datetime"])
                detailMaree = {
                    "coeff": ele.get("coef", ""),
                    "hauteur": ele["hauteur"],
                    "horaire": dateComplete.strftime("%H:%M"),
                    "etat": ele["type_etale"],
                    "nieme": i,
                    "jour": j,
                    "date": ele["datetime"],
                    "dateComplete": dateComplete.replace(tzinfo=None),
                }
                clef = f"horaire_{j}_{i}"
                myMarees[clef] = detailMaree
                # print(clef, detailMaree)
                i += 1
            j += 1
        self._donnees = myMarees

        dicoPrevis = {}
        for ele in jsondata["contenu"]["previs"]["detail"]:
            dateComplete = datetime.fromisoformat(ele["datetime"])
            detailPrevis = {
                "forcevnds": ele.get("forcevnds", ""),
                "rafvnds": ele.get("rafvnds", ""),
                "dirvdegres": ele.get("dirvdegres", ""),
                "dateComplete": dateComplete.replace(tzinfo=None),
                "nuagecouverture": ele.get("nuagecouverture", ""),
                "precipitation": ele.get("precipitation", ""),
                "teau": ele.get("teau", ""),
                "t": ele.get("t", ""),
                "risqueorage": ele.get("risqueorage", ""),
                "dirhouledegres": ele.get("dirhouledegres", ""),
                "hauteurhoule": ele.get("hauteurhoule", ""),
                "periodehoule": ele.get("periodehoule", ""),
                "hauteurmerv": ele.get("hauteurmerv", ""),
                "periodemerv": ele.get("periodemerv", ""),
                "hauteurvague": ele.get("hauteurvague", ""),
            }
            clef = dateComplete
            dicoPrevis[clef] = detailPrevis
        self._donneesPrevis = dicoPrevis

    def getnomduport(self):
        return self._nomDuPort.split("©")[0].strip()

    def getcopyright(self):
        return "©SHOM"

    def getnomcompletduport(self):
        return self._nomDuPort

    def getdatecourante(self):
        return self._dateCourante

    def getinfo(self):
        return self._donnees

    def getprevis(self):
        return self._donneesPrevis
