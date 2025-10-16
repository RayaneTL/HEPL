from machine import Pin, ADC, I2C
import utime
from pico_i2c_lcd import I2cLcd
from dht import DHT11

# -------------------------------
# CONFIGURATION DU MATÉRIEL
# -------------------------------
# Capteur DHT11 (Température/Humidité)
dht_sensor = DHT11(Pin(15))

# Potentiomètre pour la température de consigne
pot = ADC(26)  # Broche ADC0

# LED et Buzzer
led = Pin(14, Pin.OUT)
buzzer = Pin(13, Pin.OUT)

# Écran LCD I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)  # Adresse I2C 0x27 à adapter si besoin

# -------------------------------
# FONCTIONS UTILITAIRES
# -------------------------------
def lire_consigne():
    """Lit la valeur du potentiomètre et la convertit entre 15°C et 35°C"""
    valeur = pot.read_u16()  # 0 à 65535
    temp_consigne = 15 + (valeur / 65535) * (35 - 15)
    return round(temp_consigne, 1)

def alarme():
    """Active le buzzer et fait clignoter rapidement la LED"""
    for i in range(6):
        led.toggle()
        buzzer.value(1)
        utime.sleep(0.1)
        buzzer.value(0)
        utime.sleep(0.1)

def clignotement_led(vitesse):
    """Clignote à la vitesse donnée"""
    led.toggle()
    utime.sleep(vitesse)

# -------------------------------
# BOUCLE PRINCIPALE
# -------------------------------
while True:
    # Lecture du potentiomètre et du capteur DHT11
    consigne = lire_consigne()
    dht_sensor.measure()
    temp = dht_sensor.temperature()

    # Affichage sur l’écran LCD
    lcd.clear()
    lcd.putstr("Set: {:.1f}C".format(consigne))
    lcd.move_to(0, 1)
    lcd.putstr("Ambient: {:.1f}C".format(temp))

    # Contrôle de la température
    if temp > consigne + 3:
        # ALARME
        lcd.clear()
        lcd.putstr("ALARM !!!")
        alarme()
    elif temp > consigne:
        # Clignotement lent (0,5 Hz)
        clignotement_led(1.0)
    else:
        led.value(0)
        buzzer.value(0)

    utime.sleep(0.5)
