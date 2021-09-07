import os
import json

BAANPROFIELEN = [
    {'naam': 'Golfsocieteit Lage Vuursche', 'adres': 'Dolderseweg 262 3734 BS Den Dolder', 'telefoon': '030-2292594'},
    {'naam': 'Golf4All Harderwijk', 'adres': 'Pluvierenweg 5 3898 LL Zeewolde', 'telefoon': '0320-288185'},
    {'naam': 'Heidegolf Ullerberg', 'adres': 'Jhr. Sandbergweg 97A 3852 PT Leuvenum', 'telefoon': '0577-407603'},
    {'naam': 'Golfclub Zeewolde', 'adres': 'Golflaan 1 3896 LL Zeewolde', 'telefoon': '036-5222103'},
    {'naam': 'Pitch and Putt Strand Horst', 'adres': 'Palmbosweg 4 3853 LB Ermelo', 'telefoon': '0341-552431'},
    {'naam': 'Het Rijk van Nunspeet', 'adres': 'Plesmanlaan 30 8072 PT Nunspeet', 'telefoon': '0341-255255'},
    {'naam': 'De Scherpenbergh', 'adres': 'Albaweg 43 7364 CB Lieren', 'telefoon': '055-5051262'},
    # {'naam': '', 'adres': '', 'telefoon': ''},
]
GOLFBAANPROFIELEN = [
    # {'naam': 'G4A Harderwijk 18',  'aantalholes': 18, 'sr': 132, 'cr': 71.5, 'par': 72, 'baan': 'Golf4All Harderwijk', 'teekleur': 'geel'},
    {'naam': 'G4A Harderwijk 1e 9', 'aantalholes': 9, 'sr': 129, 'cr': 35.4, 'par': 36, 'baan': 'Golf4All Harderwijk', 'teekleur': 'geel'},
    {'naam': 'G4A Harderwijk 2e 9', 'aantalholes': 9, 'sr': 135, 'cr': 36.2, 'par': 36, 'baan': 'Golf4All Harderwijk', 'teekleur': 'geel'},
    # {'naam': 'Lage Vuursche 18', 'aantalholes': 18,  'sr': 138.0, 'cr': 72.4, 'par': 71, 'baan': 'Golfsocieteit Lage Vuursche', 'teekleur': 'geel'},
    {'naam': 'Lage Vuursche 1e 9', 'aantalholes': 9, 'sr': 129.0, 'cr': 35.8, 'par': 35, 'baan': 'Golfsocieteit Lage Vuursche', 'teekleur': 'geel'},
    {'naam': 'Lage Vuursche 2e 9', 'aantalholes': 9, 'sr': 147.0, 'cr': 36.7, 'par': 36, 'baan': 'Golfsocieteit Lage Vuursche', 'teekleur': 'geel'},
    {'naam': 'Heidegolf', 'aantalholes': 9, 'sr': 113.0, 'cr': 33.6, 'par': 35, 'baan': 'Heidegolf Ullerberg', 'teekleur': 'geel'},
    {'naam': 'Zeewolde Aak', 'aantalholes': 9, 'sr': 139.0, 'cr': 36.8, 'par': 36, 'baan': 'Golfclub Zeewolde', 'teekleur': 'geel'},
    {'naam': 'Zeewolde Botter', 'aantalholes': 9, 'sr': 145.0, 'cr': 37.3, 'par': 36, 'baan': 'Golfclub Zeewolde', 'teekleur': 'geel'},
    {'naam': 'Zeewolde Pluut', 'aantalholes': 9, 'sr': 132.0, 'cr': 36.1, 'par': 36, 'baan': 'Golfclub Zeewolde', 'teekleur': 'geel'},
    # {'naam': 'PnP 18', 'aantalholes': 18, 'sr': 0.0, 'cr': 0.0, 'par': 54, 'baan': 'Pitch and Putt Strand Horst', 'teekleur': 'geel'},
    {'naam': 'PnP 1e 9', 'aantalholes': 9, 'sr': 0.0, 'cr': 0.0, 'par': 27, 'baan': 'Pitch and Putt Strand Horst', 'teekleur': 'geel'},
    {'naam': 'PnP 2e 9', 'aantalholes': 9, 'sr': 0.0, 'cr': 0.0, 'par': 27, 'baan': 'Pitch and Putt Strand Horst', 'teekleur': 'geel'},
    {'naam': 'Rijk Nunspeet Noord', 'aantalholes': 9, 'sr': 138.0, 'cr': 35.6, 'par': 36, 'baan': 'Het Rijk van Nunspeet', 'teekleur': 'geel'},
    {'naam': 'Rijk Nunspeet Oost', 'aantalholes': 9, 'sr': 130.0, 'cr': 35.6, 'par': 36, 'baan': 'Het Rijk van Nunspeet', 'teekleur': 'geel'},
    {'naam': 'Rijk Nunspeet Zuid', 'aantalholes': 9, 'sr': 141.0, 'cr': 36.3, 'par': 36, 'baan': 'Het Rijk van Nunspeet', 'teekleur': 'geel'},
    {'naam': 'Scherpenbergh Zwaluwen', 'aantalholes': 9, 'sr': 128.0, 'cr': 34.9, 'par': 36, 'baan': 'De Scherpenbergh', 'teekleur': 'geel'},
    {'naam': 'Scherpenbergh Dassen', 'aantalholes': 9, 'sr': 123.0, 'cr': 35.2, 'par': 36, 'baan': 'De Scherpenbergh', 'teekleur': 'geel'},
    # {'naam': '', 'aantalholes': 0, 'sr': 0.0, 'cr': 0.0, 'par': 0, 'baan': '', 'teekleur': ''},
]

HOLES = [
    # {'hole_nr': 1, 'par': 4, 'strokeindex': 9, 'afstand': 388, 'golfbaan': 'LV 18'},
    # {'hole_nr': 2, 'par': 4, 'strokeindex': 3, 'afstand': 384, 'golfbaan': 'LV 18'},
    # {'hole_nr': 3, 'par': 4, 'strokeindex': 15, 'afstand': 270, 'golfbaan': 'LV 18'},
    # {'hole_nr': 4, 'par': 3, 'strokeindex': 11, 'afstand': 187, 'golfbaan': 'LV 18'},
    # {'hole_nr': 5, 'par': 4, 'strokeindex': 13, 'afstand': 306, 'golfbaan': 'LV 18'},
    # {'hole_nr': 6, 'par': 3, 'strokeindex': 17, 'afstand': 120, 'golfbaan': 'LV 18'},
    # {'hole_nr': 7, 'par': 4, 'strokeindex': 1, 'afstand': 397, 'golfbaan': 'LV 18'},
    # {'hole_nr': 8, 'par': 5, 'strokeindex': 5, 'afstand': 521, 'golfbaan': 'LV 18'},
    # {'hole_nr': 9, 'par': 4, 'strokeindex': 7, 'afstand': 376, 'golfbaan': 'LV 18'},
    # {'hole_nr': 10, 'par': 4, 'strokeindex': 14, 'afstand': 328, 'golfbaan': 'LV 18'},
    # {'hole_nr': 11, 'par': 4, 'strokeindex': 2, 'afstand': 398, 'golfbaan': 'LV 18'},
    # {'hole_nr': 12, 'par': 5, 'strokeindex': 10, 'afstand': 477, 'golfbaan': 'LV 18'},
    # {'hole_nr': 13, 'par': 4, 'strokeindex': 18, 'afstand': 328, 'golfbaan': 'LV 18'},
    # {'hole_nr': 14, 'par': 3, 'strokeindex': 12, 'afstand': 175, 'golfbaan': 'LV 18'},
    # {'hole_nr': 15, 'par': 4, 'strokeindex': 4, 'afstand': 370, 'golfbaan': 'LV 18'},
    # {'hole_nr': 16, 'par': 5, 'strokeindex': 6, 'afstand': 485, 'golfbaan': 'LV 18'},
    # {'hole_nr': 17, 'par': 3, 'strokeindex': 16, 'afstand': 159, 'golfbaan': 'LV 18'},
    # {'hole_nr': 18, 'par': 4, 'strokeindex': 8, 'afstand': 378, 'golfbaan': 'LV 18'},
    {'hole_nr': 1, 'par': 4,  'strokeindex': 5, 'afstand': 388, 'golfbaan': 'Lage Vuursche 1e 9'},
    {'hole_nr': 2, 'par': 4,  'strokeindex': 2, 'afstand': 384, 'golfbaan': 'Lage Vuursche 1e 9'},
    {'hole_nr': 3, 'par': 4,  'strokeindex': 8, 'afstand': 270, 'golfbaan': 'Lage Vuursche 1e 9'},
    {'hole_nr': 4, 'par': 3,  'strokeindex': 6, 'afstand': 187, 'golfbaan': 'Lage Vuursche 1e 9'},
    {'hole_nr': 5, 'par': 4,  'strokeindex': 7, 'afstand': 306, 'golfbaan': 'Lage Vuursche 1e 9'},
    {'hole_nr': 6, 'par': 3,  'strokeindex': 9, 'afstand': 120, 'golfbaan': 'Lage Vuursche 1e 9'},
    {'hole_nr': 7, 'par': 4,  'strokeindex': 1, 'afstand': 397, 'golfbaan': 'Lage Vuursche 1e 9'},
    {'hole_nr': 8, 'par': 5,  'strokeindex': 3, 'afstand': 521, 'golfbaan': 'Lage Vuursche 1e 9'},
    {'hole_nr': 9, 'par': 4,  'strokeindex': 4, 'afstand': 376, 'golfbaan': 'Lage Vuursche 1e 9'},
    {'hole_nr': 10, 'par': 4, 'strokeindex': 7, 'afstand': 328, 'golfbaan': 'Lage Vuursche 2e 9'},
    {'hole_nr': 11, 'par': 4, 'strokeindex': 1, 'afstand': 398, 'golfbaan': 'Lage Vuursche 2e 9'},
    {'hole_nr': 12, 'par': 5, 'strokeindex': 5, 'afstand': 477, 'golfbaan': 'Lage Vuursche 2e 9'},
    {'hole_nr': 13, 'par': 4, 'strokeindex': 9, 'afstand': 328, 'golfbaan': 'Lage Vuursche 2e 9'},
    {'hole_nr': 14, 'par': 3, 'strokeindex': 6, 'afstand': 175, 'golfbaan': 'Lage Vuursche 2e 9'},
    {'hole_nr': 15, 'par': 4, 'strokeindex': 2, 'afstand': 370, 'golfbaan': 'Lage Vuursche 2e 9'},
    {'hole_nr': 16, 'par': 5, 'strokeindex': 3, 'afstand': 485, 'golfbaan': 'Lage Vuursche 2e 9'},
    {'hole_nr': 17, 'par': 3, 'strokeindex': 8, 'afstand': 159, 'golfbaan': 'Lage Vuursche 2e 9'},
    {'hole_nr': 18, 'par': 4, 'strokeindex': 4, 'afstand': 378, 'golfbaan': 'Lage Vuursche 2e 9'},

    # {'hole_nr': 1,  'par': 4, 'strokeindex': 2,  'afstand': 357, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 2,  'par': 4, 'strokeindex': 12, 'afstand': 292, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 3,  'par': 3, 'strokeindex': 18, 'afstand': 142, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 4,  'par': 4, 'strokeindex': 6,  'afstand': 324, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 5,  'par': 3, 'strokeindex': 16, 'afstand': 148, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 6,  'par': 5, 'strokeindex': 10, 'afstand': 418, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 7,  'par': 4, 'strokeindex': 4,  'afstand': 293, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 8,  'par': 4, 'strokeindex': 8,  'afstand': 352, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 9,  'par': 5, 'strokeindex': 14, 'afstand': 436, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 10, 'par': 4, 'strokeindex': 9,  'afstand': 336, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 11, 'par': 3, 'strokeindex': 13, 'afstand': 165, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 12, 'par': 5, 'strokeindex': 5,  'afstand': 470, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 13, 'par': 4, 'strokeindex': 7,  'afstand': 363, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 14, 'par': 3, 'strokeindex': 17, 'afstand': 130, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 15, 'par': 4, 'strokeindex': 3,  'afstand': 345, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 16, 'par': 4, 'strokeindex': 15, 'afstand': 304, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 17, 'par': 4, 'strokeindex': 1,  'afstand': 367, 'golfbaan': 'G4A Harderwijk 18'},
    # {'hole_nr': 18, 'par': 5, 'strokeindex': 11, 'afstand': 417, 'golfbaan': 'G4A Harderwijk 18'},
    {'hole_nr': 1,  'par': 4, 'strokeindex': 1,  'afstand': 357, 'golfbaan': 'G4A Harderwijk 1e 9'},
    {'hole_nr': 2,  'par': 4, 'strokeindex': 6, 'afstand': 292, 'golfbaan': 'G4A Harderwijk 1e 9'},
    {'hole_nr': 3,  'par': 3, 'strokeindex': 9, 'afstand': 142, 'golfbaan': 'G4A Harderwijk 1e 9'},
    {'hole_nr': 4,  'par': 4, 'strokeindex': 3,  'afstand': 324, 'golfbaan': 'G4A Harderwijk 1e 9'},
    {'hole_nr': 5,  'par': 3, 'strokeindex': 8, 'afstand': 148, 'golfbaan': 'G4A Harderwijk 1e 9'},
    {'hole_nr': 6,  'par': 5, 'strokeindex': 5, 'afstand': 418, 'golfbaan': 'G4A Harderwijk 1e 9'},
    {'hole_nr': 7,  'par': 4, 'strokeindex': 2,  'afstand': 293, 'golfbaan': 'G4A Harderwijk 1e 9'},
    {'hole_nr': 8,  'par': 4, 'strokeindex': 4,  'afstand': 352, 'golfbaan': 'G4A Harderwijk 1e 9'},
    {'hole_nr': 9,  'par': 5, 'strokeindex': 7, 'afstand': 436, 'golfbaan': 'G4A Harderwijk 1e 9'},
    {'hole_nr': 10, 'par': 4, 'strokeindex': 5,  'afstand': 336, 'golfbaan': 'G4A Harderwijk 2e 9'},
    {'hole_nr': 11, 'par': 3, 'strokeindex': 7, 'afstand': 165, 'golfbaan': 'G4A Harderwijk 2e 9'},
    {'hole_nr': 12, 'par': 5, 'strokeindex': 3,  'afstand': 470, 'golfbaan': 'G4A Harderwijk 2e 9'},
    {'hole_nr': 13, 'par': 4, 'strokeindex': 4,  'afstand': 363, 'golfbaan': 'G4A Harderwijk 2e 9'},
    {'hole_nr': 14, 'par': 3, 'strokeindex': 9, 'afstand': 130, 'golfbaan': 'G4A Harderwijk 2e 9'},
    {'hole_nr': 15, 'par': 4, 'strokeindex': 2,  'afstand': 345, 'golfbaan': 'G4A Harderwijk 2e 9'},
    {'hole_nr': 16, 'par': 4, 'strokeindex': 8, 'afstand': 304, 'golfbaan': 'G4A Harderwijk 2e 9'},
    {'hole_nr': 17, 'par': 4, 'strokeindex': 1,  'afstand': 367, 'golfbaan': 'G4A Harderwijk 2e 9'},
    {'hole_nr': 18, 'par': 5, 'strokeindex': 6, 'afstand': 417, 'golfbaan': 'G4A Harderwijk 2e 9'},

    {'hole_nr': 1, 'par': 3,  'strokeindex': 6, 'afstand': 137, 'golfbaan': 'Heidegolf'},
    {'hole_nr': 2, 'par': 4,  'strokeindex': 7, 'afstand': 350, 'golfbaan': 'Heidegolf'},
    {'hole_nr': 3, 'par': 4,  'strokeindex': 9, 'afstand': 246, 'golfbaan': 'Heidegolf'},
    {'hole_nr': 4, 'par': 4,  'strokeindex': 2, 'afstand': 387, 'golfbaan': 'Heidegolf'},
    {'hole_nr': 5, 'par': 4,  'strokeindex': 3, 'afstand': 383, 'golfbaan': 'Heidegolf'},
    {'hole_nr': 6, 'par': 4,  'strokeindex': 5, 'afstand': 301, 'golfbaan': 'Heidegolf'},
    {'hole_nr': 7, 'par': 5,  'strokeindex': 4, 'afstand': 463, 'golfbaan': 'Heidegolf'},
    {'hole_nr': 8, 'par': 3,  'strokeindex': 8, 'afstand': 116, 'golfbaan': 'Heidegolf'},
    {'hole_nr': 9, 'par': 4,  'strokeindex': 1, 'afstand': 423, 'golfbaan': 'Heidegolf'},

    {'hole_nr': 1, 'par': 4,  'strokeindex': 9, 'afstand': 309, 'golfbaan': 'Zeewolde Aak'},
    {'hole_nr': 2, 'par': 3,  'strokeindex': 4, 'afstand': 165, 'golfbaan': 'Zeewolde Aak'},
    {'hole_nr': 3, 'par': 4,  'strokeindex': 1, 'afstand': 401, 'golfbaan': 'Zeewolde Aak'},
    {'hole_nr': 4, 'par': 4,  'strokeindex': 2, 'afstand': 386, 'golfbaan': 'Zeewolde Aak'},
    {'hole_nr': 5, 'par': 5,  'strokeindex': 8, 'afstand': 463, 'golfbaan': 'Zeewolde Aak'},
    {'hole_nr': 6, 'par': 4,  'strokeindex': 6, 'afstand': 333, 'golfbaan': 'Zeewolde Aak'},
    {'hole_nr': 7, 'par': 4,  'strokeindex': 3, 'afstand': 384, 'golfbaan': 'Zeewolde Aak'},
    {'hole_nr': 8, 'par': 3,  'strokeindex': 5, 'afstand': 134, 'golfbaan': 'Zeewolde Aak'},
    {'hole_nr': 9, 'par': 5,  'strokeindex': 7, 'afstand': 469, 'golfbaan': 'Zeewolde Aak'},
    {'hole_nr': 1, 'par': 4,  'strokeindex': 7, 'afstand': 344, 'golfbaan': 'Zeewolde Botter'},
    {'hole_nr': 2, 'par': 3,  'strokeindex': 8, 'afstand': 136, 'golfbaan': 'Zeewolde Botter'},
    {'hole_nr': 3, 'par': 4,  'strokeindex': 1, 'afstand': 371, 'golfbaan': 'Zeewolde Botter'},
    {'hole_nr': 4, 'par': 4,  'strokeindex': 2, 'afstand': 413, 'golfbaan': 'Zeewolde Botter'},
    {'hole_nr': 5, 'par': 3,  'strokeindex': 6, 'afstand': 176, 'golfbaan': 'Zeewolde Botter'},
    {'hole_nr': 6, 'par': 4,  'strokeindex': 5, 'afstand': 365, 'golfbaan': 'Zeewolde Botter'},
    {'hole_nr': 7, 'par': 5,  'strokeindex': 9, 'afstand': 446, 'golfbaan': 'Zeewolde Botter'},
    {'hole_nr': 8, 'par': 5,  'strokeindex': 3, 'afstand': 475, 'golfbaan': 'Zeewolde Botter'},
    {'hole_nr': 9, 'par': 4,  'strokeindex': 4, 'afstand': 378, 'golfbaan': 'Zeewolde Botter'},
    {'hole_nr': 1, 'par': 4,  'strokeindex': 5, 'afstand': 284, 'golfbaan': 'Zeewolde Pluut'},
    {'hole_nr': 2, 'par': 5,  'strokeindex': 6, 'afstand': 472, 'golfbaan': 'Zeewolde Pluut'},
    {'hole_nr': 3, 'par': 3,  'strokeindex': 3, 'afstand': 178, 'golfbaan': 'Zeewolde Pluut'},
    {'hole_nr': 4, 'par': 4,  'strokeindex': 2, 'afstand': 365, 'golfbaan': 'Zeewolde Pluut'},
    {'hole_nr': 5, 'par': 3,  'strokeindex': 9, 'afstand': 119, 'golfbaan': 'Zeewolde Pluut'},
    {'hole_nr': 6, 'par': 4,  'strokeindex': 1, 'afstand': 391, 'golfbaan': 'Zeewolde Pluut'},
    {'hole_nr': 7, 'par': 4,  'strokeindex': 8, 'afstand': 279, 'golfbaan': 'Zeewolde Pluut'},
    {'hole_nr': 8, 'par': 5,  'strokeindex': 7, 'afstand': 460, 'golfbaan': 'Zeewolde Pluut'},
    {'hole_nr': 9, 'par': 4,  'strokeindex': 4, 'afstand': 348, 'golfbaan': 'Zeewolde Pluut'},

    # {'hole_nr': 1,  'par': 3, 'strokeindex': 1,  'afstand': 50, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 2,  'par': 3, 'strokeindex': 2,  'afstand': 36, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 3,  'par': 3, 'strokeindex': 3,  'afstand': 51, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 4,  'par': 3, 'strokeindex': 4,  'afstand': 41, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 5,  'par': 3, 'strokeindex': 5,  'afstand': 63, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 6,  'par': 3, 'strokeindex': 6,  'afstand': 58, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 7,  'par': 3, 'strokeindex': 7,  'afstand': 67, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 8,  'par': 3, 'strokeindex': 8,  'afstand': 43, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 9,  'par': 3, 'strokeindex': 9,  'afstand': 48, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 10, 'par': 3, 'strokeindex': 10, 'afstand': 59, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 11, 'par': 3, 'strokeindex': 11, 'afstand': 51, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 12, 'par': 3, 'strokeindex': 12, 'afstand': 40, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 13, 'par': 3, 'strokeindex': 13, 'afstand': 37, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 14, 'par': 3, 'strokeindex': 14, 'afstand': 55, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 15, 'par': 3, 'strokeindex': 15, 'afstand': 45, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 16, 'par': 3, 'strokeindex': 16, 'afstand': 60, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 17, 'par': 3, 'strokeindex': 17, 'afstand': 56, 'golfbaan': 'PnP 18'},
    # {'hole_nr': 18, 'par': 3, 'strokeindex': 18, 'afstand': 62, 'golfbaan': 'PnP 18'},
    {'hole_nr': 1, 'par':  3, 'strokeindex': 1, 'afstand': 50,  'golfbaan': 'PnP 1e 9'},
    {'hole_nr': 2, 'par':  3, 'strokeindex': 2, 'afstand': 36,  'golfbaan': 'PnP 1e 9'},
    {'hole_nr': 3, 'par':  3, 'strokeindex': 3, 'afstand': 51,  'golfbaan': 'PnP 1e 9'},
    {'hole_nr': 4, 'par':  3, 'strokeindex': 4, 'afstand': 41,  'golfbaan': 'PnP 1e 9'},
    {'hole_nr': 5, 'par':  3, 'strokeindex': 5, 'afstand': 63,  'golfbaan': 'PnP 1e 9'},
    {'hole_nr': 6, 'par':  3, 'strokeindex': 6, 'afstand': 58,  'golfbaan': 'PnP 1e 9'},
    {'hole_nr': 7, 'par':  3, 'strokeindex': 7, 'afstand': 67,  'golfbaan': 'PnP 1e 9'},
    {'hole_nr': 8, 'par':  3, 'strokeindex': 8, 'afstand': 43,  'golfbaan': 'PnP 1e 9'},
    {'hole_nr': 9, 'par':  3, 'strokeindex': 9, 'afstand': 48,  'golfbaan': 'PnP 1e 9'},
    {'hole_nr': 10, 'par': 3, 'strokeindex': 1, 'afstand': 59,  'golfbaan': 'PnP 2e 9'},
    {'hole_nr': 11, 'par': 3, 'strokeindex': 2, 'afstand': 51,  'golfbaan': 'PnP 2e 9'},
    {'hole_nr': 12, 'par': 3, 'strokeindex': 3, 'afstand': 40,  'golfbaan': 'PnP 2e 9'},
    {'hole_nr': 13, 'par': 3, 'strokeindex': 4, 'afstand': 37,  'golfbaan': 'PnP 2e 9'},
    {'hole_nr': 14, 'par': 3, 'strokeindex': 5, 'afstand': 55,  'golfbaan': 'PnP 2e 9'},
    {'hole_nr': 15, 'par': 3, 'strokeindex': 6, 'afstand': 45,  'golfbaan': 'PnP 2e 9'},
    {'hole_nr': 16, 'par': 3, 'strokeindex': 7, 'afstand': 60,  'golfbaan': 'PnP 2e 9'},
    {'hole_nr': 17, 'par': 3, 'strokeindex': 8, 'afstand': 56,  'golfbaan': 'PnP 2e 9'},
    {'hole_nr': 18, 'par': 3, 'strokeindex': 9, 'afstand': 62,  'golfbaan': 'PnP 2e 9'},

    {'hole_nr': 1,  'par': 4, 'strokeindex': 5, 'afstand': 331, 'golfbaan': 'Rijk Nunspeet Noord'},
    {'hole_nr': 2,  'par': 3, 'strokeindex': 9, 'afstand': 141, 'golfbaan': 'Rijk Nunspeet Noord'},
    {'hole_nr': 3,  'par': 5, 'strokeindex': 3, 'afstand': 442, 'golfbaan': 'Rijk Nunspeet Noord'},
    {'hole_nr': 4,  'par': 4, 'strokeindex': 7, 'afstand': 309, 'golfbaan': 'Rijk Nunspeet Noord'},
    {'hole_nr': 5,  'par': 4, 'strokeindex': 2, 'afstand': 336, 'golfbaan': 'Rijk Nunspeet Noord'},
    {'hole_nr': 6,  'par': 4, 'strokeindex': 1, 'afstand': 367, 'golfbaan': 'Rijk Nunspeet Noord'},
    {'hole_nr': 7,  'par': 3, 'strokeindex': 6, 'afstand': 160, 'golfbaan': 'Rijk Nunspeet Noord'},
    {'hole_nr': 8,  'par': 5, 'strokeindex': 4, 'afstand': 469, 'golfbaan': 'Rijk Nunspeet Noord'},
    {'hole_nr': 9,  'par': 4, 'strokeindex': 8, 'afstand': 339, 'golfbaan': 'Rijk Nunspeet Noord'},
    {'hole_nr': 1,  'par': 5, 'strokeindex': 5, 'afstand': 477, 'golfbaan': 'Rijk Nunspeet Oost'},
    {'hole_nr': 2,  'par': 4, 'strokeindex': 9, 'afstand': 262, 'golfbaan': 'Rijk Nunspeet Oost'},
    {'hole_nr': 3,  'par': 3, 'strokeindex': 8, 'afstand': 147, 'golfbaan': 'Rijk Nunspeet Oost'},
    {'hole_nr': 4,  'par': 5, 'strokeindex': 3, 'afstand': 467, 'golfbaan': 'Rijk Nunspeet Oost'},
    {'hole_nr': 5,  'par': 4, 'strokeindex': 7, 'afstand': 322, 'golfbaan': 'Rijk Nunspeet Oost'},
    {'hole_nr': 6,  'par': 4, 'strokeindex': 1, 'afstand': 371, 'golfbaan': 'Rijk Nunspeet Oost'},
    {'hole_nr': 7,  'par': 3, 'strokeindex': 6, 'afstand': 187, 'golfbaan': 'Rijk Nunspeet Oost'},
    {'hole_nr': 8,  'par': 4, 'strokeindex': 4, 'afstand': 345, 'golfbaan': 'Rijk Nunspeet Oost'},
    {'hole_nr': 9,  'par': 4, 'strokeindex': 2, 'afstand': 391, 'golfbaan': 'Rijk Nunspeet Oost'},
    {'hole_nr': 1,  'par': 4, 'strokeindex': 7, 'afstand': 339, 'golfbaan': 'Rijk Nunspeet Zuid'},
    {'hole_nr': 2,  'par': 5, 'strokeindex': 4, 'afstand': 458, 'golfbaan': 'Rijk Nunspeet Zuid'},
    {'hole_nr': 3,  'par': 3, 'strokeindex': 9, 'afstand': 144, 'golfbaan': 'Rijk Nunspeet Zuid'},
    {'hole_nr': 4,  'par': 4, 'strokeindex': 2, 'afstand': 362, 'golfbaan': 'Rijk Nunspeet Zuid'},
    {'hole_nr': 5,  'par': 4, 'strokeindex': 1, 'afstand': 400, 'golfbaan': 'Rijk Nunspeet Zuid'},
    {'hole_nr': 6,  'par': 4, 'strokeindex': 8, 'afstand': 329, 'golfbaan': 'Rijk Nunspeet Zuid'},
    {'hole_nr': 7,  'par': 4, 'strokeindex': 5, 'afstand': 326, 'golfbaan': 'Rijk Nunspeet Zuid'},
    {'hole_nr': 8,  'par': 3, 'strokeindex': 6, 'afstand': 174, 'golfbaan': 'Rijk Nunspeet Zuid'},
    {'hole_nr': 9,  'par': 5, 'strokeindex': 3, 'afstand': 501, 'golfbaan': 'Rijk Nunspeet Zuid'},

    {'hole_nr': 1,  'par': 5, 'strokeindex': 3, 'afstand': 431, 'golfbaan': 'Scherpenbergh Zwaluwen'},
    {'hole_nr': 2,  'par': 3, 'strokeindex': 9, 'afstand': 151, 'golfbaan': 'Scherpenbergh Zwaluwen'},
    {'hole_nr': 3,  'par': 4, 'strokeindex': 4, 'afstand': 319, 'golfbaan': 'Scherpenbergh Zwaluwen'},
    {'hole_nr': 4,  'par': 3, 'strokeindex': 8, 'afstand': 130, 'golfbaan': 'Scherpenbergh Zwaluwen'},
    {'hole_nr': 5,  'par': 4, 'strokeindex': 2, 'afstand': 330, 'golfbaan': 'Scherpenbergh Zwaluwen'},
    {'hole_nr': 6,  'par': 3, 'strokeindex': 6, 'afstand': 160, 'golfbaan': 'Scherpenbergh Zwaluwen'},
    {'hole_nr': 7,  'par': 5, 'strokeindex': 7, 'afstand': 442, 'golfbaan': 'Scherpenbergh Zwaluwen'},
    {'hole_nr': 8,  'par': 5, 'strokeindex': 1, 'afstand': 455, 'golfbaan': 'Scherpenbergh Zwaluwen'},
    {'hole_nr': 9,  'par': 4, 'strokeindex': 5, 'afstand': 348, 'golfbaan': 'Scherpenbergh Zwaluwen'},
    {'hole_nr': 10, 'par': 5, 'strokeindex': 2, 'afstand': 450, 'golfbaan': 'Scherpenbergh Dassen'},
    {'hole_nr': 11, 'par': 4, 'strokeindex': 6, 'afstand': 244, 'golfbaan': 'Scherpenbergh Dassen'},
    {'hole_nr': 12, 'par': 4, 'strokeindex': 7, 'afstand': 300, 'golfbaan': 'Scherpenbergh Dassen'},
    {'hole_nr': 13, 'par': 3, 'strokeindex': 5, 'afstand': 181, 'golfbaan': 'Scherpenbergh Dassen'},
    {'hole_nr': 14, 'par': 3, 'strokeindex': 1, 'afstand': 361, 'golfbaan': 'Scherpenbergh Dassen'},
    {'hole_nr': 15, 'par': 3, 'strokeindex': 9, 'afstand': 141, 'golfbaan': 'Scherpenbergh Dassen'},
    {'hole_nr': 16, 'par': 4, 'strokeindex': 3, 'afstand': 380, 'golfbaan': 'Scherpenbergh Dassen'},
    {'hole_nr': 17, 'par': 4, 'strokeindex': 8, 'afstand': 295, 'golfbaan': 'Scherpenbergh Dassen'},
    {'hole_nr': 18, 'par': 5, 'strokeindex': 4, 'afstand': 446, 'golfbaan': 'Scherpenbergh Dassen'},

    # {'hole_nr': 0, 'par': 0, 'strokeindex': 0, 'afstand': 0, 'golfbaan': ''},

]


def check_baanprofielen():
    # Basic check on consistency of holes
    baanprofiel_namen = [item['naam'] for item in BAANPROFIELEN]
    for golfbaanprofiel in GOLFBAANPROFIELEN:
        if golfbaanprofiel['baan'] not in baanprofiel_namen:
            raise ValueError('Golfbaanprofiel {} baan {} is not in BAANPROFIELEN'.format(golfbaanprofiel['naam'],
                                                                                         golfbaanprofiel['baan']))
        holes_in_golfbaan = [item for item in HOLES if item['golfbaan'] == golfbaanprofiel['naam']]
        if len(holes_in_golfbaan) != golfbaanprofiel['aantalholes']:
            raise IndexError('Golfbaanprofiel {} aantalholes {} is not equal to number in holes collection {}'.
                             format(golfbaanprofiel['naam'], golfbaanprofiel['aantalholes'], len(holes_in_golfbaan)))
        stroke_indices = [item['strokeindex'] for item in holes_in_golfbaan]
        if min(stroke_indices) < 1 or max(stroke_indices) > len(holes_in_golfbaan) or \
           len(set(stroke_indices)) != len(stroke_indices):
            raise ValueError('Stroke indices for golfbaanprofiel {} are not consistent: {}'.
                             format(golfbaanprofiel['naam'], stroke_indices))

    golfbaanprofiel_namen = [item['naam'] for item in GOLFBAANPROFIELEN]
    for hole in HOLES:
        if hole['golfbaan'] not in golfbaanprofiel_namen:
            raise ValueError('Hole {} golfbaan {} is not in GOLFBAANPROFIELEN'.format(hole['hole_nr'],
                                                                                      hole['golfbaan']))


def export_baan_info_as_json_fixtures():
    fixtures_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    baanprofiel_namen = [item['naam'] for item in BAANPROFIELEN]
    golfbaanprofiel_namen = [item['naam'] for item in GOLFBAANPROFIELEN]
    if not os.path.exists(fixtures_directory):
        os.mkdir(fixtures_directory)
    for iteration in ['BaanProfiel', 'GolfBaanProfiel', 'Hole']:
        if iteration == 'BaanProfiel':
            json_source_list = BAANPROFIELEN
        elif iteration == 'GolfBaanProfiel':
            json_source_list = GOLFBAANPROFIELEN
        elif iteration == 'Hole':
            json_source_list = HOLES
        else:
            raise IndexError('Invalid iteration {}'.format(iteration))
        json_fixture_list = list()
        pk = 1
        for item in json_source_list:
            new_dictionary_item = {
                'model': 'luukopen21.{}'.format(iteration),
                'pk': pk,
                'fields': item,
            }
            # Change references to parent items for golfbaanprofiel and hole
            if iteration == 'GolfBaanProfiel':
                new_dictionary_item['fields']['baan'] = \
                    baanprofiel_namen.index(new_dictionary_item['fields']['baan']) + 1
                # Assume 1 teekleur (pk=1)
                new_dictionary_item['fields']['teekleur'] = 1
            elif iteration == 'Hole':
                new_dictionary_item['fields']['golfbaan'] = \
                    golfbaanprofiel_namen.index(new_dictionary_item['fields']['golfbaan']) + 1
            json_fixture_list += [new_dictionary_item]
            pk += 1
        output_filename = '{}.json'.format(iteration)
        with open(os.path.join(fixtures_directory, output_filename), 'w') as file_handle:
            json.dump(json_fixture_list, file_handle)
        print('Use python manage.py loaddata {} to re-initialize the database with the {} info'.
              format(output_filename, iteration))


def main():
    check_baanprofielen()
    export_baan_info_as_json_fixtures()


if __name__ == '__main__':
    main()
    