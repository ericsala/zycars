#-*- encoding: utf-8 -*-

import pygame
import circuit
import basiccar
import gameobject

from log import Log

class CollisionManager:
    '''
    @brief Clase encargada de comprobar si se a producido algun tipo de colision,
    tanto entre objetos, como objetos con los elemento del circuito.
    '''
    def __init__(self):
        '''
        @brief Constructor
        '''
        pass
        
    def actor_perfectcollision(self, sprite1, sprite2):
        '''
        @brief Comprueba la colision pixel por pixel enter dos sprites.
        
        @param sprite1 Sprite a comprobar
        @param sprite2 Sprite a comprobar
        
        @return True si existe colisión, False en caso contrario
        '''
        return pygame.sprite.collision_mask(sprite1, sprite2)
        
    def actor_rectanglecollision(self, sprite1, sprite2):
        '''
        @brief Comprueba la colision de los rectangulos de los sprites
        
        @param sprite1 Sprite a comprobar
        @param sprite2 Sprite a comprobar
        
        @return True si existe colisión, False en caso contrario
        '''
        return pygame.sprite.collision_rect(sprite1, sprite2)
        
    def actor_edgecollision(self, sprite1, sprite2):
        '''
        @brief  Devuelve un diccionario indicando por que lados han colisionado los sprites.
       
        @param sprite1 Sprite a comprobar
        @param sprite2 Sprite a comprobar
        
        @return Diccionario indicando por que lados han colisionado los sprites.
        '''
        
        #Obtenemos los rectagulos de cada uno de los sprites
        rect1 = sprite1.get_rect()
        rect2 = sprite2.get_rect()
        
        #Inicializmaos el diccionario
        edge = {"left": False, "right": False, "top": False, "bottom": False}
        
        if self.actor_perfectcollision(sprite1, sprite2):
            
            #Comprobamos por que lados colisiona
            if (rect1.left - rect2.left) > 0:
                edge["right"] = True
                
            if (rect1.left - rect2.left) < 0:
                edge["left"] = True
                
            if (rect1.top - rect2.top) > 0:
                edge["bottom"] = True
                
            if (rect1.top - rect2.top) < 0:
                edge["top"] = True
        
        return edge
        
    def actor_tile_edgecollision(self, sprite, tile_rect):
        '''
        @brief Función que comprueba si un sprite colisiona con un rectangulo y 
        devuelve por que lados se produce la colisión.
        
        @param sprite Sprite a comprobar
        @param tile_rect Rectangulo a comprobar
        
        @return Diccionario indicando por que lados han colisionado los sprites.
        '''
        #Obtenemos el rectangulo del sprite
        sprite_rect = sprite.get_rect()
        
        #Inicializamos el diccionario
        edge = {"left": False, "right": False, "top": False, "bottom": False}
        Log().debug('Coche: (' + str(sprite_rect.x) + ', ' + str(sprite_rect.y) + ', ' + str(sprite_rect.w) + ', ' + str(sprite_rect.h) + ')')
        Log().debug('Tile: (' + str(tile_rect.x) + ', ' + str(tile_rect.y) + ', ' + str(tile_rect.w) + ', ' + str(tile_rect.h) + ')')

        if sprite_rect.colliderect(tile_rect):
        
            #Vemos por que lados se produce la colisión
            if (sprite_rect.left - tile_rect.left) > 0:
                edge["right"] = True
                Log().debug("Collision por la derecha")

            if (sprite_rect.left - tile_rect.left) < 0:
                edge["left"] = True
                Log().debug("Collision por la izquierda")

            if (sprite_rect.top - tile_rect.top) > 0:
                edge["bottom"] = True
                Log().debug("Collision por abajo")

            if (sprite_rect.top - tile_rect.top) < 0:
                edge["top"] = True
                Log().debug("Collision por arriba")
                
        return edge
        
    def tile_collision():
        pass
        
    def level_collision(self, sprite, circ):
        '''
        @brief Comprueba la colision de un sprite con los elementos del circuito,
        si se produce alguna colisión, se corrige la posicion del objeto.
        
        @param sprite Sprite a comprobar
        @param circ Circuito a comprobar
        '''
        #Comprobamos el eje X.
        x_collision = False
        y_collision = False
        result = None
        tile_pos = None
        tile_rect = None

        #Colisiones verticales, con el eje x
        if sprite.go_left():
            result = self.__collision_ver(sprite, circ, "left")
            
        elif not result and sprite.go_right():
            result = self.__collision_ver(sprite, circ, "right")
            
        #Colision horizontales, con el eje y
        elif not result and sprite.go_up():
            result = self.__collision_hor(sprite, circ, "up")
            
        elif not result and sprite.go_down():
            result = self.__collision_hor(sprite, circ, "down")
            
        #Si hemos obtenido algún resultado y es de tipo colisionable
        if result and result['type'] == circuit.NOPASSABLE:
            
            tile_rect = result['rect']
            #Vemos por que lados colisiona
            edge = self.actor_tile_edgecollision(sprite, tile_rect)
                        
            collision = collision_top = collision_bottom = \
            collision_left = collision_right = False
            
            #Comprobamos que lado debemos corregir, viendo que parte del sprite
            #Esta mas superpuesto con el tile
            if edge['left'] and edge['bottom']:
                left_car = tile_rect.left - sprite.rect.left
                bottom_car = sprite.rect.bottom - tile_rect.bottom
                
                if left_car > bottom_car:
                    Log().info('Corregiriamos colision por la izquierda')
                    collision_left = True
                elif left_car < bottom_car:
                    Log().info('Corregiriamos colision por abajo')
                    collision_bottom = True
                    
            elif edge['left'] and edge['top']:
                left_car = tile_rect.left - sprite.rect.left
                top_car = tile_rect.top - sprite.rect.top
                
                if left_car > top_car:
                    Log().info('Corregiriamos colision por la izquierda')
                    collision_left = True
                elif left_car < top_car:
                    Log().info('Corregiriamos colision por arriba')
                    collision_top = True
                                    
            elif edge['right'] and edge['bottom']:
                right_car = sprite.rect.right - tile_rect.right
                bottom_car = sprite.rect.bottom - tile_rect.bottom
                
                if right_car > bottom_car:
                    Log().info('Corregiriamos colision por la derecha')
                    collision_right = True
                elif right_car < bottom_car:
                    Log().info('Corregiriamos colision por abajo')
                    collision_bottom = True
                
            elif edge['right'] and edge['top']:
                right_car = sprite.rect.right - tile_rect.right
                top_car = tile_rect.top - sprite.rect.top
                
                if right_car > top_car:
                    Log().info('Corregiriamos colision por la derecha')
                    collision_right = True
                elif right_car < top_car:
                    Log().info('Corregiriamos colision por arriba')
                    collision_top = True
            
            #Según la colisión corregiremos de una forma u otra el rectangulo del sprite   
            if sprite.dx < 0:         
                if collision_right:
                    #sprite.rect.x = tile_rect.x + tile_rect.w
                    sprite.x = tile_rect.x + tile_rect.w + (sprite.rect.w / 2)
                    sprite.actual_speed *= -1
                    collision = True
            else:
                if collision_left:
                    #sprite.rect.x = tile_rect.x - sprite.rect.w
                    sprite.x = tile_rect.x - (sprite.rect.w / 2)
                    sprite.actual_speed *= -1
                    collision = True
                    
            if sprite.dy < 0:
                if collision_bottom:
                    sprite.y = tile_rect.y + tile_rect.w + (sprite.rect.h / 2)
                    sprite.actual_speed *= -1
                    #sprite.rect.y = tile_rect.y + tile_rect.h
                    collision = True
            else:
                if collision_top:
                    sprite.y = tile_rect.y - (sprite.rect.h / 2)
                    sprite.actual_speed *= -1
                    #sprite.rect.y = tile_rect.y - sprite.rect.h
                    collision = True
            
            #Vemos en que estado esta el coche para aplicar una fuerza en una dirección u otra
            '''if collision:
                #print Log().critical(sprite.get_state())
                #print Log().critical(sprite.get_old_state())
                
                if (sprite.get_state() == gameobject.REVERSE or \
                    (sprite.get_state() == gameobject.NOACTION and sprite.get_old_state() == gameobject.REVERSE))\
                    and sprite.actual_speed < 0:
                    Log().debug("1")
                    sprite.actual_speed = sprite.get_max_speed()
                    
                elif (sprite.get_state() == gameobject.RUN or \
                    (sprite.get_state() == gameobject.NOACTION and sprite.get_old_state() == gameobject.RUN))\
                    and sprite.actual_speed > 0:
                    sprite.actual_speed = -sprite.get_max_speed()
                    Log().debug("2")'''
                    
                #elif sprite.get_state() != gameobject.REVERSE and sprite.get_state() != gameobject.RUN and sprite.actual_speed > 0:
                #    sprite.actual_speed = -sprite.get_max_speed()
                #    Log().debug("2")
                #elif sprite.get_state() != gameobject.REVERSE and sprite.get_state() != gameobject.RUN and sprite.actual_speed < 0:
                #    sprite.actual_speed = sprite.get_max_speed()
                #    Log().debug("3")
                #elif (sprite.get_old_state() == gameobject.RUN or sprite.get_state() == gameobject.RUN) and sprite.actual_speed < 0:
                #    sprite.actual_speed = sprite.get_max_speed()
                #elif (sprite.get_old_state() == gameobject.REVERSE or sprite.get_state() == gameobject.REVERSE) and sprite.actual_speed > 0:
                #    sprite.actual_speed = -sprite.get_max_speed()

                #sprite.actual_speed *= -1
                
        #Si hemos obtenido colisión y es de tipo lag
        elif result and result['type'] == circuit.LAG:
            
            #Si el coche va mas rapido que la mitad de su velocidad maxima
            if(abs(sprite.actual_speed) > (abs(sprite.get_max_speed()) / 2)):
                
                #Reducimos su velocidad a la mitad de su máximo
                if sprite.actual_speed > 0:
                    sprite.actual_speed = abs(sprite.get_max_speed()) / 2
                else:
                    sprite.actual_speed = -1 * (abs(sprite.get_max_speed()) / 2)
                
    def __collision_ver(self, sprite, circ, direction):

        tile_y0 = sprite.rect.y / circ.get_tile_height()
        tile_y1 = (sprite.rect.y + sprite.rect.h) / circ.get_tile_height()
        
        if direction == "left":
            tilecoordx = sprite.rect.x / circ.get_tile_width()
        else:
            tilecoordx = (sprite.rect.x + sprite.rect.w) / circ.get_tile_width()
        
        i = tile_y0
        
        while i <= tile_y1:
            if (circ.get_tile(1, tilecoordx, i).type == circuit.NOPASSABLE) or \
            (circ.get_tile(0, tilecoordx, i).type == circuit.NOPASSABLE):
                tilecoordx *= circ.get_tile_width()
                
                result = {}
                result['type'] = circuit.NOPASSABLE
                result['rect'] = pygame.Rect((tilecoordx, i * circ.get_tile_height(), \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return result
            
            elif (circ.get_tile(1, tilecoordx, i).type == circuit.LAG) or \
            (circ.get_tile(0, tilecoordx, i).type == circuit.LAG):
                
                result = {}
                result['type'] = circuit.LAG
                result['rect'] = pygame.Rect((tilecoordx, i * circ.get_tile_height(), \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return result
                
            i += 1
        
        return False
            
    def __collision_hor(self, sprite, circ, direction):

        tile_x0 = sprite.rect.x / circ.get_tile_width()
        tile_x1 = (sprite.rect.x + sprite.rect.w) / circ.get_tile_width()
        
        if direction == "up":
            tilecoordy = sprite.rect.y /circ.get_tile_height()
        else:
            tilecoordy = (sprite.rect.y + sprite.rect.h) /circ.get_tile_height()
        
        i = tile_x0
        
        while i <= tile_x1:
            if (circ.get_tile(1, i, tilecoordy).type == circuit.NOPASSABLE) or \
            (circ.get_tile(0, i, tilecoordy).type == circuit.NOPASSABLE):
                tilecoordy *= circ.get_tile_height()
                
                result = {}
                result['type'] = circuit.NOPASSABLE
                resutl['rect'] = pygame.Rect((i * circ.get_tile_width(), tilecoordy, \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return rect
            elif (circ.get_tile(1, i, tilecoordy).type == circuit.LAG) or \
            (circ.get_tile(0, i, tilecoordy).type == circuit.LAG):
                
                result = {}
                result['type'] = circuit.LAG
                result['rect'] = pygame.Rect((i * circ.get_tile_width(), tilecoordy, \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return result
                
            i += 1
            
        return False
