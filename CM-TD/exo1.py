#!/usr/bin/env python3

import os
import argparse
import logging
import subprocess
import signal
import shutil
import difflib
from pprint import pprint

colors = {"red": "\033[31m", "green": "\033[32m", "reset": "\033[0m"}


def delete_history():
    """
    Delete .bash_history file and execute history -c
    Ca nécessite de fermer la session et de la réouvrir
    """
    print(
        "***Cette fonction va fermer automatiquement votre session ssh***\nRéouvrir une session ssh après son exécution"
    )
    home_directory = os.path.expanduser("~")
    history_path = os.path.join(home_directory, ".bash_history")
    if os.path.isfile(history_path):
        os.remove(history_path)
    subprocess.run(["history", "-c"], shell=True)
    os.kill(os.getppid(), signal.SIGHUP)


def init():
    logging.debug("Init not finished yet. Don't use")
    delete_history()
    home_directory = os.path.expanduser("~")
    path = os.path.join(home_directory, "exercice1")
    shutil.rmtree(path)
    path = os.path.join(home_directory, "exercice1_b.txt")
    if os.path.isfile(path):
        os.remove(path)


def compare_two_text(text1, text2):
    """
    Give two text and compare them
    """
    text1 = text1.splitlines(keepends=False)
    text2 = text2.splitlines(keepends=False)
    differ = difflib.Differ()
    diff = list(differ.compare(text1, text2))
    same_text = True
    for line in diff:
        if line[0] != " ":
            same_text = False
            pprint(diff)
            break
    return same_text


def check_content_of_file(file_path, expected_content):
    if os.path.exists(file_path):
        print(f"{colors.get('green')} {file_path} -> found {colors['reset']}")
        with open(file_path, "r") as file:
            read_content = file.read()
            logging.debug(
                "File {}\nExpected content: {}\nRead content: {}".format(
                    file_path, expected_content, read_content
                )
            )

            if compare_two_text(expected_content, read_content):
                print(
                    f"{colors['green']} content of {file_path} -> OK {colors['reset']}"
                )
            else:
                print(f"{colors['red']} content of {file_path} -> KO {colors['reset']}")
    else:
        print(f"{colors['red']} {file_path} -> not found {colors['reset']}")


def check():
    logging.debug("Check not finished yet. Don't use")
    # Check exercice1_a.txt
    folder = "/home/etudiant/exercice1"
    file1 = "exercice1_a.txt"
    file2 = "exercice1-b.txt"
    expected_content_file1 = """Premier test de création de fichier\n"""
    expected_content_file2 = """Deuxième test de création de fichier.
    Utilisation d'un éditeur.
    C'est moins rapide mais ça fonctionne aussi."""
    if os.path.exists(folder):
        print(f"{colors['green']} {folder} -> found {colors['reset']}")
        file_path = os.path.join(folder, file1)
        check_content_of_file(
            file_path=file_path, expected_content=expected_content_file1
        )
        file_path = os.path.join(folder, file2)
        check_content_of_file(
            file_path=file_path, expected_content=expected_content_file1
        )
    else:
        print(f"{colors['red']} {folder} -> not found {colors['reset']}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        prog="exo1",
        description="Programme de test et d'initialisation de l'exo1 lié au CM et TD",
    )
    parser.add_argument(
        "action", choices=["init", "check"], help="2 possible actions : check or init"
    )
    args = parser.parse_args()
    action = vars(args)["action"]
    if action == "init":
        init()
    elif action == "check":
        check()
