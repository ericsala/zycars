#-*- encoding: utf-8 -*-

import data
import keyboard
import pygame
import basicmenu
import optionmenu
import charactermenu
import xml.dom.minidom
import config

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
            
    def treat_option(self, option):
        '''
        @brief Método que controla la opción elegida y que hacer según el caso.
        '''
        if option == u"Carrera Rápida":
            print "Elegido: Carrera Rapida"
            config.Config().set_mode(config.FASTRACE)
            self.game.change_state(charactermenu.CharacterMenu(self.game, 'menu/charactermenu.xml'))
            
        elif option == "Campeonato":
            print "Elegido: Campeonato"
            config.Config().set_mode(config.CHAMPIONSHIP)
            self.game.change_state(charactermenu.CharacterMenu(self.game, 'menu/charactermenu.xml'))
            
        elif option == "Contrarreloj":
            print "Ha elegido: Contrarreloj"
            config.Config().set_mode(config.TIMED)
            self.game.change_state(charactermenu.CharacterMenu(self.game, 'menu/charactermenu.xml'))
            
        elif option == "Opciones":
            print "Ha elegido: Opciones"
            self.game.change_state(optionmenu.OptionMenu(self.game, 'menu/optionmenu.xml'))
        
        elif option == u'Créditos':
            print "Ha elegido: Créditos"
            self.game.change_state(CreditsMenu(self.game, 'menu/creditsmenu.xml'))

        elif option == "Salir":
            print "Ha elegido: Salir"
            keyboard.set_quit(True)

class CreditsMenu(basicmenu.BasicMenu):
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

        self.developer = self.font.render('Desarrollador', True, (0,0,0))
        self.developer_name = self.font.render(u'José J. Marente Florín', True, (189, 9, 38))
        self.artist = self.font.render(u'Diseñador gráfico', True, (0,0,0))
        self.artist_name = self.font.render(u'David Nieto Rojas', True, (189, 9, 38))
        self.music = self.font.render(u'Música', True, (0,0,0))
        self.music_name1 = self.font.render(u'Bob Wizman', True, (189, 9, 38))
        self.music_name2 = self.font.render(u'Pirato Ketchup', True, (189, 9, 38))
        self.music_name3 = self.font.render(u'Los Cadaver', True, (189, 9, 38))
        self.music_name4 = self.font.render(u'The Wavers', True, (189, 9, 38))

    def draw(self, screen):
        '''
        @brief Método que dibuja todos los elementos en pantalla
        
        @param screen Superficie destino
        '''
        #Dibujamos todos los elementos basicos
        self.draw_basic_elements(screen)
        
        screen.blit(self.developer, (20, 200))
        screen.blit(self.developer_name, (280, 200))
        screen.blit(self.artist, (20, 280))
        screen.blit(self.artist_name, (280, 280))
        screen.blit(self.music, (20, 360))
        screen.blit(self.music_name1, (280, 360))
        screen.blit(self.music_name2, (280, 390))
        screen.blit(self.music_name3, (280, 420))
        screen.blit(self.music_name4, (280, 450))
        
        #Dibujamos el cursor
        self.cursor.draw(screen)

    def treat_option(self, option):
        '''
        @brief Método que controla la opción elegida y que hacer según el caso.
        '''
        if option == u"Volver":
            self.game.change_state(MainMenu(self.game, 'menu/mainmenu.xml'))
            
