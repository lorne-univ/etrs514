#!/usr/bin/env python3

import os
import argparse
import logging
import subprocess
import signal


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

def check():
    logging.debug("Check not finished yet. Don't use")

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

    
