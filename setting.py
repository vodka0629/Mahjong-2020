#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/17 23:00
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: setting.py
# @Software: Mahjong II
# @Blog    :

class Setting(object):
    game_name = 'Chinese Standard Mahjong 2020'
    win_w = 1280
    win_h = 640
    win_w_h_half = (win_w - win_h) // 2  # difference between window's width and height
    FPS = 5
    cmd_FPS = 60

    # game rule
    game_flowers = True
    game_circles = 1
    game_start_coin = 500
    game_stop_at_broken = True
    game_player_name = '向明'
    game_opposites = ['貂蝉', '大乔', '小乔', '西施', '花木兰', '孙尚香', '甄姬', '王昭君', ]
    avatar_base = './resource/avatar/'

    # background music & image
    background_music = ['resource/background/music2.mp3', 'resource/background/avalon.mp3']
    background_img = 'resource/background.png'

    # images
    tile_img_path = './resource/tiles/64x64/'
    face_down_img = 'face-down.png'

    # distance and length
    concealed_left = 50
    concealed_bottom = 30

    exposed_left = 50
    exposed_bottom = 110

    discarded_left = 50
    discarded_bottom = 170
    discarded_step = 30
    discarded_line_limit = 6

    current_jump = 10  # current tile jump height

    flowers_left = 590  # flowers tiles from screen left side
    flower_line_limit = 10

    # sounds
    sound_base = './resource/sound/'

    sound_discard = 'discard.wav'
    sound_draw_stack = 'draw_stack.wav'

    sound_pong = 'pong.wav'
    sound_kong = 'kong.wav'
    sound_chow = 'chow.wav'

    sound_hu = 'girl_hu.wav'
    sound_self_hu = 'girl_self_hu.wav'

    girl_sound = {
        'girl_hu': 'girl_hu.wav',
        'girl_self_hu': 'girl_self_hu.wav',
        'player_fire': 'player_fire.wav',
        'player_win': 'player_win.wav',
        'withdraw': 'withdraw.wav',
    }

    # info pad
    font = './resource/font/cloud2.ttf'
    small_font_size = 15
    normal_font_size = 20
    big_font_size = 30
    huge_font_size = 40
    info_color = (255, 205, 66)
    position_color = (255, 250, 227)

    # sprites
    sprite_base = './resource/sprites/'
    waiting_img = {
        'chow': 'chow.png',
        'pong': 'pong.png',
        'kong': 'kong.png',
        'listen': 'listen.png',
        'cancel': 'cancel.png',
        'hu': 'hu.png',
        'ignore': 'ignore.png',
    }
    waiting_img_span = 10
    girl_img = {
        'win': 'girl_win.png',
        'lose': 'girl_lose.png',
        'start': 'girl_start.png',
        'draw': 'girl_draw.png',
    }
    girl_start_left = 0
    girl_end_left = 50
    girl_top = 50
    btn_img = {
        'start': 'btn_start.png',
        'end': 'btn_end.png',
    }

    # hand name
    hand_name_left = 100
    hand_name_top = 3
    player_name_span = 30

    # score board
    score_board_girl_left = -20
    score_board_girl_top = 50

    score_board_flower_left = 0
    score_board_flower_y_span = 10

    score_board_left = 300
    score_board_bottom = 300

    score_board_score_y_span = 50
    score_board_score_x_span = 150
    score_board_score_width = 250

    score_board_concealed_left = 300
    score_board_concealed_bottom = 100

    score_board_exposed_left = 300
    score_board_exposed_bottom = 200
    score_board_exposed_x_span = 42

    score_board_player_left = 300
    score_board_player_bottom = 20
    score_board_player_y_span = 30
    score_board_player_x_span = 100

    # end screen
    end_left = 'left_corner.png'
    end_right = 'right_corner.png'
    history = 'history.json'
    history_left = 200
    history_right = 100
    history_top = 200
    history_y_span = 40

    end_top = 50
