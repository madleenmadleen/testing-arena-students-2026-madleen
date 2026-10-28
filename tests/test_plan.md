def parse_time(time_text)
Normalfall: 14:21 & 22:08, ohne Nullen 9:05 09:5 9:5
Grenzfälle: 00:00 & 23:59
Fehlerfälle: Ungültige Stunde & Minute, Buchstaben, falsches Trennzeichen 

def parse_measurement(line)
Normalfall normale Eingabe, mit Leerzeichen,  
Grenzfälle negative Temperatur
Fehlerfälle zwei Strings, falsches Trennzeichen, falsche Uhrzeit, vier Werte

def filter_by_temperature(measurements, lower, upper)
Normalfall minus Grad, normale Eingabe, doppelte Messungen, Reihenfolge
Grenzfälle gleiche Temperaturen, Temperatur als Grenze, leere Liste übergeben, nichts in der Range  
Fehlerfälle lower größer als upper, minus Grad als größere Zahl, 

def average_temperature(measurements, city)
Normalfall unterschiedliche Namen, mehrere Städte, 
Grenzfälle eine Messung pro Stadt, negativ Temperaturen, Leerzeichen bei Städten 
Fehlerfälle ein Parameter fehlt, Stadt gibts nicht 

def hottest_measurement(measurements)
Normalfall normale Eingabe
Grenzfälle minus Grad, nur eine Stadt, lange Kommazahlen, gleiche Temperatur (& gleiche Uhrzeit)   
Fehlerfälle Parameter fehlt, leere Liste