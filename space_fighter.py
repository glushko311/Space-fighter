#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

from pygame.locals import *

pygame.font.init()#инициализация шрифтов

#Размеры окна 600х600
a = 600
b = 600
info_string_width = 50
#Размеры окна 600х600


#Ширина строки состояния
info_string_width=50
#Ширина строки состояния
#Стартовый уровень и здоровье врага
level = 1
enemy_health = 10
#Стартовый уровень и здоровье врага

#Создание окна, название, поверхность, шрифт
window = pygame.display.set_mode((a,b+info_string_width))
pygame.display.set_caption('SPACE FIGHTER')
screen = pygame.Surface((a,b))





#Функция включающая игровой цикл
def start_game(enemy_health, level, score_glob):
    pygame.mixer.init()
    score=score_glob

    #Размеры героя и цели 40х40
    a2 = 46
    b2 = 40
    #Размеры героя и цели 40х40

    #Переменные для движения объектов по экрану
    h=a/3 #высота дозволенного перемещения героя по oY
    strela_width=11 #ширина стрелы (высота стрелы равна 40!)
    strela_speed=5  #скорость движения стрелы
    increase_speed_x=0.2 #приращение к скорости движения цели при попадании
    increase_speed_y=0.2
    #Переменная для выхода из бесконечного цикла
    done = True
    x_speed = 2 #скорость движения цели по оХ
    y_speed = 0 #скорость движения цели по оУ
    #Переменные для движения объекта по экрану
    total_delay = 5
    hero_speed = 10
    zet_fire_speed = 8
    zet_fire1_width = 20
    zet_hit = 10
    area_multiplyer = 1.1
    #Переменные для движения объектов по экрану
    #--------------------------------------------------------------------

    #Создание окна 600х600
    window = pygame.display.set_mode((a,b+info_string_width))
    pygame.display.set_caption('SPACE FIGHTER')
    screen = pygame.Surface((a,b))
    #Создание окна 600х600

    #Создание инфо строки
    info_string = pygame.Surface((a,info_string_width))
    #Создание инфо строки

    #Создание звуковых объектов
    fire_z = pygame.mixer.Sound('data/fire_z1.wav')
    fire_h = pygame.mixer.Sound('data/fire_h.wav')
    bang = pygame.mixer.Sound('data/bang.wav')
    hit = pygame.mixer.Sound('data/hit.wav')
    music = pygame.mixer.Sound('data/diego_modena.wav')
    pygame.mixer.Sound.play(music,-1)
    #Создание звуковых объектов

    #Создание шрифтов

    zet_font = pygame.font.SysFont('Purisa', 24, True, True)
    hero_font = pygame.font.SysFont('Purisa', 24, True, True)
    game_over_font = pygame.font.SysFont('Pursia',60, True, False)
    you_win_font = pygame.font.SysFont('Pursia', 60, True, False)

    #Создание шрифтов

    #Создание класса героев и целей
    class Sprite:
        def __init__(self, xpos, ypos, filename):
            self.x = xpos
            self.y = ypos
            self.bitmap = pygame.image.load(filename)
            self.bitmap.set_colorkey((0,0,0))#Чёрный фон не будет отрисовываться!
        def render(self):
            #Отрисовка объекта
            screen.blit(self.bitmap, (self.x,self.y))
    #Создание класса героев и целей

        
    field = Sprite(0, 0, 'data/field_space.png')#Создание красивого игрового поля(картинка)

    zet = Sprite(10, 10, 'data/zet.png')#Создание цели
    zet.go_right=True
    zet.go_down = True
    zet.health = enemy_health
    zet.destroyed = False

    #Создание выстрела цели
    zet_fire1 = Sprite(-100,-100,'data/zet_fire.png')
    zet_fire1.push = False

    zet_fire2 = Sprite(-100,-100,'data/zet_fire.png')
    zet_fire2.push = False

    hero = Sprite(200, b-50, 'data/ship.png')#Создание героя
    hero.health = 10
    hero.destroyed = False

    strela = Sprite(-100,-100,'data/bolt.png')#создание выстрела героя
    strela.push = False

    #button_play_again = Sprite(-500,-500,'replay.png')#Создание кнопки реплей



    def intersect(x1,x2,y1,y2,db1,db2):
        #Если объёкты пересекаются вернёт True иначе False

        #В качестве аргументов принимает координаты двух объектов и их ширина
        #db1 - ширина первого объекта(стрела) db2 - ширина второго объекта(цель)
        if (x1 > x2-db1) and (x1 < x2+db2) and (y1 > y2-db1) and (y1 < y2+db2):
            return 1
        else:
            return 0
    pygame.key.set_repeat(2,1)#Дублирует нажатие при зажатой кнопке
    #2-задержка перед первым дублированием мс
    #1-задержка перед последующими дублированиями мс


    
    while done:

    #Цикл обработки событий
        for event in pygame.event.get():
                #Обработка события выход
            if event.type == pygame.QUIT:
                    exit()
                #Обработка события выход
            
                #Обработчик перемещение героя с клавиатуры
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if hero.x>10:
                        hero.x-=hero_speed
                if event.key == pygame.K_RIGHT:
                    if hero.x<a-a2-10:
                        hero.x+=hero_speed
                if event.key == pygame.K_UP:
                    if hero.y>b-h-b2:
                        hero.y-=hero_speed
                if event.key == pygame.K_DOWN:
                    if hero.y<b-b2-5:
                        hero.y+=hero_speed
                if event.key == pygame.K_p:
                    pause_game()
                    #Обработчик перемещение героя с клавиатуры
                    #Обработчик запуска стрелы        
                if event.key == pygame.K_SPACE:
                        if strela.push == False:
                            pygame.mixer.Sound.play(fire_h)
                            strela.x = hero.x+15
                            strela.y = hero.y
                            strela.push = True
                            score-=3

                    #Обработчик запуска стрелы
                #Обработчик движения мыши(перемещение героя)
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(False)
                m = pygame.mouse.get_pos()
                if m[0]< a-a2-10 and m[0] > 10:
                    hero.x = m[0]
                if m[1] < b-b2-5 and m[1] > b-h-b2:
                    hero.y = m[1] 
                #Обработчик движения мыши(перемещение героя)
                #Обработчик запуска стрелы мышью(левая кнопка)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button ==1:
                    if strela.push == False:
                        pygame.mixer.Sound.play(fire_h)
                        strela.x=hero.x+15
                        strela.y=hero.y
                        strela.push = True
                        score-=3
                        

                #Обработчик запуска стрелы мышью(левая кнопка)      
                    
        #Цикл обработки событий
            #Описание поведения ответного выстрела цели (прицельный выстрел)            
        if zet.x<hero.x+5 and zet.x>hero.x-5 and zet_fire1.push == False:
            zet_fire1.push=True
            pygame.mixer.Sound.play(fire_z) #Звук выстрела
            zet_fire1.x=zet.x
            zet_fire1.y=zet.y
        if zet_fire1.push:
            zet_fire1.y+=zet_fire_speed
            if zet_fire1.y >a:
                zet_fire1.x=-100
                zet_fire1.y=-100
                zet_fire1.push=False
        
        if intersect(zet_fire1.x, hero.x, zet_fire1.y, hero.y, zet_fire1_width, a2):
            zet_fire1.x=-100
            zet_fire1.y=-100
            zet_fire1.push=False
            hero.health-=2
            score-=zet_hit
            pygame.mixer.Sound.play(hit)

        #Описание поведения ответного выстрела цели (прицельный выстрел)         


            #Описание поведения ответного выстрела цели (случайный выстрел)            
        if zet_fire2.push == False:
            zet_fire2.push=True
            zet_fire2.x=zet.x
            zet_fire2.y=zet.y
            pygame.mixer.Sound.play(fire_z)
        if zet_fire2.push:
            zet_fire2.y+=zet_fire_speed
        if zet_fire2.y >a:
            zet_fire2.x=-100
            zet_fire2.y=-100
            zet_fire2.push=False
        
        if intersect(zet_fire2.x, hero.x, zet_fire2.y, hero.y, zet_fire1_width, a2):
            zet_fire2.x=-100
            zet_fire2.y=-100
            zet_fire2.push=False
            score-=zet_hit
            hero.health-=2
            pygame.mixer.Sound.play(hit)

            #Описание поведения ответного выстрела цели (случайный выстрел)
                    

        #Движение объёкта zet - цель по оси oX
        if zet.go_right:
            zet.x+=x_speed
            if zet.x>a-a2:
                zet.go_right = False
                #Поворот героя примитивная анимация
                zet.bitmap=pygame.image.load('data/zet.png')
                zet.bitmap.set_colorkey((0,0,0))#отмена отрисовки черного в zet_left.png
        else:
            zet.x -= x_speed 
            if zet.x < 0:
                zet.go_right = True
                    #Поворот героя примитивная анимация
                zet.bitmap=pygame.image.load('data/zet.png')
                zet.bitmap.set_colorkey((0,0,0))#отмена отрисовки черного в zet_left
        #Движение объёкта zet - цель по оси oX
    
        #Движение объекта zet - цель по оси oY
        if zet.go_down:
            zet.y+=y_speed
            if zet.y>b-b2-b/area_multiplyer:
                zet.go_down=False
        else:
            zet.y-=y_speed
            if zet.y<0:
                zet.go_down = True
            
        #Движение объекта zet - цель по оси oY
        #Проверка попадания стрелы
        if intersect(strela.x, zet.x, strela.y, zet.y, strela_width, a2):
            x_speed+=increase_speed_x
            y_speed+=increase_speed_y
            score+=x_speed*5
            zet.health-=2     
            strela.push=False
            strela.x=-100
            strela.y=-100
            area_multiplyer+=0.5
            pygame.mixer.Sound.play(hit)
        #Проверка попадания стрелы
        #Проверка столкновения корабля и цели
        if intersect(hero.x, zet.x, hero.y, zet.y, a2, a2):
            hero.bitmap=pygame.image.load('data/bang3.png')
            hero.bitmap.set_colorkey((0,0,0))
            hero.health=0
            zet.health=0
            zet.bitmap=pygame.image.load('data/bang3.png')
            zet.bitmap.set_colorkey((0,0,0))
            pygame.mixer.Sound.play(bang)
    #Проверка столкновения корабля и цели   
        if strela.push:
            if strela.y < 0:            
                strela.x=-100
                strela.y=-100
                strela.push = False
            else:
                strela.y-=strela_speed
        #Движение объекта zet - цель по оси oY
            
        #Проверка победы или поражения
        if hero.health<=0:
            hero.bitmap=pygame.image.load('data/bang3.png')
            hero.bitmap.set_colorkey((0,0,0))
            done=False
            pygame.mixer.Sound.play(bang)

        if zet.health<=0:
            zet.bitmap=pygame.image.load('data/bang3.png')
            zet.bitmap.set_colorkey((0,0,0))
            done=False
            pygame.mixer.Sound.play(bang)
        #Проверка победы или поражения

        #Циклическая отрисовка экрана героя и цели
        pygame.time.delay(total_delay)
        screen.fill((50,50,50 )) #Цвет фона - серый
        info_string.fill((21,126,41))
    
        #Отрисовка героя и цели

        field.render()
        zet.render()
        hero.render()
        strela.render()
        zet_fire1.render()
        zet_fire2.render()

        #Отрисовка героя и цели

        #Отрисовка шрифтов
        info_string.blit(hero_font.render('ship armour: '+str(hero.health),3,(0,0,0)), (10,10))
        info_string.blit(zet_font.render('enemy armor: '+str(zet.health),3,(0,0,0)), (350,10))

        #Отрисовка шрифтов
    
        #Отрисовка холста
        window.blit(screen, (0,0))
        window.blit(info_string, (0,b))
        pygame.display.flip()
    if hero.health==0:
        window.blit(game_over_font.render('GAME OVER',3,(0,0,0)),(160,310))
        window.blit(game_over_font.render('your score is  '+ str(int(score)),3,(0,0,0)),(105,350))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.mixer.quit()#окончание работы со звуком
        pygame.time.delay(5000)
        menu()       
    else:
        window.blit(game_over_font.render('YOU WIN!',3,(0,0,0)),(180,310))
        pygame.display.flip()
        pygame.time.delay(2000)
        level+=1
        enemy_health+=5
        score+=10
        show_level(level,score)
        pygame.time.delay(2000)
        pygame.mixer.quit()#окончание работы со звуком
        start_game(enemy_health, level, score)

# Функция с игровым циклом        
        
#Создание функции меню
def menu():
    mini_menu = pygame.font.SysFont('Pursia', 40, False, True)
    while 1:
        screen.fill((50,50,50 ))
        screen.blit(mini_menu.render('Push SPACEBAR to start game.',3,(255,0,0)), (80,220))
        screen.blit(mini_menu.render('Push ESC to quit',3,(255,0,0)), (80,250))
        window.blit(screen, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game(6, 1, 0)
                if event.key == pygame.K_ESCAPE:
                    pygame.font.quit()#окончание работы со шрифтами
                    pygame.mixer.quit()#окончание работы со звуком
                    exit()
def show_level(level, score):
    screen.fill((50,50,50 ))
    mini_menu = pygame.font.SysFont('Pursia', 60, False, True)
    show_score = pygame.font.SysFont('Pursia', 30, False, True)
    screen.blit(mini_menu.render('Level '+ str(level),3,(0,150,0)), (210,250))
    screen.blit(show_score.render('your score is  '+ str(int(score)),3,(0,150,0)), (210,300))                                 
    window.blit(screen, (0,0))
    pygame.display.flip()           
def show_results():
    pass

def pause_game():
    done = True
    while done:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        done = False
        
        

menu() #Запуск стартового меню






