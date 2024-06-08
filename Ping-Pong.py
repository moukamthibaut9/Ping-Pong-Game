import pygame
import time,sys,random

pygame.init()

longueur_ecran=500
largeur_ecran=700
nbr_cell_x=50
nbr_cell_y=70
taille_cell=10
taille_ecran=(longueur_ecran,largeur_ecran)


ecran=pygame.display.set_mode(taille_ecran,pygame.RESIZABLE)
pygame.display.set_caption("PING-PONG")


class Terrain:
    def __init__(self):
        self.rect_bordures=[pygame.Rect(0,0,longueur_ecran,10),pygame.Rect(longueur_ecran-10,10,10,largeur_ecran-10),
                            pygame.Rect(0,largeur_ecran-10,longueur_ecran-10,10),pygame.Rect(0,10,10,largeur_ecran-10)]
        self.rect_barre_milieu=pygame.Rect(0,largeur_ecran/2-5,longueur_ecran,10)
        self.rect_limite=pygame.Rect(0,0,longueur_ecran,largeur_ecran)
    def dessin_terrain(self):
        for rect in self.rect_bordures:
            pygame.draw.rect(ecran,pygame.Color("green"),rect)
        pygame.draw.rect(ecran,pygame.Color("red"),self.rect_barre_milieu)

class Joueur:
    def __init__(self):
        self.rect_joueur=pygame.Rect((longueur_ecran-100)/2,largeur_ecran-20,100,10)
        self.direction_j_x=0
    def dessin_joueur(self):
        pygame.draw.rect(ecran,pygame.Color("black"),self.rect_joueur)
    def deplacement_joueur(self,vitesse):
        self.rect_joueur.x+=vitesse*self.direction_j_x
        
class Game:
    def __init__(self):
        self.joueur=Joueur()
        self.terrain=Terrain()
        self.rect_balle=pygame.Rect((longueur_ecran-20)/2,0*taille_cell,20,20)
        self.direction_b_x=random.randint(-1,2)
        self.direction_b_y=1
        if self.direction_b_x==1:
            self.etat="droite-bas"
        else:self.etat="gauche-bas"
        self.liste=[]
    def dessin(self):
        pygame.draw.rect(ecran,pygame.Color("blue"),self.rect_balle)
        self.rect_balle.clamp_ip(self.terrain.rect_limite)
        self.joueur.rect_joueur.clamp_ip(self.terrain.rect_limite)
        self.terrain.dessin_terrain()
        self.joueur.dessin_joueur()
    def deplacement(self,vitesse):
        if self.rect_balle.colliderect(self.terrain.rect_bordures[0]) and self.etat=="droite-haut":
            self.etat="droite-bas"
            self.direction_b_x=1
            self.direction_b_y=1
        elif self.rect_balle.colliderect(self.terrain.rect_bordures[0]) and self.etat=="gauche-haut":
            self.etat="gauche-bas"
            self.direction_b_x=-1
            self.direction_b_y=1
        if self.rect_balle.colliderect(self.terrain.rect_bordures[1]) and self.etat=="droite-bas":
            self.etat="gauche-bas"
            self.direction_b_x=-1
            self.direction_b_y=1
        elif self.rect_balle.colliderect(self.terrain.rect_bordures[1]) and self.etat=="droite-haut":
            self.etat="gauche-haut"
            self.direction_b_x=-1
            self.direction_b_y=-1
        elif self.rect_balle.colliderect(self.terrain.rect_bordures[2]):
            police=pygame.font.SysFont("algerian",100,True,True)
            affichage=police.render("PERDU",False,(0,0,0)) 
            ecran.blit(affichage,(100,300,300,100))
            pygame.display.flip()
            time.sleep(5)
            pygame.quit()
            sys.exit()    
        if self.rect_balle.colliderect(self.terrain.rect_bordures[3]) and self.etat=="gauche-haut":
            self.etat="droite-haut"
            self.direction_b_x=1
            self.direction_b_y=-1
        elif self.rect_balle.colliderect(self.terrain.rect_bordures[3]) and self.etat=="gauche-bas":
            self.etat="droite-bas"
            self.direction_b_x=1
            self.direction_b_y=1
        if self.rect_balle.colliderect(self.joueur.rect_joueur) and self.etat=="gauche-bas":
            self.etat="gauche-haut"
            self.direction_b_x=-1
            self.direction_b_y=-1
            self.liste.append(1)
        elif self.rect_balle.colliderect(self.joueur.rect_joueur) and self.etat=="droite-bas":
            self.etat="droite-haut"
            self.direction_b_x=1
            self.direction_b_y=-1
            self.liste.append(1)
        self.rect_balle.x+=vitesse*self.direction_b_x
        self.rect_balle.y+=vitesse*self.direction_b_y
        self.joueur.deplacement_joueur(1)
        #print("[{},{}]".format(self.rect_balle.x,self.rect_balle.y))


police1=pygame.font.SysFont("algerian",57,True,True)    
police2=pygame.font.SysFont("arial",17,True,True)
message1=police1.render("JEU DE PING-PONG",False,(255,255,255))
message2=police2.render("Avec la barre en noir, empechez la balle bleu de toucher le sol",True,(255,0,255))
ecran.blit(message1,(0,150,longueur_ecran,57))
ecran.blit(message2,(0,400,longueur_ecran,17))
pygame.display.flip()
time.sleep(5)


game=Game()
while True:
    score=police1.render(str(len(game.liste)),True,(255,255,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                game.joueur.direction_j_x=1
            if event.key==pygame.K_a or event.key==pygame.K_LEFT:
                game.joueur.direction_j_x=-1 
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_d or event.key==pygame.K_RIGHT or event.key==pygame.K_a or event.key==pygame.K_LEFT:
                game.joueur.direction_j_x=0                
                     
    ecran.fill(pygame.Color("gray"))  
    game.dessin()
    game.deplacement(1)  
    ecran.blit(score,(longueur_ecran-100,10,100,57))
    pygame.display.flip() 
    pygame.display.update()
