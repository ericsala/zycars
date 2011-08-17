#-*- encoding: utf-8 -*-

'''
@file start.py
Implementa la clase Start
@author José Jesús Marente Florín
@date Febrero 2011.
'''

import config
import resource
import playercar
import ia


class Start:
    '''
    @brief Clase encargada de situar la linea de salida en el circuito, así 
    como los distinos coches que compitan
    '''
    def __init__(self, game_control, circuit, x, y, image_code, orientation, 
    car_angle):
        '''
        @brief Constructor.
        
        @param game_control Referencia a GameControl
        @param circuit Referencia a Circuit
        @param x Posición en el eje x
        @param y Posición en el eje y
        @param image_code Código de la imagen(será del mismo ancho y algo que 
        los tiles de circuito)
        @param orientation Indica si la linea será horizontal o vertical
        @param car_angle angulo para situar al coche
        '''
        #Referencias
        self.game_control = game_control
        self.circuit = circuit
        
        #Posición
        self.x = x
        self.y = y
        
        #Imagen
        self.image = resource.get_image(image_code)
        
        self.orientation = orientation
        
        self.car_angle = car_angle
        
        if config.Config().get_mode() == config.TIMED:
            self.place_player() 
        else:
            self.place_cars()


    def draw(self, screen):
        '''
        @brief Método que dibuja la linea de meta en pantalla
        
        @param screen Superficie destino
        '''
        
        #Segun la orientación de la linea de meta, la dibujamos de una forma 
        #u otra
        if self.orientation == 'vertical':
            aux_y = 0
            for i in range(self.circuit.get_goal_width()):
                screen.blit(self.image, 
                            (self.x - self.game_control.circuit_x(),
                            aux_y + self.y - self.game_control.circuit_y()))
                #Obtenemos la posicion de la siguiente
                aux_y += self.image.get_height()
        else:
            aux_x = 0
            for i in range(self.circuit.get_goal_width()):
                screen.blit(self.image, 
                        (aux_x + self.x - self.game_control.circuit_x(),
                        self. y - self.game_control.circuit_y()))
                #Obtenemos la posicion de la siguiente
                aux_x += self.image.get_width()
    
    def place_player(self):
        '''
        @brief Situa al jugador en la linea de salida
        '''
        player = config.Config().get_player()
        #Si hemos indicado que la posición es vertical
        if self.orientation == 'vertical':
            #Obtenemos una superfice con el ancho de la "carretera" del 
            #circuito como referencia
            #Situamos al coche según el angulo indicado
            
            #A la izquierda de la linea
            if self.car_angle == 0:
                self.game_control.add_player(playercar.PlayerCar(
                self.game_control, 
                player, self.x - self.circuit.get_tile_width(), 
                self.y + self.circuit.get_tile_height() * 2, 0))
            
            #A la derecha de la linea
            elif self.car_angle == 180:
                self.game_control.add_player(playercar.PlayerCar(
                self.game_control, 
                player, self.x + self.circuit.get_tile_width() * 2, 
                self.y + self.circuit.get_tile_height() * 3, 180))
        
        #Si por el contrario la posición es horizontal
        else:
            #Creamos una superficie con el alto de la carretera del circuito 
            #como referencia
            #Situamos el coche en el angulo adecuado
            
            #Debajo de la linea
            if self.car_angle == 90:
                self.game_control.add_player(playercar.PlayerCar(
                self.game_control, 
                player, self.x + self.circuit.get_tile_width() * 2, 
                self.y - self.circuit.get_tile_height(), 90))

            #Arriba de la linea
            elif self.car_angle == 270:
                self.game_control.add_player(playercar.PlayerCar(
                self.game_control, 
                player, self.x + self.circuit.get_tile_width() * 2, 
                self.y + self.circuit.get_tile_height() * 2, 270))
    
    def place_cars(self):
        '''
        @brief Situa a todos los jugadores tras la linea de salida
        '''
        rivals = config.Config().get_competitors()
        player = config.Config().get_player()
        #Si hemos indicado que la posición es vertical
        if self.orientation == 'vertical':
            #Obtenemos una superfice con el ancho de la "carretera" del 
            #circuito como referencia
            #Situamos al coche según el angulo indicado
            
            #A la izquierda de la linea
            if self.car_angle == 0:
                #Cuarto
                self.game_control.add_player(playercar.PlayerCar(
                self.game_control, 
                player, self.x - self.circuit.get_tile_width() * 3 - 45, 
                self.y + self.circuit.get_tile_height() * 3, 0))

                #Primero
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[0], self.x - self.circuit.get_tile_width(), 
                self.y + self.circuit.get_tile_height() * 2, 0))
                #Segundo
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[1], self.x - self.circuit.get_tile_width() - 45, 
                self.y + self.circuit.get_tile_height() * 3, 0))
                #Tercero
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[2], self.x - self.circuit.get_tile_width() * 3, 
                self.y + self.circuit.get_tile_height() * 2, 0))
            
            #A la derecha de la linea
            elif self.car_angle == 180:
                #Cuarto
                self.game_control.add_player(playercar.PlayerCar(
                self.game_control, 
                player, self.x + self.circuit.get_tile_width() * 4 + 45, 
                self.y + self.circuit.get_tile_height() * 2, 180))

                #Primero
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[0], self.x + self.circuit.get_tile_width() * 2, 
                self.y + self.circuit.get_tile_height() * 3, 180))
                #Segundo
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[1], self.x + self.circuit.get_tile_width() * 2 + 45, 
                self.y + self.circuit.get_tile_height() * 2, 180))
                #Tercero
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[2], self.x + self.circuit.get_tile_width() * 4, 
                self.y + self.circuit.get_tile_height() * 3, 180))
        
        #Si por el contrario la posición es horizontal
        else:
            #Creamos una superficie con el alto de la carretera del circuito 
            #como referencia
            #Situamos el coche en el angulo adecuado
            
            #Debajo de la linea
            if self.car_angle == 90:
                #Cuarto
                self.game_control.add_player(playercar.PlayerCar(
                self.game_control, 
                player, self.x + self.circuit.get_tile_width() * 3, 
                self.y - self.circuit.get_tile_height() * 4 - 45, 90))
                
                #Primero
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[0], self.x + self.circuit.get_tile_width() * 2, 
                self.y - self.circuit.get_tile_height(), 90))
                #Segundo
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[1], self.x + self.circuit.get_tile_width() * 3, 
                self.y - self.circuit.get_tile_height() - 45, 90))
                #Tercero
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[2], self.x + self.circuit.get_tile_width() * 2, 
                self.y - self.circuit.get_tile_height() * 4, 90))

            
            #Arriba de la linea
            elif self.car_angle == 270:
                #Cuarto
                self.game_control.add_player(playercar.PlayerCar(
                self.game_control, 
                player, self.x + self.circuit.get_tile_width() * 3, 
                self.y + self.circuit.get_tile_height() * 4 + 45, 270))
                
                #Primero
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[2], self.x + self.circuit.get_tile_width() * 2, 
                self.y + self.circuit.get_tile_height() * 2, 270))
                #Segundo
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[0], self.x + self.circuit.get_tile_width() * 3, 
                self.y + self.circuit.get_tile_height() * 2 + 45, 270))
                #Tercero
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                rivals[1], self.x + self.circuit.get_tile_width() * 2, 
                self.y + self.circuit.get_tile_height() * 4, 270))
