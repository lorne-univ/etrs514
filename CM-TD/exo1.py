#!/usr/bin/env python3

import os
import argparse
import logging
import subprocess
import signal
import shutil

colors= {'red':"\033[31m", 'green':"\033[32m", 'reset':"\033[0m"}



def delete_history():
    '''
    Delete .bash_history file and execute history -c
    Ca nécessite de fermer la session et de la réouvrir
    '''
    print ("***Cette fonction va fermer automatiquement votre session ssh***\nRéouvrir une session ssh après son exécution")
    home_directory=os.path.expanduser("~")
    history_path=os.path.join(home_directory,".bash_history")
    if os.path.isfile(history_path):
        os.remove(history_path)
    subprocess.run(["history","-c"],shell=True)
    os.kill(os.getppid(),signal.SIGHUP)
    
    

def init():
    logging.debug("Init not finished yet. Don't use")
    delete_history()
    home_directory=os.path.expanduser("~")
    path=os.path.join(home_directory,"exercice1")
    shutil.rmtree(path)
    path=os.path.join(home_directory,"exercice1_b.txt")
    if os.path.isfile(path):
        os.remove(path)


def check():
    logging.debug("Check not finished yet. Don't use")
    #Check exercice1_a.txt
    folder = "/home/etudiant/exercice1"
    file = "exercice1_a.txt"
    expected_content = "Premier test de création de fichier"
    if os.path.exists(folder):
        print(f"{colors['green']} {folder} -> found {colors['reset']}")
        if path:=os.path.exists(os.path.join(folder,file)):
            print(f"{colors.get('green')} {file} -> OK {colors['reset']}")
            with open(path,"r") as file:
                content=file.read()
                if content==expected_content:
                    print(f"{colors['green']} content of {file} -> OK {colors['reset']}")
                else:
                    print(f"{colors['red']} content of {file} -> KO {colors['reset']}")
        else:
            print(f"{colors['red']} {file} -> not found {colors['reset']}")
    else:
        print(f"{colors['red']} {folder} -> not found {colors['reset']}")

if __name__=="__main__":

    logging.basicConfig(level=logging.DEBUG)
    parser=argparse.ArgumentParser(prog="exo1", description="Programme de test et d'initialisation de l'exo1 lié au CM et TD")
    parser.add_argument("action", choices=["init","check"], help="2 possible actions : check or init")
    args=parser.parse_args()
    action=vars(args)['action']
    if action=="init":
        init()
    elif action=="check":
        check()

    
