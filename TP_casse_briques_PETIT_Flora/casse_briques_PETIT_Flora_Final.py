import random #Pour les tirages aleatoires
import sys #Pour quitter proprement
import pygame #Le module Pygame
import pygame.freetype #Pour afficher du texte
import math

# Initialisation de Pygame
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

# Chargement des sons
collision_sound = pygame.mixer.Sound("collision.wav")

# Initialisation de Pygame FreeType pour le texte
pygame.freetype.init()
myfont = pygame.freetype.SysFont(None, 20) #Texte de taille 20

# Taille de la fenetre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping")

# Pour limiter le nombre d'image par seconde
clock = pygame.time.Clock()
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE1 = (255, 100, 100)
ROUGE2 = (255, 150, 150)
ROUGE3 = (255, 200, 200)
VERT = (122, 255, 147)
BLEU = (18, 43, 140)
RAYON_BALLE = 10
XMIN_INFO, YMIN_INFO = 0, 0
XMAX_INFO, YMAX_INFO = width, 100
XMIN, YMIN = 0, YMAX_INFO
XMAX, YMAX = width, height


class Balle:
    """Classe représentant la balle du jeu."""

    def vitesse_par_angle(self, angle):
        """
        Calculer la vitesse en fonction de l'angle.

        Args:
            angle (float): L'angle de déplacement de la balle en degrés.
        """
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))


    def __init__(self):
        """Initialiser la balle."""
        self.x, self.y = (400, 400)
        self.vitesse = 8 # vitesse initiale
        self.vitesse_par_angle(60) # vecteur vitesse
        self.sur_raquette = True


    def afficher(self):
        """Afficher la balle."""
        pygame.draw.circle(screen, BLANC, (int(self.x), int(self.y)), RAYON_BALLE)


    def rebond_raquette(self, raquette):
        """
        Gérer le rebond de la balle sur la raquette.

        Args:
            raquette (Raquette): L'objet Raquette avec lequel la balle peut entrer en collision.
        """
        diff = raquette.x - self.x
        longueur_totale = raquette.longueur / 2 + RAYON_BALLE
        angle = 90 + 80 * diff / longueur_totale
        self.vitesse_par_angle(angle)


    def deplacer(self, raquette):
        """
        Déplacer la balle en fonction de sa vitesse et détecter les collisions.

        Args:
            raquette (Raquette): L'objet Raquette avec lequel la balle peut entrer en collision.
        """
        if self.sur_raquette:
            self.y = raquette.y - 2 * RAYON_BALLE
            self.x = raquette.x
        else:
            self.x += self.vx
            self.y += self.vy
        if raquette.collision_balle(self) and self.vy > 0:
            self.rebond_raquette(raquette)
        if self.x + RAYON_BALLE > XMAX or self.x - RAYON_BALLE < XMIN:
            self.vx = -self.vx
            pygame.mixer.Sound.play(collision_sound)
        if self.y + RAYON_BALLE > YMAX:
            self.vie_perdue()
        if self.y - RAYON_BALLE < YMIN:
            self.vy = -self.vy
            pygame.mixer.Sound.play(collision_sound)


    def vie_perdue(self):
        """Gérer la perte de vie lorsque la balle touche le bas de l'écran."""
        jeu.perdre_vie()
        self.sur_raquette = True


class Jeu:
    """Classe représentant le jeu."""

    def __init__(self):
        """Initialiser le jeu."""
        self.vies = 2  # Nombre initial de vies
        self.score_value = 0
        self.level = 1
        self.reset_game(False)


    def niveau(self,nb):
        """
        Créer les différents niveaux du jeu.

        Args:
            nb (int): Le numéro du niveau à créer.
        """
        if nb == 1:
            # Niveau avec un block de briques de 6 par 3
            for x in range(235, 565, 55):
                for y in range(200, 280, 35):
                    self.briques.append(Brique(x, y, 1))
        elif nb == 2:
            # Niveau avec un block de briques de 14 par 3
            for x in range(45, width, 55):
                for y in range(200, 300, 35):
                    self.briques.append(Brique(x, y, 1))
        elif nb == 3:
            # Niveau avec un block de briques de 14 par 4 en damier
            for x in range(45, width, 55):
                for y in range(200, 320, 35):
                    if (x - 45) // 55 % 2 == (y - 200) // 35 % 2:
                        self.briques.append(Brique(x, y, 1))
                    else:
                        self.briques.append(Brique(x, y, 2))
        elif nb == 4:
            # Niveau avec un block de briques de 14 par 4 ou lignes de briques alternant entre 2 types
            for x in range(45, width, 55):
                for y in range(200, 320, 35):
                    if y == 200 or y == 270:
                        self.briques.append(Brique(x, y, 2))
                    else:
                        self.briques.append(Brique(x, y, 1))
        elif nb == 5:
            # Niveau avec un block de briques de 14 par 6 avec 4 types répétées verticalement
            for x in range(45, width, 55):
                for y in range(200, 380, 35):
                    type_brique = ((x - 45) // 55) % 4 + 1
                    self.briques.append(Brique(x, y, type_brique))
        elif nb == 6:
            # Niveau avec un block de briques de 14 par 6 avec 4 types répétées en diagonal
            for x in range(45, width, 55):
                for y in range(200, 380, 35):
                    type_brique = ((x - 45) // 55 + (y - 200) // 35) % 4 + 1
                    self.briques.append(Brique(x, y, type_brique))
        elif nb == 7:
            # Niveau avec un block de briques de 14 par 6 avec 4 types répétées en tartan
            for x in range(45, width, 55):
                for y in range(200, 380, 35):
                    if (x - 45) // 55 % 2 == 0:
                        if y == 200 or y == 380:
                            self.briques.append(Brique(x, y, 4))
                        else:
                            if (y - 200) // 35 % 2 == 0:
                                self.briques.append(Brique(x, y, 4))
                            else:
                                self.briques.append(Brique(x, y, 3))
                    else:
                        if (y - 200) // 35 % 2 == 0:
                            self.briques.append(Brique(x, y, 3))
                        else:
                            if (y - 200) // 35 % 2 == 0:
                                self.briques.append(Brique(x, y, 2))
                            else:
                                self.briques.append(Brique(x, y, 1))


    def reset_game(self, reset_score):
        """
        Réinitialiser le jeu.

        Args:
            reset_score (bool): Indique si le score doit être réinitialisé.
        """
        self.balle = Balle()
        self.raquette = Raquette()
        if reset_score:  # Réinitialiser le score seulement si reset_score est True
            self.score_value = 0
            self.vies = 2
        self.vies += 1
        self.briques = []
        self.niveau(self.level)


    def rejouer(self, victoire):
        """
        Gérer l'écran de fin de partie et la possibilité de rejouer.

        Args:
            victoire (bool): Indique si le joueur a gagné la partie.
        """
        question_text, question_rect = myfont.render("Voulez-vous rejouer ?", NOIR)
        question_rect.center = (width // 2, height // 2)
        screen.blit(question_text, question_rect)

        # Création des boutons "Oui" et "Non"
        button_yes_text, button_yes_rect = myfont.render("Oui", NOIR)
        button_no_text, button_no_rect = myfont.render("Non", NOIR)
        button_yes_rect.center = (width // 2 - 50, height // 2 + 50)
        button_no_rect.center = (width // 2 + 50, height // 2 + 50)

        # Affichage des boutons
        screen.blit(button_yes_text, button_yes_rect)
        screen.blit(button_no_text, button_no_rect)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if button_yes_rect.collidepoint(x, y):# Si le bouton "Oui" est cliqué
                        if victoire:
                            self.reset_game(False)  # Réinitialiser le jeu en gardant le score
                        else:
                            self.reset_game(True)  # Réinitialiser le jeu en remettant le score a 0
                        return
                    elif button_no_rect.collidepoint(x, y):  # Si le bouton "Non" est cliqué
                        pygame.quit()  # Quitter le jeu
                        sys.exit()


    def gagner(self):
        """Gérer la victoire du joueur."""
        if all(brique.en_vie() == False for brique in self.briques):
            text, rect = myfont.render("You won !", NOIR)
            rect.center = (width // 2, height // 2 - 50)
            screen.blit(text, rect)
            pygame.display.flip()
            if self.level < 7:
                self.level += 1
                self.score_value += 1000
            else:
                self.level = 1
            self.rejouer(True)


    def perdre_vie(self):
        """Gérer la perte de vie du joueur."""
        self.vies -= 1
        if self.vies <= 0:
            text, rect = myfont.render("Game Over", NOIR)
            rect.center = (width // 2, height // 2 - 50)
            screen.blit(text, rect)
            pygame.display.flip()
            self.level = 1
            self.rejouer(False)


    def gestion_evenements(self):
        """Gérer les événements pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # Pour quitter
            elif event.type == pygame.MOUSEBUTTONDOWN: # On vient de cliquer
                if event.button == 1: # Boutton gauche
                    if self.balle.sur_raquette:
                        self.balle.sur_raquette = False
                        self.balle.vitesse_par_angle(60)


    def mise_a_jour(self):
        """Mettre à jour l'état du jeu."""
        x, y = pygame.mouse.get_pos()
        self.balle.deplacer(self.raquette)
        for brique in self.briques:
            if brique.en_vie():
                if brique.collision_balle(self.balle):
                    self.score_value += 10  # Augmenter le score lorsque la balle touche une brique
                    pygame.mixer.Sound.play(collision_sound)
                    break  # Sortir de la boucle dès qu'une brique est touchée
        self.raquette.deplacer(x)


    def afficher_score(self):
        """Afficher le score du joueur."""
        text, rect = myfont.render(f"Score: {self.score_value}", BLANC)
        rect.topleft = (20, 40)
        screen.blit(text, rect)


    def afficher_vie(self):
        """Afficher le nombre de vies restantes du joueur."""
        text, rect = myfont.render(f"Vie: {self.vies}", BLANC)
        rect.topleft = (270, 40)
        screen.blit(text, rect)


    def afficher_niveau(self):
        """Afficher le niveau actuel du jeu."""
        text, rect = myfont.render(f"Niveau: {self.level}", BLANC)
        rect.topleft = (520, 40)
        screen.blit(text, rect)


    def affichage(self):
        """Afficher les éléments du jeu."""
        screen.fill(BLEU)
        pygame.draw.rect(screen, VERT, (XMIN_INFO, YMIN_INFO, XMAX_INFO, YMAX_INFO))  # Bandeau noir pour les informations
        self.balle.afficher()
        self.raquette.afficher()
        for brique in self.briques:
            if brique.en_vie():
                brique.afficher()
        self.afficher_score()
        self.afficher_vie()
        self.afficher_niveau()


class Raquette:
    """Classe représentant la raquette du joueur."""

    def __init__(self):
        """Initialiser la raquette."""
        self.x = (XMIN + XMAX) / 2
        self.y = YMAX - RAYON_BALLE
        self.longueur = 10 * RAYON_BALLE


    def afficher(self):
        """Afficher la raquette."""
        pygame.draw.rect(screen, BLANC, (int(self.x-self.longueur/2), int(self.y-RAYON_BALLE),
        self.longueur, 2*RAYON_BALLE), 0)


    def deplacer(self, x):
        """
        Déplacer la raquette horizontalement en fonction de la position de la souris.

        Args:
            x (int): La position x de la souris.
        """
        if x - self.longueur / 2 < XMIN:
            self.x = XMIN + self.longueur / 2
        elif x + self.longueur / 2 > XMAX:
            self.x = XMAX - self.longueur / 2
        else:
            self.x = x


    def collision_balle(self, balle):
        """
        Vérifier si la balle entre en collision avec la raquette.

        Args:
            balle (Balle): L'objet Balle à vérifier.

        Returns:
            bool: True si la collision est détectée, False sinon.
        """
        vertical = abs(self.y - balle.y) < 2 * RAYON_BALLE
        horizontal = abs(self.x - balle.x) < self.longueur / 2 + RAYON_BALLE
        return vertical and horizontal


class Brique:
    """Classe représentant une brique dans le jeu."""

    def __init__(self, x, y, v):
        """
        Initialiser une brique.

        Args:
            x (int): La position x de la brique.
            y (int): La position y de la brique.
            v (int): La valeur de vie de la brique.
        """
        self.x = x
        self.y = y
        self.vie = v
        self.longueur = 5 * RAYON_BALLE
        self.largeur = 3 * RAYON_BALLE


    def couleur_brique(self):
        """
        Déterminer la couleur de la brique en fonction de sa valeur de vie.

        Returns:
            tuple: Un tuple représentant la couleur au format RGB.
        """
        if self.vie == 1:
            return BLANC
        elif self.vie == 2:
            return ROUGE3
        elif self.vie == 3:
            return ROUGE2
        elif self.vie == 4:
            return ROUGE1


    def en_vie(self):
        """
        Vérifier si la brique est toujours en vie.

        Returns:
            bool: True si la brique est en vie, False sinon.
        """
        return self.vie > 0


    def afficher(self):
        """Afficher la brique."""
        pygame.draw.rect(screen, self.couleur_brique(), (int(self.x-self.longueur/2),
        int(self.y-self.largeur/2),
        self.longueur, self.largeur), 0)


    def collision_balle(self, balle):
        """
        Vérifier si la balle entre en collision avec la brique.

        Args:
            balle (Balle): L'objet Balle à vérifier.

        Returns:
            bool: True si la collision est détectée, False sinon.
        """
        # On suppose que largeur<longueur
        marge = self.largeur/2 + RAYON_BALLE
        dy = balle.y - self.y
        touche = False
        if balle.x >= self.x: # On regarde a droite
            dx = balle.x - (self.x + self.longueur/2 - self.largeur/2)
            if abs(dy) <= marge and dx <= marge: # On touche
                touche = True
                if dx <= abs(dy):
                    balle.vy = -balle.vy
                else: # A droite
                    balle.vx = -balle.vx
        else: # On regarde a gauche
            dx = balle.x - (self.x - self.longueur/2 + self.largeur/2)
            if abs(dy) <= marge and -dx <= marge: # On touche
                touche = True
                if -dx <= abs(dy):
                    balle.vy = -balle.vy
                else: # A gauche
                    balle.vx = -balle.vx
        if touche:
            self.vie -= 1
            return touche


jeu = Jeu()
while True:
    jeu.gestion_evenements()
    jeu.mise_a_jour()
    jeu.affichage()
    jeu.gagner()
    pygame.display.flip() # Envoie de l'image à la carte graphique
    clock.tick(60) # On attend pour ne pas depasser 60 images/seconde
