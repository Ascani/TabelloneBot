#TabelloneBot

Tabellone elettronico per biliardino

![Tabellone elettronico](tabellone.jpg)

##Sorgenti tabellone

* [tabellone.py](tabellone.py) Sorgente principale del programma che gira all'interno dei tabelloni a led RGB

##Sorgenti biliardino

* [biliardino.py](biliardino.py) Sorgente principale del programma che gira all'interno del biliardino
* [acmepins.py](acmepins.py) Modulo di gestione dei pin di Arietta G25
* [cronometro.py](cronometro.py) Modulo per la misurazione del tempo di gioco trascorso

##Pacchetti da installare 

[Python-Telegram-Bot](https://github.com/python-telegram-bot/python-telegram-bot) per interagire con [Telegram](https://telegram.org/)

	apt-get update
	apt-get install python-pip
	pip install python-telegram-bot

##Connessioni da Arietta verso i sensori

Segnali su connettore flat 8+8 pin

| Pin # | Signal   | Arietta pin # |
|-------|----------|---------------|
| 1     | GND      | J4.9          |
| 2     | LED_BLUE | J4.34         |
| 3     | GND      | J4.9          |
| 4     | GND      | J4.9          |
| 5     | IR_BLUE  | J4.38         |
| 6     | GND      | J4.9          |
| 7     | 3V3      | J4.5          |
| 8     | GND      | J4.9          |
| 9     | LED_RED  | J4.34         |
| 10    | GND      | J4.9          |
| 11    | GND      | J4.9          |
| 12    | IR_RED   | J4.26         |
| 13    | GND      | J4.9          |
| 14    | 3V3      | J4.5          |
| 15    | N.C.     |               |
| 16    | N.C.     |               |


Altri segnali

| Signal     | Arietta pin # |
|------------|---------------|
| Spia verde | J4.26         |
| IR_PULL    | J4.40         |

##Links

* [@TabelloneBot](https://telegram.me/TabelloneBot)
* [Pinout Arietta G25](http://pinout.acmesystems.it)
* [Acme Arietta G25](http://www.acmesystems.it/arietta)
* [Hardware per la realizzazione del tabellone](http://www.acmesystems.it/ledpanel)
* [Datasheet del diodo IR trasmettitore](http://www.mouser.com/ds/2/239/S_110_E5208A-336877.pdf)
* [Datasheet del ricevitore IR](http://www.mouser.com/ds/2/427/tsop321-531469.pdf)

Copyright (C) 2016 - Sergio Tanzilli - tanzilli@acmesystems.it
