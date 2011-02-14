#-*- encoding: utf-8 -*-

import state
import data
import resource
import button
import keyboard
import pygame
import cursor
import basicmenu
import optionmenu
import charactermenu
import xml.dom.minidom
import unicodedata

class MainMenu(basicmenu.BasicMenu):
    '''
    @brief Clase que modela el comportamiento del menú principal del juego
    '''
    def __init__(self, game, path_xml):
        '''
        @brief Constructor
        
        @param game Referencia a game
        @param path_xml Ruta del archivo xml con las características del menú
        '''
        basicmenu.BasicMenu.__init__(self, game)
        
        #Cambiamos el titulo de la ventana
        pygame.display.set_caption("Zycars: Menú Principal")
        
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        #Le pasamos el archivo parseado a BasicMenu para que obtenga los elementos básicos
        self.parser_basic_info(parse)

    def draw(self, screen):
        '''
        @brief Método que dibuja todos los elementos en pantalla
        
        @param screen Superficie destino
        '''
        #Dibujamos todos los elementos basicos
        self.draw_basic_elements(screen)
        
        #Dibujamos el cursor
        self.cursor.draw(screen)
    
    def update(self):
        '''
        @brief Método que actualiza los elementos del menú
        '''
        #Comprobamos si el punto esta situado sobre algun botón
        self.actual_option = None
        for button in self.buttons:
            button.update()
            if button.get_selected():
                self.actual_option = button.get_option()
        
        #Si es asi cambiamos la imagen del cursor
        if self.actual_option:
            self.cursor.over()
            if pygame.mouse.get_pressed()[0]:
                self.treat_option()
        else:
            self.cursor.normal()
        
        #Actualizamos el cursor
        self.cursor.update()
            
    def treat_option(self):
        '''
        @brief Método que controla la opción elegida y que hacer según el caso.
        '''
        if self.actual_option == u"Carrera Rápida":
            print "Elegido: Carrera Rapida"
            self.game.change_state(charactermenu.CharacterMenu(self.game, 'menu/charactermenu.xml'))
        elif self.actual_option == "Campeonato":
            print "Elegido: Campeonato"
            self.game.change_state(charactermenu.CharacterMenu(self.game, 'menu/charactermenu.xml'))
        elif self.actual_option == "Contrarreloj":
            print "Ha elegido: Contrarreloj"
            self.game.change_state(charactermenu.CharacterMenu(self.game, 'menu/charactermenu.xml'))
        elif self.actual_option == "Opciones":
            print "Ha elegido: Opciones"
            self.game.change_state(optionmenu.OptionMenu(self.game, 'menu/optionmenu.xml'))
        elif self.actual_option == "Salir":
            print "Ha elegido: Salir"
            keyboard.set_quit(True)
