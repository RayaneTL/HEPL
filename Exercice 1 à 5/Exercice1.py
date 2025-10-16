from machine import Pin
import time

# Configuration des broches
led = Pin(15, Pin.OUT)       # Broche où la LED est connectée (ex : GP15)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)  # Broche du bouton (ex : GP14)

# Variables
press_count = 0
last_state = 0
delay = 1.0  # Délai initial pour 0,5 Hz (1 seconde entre ON/OFF)

# Fonction principale
while True:
    current_state = button.value()
    
    # Détection d’un appui (front montant)
    if current_state == 1 and last_state == 0:
        press_count += 1
        print("Bouton pressé :", press_count)
        time.sleep(0.3)  # Anti-rebond
        
        # Réinitialiser le compteur après 3 appuis
        if press_count > 3:
            press_count = 1

    last_state = current_state

    # Gestion des modes de clignotement selon le nombre d'appuis
    if press_count == 1:
        led.toggle()
        time.sleep(1.0)  # 0,5 Hz
    elif press_count == 2:
        led.toggle()
        time.sleep(0.3)  # clignotement plus rapide
    elif press_count == 3:
        led.value(0)  # LED éteinte
        time.sleep(0.1)
