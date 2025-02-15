import trafilatura
import requests
import re
import numpy as np
from sacremoses import MosesDetokenizer, MosesTokenizer
import jieba
import jieba.posseg as pseg

dictOldBooksNTLH = {"Gênesis": 50,
"Êxodo": 40,
"Levítico": 27,
"Números": 36,
"Deuteronômio": 34,
"Josué": 24,
"Juízes": 21,
"Rute": 4,
"1%20Samuel": 31,
"2%20Samuel": 24,
"1%20Reis": 22,
"2%20Reis": 25,
"1%20Crônicas": 29,
"2%20Crônicas": 36,
"Esdras": 10,
"Neemias": 13,
"Ester": 10,
"Jó": 42,
"Salmos": 150,
"Provérbios": 31,
"Eclesiastes": 12,
"Cântico%20dos%20Cânticos": 8,
"Isaías": 66,
"Jeremias": 52,
"Lamentações%20de%20Jeremias": 5,
"Ezequiel": 48,
"Daniel": 12,
"Oseias": 14,
"Joel": 3,
"Amós": 9,
"Obadias": 1,
"Jonas": 4,
"Miqueias": 7,
"Naum": 3,
"Habacuque": 3,
"Sofonias": 3,
"Ageu": 2,
"Zacarias":14,
"Malaquias": 4}



dictOldBooksARC = {"Gênesis": 50,
"Êxodo": 40,
"Levítico": 27,
"Números": 36,
"Deuteronômio": 34,
"Josué": 24,
"Juízes": 21,
"Rute": 4,
"1%20Samuel": 31,
"2%20Samuel": 24,
"1%20Reis": 22,
"2%20Reis": 25,
"1%20Crônicas": 29,
"2%20Crônicas": 36,
"Esdras": 10,
"Neemias": 13,
"Ester": 10,
"Jó": 42,
"Salmos": 150,
"Provérbios": 31,
"Eclesiastes": 12,
"Cantares": 8,
"Isaías": 66,
"Jeremias": 52,
"Lamentações": 5,
"Ezequiel": 48,
"Daniel": 12,
"Oseias": 14,
"Joel": 3,
"Amós": 9,
"Obadias": 1,
"Jonas": 4,
"Miqueias": 7,
"Naum": 3,
"Habacuque": 3,
"Sofonias": 3,
"Ageu": 2,
"Zacarias":14,
"Malaquias": 4}

dicNewBookARC = {"Mateus": 28,
"Marcos": 16,
"Lucas": 24,
"João": 21,
"Atos": 26,
"Romanos": 16,
"1%20Coríntios": 16,
"2%20Coríntios": 13,
"Gálatas": 6,
"Efésios": 6,
"Filipenses": 4,
"Colossenses": 4,
"1%20Tessalonicenses": 5,
"2%20Tessalonicenses": 3,
"1%20Timóteo": 6,
"2%20Timóteo": 4,
"Tito": 3,
"Filemom": 1,
"Hebreus": 13,
"Tiago": 5,
"1%20Pedro": 5,
"2%20Pedro": 3,
"1%20João": 5,
"2%20João": 1,
"3%20João": 1,
"Judas": 1,
"Apocalipse": 22}

dicNewBookVFL = {"Mateus": 28,
"Marcos": 16,
"Lucas": 24,
"João": 21,
"Atos": 26,
"Romanos": 16,
"1%20Coríntios": 16,
"2%20Coríntios": 13,
"Gálatas": 6,
"Efésios": 6,
"Filipenses": 4,
"Colossenses": 4,
"1%20Tessalonicenses": 5,
"2%20Tessalonicenses": 3,
"1%20Timóteo": 6,
"2%20Timóteo": 4,
"Tito": 3,
"Filemom": 1,
"Hebreus": 13,
"Tiago": 5,
"1%20Pedro": 5,
"2%20Pedro": 3,
"1%20João": 5,
"2%20João": 1,
"3%20João": 1,
"Judas": 1,
"Apocalipse": 22}


dicNewBookNTLH = {"Mateus": 28,
"Marcos": 16,
"Lucas": 24,
"João": 21,
"Atos": 26,
"Romanos": 16,
"1%20Coríntios": 16,
"2%20Coríntios": 13,
"Gálatas": 6,
"Efésios": 6,
"Filipenses": 4,
"Colossenses": 4,
"1%20Tessalonicenses": 5,
"2%20Tessalonicenses": 3,
"1%20Timóteo": 6,
"2%20Timóteo": 4,
"Tito": 3,
"Filemom": 1,
"Hebreus": 13,
"Tiago": 5,
"1%20Pedro": 5,
"2%20Pedro": 3,
"1%20João": 5,
"2%20João": 1,
"3%20João": 1,
"Judas": 1,
"Apocalipse": 22}



dicNewBookNVT = {"Mateus": 28,
"Marcos": 16,
"Lucas": 24,
"João": 21,
"Atos": 26,
"Romanos": 16,
"1%20Coríntios": 16,
"2%20Coríntios": 13,
"Gálatas": 6,
"Efésios": 6,
"Filipenses": 4,
"Colossenses": 4,
"1%20Tessalonicenses": 5,
"2%20Tessalonicenses": 3,
"1%20Timóteo": 6,
"2%20Timóteo": 4,
"Tito": 3,
"Filemón": 1,
"Hebreus": 13,
"Tiago": 5,
"1%20Pedro": 5,
"2%20Pedro": 3,
"1%20João": 5,
"2%20João": 1,
"3%20João": 1,
"Judas": 1,
"Apocalipse": 22}


dictOldBookNVT = {"Gênesis": 50,
"Êxodo": 40,
"Levítico": 27,
"Números": 36,
"Deuteronômio": 34,
"Josué": 24,
"Juízes": 21,
"Rute": 4,
"1%20Samuel": 31,
"2%20Samuel": 24,
"1%20Reis": 22,
"2%20Reis": 25,
"1%20Crônicas": 29,
"2%20Crônicas": 36,
"Esdras": 10,
"Neemias": 13,
"Ester": 10,
"Jó": 42,
"Salmos": 150,
"Provérbios": 31,
"Eclesiastes": 12,
"Cantares%20de%20Salomâo": 8,
"Isaías": 66,
"Jeremias": 52,
"Lamentações%20de%20Jeremias": 5,
"Ezequiel": 48,
"Daniel": 12,
"Oseias": 14,
"Joel": 3,
"Amós": 9,
"Obadias": 1,
"Jonas": 4,
"Miquéias": 7,
"Naum": 3,
"Habacuque": 3,
"Sofonias": 3,
"Ageu": 2,
"Zacarias":14,
"Malaquias": 4}



dictOldBookNVIPT = {"Gênesis": 50,
"Êxodo": 40,
"Levítico": 27,
"Números": 36,
"Deuteronômio": 34,
"Josué": 24,
"Juízes": 21,
"Rute": 4,
"1%20Samuel": 31,
"2%20Samuel": 24,
"1%20Reis": 22,
"2%20Reis": 25,
"1%20Crônicas": 29,
"2%20Crônicas": 36,
"Esdras": 10,
"Neemias": 13,
"Ester": 10,
"Jó": 42,
"Salmos": 150,
"Provérbios": 31,
"Eclesiastes": 12,
"Cantares%20de%20Salomâo": 8,
"Isaías": 66,
"Jeremias": 52,
"Lamentações%20de%20Jeremias": 5,
"Ezequiel": 48,
"Daniel": 12,
"Oseias": 14,
"Joel": 3,
"Amós": 9,
"Obadias": 1,
"Jonas": 4,
"Miquéias": 7,
"Naum": 3,
"Habacuque": 3,
"Sofonias": 3,
"Ageu": 2,
"Zacarias":14,
"Malaquias": 4}


dicNewBookNVIPT = {"Mateus": 28,
"Marcos": 16,
"Lucas": 24,
"João": 21,
"Atos": 26,
"Romanos": 16,
"1%20Coríntios": 16,
"2%20Coríntios": 13,
"Gálatas": 6,
"Efésios": 6,
"Filipenses": 4,
"Colossenses": 4,
"1%20Tessalonicenses": 5,
"2%20Tessalonicenses": 3,
"1%20Timóteo": 6,
"2%20Timóteo": 4,
"Tito": 3,
"Filemón": 1,
"Hebreus": 13,
"Tiago": 5,
"1%20Pedro": 5,
"2%20Pedro": 3,
"1%20João": 5,
"2%20João": 1,
"3%20João": 1,
"Judas": 1,
"Apocalipse": 22}




dictOldBookOL = {"Gênesis": 50,
"Êxodo": 40,
"Levítico": 27,
"Números": 36,
"Deuteronômio": 34,
"Josué": 24,
"Juízes": 21,
"Rute": 4,
"1%20Samuel": 31,
"2%20Samuel": 24,
"1%20Reis": 22,
"2%20Reis": 25,
"1%20Crônicas": 29,
"2%20Crônicas": 36,
"Esdras": 10,
"Neemias": 13,
"Ester": 10,
"Jó": 42,
"Salmos": 150,
"Provérbios": 31,
"Eclesiastes": 12,
"Cantares%20de%20Salomâo": 8,
"Isaías": 66,
"Jeremias": 52,
"Lamentações%20de%20Jeremias": 5,
"Ezequiel": 48,
"Daniel": 12,
"Oseias": 14,
"Joel": 3,
"Amós": 9,
"Obadias": 1,
"Jonas": 4,
"Miquéias": 7,
"Naum": 3,
"Habacuque": 3,
"Sofonias": 3,
"Ageu": 2,
"Zacarias":14,
"Malaquias": 4}


dicNewBookOL = {"Mateus": 28,
"Marcos": 16,
"Lucas": 24,
"João": 21,
"Atos": 26,
"Romanos": 16,
"1%20Coríntios": 16,
"2%20Coríntios": 13,
"Gálatas": 6,
"Efésios": 6,
"Filipenses": 4,
"Colossenses": 4,
"1%20Tessalonicenses": 5,
"2%20Tessalonicenses": 3,
"1%20Timóteo": 6,
"2%20Timóteo": 4,
"Tito": 3,
"Filemón": 1,
"Hebreus": 13,
"Tiago": 5,
"1%20Pedro": 5,
"2%20Pedro": 3,
"1%20João": 5,
"2%20João": 1,
"3%20João": 1,
"Judas": 1,
"Apocalipse": 22}





dictEnglishOld = {"Genesis": 50,
"Exodus": 40,
"Leviticus": 27,
"Numbers": 36,
"Deuteronomy": 34,
"Joshua": 24,
"Judges": 21,
"Ruth": 4,
"1%20Samuel": 31,
"2%20Samuel": 24,
"1%20Kings": 22,
"2%20Kings": 25,
"1%20Chronicles": 29,
"2%20Chronicles": 36,
"Ezra": 10,
"Nehemiah": 13,
"Esther": 10,
"Job": 42,
"Psalms": 150,
"Proverbs": 31,
"Ecclesiastes": 12,
"Song%20of%20Solomon": 8,
"Isaiah": 66,
"Jeremiah": 52,
"Lamentations": 5,
"Ezekiel": 48,
"Daniel": 12,
"Hosea": 14,
"Joel": 3,
"Amos": 9,
"Obadiah": 1,
"Jonah": 4,
"Micah": 7,
"Nahum": 3,
"Habakkuk": 3,
"Zephaniah": 3,
"Haggai": 2,
"Zechariah": 14,
"Malachi": 4}

dicEnglishNew = {"Matthew": 28,
"Mark": 16,
"Luke": 24,
"John": 21,
"Romans": 16,
"1%20Corinthians": 16,
"2%20Corinthians": 13,
"Galatians": 6,
"Ephesians": 6,
"Philippians": 4,
"Colossians": 4,
"1%20Thessalonians": 5,
"2%20Thessalonians": 3,
"1%20Timothy": 6,
"2%20Timothy": 4,
"Titus": 3,
"Philemon": 1,
"Hebrews": 13,
"James": 5,
"1%20Peter": 5,
"2%20Peter": 3,
"1%20John": 5,
"2%20John": 1,
"3%20John": 1,
"Jude": 1,
"Revelation": 22
}



dicSpanishNew = {"Mateo": 28,
"Marcos": 16,
"Lucas": 24,
"Juan": 21,
"Actos%20de%20los%20Apóstoles": 28,
"Romanos": 16,
"1%20Corintios": 16,
"2%20Corintios": 13,
"Gálatas": 6,
"Efesios": 6,
"Filipenses": 4,
"Colosenses": 4,
"1%20Tesalonicenses": 5,
"2%20Tesalonicenses": 3,
"1%20Timoteo": 6,
"2%20Timoteo": 4,
"Tito": 3,
"Filemón": 1,
"Hebreos": 13,
"Santiago": 5,
"1%20Pedro": 5,
"2%20Pedro": 3,
"1%20Juan": 5,
"2%20Juan": 1,
"3%20Juan": 1,
"Judas": 1,
"Apocalipsis": 22
}

dictSpanishOld = {"Génesis": 50,
"Éxodo": 40,
"Levítico": 27,
"Números": 36,
"Deuteronomio": 34,
"Josué": 24,
"Jueces": 21,
"Rut": 4,
"1%20Samuel": 31,
"2%20Samuel": 24,
"1%20Reyes": 22,
"2%20Reyes": 25,
"1%20Crónicas": 29,
"2%20Crónicas": 36,
"Esdras": 10,
"Nehemías": 13,
"Ester": 10,
"Job": 42,
"Salmos": 150,
"Proverbios": 31,
"Eclesiastés": 12,
"Cantar%20de%20los%20Cantares": 8,
"Isaías": 66,
"Jeremías": 52,
"Lamentaciones": 5,
"Ezequiel": 48,
"Daniel": 12,
"Oseas": 14,
"Joel": 3,
"Amós": 9,
"Obadías": 1,
"Jonás": 4,
"Miqueas": 7,
"Naún": 3,
"Habacuque": 3,
"Sofonías": 3,
"Ageo": 2,
"Zacarías": 14,
"Malaquías": 4}

dictFrenchOld = {"Genèse": 50,
"Exode": 40,
"Lévitique": 27,
"Nombres": 36,
"Deutéronome": 34,
"Josué": 24,
"Juges": 21,
"Ruth": 4,
"1%20Samuel": 31,
"2%20Samuel": 24,
"1%20Rois": 22,
"2%20Rois": 25,
"1%20Chroniques": 29,
"2%20Chroniques": 36,
"Esdras": 10,
"Néhémie": 13,
"Esther": 10,
"Job": 42,
"Psaumes": 150,
"Proverbes": 31,
"Ecclésiaste": 12,
"Cantique%20des%20Cantiques": 8,
"Ésaïe": 66,
"Jérémie": 52,
"Lamentations": 5,
"Ézéchiel": 48,
"Daniel": 12,
"Osée": 14,
"Joël": 3,
"Amos": 9,
"Abdias": 1,
"Jonas": 4,
"Michée": 7,
"Nahum": 3,
"Habacuc": 3,
"Sophonie": 3,
"Aggée": 2,
"Zacharie": 14,
"Malachie": 4}



dicFenchNew = {"Matthieu": 28,
"Marc": 16,
"Luc": 24,
"Jean": 21,
"Actes": 28,
"Romains": 16,
"1%20Corinthiens": 16,
"2%20Corinthiens": 13,
"Galates": 6,
"Éphésiens": 6,
"Philippiens": 4,
"Colossiens": 4,
"1%20Thessaloniciens": 5,
"2%20Thessaloniciens": 3,
"1%20Timothée": 6,
"2%20Timothée": 4,
"Tite": 3,
"Philémon": 1,
"Hébreux": 13,
"Jacques": 5,
"1%20Pierre": 5,
"2%20Pierre": 3,
"1%20Jean": 5,
"2%20Jean": 1,
"3%20Jean": 1,
"Jude": 1,
"Apocalypse": 22
}

dictItalianOld = {"Genesi": 50,
"Esodo": 40,
"Levitico": 27,
"Numeri": 36,
"Deuteronomio": 34,
"Giosué": 24,
"Giudici": 21,
"Rut": 4,
"1%20Samuele": 31,
"2%20Samuele": 24,
"1%20Re": 22,
"2%20Re": 25,
"1%20Cronaches": 29,
"2%20Cronache": 36,
"Esdra": 10,
"Neemia": 13,
"Ester": 10,
"Giobbe": 42,
"Salmi": 150,
"Proverbi": 31,
"Ecclesiaste": 12,
"Cantico%20dei%20Cantici": 8,
"Isaia": 66,
"Geremia": 52,
"Lamentazioni": 5,
"Ezechiele": 48,
"Daniele": 12,
"Osea": 14,
"Gioele": 3,
"Amos": 9,
"Abdia": 1,
"Giona": 4,
"Michea": 7,
"Nahum": 3,
"Abacuc": 3,
"Sofonia": 3,
"Aggeo": 2,
"Zaccaria": 14,
"Malachia": 4}

dictItalianNew = {"Matteo": 28,
"Marco": 16,
"Luca": 24,
"Giovanni": 21,
"Atti": 28,
"Romani": 16,
"1%20Corinzi": 16,
"2%20Corinzi": 13,
"Galati": 6,
"Efesini": 6,
"Filippesi": 4,
"Colossesi": 4,
"1%20Tessalonicesi": 5,
"2%20Tessalonicesi": 3,
"1%20Timoteo": 6,
"2%20Timoteo": 4,
"Tito": 3,
"Filemone": 1,
"Ebrei": 13,
"Giacomo": 5,
"1%20Pietro": 5,
"2%20Pietro": 3,
"1%20Giovanni": 5,
"2%20Giovanni": 1,
"3%20Giovanni": 1,
"Giuda": 1,
"Apocalisse": 22
}

dictGermanOld = {"1%20Mose": 50,
"2%20Mose": 40,
"3%20Mose": 27,
"4%20Mose": 36,
"5%20Mose": 34,
"Josua": 24,
"Richter": 21,
"Ruth": 4,
"1%20Samuel": 31,
"2%20Samuel": 24,
"1%20Könige": 22,
"2%20Könige": 25,
"1%20Chronik": 29,
"2%20Chronik": 36,
"Esra": 10,
"Nehemia": 13,
"Ester": 10,
"Hiob": 42,
"Psalmen": 150,
"Sprüche": 31,
"Prediger": 12,
"Hohelied": 8,
"Jesaja": 66,
"Jeremia": 52,
"Klagelieder": 5,
"Hesekiel": 48,
"Daniel": 12,
"Hosea": 14,
"Joel": 3,
"Amos": 9,
"Obadja": 1,
"Jona": 4,
"Micha": 7,
"Nahum": 3,
"Habakuk": 3,
"Zephanja": 3,
"Haggai": 2,
"Sacharja": 14,
"Maleachi": 4}



dictGermanNew = {"Matthäus": 28,
"Markus": 16,
"Lukas": 24,
"Johannes": 21,
"Apostelgeschichte": 28,
"Römer": 16,
"1%20Korinther": 16,
"2%20Korinther": 13,
"Galater": 6,
"Epheser": 6,
"Philipper": 4,
"Kolosser": 4,
"1%20Thessalonicher": 5,
"2%20Thessalonicher": 3,
"1%20Timotheus": 6,
"2%20Timotheus": 4,
"Titus": 3,
"Philemon": 1,
"Hebräer": 13,
"Jakobus": 5,
"1%20Petrus": 5,
"2%20Petrus": 3,
"1%20Johannes": 5,
"2%20Johannes": 1,
"3%20Johannes": 1,
"Judas": 1,
"Offenbarung": 22
}


def toDict(estilo : list, capitulo : list, livro : list, versiculos : list, textos : list) -> dict:
    return {"estilo": estilo, "livro": livro,  "capitulo": capitulo, "versiculo": versiculos, "texto": textos}


def crawlSiteEsp(url: str) -> dict:
    versiculos = {}
    response = requests.get(url)
    htmlContent = response.text
    tokenizer  = MosesTokenizer("es")
    verses = trafilatura.extract(htmlContent, include_images=False, include_formatting=False)
    words         = tokenizer.tokenize(verses)
    isFirstCheck  = 1
    listVersicles = [str(i) for i in [int(x) for x in words if x.isnumeric()]]
    verse         = []
    
    for word in words:
        #fazer quebra por numeros
        if word in listVersicles:
            
            if isFirstCheck == 0:
                #caso 2,3... até n-1
                versiculos[listVersicles[0]] = " ".join(verse)
                verse = []
                listVersicles = listVersicles[1:]

            elif isFirstCheck == 1:
                #caso 1
                isFirstCheck = 0
            

        elif (word not in listVersicles) and (isFirstCheck == 0):
            #já encontrou os versiculos está preenchendo o recheio
            verse.append(word)

    #case n
    if len(listVersicles) >= 1:
        versiculos[listVersicles[0]] = " ".join(verse)
        verse = []
        listVersicles = listVersicles[1:]
    
    return versiculos


def crawlSiteFRA(url: str) -> dict:
    versiculos = {}
    response = requests.get(url)
    htmlContent = response.text
    tokenizer  = MosesTokenizer("fr")
    verses = trafilatura.extract(htmlContent, include_images=False, include_formatting=False)
    words         = tokenizer.tokenize(verses)
    isFirstCheck  = 1
    listVersicles = [str(i) for i in [int(x) for x in words if x.isnumeric()]]
    verse         = []
    
    for word in words:
        #fazer quebra por numeros
        if word in listVersicles:
            
            if isFirstCheck == 0:
                #caso 2,3... até n-1
                versiculos[listVersicles[0]] = " ".join(verse)
                verse = []
                listVersicles = listVersicles[1:]

            elif isFirstCheck == 1:
                #caso 1
                isFirstCheck = 0
            

        elif (word not in listVersicles) and (isFirstCheck == 0):
            #já encontrou os versiculos está preenchendo o recheio
            verse.append(word)

    #case n
    if len(listVersicles) >= 1:
        versiculos[listVersicles[0]] = " ".join(verse)
        verse = []
        listVersicles = listVersicles[1:]
    
    return versiculos

def crawlSiteGER(url: str) -> dict:
    versiculos = {}
    response = requests.get(url)
    htmlContent = response.text
    tokenizer  = MosesTokenizer("de")
    verses = trafilatura.extract(htmlContent, include_images=False, include_formatting=False)
    words         = tokenizer.tokenize(verses)
    isFirstCheck  = 1
    listVersicles = [str(i) for i in [int(x) for x in words if x.isnumeric()]]
    verse         = []
    
    for word in words:
        #fazer quebra por numeros
        if word in listVersicles:
            
            if isFirstCheck == 0:
                #caso 2,3... até n-1
                versiculos[listVersicles[0]] = " ".join(verse)
                verse = []
                listVersicles = listVersicles[1:]

            elif isFirstCheck == 1:
                #caso 1
                isFirstCheck = 0
            

        elif (word not in listVersicles) and (isFirstCheck == 0):
            #já encontrou os versiculos está preenchendo o recheio
            verse.append(word)

    #case n
    if len(listVersicles) >= 1:
        versiculos[listVersicles[0]] = " ".join(verse)
        verse = []
        listVersicles = listVersicles[1:]
    
    return versiculos


def crawlSiteITA(url: str) -> dict:
    versiculos = {}
    response = requests.get(url)
    htmlContent = response.text
    tokenizer  = MosesTokenizer("it")
    verses = trafilatura.extract(htmlContent, include_images=False, include_formatting=False)
    words         = tokenizer.tokenize(verses)
    isFirstCheck  = 1
    listVersicles = [str(i) for i in [int(x) for x in words if x.isnumeric()]]
    verse         = []
    
    for word in words:
        #fazer quebra por numeros
        if word in listVersicles:
            
            if isFirstCheck == 0:
                #caso 2,3... até n-1
                versiculos[listVersicles[0]] = " ".join(verse)
                verse = []
                listVersicles = listVersicles[1:]

            elif isFirstCheck == 1:
                #caso 1
                isFirstCheck = 0
            

        elif (word not in listVersicles) and (isFirstCheck == 0):
            #já encontrou os versiculos está preenchendo o recheio
            verse.append(word)

    #case n
    if len(listVersicles) >= 1:
        versiculos[listVersicles[0]] = " ".join(verse)
        verse = []
        listVersicles = listVersicles[1:]
    
    return versiculos


def crawlSiteEng(url: str) -> dict:
    versiculos = {}
    response = requests.get(url)
    htmlContent = response.text
    tokenizer  = MosesTokenizer("en")
    verses = trafilatura.extract(htmlContent, include_images=False, include_formatting=False)
    words         = tokenizer.tokenize(verses)
    isFirstCheck  = 1
    listVersicles = [str(i) for i in [int(x) for x in words if x.isnumeric()]]
    verse         = []
    
    for word in words:
        #fazer quebra por numeros
        if word in listVersicles:
            
            if isFirstCheck == 0:
                #caso 2,3... até n-1
                versiculos[listVersicles[0]] = " ".join(verse)
                verse = []
                listVersicles = listVersicles[1:]

            elif isFirstCheck == 1:
                #caso 1
                isFirstCheck = 0
            

        elif (word not in listVersicles) and (isFirstCheck == 0):
            #já encontrou os versiculos está preenchendo o recheio
            verse.append(word)

    #case n
    if len(listVersicles) >= 1:
        versiculos[listVersicles[0]] = " ".join(verse)
        verse = []
        listVersicles = listVersicles[1:]
    
    return versiculos


def crawlSite(url: str) -> dict:
    versiculos = {}
    response = requests.get(url)
    htmlContent = response.text
    tokenizer  = MosesTokenizer("pt")
    verses = trafilatura.extract(htmlContent, include_images=False, include_formatting=False)
    words         = tokenizer.tokenize(verses)
    isFirstCheck  = 1
    listVersicles = [str(i) for i in [int(x) for x in words if x.isnumeric()]]
    verse         = []
    
    for word in words:
        #fazer quebra por numeros
        if word in listVersicles:
            
            if isFirstCheck == 0:
                #caso 2,3... até n-1
                versiculos[listVersicles[0]] = " ".join(verse)
                verse = []
                listVersicles = listVersicles[1:]

            elif isFirstCheck == 1:
                #caso 1
                isFirstCheck = 0
            

        elif (word not in listVersicles) and (isFirstCheck == 0):
            #já encontrou os versiculos está preenchendo o recheio
            verse.append(word)

    #case n
    if len(listVersicles) >= 1:
        versiculos[listVersicles[0]] = " ".join(verse)
        verse = []
        listVersicles = listVersicles[1:]
    
    return versiculos

def crawlSite_depreciado(url: str, chapter: str):
    versiculos = {}
    response = requests.get(url)
    htmlContent = response.text
    verses = trafilatura.extract(htmlContent, include_images=False, include_formatting=False)
    #print(getAllSentencesBetweenHifen(verses))
    #text = verses.replace("—", "")
    text = verses.split("\n")
    
    

    # pega os principais versículos
     
    check = 0
    # procura por versículos que estejam dentro de versículos
    for s in text:
        str0 = s.split(" ")[0]
        if str0.isnumeric():
            #True    
            #is first time
            if check == 0:
                check = 1
                #tem sub versiculos?
                #faszer quebra por numeros
                
                #contains other versicles at the same string?
                if len(re.findall('[0-9]+', s)) > 1:
                    for subVersicle in getAllSubVersicles(s):
                        subVersicle = tokenize.word_tokenize(subVersicle, language='portuguese')
                        tail = subVersicle[1:]
                        head = subVersicle[0]
                        if head == chapter:
                            versiculos["1"] = " ".join(tail)
                        else:
                            versiculos[head] = " ".join(tail)
                    

            else:
                #is not first time
                #tem sub versiculos?
                #contains other versicles at the same string?
                if len(re.findall('[0-9]+', s)) > 1:
                    for subVersicle in getAllSubVersicles(s):
                        subVersicle = tokenize.word_tokenize(subVersicle, language='portuguese')
                        tail = subVersicle[1:]
                        head = subVersicle[0]
                        versiculos[head] = " ".join(tail)
                else:
                    versiculos[str0] = " ".join(s.split(" ")[1:])
    
    return versiculos

def getAllSubVersicles(text):
    sents = []
    sent = []
    isprimeiro = 0
    wholeString = tokenize.word_tokenize(text, language='portuguese')
    sizeString = len(wholeString)
    for word in range(sizeString):
        
        if wholeString[word].isnumeric() and isprimeiro==0:
            isprimeiro = 1
            sent.append(wholeString[word])
        elif wholeString[word].isnumeric() and isprimeiro==1:
            sents.append(" ".join(sent))
            sent = []
            sent.append(wholeString[word])
        elif word == len(wholeString)-1:
            sents.append(" ".join(sent))
            sent = []
        else:
            sent.append(wholeString[word])
    return sents





def getAllSentencesBetweenHifen(texts: str):
   
    
   for sent in tokenize.sent_tokenize(texts, language='portuguese'):
        str0 = sent.split(" ")[0]
        if str0.isnumeric():
            print("é numérico:  ", sent)
        else: 
            print("não é numérico:  ", sent)
        input()
   return "matches"

def processContent(content: list):
    padrao = r"\d+(\D+)"
    matchesVersiculos = re.findall(padrao, content)
    versos = matchesVersiculos[2:-1]
    print(len(versos))
    #secoes = re.findall('\d+', " ".join(content))[2:-1]
    return versos
