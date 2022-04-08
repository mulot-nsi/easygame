import pygame

#
# Documentation : https://readthedocs.org/projects/pygame/downloads/pdf/latest/
#

EVENEMENTS_CLAVIER = [pygame.KEYDOWN, pygame.KEYUP]
EVENEMENTS_SOURIS = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]


#
# Classe de gestion des variables du jeu
# Les variables sont stockées dans un dictionnaire
#
class Variables:
    _variables = {}

    def affecter(self, nom, valeur):
        self._variables[nom] = valeur

    def valeur(self, nom):
        return self._variables[nom]

    def incrementer(self, nom, valeur):
        self._variables[nom] = self._variables[nom] + valeur

    def decrementer(self, nom, valeur):
        self._variables[nom] = self._variables[nom] - valeur


#
# Classe de gestion du jeu :
# Boucle principale, fonctions de calcul et de dessin, événements

class Jeu:
    variables = Variables()

    def __init__(self, largeur=640, hauteur=480, titre="Pygame"):
        self.largeur = largeur
        self.hauteur = hauteur

        pygame.init()
        pygame.display.set_caption(titre)

        self._ecran = Ecran(self, pygame.display.set_mode((largeur, hauteur)))
        self._fonction_boucle = None
        self._fonction_dessin = None
        self._fonction_evenement_clavier = None
        self._fonction_evenement_souris = None
        self._images = {}
        self._horloge = None
        self._police = None

    def initialiser_police(self, taille):
        self._police = pygame.font.SysFont(None, taille)

    def fonction_boucle(self, fonction):
        self._fonction_boucle = fonction

    def fonction_dessin(self, fonction):
        self._fonction_dessin = fonction

    def fonction_evenement_clavier(self, fonction):
        self._fonction_evenement_clavier = fonction

    def fonction_evenement_souris(self, fonction):
        self._fonction_evenement_souris = fonction

    def charger_image(self, reference, fichier):
        image = pygame.image.load(fichier)
        image.convert()
        self._images[reference] = image

    def horloge(self, tic):
        self._horloge = tic

    def lancer(self):
        """
        Exécute la boucle principale.
        """
        actif = True
        horloge = pygame.time.Clock()

        while actif:
            if self._fonction_boucle:
                self._fonction_boucle()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    actif = False

                elif event.type in EVENEMENTS_CLAVIER and self._fonction_evenement_clavier:
                    self._fonction_evenement_clavier(self, event)

                elif event.type in EVENEMENTS_SOURIS and self._fonction_evenement_souris:
                    self._fonction_evenement_souris(self, event)

            if self._fonction_dessin:
                self._fonction_dessin(self._ecran)

            pygame.display.flip()

            if self._horloge:
                horloge.tick(self._horloge)

        pygame.quit()


#
# Classe de gestion les tracés à l'écran.
# Une instance est fournie à la fonction de dessin.
#
class Ecran:
    def __init__(self, jeu, ecran):
        self._jeu = jeu
        self._ecran = ecran

    def fond(self, couleur):
        self._ecran.fill(couleur)

    def ligne(self, x_a, y_a, x_b, y_b, couleur=(0, 0, 0), epaisseur=1):
        pygame.draw.line(self._ecran, couleur, (x_a, y_a), (x_b, y_b), epaisseur)

    def rectangle(self, x, y, largeur, hauteur, couleur=(0, 0, 0), epaisseur=0):
        pygame.draw.rect(self._ecran, couleur, pygame.Rect((x, y), (largeur, hauteur)), epaisseur)

    def cercle(self, x, y, rayon, couleur=(0, 0, 0), epaisseur=0):
        pygame.draw.circle(self._ecran, couleur, (x, y), rayon, epaisseur)

    def image(self, reference, x, y):
        image = self._jeu._images[reference]
        rectangle = image.get_rect()
        rectangle.topleft = (x, y)
        self._ecran.blit(image, rectangle)

    def texte(self, x, y, message, couleur=(0, 0, 0)):
        if not self._jeu._police:
            return None

        image = self._jeu._police.render(message, True, couleur)
        self._ecran.blit(image, (x, y))
