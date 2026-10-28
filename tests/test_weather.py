
"""Tests for the weather module."""

import pytest

from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)


def test_parse_time_regular_time():
    # Normalfälle
    assert parse_time("14:21") == 861
    assert parse_time("22:08") == 1328
    assert parse_time("9:05") == 545
    assert parse_time("09:5") == 545
    assert parse_time("9:5") == 545

    # Grenzfälle
    assert parse_time("00:00") == 0
    assert parse_time("23:59") == 1439

    # Fehlerfälle
    with pytest.raises(ValueError):
        parse_time("24:00")

    with pytest.raises(ValueError):
        parse_time("12:60")

    with pytest.raises(ValueError):
        parse_time("ab:cd")

    with pytest.raises(ValueError):
        parse_time("12-30")


def test_parse_measurement_regular_line():
    # Normalfälle
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)
    assert parse_measurement(" Köln ; 14:21 ; 21.7 ") == ("Köln", 861, 21.7)

    # Grenzfälle
    assert parse_measurement("Bonn;10:00;-5.5") == ("Bonn", 600, -5.5)

    # Fehlerfälle
    with pytest.raises(ValueError):
        parse_measurement("Köln;12:00")

    with pytest.raises(ValueError):
        parse_measurement("Köln,12:00,20")

    with pytest.raises(ValueError):
        parse_measurement("Köln;25:00;20")

    with pytest.raises(ValueError):
        parse_measurement("Köln;12:00;20;30")


def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    # Normalfälle
    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]

    # Negative Temperaturen
    negative = [
        ("Köln", 600, -10.0),
        ("Bonn", 700, -5.0),
        ("Essen", 800, 10.0),
    ]
    assert filter_by_temperature(negative, -10, 0) == [
        ("Köln", 600, -10.0),
        ("Bonn", 700, -5.0),
    ]

    # Doppelte Messungen
    duplicates = [
        ("Köln", 600, 20.0),
        ("Köln", 600, 20.0),
        ("Bonn", 700, 30.0),
    ]
    assert filter_by_temperature(duplicates, 15, 25) == [
        ("Köln", 600, 20.0),
        ("Köln", 600, 20.0),
    ]

    # Reihenfolge beibehalten
    assert filter_by_temperature(measurements, 0, 30) == measurements

    # Grenzfälle: gleiche Temperaturen
    same = [
        ("Köln", 600, 15.0),
        ("Bonn", 700, 15.0),
    ]
    assert filter_by_temperature(same, 15, 15) == same

    # Temperatur liegt genau auf der Grenze
    assert filter_by_temperature(measurements, 10, 25) == measurements

    # Leere Liste
    assert filter_by_temperature([], 10, 20) == []

    # Keine Temperatur im Bereich
    assert filter_by_temperature(measurements, 30, 40) == []

    # Fehlerfälle
    with pytest.raises(ValueError):
        filter_by_temperature(measurements, 30, 10)

    with pytest.raises(ValueError):
        filter_by_temperature(measurements, -5, -20)


def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    # Normalfall
    assert average_temperature(measurements, "Köln") == 15.0

    # Unterschiedliche Namen und mehrere Städte
    cities = [
        ("Köln", 600, 10.0),
        ("Bonn", 700, 30.0),
        ("köln", 800, 40.0),
        ("Köln", 900, 20.0),
    ]
    assert average_temperature(cities, "Köln") == 15.0
    assert average_temperature(cities, "Bonn") == 30.0
    assert average_temperature(cities, "köln") == 40.0

    # Grenzfall: eine Messung pro Stadt
    one = [
        ("Köln", 600, 18.0),
        ("Bonn", 700, 25.0),
    ]
    assert average_temperature(one, "Köln") == 18.0

    # Negative Temperaturen
    negative = [
        ("Köln", 600, -10.0),
        ("Köln", 700, -20.0),
    ]
    assert average_temperature(negative, "Köln") == -15.0

    # Leerzeichen bei Städten
    spaces = [
        parse_measurement(" Köln ;10:00;10"),
        parse_measurement("Köln;12:00;20"),
    ]
    assert average_temperature(spaces, "Köln") == 15.0

    # Fehlerfälle: Parameter fehlt
    with pytest.raises(TypeError):
        average_temperature(measurements)

    # Stadt existiert nicht
    with pytest.raises(ValueError):
        average_temperature(measurements, "Berlin")


def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    # Normalfall
    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)

    # Grenzfall: negative Temperaturen
    negative = [
        ("Köln", 600, -10.0),
        ("Bonn", 700, -5.0),
        ("Essen", 800, -20.0),
    ]
    assert hottest_measurement(negative) == ("Bonn", 700, -5.0)

    # Nur eine Stadt
    one_city = [
        ("Köln", 600, 10.0),
        ("Köln", 700, 25.0),
    ]
    assert hottest_measurement(one_city) == ("Köln", 700, 25.0)

    # Lange Kommazahlen
    decimals = [
        ("Köln", 600, 20.1234567),
        ("Bonn", 700, 20.1234568),
    ]
    assert hottest_measurement(decimals) == ("Bonn", 700, 20.1234568)

    # Gleiche Temperatur, unterschiedliche Uhrzeit
    same_temp = [
        ("Köln", 800, 25.0),
        ("Bonn", 600, 25.0),
    ]
    assert hottest_measurement(same_temp) == ("Bonn", 600, 25.0)

    # Gleiche Temperatur und gleiche Uhrzeit
    same_time = [
        ("Köln", 600, 25.0),
        ("Bonn", 600, 25.0),
    ]
    assert hottest_measurement(same_time) == ("Köln", 600, 25.0)

    # Fehlerfälle: Parameter fehlt
    with pytest.raises(TypeError):
        hottest_measurement()

    # Leere Liste
    with pytest.raises(ValueError):
        hottest_measurement([])
