import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
largeur_fenetre = 600
hauteur_fenetre = 400
taille_case = 20
record_fichier = "highscore.txt"

# Couleurs
couleur_fond = (0, 0, 0)
couleur_serpent = (0, 255, 0)
couleur_pomme = (255, 0, 0)
couleur_texte = (255, 255, 255)

# Direction initiale du serpent
direction = ""

# Fonction principale du jeu
def jeu():
    global direction
    pygame.display.set_caption("Jeu du Serpent")
    
    # Initialisation de la fenêtre
    fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
    horloge = pygame.time.Clock()
    
    while True:
        record = lire_highscore()
        jouer_partie(fenetre, horloge, record)

def jouer_partie(fenetre, horloge, record):
    global direction
    # Position initiale du serpent
    serpent = [{"x": largeur_fenetre // 2, "y": hauteur_fenetre // 2}]
    
    # Position initiale de la pomme
    pomme = {"x": random.randrange(0, largeur_fenetre, taille_case),
             "y": random.randrange(0, hauteur_fenetre, taille_case)}
    
    # Score
    score = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "BAS":
                    direction = "HAUT"
                elif event.key == pygame.K_DOWN and direction != "HAUT":
                    direction = "BAS"
                elif event.key == pygame.K_LEFT and direction != "DROITE":
                    direction = "GAUCHE"
                elif event.key == pygame.K_RIGHT and direction != "GAUCHE":
                    direction = "DROITE"
        
        # Déplacement du serpent
        for i in range(len(serpent) - 1, 0, -1):
            serpent[i]["x"] = serpent[i - 1]["x"]
            serpent[i]["y"] = serpent[i - 1]["y"]

        if direction == "HAUT":
            serpent[0]["y"] -= taille_case
        elif direction == "BAS":
            serpent[0]["y"] += taille_case
        elif direction == "GAUCHE":
            serpent[0]["x"] -= taille_case
        elif direction == "DROITE":
            serpent[0]["x"] += taille_case

        # Assurer que le serpent traverse les bords de l'écran
        serpent[0]["x"] = serpent[0]["x"] % largeur_fenetre
        serpent[0]["y"] = serpent[0]["y"] % hauteur_fenetre
        
        # Vérifier si la tête du serpent touche son propre corps
        for partie in serpent[1:]:
            if serpent[0]["x"] == partie["x"] and serpent[0]["y"] == partie["y"]:
                record = mettre_a_jour_highscore(score, record)
                afficher_texte(fenetre, "Game Over", couleur_texte, (largeur_fenetre // 2, hauteur_fenetre // 2))
                afficher_texte(fenetre, f"Rejouer(O/N)-Record:{record}", couleur_texte, (largeur_fenetre // 2, hauteur_fenetre // 2 + 50))
                afficher_score(fenetre, score, couleur_texte, (largeur_fenetre - 50, 20))
                afficher_record(fenetre, record, couleur_texte, (50, 20))
                attente_rejouer(fenetre, horloge)
                return
        
        # Vérifier si le serpent a mangé la pomme
        if serpent[0]["x"] == pomme["x"] and serpent[0]["y"] == pomme["y"]:
            score += 1
            pomme = {"x": random.randrange(0, largeur_fenetre, taille_case),
                     "y": random.randrange(0, hauteur_fenetre, taille_case)}
            
            # Ajouter une nouvelle partie au serpent
            nouvelle_partie = {"x": serpent[-1]["x"], "y": serpent[-1]["y"]}
            serpent.append(nouvelle_partie)
        
        # Affichage du fond
        fenetre.fill(couleur_fond)
        
        # Affichage du serpent
        for partie in serpent:
            pygame.draw.circle(fenetre, couleur_serpent, (partie["x"] + taille_case // 2, partie["y"] + taille_case // 2), taille_case // 2)
        
        # Affichage de la pomme
        pygame.draw.circle(fenetre, couleur_pomme, (pomme["x"] + taille_case // 2, pomme["y"] + taille_case // 2), taille_case // 2)
        
        # Affichage du score
        afficher_score(fenetre, score, couleur_texte, (largeur_fenetre - 50, 20))
        
        # Affichage du record maximal
        afficher_record(fenetre, record, couleur_texte, (50, 20))
        
        # Mise à jour de l'affichage
        pygame.display.flip()
        
        # Contrôle de la vitesse du jeu
        horloge.tick(8)  # Vous pouvez ajuster la vitesse en changeant ce nombre

def afficher_texte(fenetre, texte, couleur, position):
    font = pygame.font.Font(None, 74)
    texte_surface = font.render(texte, True, couleur)
    rect = texte_surface.get_rect(center=position)
    fenetre.blit(texte_surface, rect)

def afficher_score(fenetre, score, couleur, position):
    font = pygame.font.Font(None, 36)
    texte_surface = font.render(f"Score: {score}", True, couleur)
    rect = texte_surface.get_rect(midright=position)
    fenetre.blit(texte_surface, rect)

def afficher_record(fenetre, record, couleur, position):
    font = pygame.font.Font(None, 24)
    texte_surface = font.render(f"Record : {record}", True, couleur)
    rect = texte_surface.get_rect(topleft=position)
    fenetre.blit(texte_surface, rect)

def lire_highscore():
    try:
        with open(record_fichier, "r") as fichier:
            return int(fichier.read())
    except FileNotFoundError:
        return 0

def mettre_a_jour_highscore(nouveau_score, record_actuel):
    if nouveau_score > record_actuel:
        with open(record_fichier, "w") as fichier:
            fichier.write(str(nouveau_score))
        return nouveau_score
    else:
        return record_actuel

def attente_rejouer(fenetre, horloge):
    attente = True
    while attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    attente = False
                    jouer_partie(fenetre, horloge, lire_highscore())
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

        horloge.tick(5)
        pygame.display.flip()

# Lancer le jeu
if __name__ == "__main__":
    jeu()
