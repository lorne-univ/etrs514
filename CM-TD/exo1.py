#!/usr/bin/env python3

import os
import argparse
import logging


def init():
    logging.debug("Init not finished yet. Don't use")

def check():
    logging.debug("Check not finished yet. Don't use")

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser=argparse.ArgumentParser(prog="exo1", description="Programme de test et d'initialisation de l'exo1 lié au CM et TD")
    parser.add_argument("action", required=True,help="2 possible actions : check or init")
    args=parser.parse_args()
    action=vars(args)['action']
    if action=="init":
        init()
    elif action=="check":
        check()
    else:
        print("Argument must be init or check")
    
