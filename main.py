import winreg
import os
import requests
import subprocess

def download_file(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
def change_registry(path_to_reg):
    subprocess.run(['regedit', '/s', path_to_reg], check=True)
    os.remove(path_to_reg)
    
def game_launch(path_to_steam_exe, id_game):
    subprocess.run([path_to_steam_exe, '-applaunch', id_game])
    print('Игра запущена.')
        
def get_steam_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam")
        steam_path, type = winreg.QueryValueEx(key, "SteamPath")
        winreg.CloseKey(key)
        return steam_path
    except Exception as e:
        return None

def get_game_path(id_game):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App " + id_game)
        game_path, type = winreg.QueryValueEx(key, "InstallLocation")
        winreg.CloseKey(key)
        return game_path
    except Exception as e:
        return None

def main():
    id_game = '1568590'
    url_reg_file = (r'https://drive.usercontent.google.com/download?'
                    'id=1IGENwFzLm8bBEboISadYSNEdxbnjz1fH&export=download&authuser=0&confirm=t&'
                    'uuid=fec8066d-4c44-4d76-9d5d-907dc25fb6fc&at=APZUnTVoQeJneTkDbYM9CdJFPyTB%3A1721058416556')   
                    
    path_to_steam = get_steam_path()
    path_to_game = get_game_path(id_game)
    print("Путь до Steam:", path_to_steam)
    print("Путь до игры:", path_to_game)
    if path_to_steam:
        path_to_steam_exe = os.path.join(path_to_steam, 'steam.exe')
        if path_to_game:
            path_to_reg = os.path.join(path_to_game, 'settings.reg')
            download_file(url_reg_file, path_to_reg)
            change_registry(path_to_reg)
            game_launch(path_to_steam_exe, id_game)
        else:
            subprocess.run([os.path.join(path_to_steam, "steam.exe")])
            print('Путь к игре не был найден. Запускается Steam.')
    else:
        print("Путь к Steam не был найден в реестре.")
    
if __name__ == '__main__':
    main()