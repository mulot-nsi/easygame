import easygame
import pygame
import math

#
# Documentation PyGame : https://readthedocs.org/projects/pygame/downloads/pdf/latest/
#


# Constantes
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
BLANC = (255, 255, 255)

# Initialisation du jeu
jeu = easygame.Jeu(640, 480, "Test")  # Taille et titre de la fenêtre
jeu.initialiser_police(20)  # Initialisation de la taille du texte à 20 pixels
jeu.charger_image("balle", "balle.png")  # Chargement de l'image de la balle
jeu.charger_image("mario", "mario.png")  # Chargement de l'image de Mario
jeu.horloge(500)  # Vitesse du jeu (lent si petit, rapide si grand)

# Initialisation des variables du jeu
jeu.variables.affecter("texte", "Projet NSI")
jeu.variables.affecter("balle_delta", 0)
jeu.variables.affecter("balle_y", 200)
jeu.variables.affecter("couleur_fond", BLANC)
jeu.variables.affecter("mario_x", 0)
jeu.variables.affecter("mario_y", 0)
jeu.variables.affecter("mario_pixel_x", 0)
jeu.variables.affecter("mario_pixel_y", 0)


#
# Fonction de calcul du jeu appelée à chaque tour de boucle (facultative, on pourrait tout faire dans dessin)
#
def boucle():
    # Exemple d'animation
    balle_delta = jeu.variables.valeur("balle_delta")
    balle_delta = (balle_delta + 0.01) % 360
    jeu.variables.affecter("balle_delta", balle_delta)
    jeu.variables.affecter("balle_y", 200 + (50 * math.sin(balle_delta)))

    # Calcul de la position de Mario de l'unité vers les pixels.
    jeu.variables.affecter("mario_pixel_x", 200 + 50 * jeu.variables.valeur("mario_x"))
    jeu.variables.affecter("mario_pixel_y", 200 + 50 * jeu.variables.valeur("mario_y"))


#
# Fonction de dessin du jeu, appelée à chaque tour de boucle
#
def dessin(ecran):
    # Change la couleur du fond
    ecran.fond(jeu.variables.valeur("couleur_fond"))

    # Dessine des lignes de plus en plus épaisses
    for i in range(10):
        ecran.ligne(10 + (20 * i), 10, 50 + (20 * i), 50, NOIR, i)

    # Dessine des cercles de plus en plus gros (et variation de la bordure, c'est le dernier paramètre)
    for i in range(10):
        ecran.cercle(20 + (50 * i), 70, 10 + i, NOIR, i)

    # Dessine des rectangles de plus en plus gros (et variation de la bordure, c'est le dernier paramètre)
    for i in range(10):
        ecran.rectangle(20 + (50 * i), 100, 30, 30, BLEU, i)

    # Ecriture d'un texte
    ecran.texte(300, 20, jeu.variables.valeur("texte"))

    # Dessin de la balle
    ecran.image("balle", 200, jeu.variables.valeur("balle_y"))

    # Dessin de la mario
    ecran.image("mario", jeu.variables.valeur("mario_pixel_x"), jeu.variables.valeur("mario_pixel_y"))


#
# Gestion des événements du clavier
# Le paramètre evenement est de type pygame.event
# Pour en savoir plus : https://www.pygame.org/docs/ref/event.html
#
def detection_clavier(jeu, evenement):
    if evenement.type == pygame.KEYDOWN:
        if evenement.key == pygame.K_LEFT:
            jeu.variables.decrementer("mario_x", 1)
        elif evenement.key == pygame.K_RIGHT:
            jeu.variables.incrementer("mario_x", 1)
        elif evenement.key == pygame.K_UP:
            jeu.variables.decrementer("mario_y", 1)
        elif evenement.key == pygame.K_DOWN:
            jeu.variables.incrementer("mario_y", 1)
        elif evenement.key == pygame.K_SPACE:
            jeu.variables.affecter("texte", input("Texte à afficher : "))


#
# Gestion des événements de la souris
# Le paramètre evenement est de type pygame.event
# Pour en savoir plus : https://www.pygame.org/docs/ref/event.html
#
def detection_souris(jeu, evenement):
    # Détection du clic.
    if evenement.type == pygame.MOUSEBUTTONDOWN:
        jeu.variables.affecter("couleur_fond", ROUGE)
    elif evenement.type == pygame.MOUSEBUTTONUP:
        jeu.variables.affecter("couleur_fond", BLANC)

    # position de la souris
    if evenement.type == pygame.MOUSEBUTTONDOWN or evenement.type == pygame.MOUSEBUTTONUP:
        position = evenement.pos
        print("Souris - X=", position[0], " Y=", position[1])


jeu.fonction_boucle(boucle)
jeu.fonction_dessin(dessin)
jeu.fonction_evenement_clavier(detection_clavier)
jeu.fonction_evenement_souris(detection_souris)
jeu.lancer()
