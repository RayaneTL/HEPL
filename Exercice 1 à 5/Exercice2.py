from machine import Pin, PWM, ADC
from time import sleep

# --- Configuration des broches ---
buzzer = PWM(Pin(15))      # Buzzer connecté à GP15
pot = ADC(Pin(26))         # Potentiomètre sur GP26 (ADC0)

# Fréquences d'une mélodie simple (Do, Ré, Mi, Fa, Sol, La, Si, Do)
notes = [262, 294, 330, 349, 392, 440, 494, 523]

# --- Boucle principale ---
while True:
    # Lecture du potentiomètre (0 à 65535)
    pot_value = pot.read_u16()
    
    # Conversion du potentiomètre en rapport de volume (0.0 à 1.0)
    volume = pot_value / 65535
    
    for freq in notes:
        # Définir la fréquence du buzzer
        buzzer.freq(freq)
        
        # Ajuster le volume via le rapport cyclique (duty cycle)
        duty = int(volume * 32768)  # max 65535/2 pour éviter saturation
        buzzer.duty_u16(duty)
        
        # Jouer chaque note 0.3 s
        sleep(0.3)
    
    # Arrêter le son entre deux boucles
    buzzer.duty_u16(0)
    sleep(0.2)
