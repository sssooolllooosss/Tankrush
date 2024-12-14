import pygame
import sys
import os
from intro import play_intro
from main import play_main
from select_pvp import select_pvp
from select_pve import select_pve
from pvp import play_pvp

def main():
    pygame.init()
    pygame.mixer.init()
    
    pygame.mixer.music.load(os.path.join('sound', 'intro.mp3'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    
    while True:
        intro_result = play_intro()
        if intro_result == "quit":
            break
            
        selected_mode = play_main()
        if selected_mode == "quit":
            break
            
        pygame.mixer.music.stop()
            
        if selected_mode == "PVP":
            num_players, selected_chars = select_pvp()
            if num_players is None:
                pygame.mixer.music.play(-1)
                continue
            
            result = play_pvp(num_players, selected_chars)
            if result == "MAIN":
                pygame.mixer.music.play(-1)
                continue
                
        elif selected_mode == "PVE":
            num_players, selected_chars = select_pve()
            if num_players is None:
                pygame.mixer.music.play(-1)
                continue
                
            break
        else:
            break

    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
