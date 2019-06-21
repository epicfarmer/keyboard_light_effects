import NoEffect as ne
import FlashEffect as fe
import CrashEffect as cre
import CircleEffect as cie
import DictionaryEffect as de
import FadeMarquisEffect as fme

testing_keymap = {
        61:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(0,0,0)} },
        62:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(255,0,0)} },
        63:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(0,255,0)} },
        64:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(0,0,255)} },
        65:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(255,255,0)} },
        66:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(255,0,255)} },
        67:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(0,255,255)} },
        68:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(255,255,255)} },
        69:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(124,0,0)} },
        70:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(0,124,0)} },
        71:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(0,0,124)} },
        72:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(124,255,0)} },
        73:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(255,124,0)} },
        74:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(124,124,0)} },
        75:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(124,0,255)} },
        76:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(255,0,124)} },
        77:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(124,0,124)} },
        78:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(0,124,255)} },
        79:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(0,255,124)} },
        80:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(0,124,124)} },
        81:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(124,124,124)} },
        82:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(124,255,124)} },
        83:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(124,124,255)} },
        84:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(124,255,255)} },
        85:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(255,124,124)} },
        86:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(255,255,124)} },
        87:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(255,124,255)} },
        88:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(255,255,255)} }
        }

global_mode_keymap = {
        0:{"song":"next"},
        60:{"mode":0},
        61:{"mode":1},
        62:{"mode":2},
        63:{"mode":3},
        64:{"mode":4},
        65:{"mode":5},
        66:{"mode":6},
        67:{"mode":7},
        68:{"mode":8},
        69:{"mode":9},
        70:{"mode":10},
        71:{"mode":11},
        72:{"mode":12},
        73:{"mode":13},
        74:{"mode":14},
        75:{"mode":15},
        76:{"mode":16},
        77:{"mode":17},
        78:{"mode":18},
        79:{"mode":19},
        80:{"mode":20},
        }


## debug_global_mode
keymap_0 = {
        89:{"effect":de.DictionaryEffect, "args":{"state":"11000000000000000000000000000011","on_color":(255,0,255)} },
        87:{"effect":de.DictionaryEffect, "args":{"state":"0011000000000000000000000000110O","on_color":(255,0,255)} },
        82:{"effect":de.DictionaryEffect, "args":{"state":"0000111000000000000000000111000O","on_color":(255,0,255)} },
        81:{"effect":de.DictionaryEffect, "args":{"state":"0000000110000000000000011000000O","on_color":(255,0,255)} },
        71:{"effect":de.DictionaryEffect, "args":{"state":"0000000001110000000011100000000O","on_color":(255,0,255)} },
        67:{"effect":de.DictionaryEffect, "args":{"state":"0000000000001100001100000000000O","on_color":(255,0,255)} },
        69:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(250,250,250)} }
        }

keymap_1 = {
        72:{"effect":de.DictionaryEffect, "args":{"state":"00001111111100000000111111110000"} },
        80:{"effect":de.DictionaryEffect, "args":{"state":"11111111000000001111111100000000"} },
        68:{"effect":de.DictionaryEffect, "args":{"state":"00000000111111110000000011111111"} },
        77:{"effect":de.DictionaryEffect, "args":{"state":"11110000000011111111000000001111"} },
        79:{
            "effect":fme.FadeMarquisEffect,
            "args":{
                "transition_time" : 3.5,
                "color1" : (155,255,155),
                "color2" : (0,0,0)
                }
            }
        }

keymap_2 = {
        98:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"01000000000000100000100000100010",
                "on_color":(0,125,0)
                }
            },
        97:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"01000100000100100010100010100010",
                "on_color":(0,110,50)
                }
            },
        94:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"11010100001100100010100110101010",
                "on_color":(0,100,80)
                }
            },
        84:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"11010101001100101110100110101110",
                "on_color":(0,80,100)
                }
            },
        83:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"11011101101110101110101110111110",
                "on_color":(0,50,110)
                }
            },
        82:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"11011111101110111110111111111110",
                "on_color":(0,0,125)
                }
            },
        72:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"11111111111111111111111111111111",
                "on_color":(255,0,0)
                }
            }
        }

keymap_3 = {
        69:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"10000000000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        74:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"01000000000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        79:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00100000000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        82:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00010000000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        80:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00001000000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        85:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00000100000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        65:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00000010000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        68:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00000001000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        87:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00000000100000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        59:{
            "effect":fe.FlashEffect,
            "args":{
                "state":"00000000100000000000000000000000",
                "on_color":(125,125,0)
                }
            },
        50:{
            "effect":fe.FlashEffect,
            "args":{
                "state":"00000000100000000000000000000000",
                "on_color":(0,125,125)
                }
            },
        }

keymap_4 = {
        }

keymap_5 = {
        "86": {
            "effect":cre.CrashEffect,
            "args":{
                "state":"00000000100000000000000000000000",
                "on_color":(0,125,125)
                }
            }
        }

keymap_6 = {

        }

keymap_7 = {

        }

keymap_8 = {

        }

keymap_9 = {

        }

key_maps_by_mode = [
        keymap_0, # 0
        keymap_1, # 1
        keymap_2, # 2
        keymap_0, # 3
        keymap_3, # 4
        keymap_4, # 5
        keymap_0, # 6
        keymap_3, # 7
        keymap_9, # 8  # 3 pulses of clusters of notes
        keymap_5, # 9  #
        keymap_6, # 10
        keymap_0, # 11
        keymap_3, # 12
        keymap_7, # 13 # Modified for synth
        keymap_8, # 14 # Modified for synth
        keymap_8, # 15 # Modified for synth
        ];

key_maps_by_mode_clock_song = [
        keymap_0, # 0
        keymap_1, # 1
        keymap_2, # 2
        keymap_0, # 3
        keymap_3, # 4
        keymap_4, # 5
        keymap_0, # 6
        keymap_3, # 7
        keymap_9, # 8  # 3 pulses of clusters of notes
        keymap_5, # 9  #
        keymap_6, # 10
        keymap_0, # 11
        keymap_3, # 12
        keymap_7, # 13 # Modified for synth
        keymap_8, # 14 # Modified for synth
        keymap_8, # 15 # Modified for synth
   ];

key_maps_by_mode_black_hole = [
        keymap_0, # 0
    ];

key_maps_by_mode_testing = [
        testing_keymap
    ];

key_map_arrays_by_song = [
        key_maps_by_mode_clock_song,
        key_maps_by_mode_black_hole,
        key_maps_by_mode_testing
    ];

