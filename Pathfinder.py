import pygame
from pygame.locals import *
walls = []
Pixel_group = pygame.sprite.Group()
##font = pygame.font.Font('Constantia', 36)

Clock = pygame.time.Clock()

class Vector2:
     def __init__(self,x,y):
          self.x = x
          self.y = y

class FinderTree:

     def __init__(self, root: 'Node', pixels):
          self.pixels = pixels
          

          root.children = self.getChildren(root)

          self.root = root
          self.frontier = [] 
          self.explored = []
    
     def findPath(self,to):
          self.to = to
          current = self.root
          self.explored.append(self.root)
          self.explore(current)

          
          new_pixel = Pixel((current.pos.x, current.pos.y), 'caracter')
          Pixel_group.add(new_pixel)


          while(len(self.frontier) > 0):
               ##print('loopou')
               pygame.time.delay(10) 

               screen.fill((255, 255, 255))
               Pixel_group.draw(screen)
               pygame.display.flip()

               current = self.getSmallestCostNode()
               ##print(f"{current.pos.x},{current.pos.y}")
               self.explore(current)
               self.explored.append(current)
               self.frontier.remove(current)

               new_pixel = Pixel((current.pos.x, current.pos.y), 'explored')
               Pixel_group.add(new_pixel)

               if(current.pos.x == to.x and current.pos.y == to.y):
                    return self.searchPath(current)
    
     def explore(self, node: 'Node'):
         ##print("explore")
         testChildren = self.getChildren(node)

         for child in testChildren:
               ##print(f"{child.pos.x};{child.pos.y} Test")
               if(not Pixel.TesteColide(child.pos.x,child.pos.y)):
                         b = True
                         for node in self.explored:
                              ##print(F"Compare {node.pos.x};{node.pos.y}  and  {child.pos.x}; {child.pos.y}")
                              if(node.pos.x == child.pos.x and node.pos.y == child.pos.y):
                                   ##print('ingual')
                                   b = False
                         for node in self.frontier:
                              ##print(F"Compare {node.pos.x};{node.pos.y}  and  {child.pos.x}; {child.pos.y}")
                              if(node.pos.x == child.pos.x and node.pos.y == child.pos.y):
                                   ##print('ingual')
                                   b = False
                         if(b):
                              ##print(f"{child.pos.x};{child.pos.y} appended")
                              self.frontier.append(child)
                              new_pixel = Pixel((child.pos.x, child.pos.y), 'frontier')
                              Pixel_group.add(new_pixel)
         ##print("EndExplore")

         return

     def searchPath(self,node:'Node'):
          while(node.parent != None):
               Pixel_group.draw(screen)
               pygame.display.flip()
               new_pixel = Pixel((node.pos.x, node.pos.y), 'path')
               Pixel_group.add(new_pixel)
               print(node.gcost)
               node = node.parent

     
     def getChildren(self,node:'Node'):
          children = []
          ##print('StartGetCHildren')
     
          child = Node(Vector2(node.pos.x +squareSize, node.pos.y) ,node)
          children.append(child )

          child = Node(Vector2(node.pos.x -squareSize, node.pos.y) ,node)
          children.append(child )
          
          child = Node(Vector2(node.pos.x, node.pos.y + squareSize) ,node)
          children.append(child )

          child = Node(Vector2(node.pos.x, node.pos.y - squareSize) ,node)
          children.append(child )

          ##print("EndGetChildren")
          return children
     
     def getSmallestCostNode(self):
          ##print('getsmallestcostnode')
          current = self.frontier[0]
          currentcost = current.getCost(self.to)
          for node in self.frontier:
               nodecost = node.getCost(self.to)
               if(nodecost < currentcost):
                    currentcost = nodecost
                    current = node
          ##print(f"smallestcost = {currentcost}")
          ##print('endgetsmallestcostnoed')
          return current

          """'''''''''"""
"""
     def drawpath(self):
         steps = []
         for step in steps:
               Pixel_group.draw(Pixel(self.pixels.postoScreen(step.pos.x),self.pixels.postoScreen(step.pos.y)))
               draw_text(f'{steps.index(step) +1}')
               """
class Node:
    

    def __init__(self,pos:Vector2, parent:'Node' = None):
          print(type(parent))
          self.pos = pos
          self.parent = parent
          if(parent != None):
               if(parent.gcost != None):
                    self.gcost = parent.gcost + 1
          else:
               self.gcost = 0
                    

        
    
    
    
    def getCost(self,to:'Vector2' = None ) -> int:
          if(to == None):
               return 0
          cost = round( (((self.pos.x - to.x)**2 + (self.pos.y - to.y)**2)**(1/2))/squareSize)
          ##print(f"hcost = {cost}; gcost = {self.gcost}")
          return cost + self.gcost

pygame.init()
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width,screen_height))
pixel_color = (0,0,0)
player_color = (255,0,0)
screen.fill((255,255,255))
running = True
start = Vector2(0,0)
end = Vector2(0,0)
squareSize = 40
drawing = False
candrawFrom = True
candrawTo = True
startPos:Vector2
finalPos:Vector2
class Pixel(pygame.sprite.Sprite):
     def __init__(self, position, group):
        pygame.sprite.Sprite.__init__(self)
        self.group = group
        if self.group == "wall":
          self.image = pygame.Surface((squareSize, squareSize))
          self.image.fill(pixel_color)
          self.rect = self.image.get_rect(topleft=position)
        elif self.group == "caracter":
          self.image = pygame.Surface((squareSize, squareSize))
          self.image.fill(player_color)
          self.rect = self.image.get_rect(topleft=position)
        elif self.group == "end":
          self.image = pygame.Surface((squareSize, squareSize))
          self.image.fill((0,255,0))
          self.rect = self.image.get_rect(topleft=position)
        elif self.group == "frontier":
          self.image = pygame.Surface((squareSize, squareSize))
          self.image.fill((255, 165, 0))
          self.rect = self.image.get_rect(topleft=position)
        elif self.group == "explored":
          self.image = pygame.Surface((squareSize, squareSize))
          self.image.fill((255, 0, 0))
          self.rect = self.image.get_rect(topleft=position)
        elif self.group == "path":
          self.image = pygame.Surface((squareSize, squareSize))
          self.image.fill((0, 255, 255))
          self.rect = self.image.get_rect(topleft=position)

     def screenpixeltoPos(self,x,y):
          x = round(x/squareSize)*squareSize
          y = round(y/squareSize)*squareSize         
          return(x,y)  
     def screendottoPos(x):
          x = round(x/squareSize)*squareSize
          return x
     def postoScreen(x):
          return x*squareSize
     def TesteColide(x,y):
          x = round(x/squareSize)*squareSize
          y = round(y/squareSize)*squareSize
          for pixel in Pixel_group:
               if pixel.group == "wall":
                    if pixel.rect.collidepoint(x,y):
                         print(f"{x},{y}")
                         return True
          return False
     def add_borders():
          for x in range(0, screen_width, squareSize):
               top_pixel = Pixel((x, 0), 'wall')
               bottom_pixel = Pixel((x, screen_height - squareSize), 'wall')
               Pixel_group.add(top_pixel, bottom_pixel)

          for y in range(0, screen_height, squareSize):
               left_pixel = Pixel((0, y), 'wall')
               right_pixel = Pixel((screen_width - squareSize, y), 'wall')
               Pixel_group.add(left_pixel, right_pixel)
               ##nove função que recebe posição em vector de 0 a 25 e desenha um quadrado nessa posição 
               

     ## def funcção leandro colisaõ  (recebe uma posição em pontos do mapa (de 0 a 25) e retorna se existe um quadrado la ou não )
     ## recebe vector2 como inpu
pixel:Pixel
Pixel.add_borders()
while running:
    Clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                x = Pixel.screendottoPos(event.pos[0] - squareSize / 2)
                y = Pixel.screendottoPos(event.pos[1] - squareSize / 2)
                new_pixel = Pixel((x, y), 'wall')
                Pixel_group.add(new_pixel)
            elif event.button == 2 and candrawFrom:
                candrawFrom = False
                drawing = True
                x = Pixel.screendottoPos(event.pos[0] - squareSize / 2)
                y = Pixel.screendottoPos(event.pos[1] - squareSize / 2)
                new_pixel = Pixel((x, y), 'caracter')
                startPos = Vector2(x,y)
                pixel = new_pixel
                Pixel_group.add(new_pixel)
            elif event.button == 3 and candrawTo:
                candrawTo = False
                drawing = True
                x = Pixel.screendottoPos(event.pos[0] - squareSize / 2)
                y = Pixel.screendottoPos(event.pos[1] - squareSize / 2)
                new_pixel = Pixel((x, y), 'end')
                endPos = Vector2(x,y)
                Pixel_group.add(new_pixel)
        elif event.type == MOUSEBUTTONUP:
            if event.button in {1, 2, 3}:
                drawing = False
        elif event.type == MOUSEMOTION and drawing and event.buttons[0] == 1:
            x = Pixel.screendottoPos(event.pos[0] - squareSize / 2)
            y = Pixel.screendottoPos(event.pos[1] - squareSize / 2)
            new_pixel = Pixel((x, y), 'wall')
            Pixel_group.add(new_pixel)
        elif event.type == KEYDOWN:
               if event.key == K_SPACE:
                    x = Pixel.screendottoPos(pygame.mouse.get_pos()[0] - squareSize / 2)
                    y = Pixel.screendottoPos(pygame.mouse.get_pos()[1] - squareSize / 2)
                    if(not candrawFrom and not candrawTo):
                         startPos = pixel.screenpixeltoPos(startPos.x,startPos.y) 
                         startPos = Vector2(startPos[0],startPos[1])
                         Arvore = FinderTree(Node(startPos),pixel)
                         Arvore.findPath(endPos)
                    # Desenhando na tela
               if event.key == K_f:
                    Pixel.TesteColide(Pixel.screendottoPos(pygame.mouse.get_pos()[0]),Pixel.screendottoPos(pygame.mouse.get_pos()[1]))
    screen.fill((255, 255, 255))
    Pixel_group.draw(screen)
    pygame.display.flip()

pygame.quit()