# -*- encoding: utf-8 -*-

'''
@file item.py
@brief Implementa la clase Ball, Missile, Item y Oil
@author José Jesús Marente Florín
@date Febrero 2011.
'''

import gameobject
import particle
import data
import resource
import collisionmanager
import animation
import xml.dom.minidom
import math

#Distintos tipos de items
MISSILE, OIL, GUM, BALL = range(4)

class Item(gameobject.GameObject):
    '''
    @brief Clase que contiene los aspectos básicos de los items recogidos
    '''
    def __init__(self, game_control, owner, path_xml, x, y, angle):
        '''
        @brief Constructor.
        
        @param game_control Referencia a GameControl
        @param owner GameObject que lanza el item.
        @param path_xml Archivo xml con las características del item
        @param x Posición en el eje x
        @param y Posición en el eje y
        @param angle Ángulo del item
        '''
        gameobject.GameObject.__init__(self, game_control)
        
        #Parseamos la información básica
        parser = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        self.parser_basic_info(parser)
        
        #Propietario
        self.owner = owner
        
        #Definimos la posición del objeto
        self.x = self.old_x = x
        self.y = self.old_y = y
        
        #Si el angulo es 0, no hacemos nada
        if angle == 0:
            self.dx = 0
            self.dy = 0
        #Si es 0 actualizamos el angulo del item
        else:
            self.actual_angle = angle
            self.dx = math.cos(angle) * self.actual_speed
            self.dy = math.sin(angle) * self.actual_speed
        
        #Actualizamos la posicion del coche según su angulo
        self.update_position()
        #Actualizamos la rotación de la imagen del coche
        self.update_image()
        self.type = None
    
    def update(self):
        '''
        @brief Actualiza
        '''
        pass

class Missile(Item):
    '''
    @brief Clase que simula el comportamiento de un misil
    '''
    def __init__(self, game_control, owner, path_xml, x, y, angle):
        '''
        @brief Constructor.
        
        @param game_control Referencia a GameControl
        @param owner GameObject que lanza el item.
        @param path_xml Archivo xml con las características del item
        @param x Posición en el eje x
        @param y Posición en el eje y
        @param angle Ángulo del item
        '''
        Item.__init__(self, game_control, owner, path_xml, x, y, angle)
        
        self.type = MISSILE
        
        parser = xml.dom.minidom.parse(data.get_path_xml(path_xml))

        root = parser.firstChild
        
        #Inicializamos atributos
        self.aceleration = float(root.getAttribute('aceleration'))
        self.max_speed = float(root.getAttribute('max_speed'))
        self.explosion_sprite = resource.get_new_sprite('explosion')
        self.explosion_animation = animation.Animation('0,1,2,3,4,5,6,7,8,9,10,11,2,13,14,15,16,17,18,19,20,22,23,24,25', 0)
        
        #Funciones para cada estado
        self.states = {
            gameobject.NORMAL: self.__normal_state, 
            gameobject.RUN: self.__run_state, 
            gameobject.EXPLOSION: self.__explosion_state, 
            gameobject.ERASE: self.__erase_state, 
            }
        
        #Creamos el sistema de particulas, para cuando colisionemos con la caja
        self.explosion = False
        self.rect_explosion = self.explosion_sprite.get_frame(0).get_rect()
        self.actual_speed = 0.1

    def update(self):
        '''
        @brief Método que actualiza lógicamente el misil
        '''
        #Controlamos el cambio de estado para reiniciar la animación
        if self.state != self.previous_state:
            self.previous_state = self.state
            if self.state != gameobject.EXPLOSION:
                self.animations[self.state].restart()
        
        #Llamamos a la función del estado actual para actualizar
        self.states[self.state]()

        #Si el coche no se encuentra cayendo
        if self.state != gameobject.EXPLOSION:
            #Actualizmaos posicion. imagen y dirección
            self.update_position()
            self.update_direction()
            self.update_angle()

    def draw(self, screen):
        '''
        @brief Método que dibuja el elemento en pantalla
        
        @param screen Superficie destino
        '''
        #Si el estado no es de explosión dibujamos normal
        if self.state != gameobject.EXPLOSION:
            gameobject.GameObject.draw(self, screen)
            
        #Si el estado es de explosión y ya hemos creado el sistema de particulas
        #dibujamos el sistema de particulas
        elif self.explosion:
            image = self.explosion_sprite.get_frame(self.explosion_animation.get_frame())
            screen.blit(image, (self.rect_explosion.x - self.game_control.circuit_x(), self.rect_explosion.y - self.game_control.circuit_y()))
            
    def __normal_state(self):
        '''
        @brief Método privado que actualia la caja cuando esta en estado normal
        '''
        self.move(cmp(self.actual_speed, 0))
        
        #Y la trigonometria del mismo
        self.trigonometry()
        
        #Si el coche que soltó la mancha de aceite ya la a dejao atras cambiamos su estado,
        #Para que ya pueda colisionar con él
        if not collisionmanager.CollisionManager().actor_rectanglecollision(self, self.owner):
            self.state = gameobject.RUN
            
    def __run_state(self):
        '''
        @brief Método privado que actualia la caja cuando esta en estado de avance
        '''
        self.move(cmp(self.actual_speed, 0))
        
        #Y la trigonometria del mismo
        self.trigonometry() 
           
    def __erase_state(self):
        '''
        @brief Método privado que actualia la caja cuando esta en estado de borrado
        '''
        self.kill()
        
    def __explosion_state(self):
        '''
        @brief Método privado que actualia la caja cuando esta en estado de explosión
        '''
        if not self.explosion:
            self.rect_explosion.centerx = self.rect.centerx
            self.rect_explosion.centery = self.rect.centery
            self.explosion = True
            
        if self.explosion_animation.update():
            self.kill()
        
class Oil(Item):
    '''
    @brief Clase que representa una mancha de aceite, tambié servirá para representar un chicle
    '''
    def __init__(self, game_control, owner, path_xml, x, y, angle, gum = False):
        '''
        @brief Constructor.
        
        @param game_control Referencia a GameControl
        @param owner GameObject que lanza el item.
        @param path_xml Archivo xml con las características del item
        @param x Posición en el eje x
        @param y Posición en el eje y
        @param angle Ángulo del item
        @param 
        '''
        Item.__init__(self, game_control, owner, path_xml, x, y, angle)
        
        if gum:
            self.type = GUM
        else:
            self.type = OIL
        
        #Funciones para cada estado
        self.states = {
            gameobject.NORMAL: self.__normal_state, 
            gameobject.RUN: self.__run_state, 
            }
            
    def update(self):
        '''
        @brief Método que actualiza lógicamente la macha de aceite
        '''
        #Controlamos el cambio de estado para reiniciar la animación
        if self.state != self.previous_state:
            self.previous_state = self.state
            if self.state != gameobject.EXPLOSION:
                self.animations[self.state].restart()
        
        #Llamamos a la función del estado actual para actualizar
        self.states[self.state]()        
            
    def __normal_state(self):
        '''
        @brief Método privado que actualia la caja cuando esta en estado normal
        '''
        #Si el coche que soltó la mancha de aceite ya la a dejao atras cambiamos su estado,
        #Para que ya pueda colisionar con él
        if not collisionmanager.CollisionManager().actor_rectanglecollision(self, self.owner):
            self.state = gameobject.RUN
            
    def __run_state(self):
        '''
        @brief Método privado que actualia la caja cuando esta en estado de avance
        '''
        pass

class Ball(Item):
    '''
    @brief Clase que representa la bola, hereda de la clase misil, ya que tendrá
    las mismas características, solo cambia en la colisión con los tiles
    '''
    def __init__(self, game_control, owner, path_xml, x, y, angle):
        '''
        @brief Constructor.
        
        @param game_control Referencia a GameControl
        @param owner GameObject que lanza el item.
        @param path_xml Archivo xml con las características del item
        @param x Posición en el eje x
        @param y Posición en el eje y
        @param angle Ángulo del item
        '''
        Item.__init__(self, game_control, owner, path_xml, x, y, angle)

        #Indicamos que es de tipo bola
        self.type = BALL
        
        parser = xml.dom.minidom.parse(data.get_path_xml(path_xml))

        root = parser.firstChild
        
        #Inicializamos atributos
        self.aceleration = float(root.getAttribute('aceleration'))
        self.max_speed = float(root.getAttribute('max_speed'))
        self.particle_code = root.getAttribute('particle_code')

        #Funciones para cada estado
        self.states = {
            gameobject.NORMAL: self.__normal_state, 
            gameobject.RUN: self.__run_state, 
            gameobject.EXPLOSION: self.__explosion_state, 
            gameobject.ERASE: self.__erase_state, 
            }
        
        #Creamos el sistema de particulas, para cuando colisionemos con la caja
        self.particles = None
        self.actual_speed = 0.1

    def update(self):
        '''
        @brief Método que actualiza lógicamente el misil
        '''
        #Controlamos el cambio de estado para reiniciar la animación
        if self.state != self.previous_state:
            self.previous_state = self.state
            if self.state != gameobject.EXPLOSION:
                self.animations[self.state].restart()
        
        #Llamamos a la función del estado actual para actualizar
        self.states[self.state]()

        #Si el coche no se encuentra cayendo
        if self.state != gameobject.EXPLOSION:
            #Actualizmaos posicion. imagen y dirección
            self.update_position()
            self.update_direction()
            self.update_angle()

    def draw(self, screen):
        '''
        @brief Método que dibuja el elemento en pantalla
        
        @param screen Superficie destino
        '''
        #Si el estado no es de explosión dibujamos normal
        if self.state != gameobject.EXPLOSION:
            gameobject.GameObject.draw(self, screen)
            
        #Si el estado es de explosión y ya hemos creado el sistema de particulas
        #dibujamos el sistema de particulas
        elif self.particles:
            self.particles.draw(screen)
                     
    def __normal_state(self):
        '''
        @brief Método privado que actualia la caja cuando esta en estado normal
        '''
        self.move(cmp(self.actual_speed, 0))
        
        #Y la trigonometria del mismo
        self.trigonometry()
        
        #Si el coche que soltó la mancha de aceite ya la a dejao atras cambiamos su estado,
        #Para que ya pueda colisionar con él
        if not collisionmanager.CollisionManager().actor_rectanglecollision(self, self.owner):
            self.state = gameobject.RUN
            
    def __run_state(self):
        '''
        @brief Método privado que actualia la caja cuando esta en estado de avance
        '''
        self.move(cmp(self.actual_speed, 0))
        
        #Y la trigonometria del mismo
        self.trigonometry() 
           
    def __erase_state(self):
        '''
        @brief Método privado que actualia la caja cuando esta en estado de borrado
        '''
        self.kill()
        
    def __explosion_state(self):
        '''
        @brief Método privado que actualia la caja cuando esta en estado de explosión
        '''
        if not self.particles:
            self.particles = particle.SystemParticle(self.game_control, 
                                                    self.rect.centerx, 
                                                    self.rect.centery, 
                                                    [self.particle_code,], 
                                                    25, 1, 5, 100, 0.5)

        #Actualizamos el sistema de particulas
        self.particles.update()
        
        #Si se ha acabado, cambiamos el estado de la caja y 
        #reiniciamos el sistema de particulas
        if self.particles.done():
            self.particles = None
            self.state = gameobject.ERASE
            self.kill()
