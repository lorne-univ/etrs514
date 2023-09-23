#!/usr/bin/env python3

import os
import argparse
import logging
import subprocess
import signal
import shutil
import difflib


colors = {"red": "\033[31m", "green": "\033[32m", "reset": "\033[0m"}


def print_red(string):
    """
    print in red
    string : string to print

    """
    print(f"{colors['red']}{string}{colors['reset']}")


def print_green(string):
    """
    print in green
    string : string to print

    """
    print(f"{colors['green']}{string}{colors['reset']}")


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
    # delete_history()
    home_directory = os.path.expanduser("~")
    path = os.path.join(home_directory, "exercice1")
    if os.path.exists(path):
        shutil.rmtree(path)
    path = os.path.join(home_directory, "exercice1_b.txt")
    if os.path.isfile(path):
        os.remove(path)


def compare_two_text(text1, text2):
    """
    Give two text and compare them
    Return : {"same_text":same_text,"diff":diff}
    same_text : Boolean
    diff : differences between text
    """
    text1 = text1.splitlines(keepends=False)
    text2 = text2.splitlines(keepends=False)
    differ = difflib.Differ()
    diff = differ.compare(text1, text2)
    diff_list = list(diff)
    logging.debug("Diff_list : {}".format(diff_list))
    same_text = True
    for i, line in enumerate(diff_list):
        if line[0:1] != " ":
            try:
                text1_line = text1[i]
            except IndexError:
                text1_line = ""
            try:
                text2_line = text2[i]
            except IndexError:
                text2_line = ""
            diff = f"Line {i} are not the same : {text1_line}  {text2_line}"
            same_text = False

            break
    return {"same_text": same_text, "diff": diff}


def check_content_of_file(file_path, expected_content):
    if os.path.exists(file_path):
        print_green(f"{file_path} -> found")
        with open(file_path, "r") as file:
            read_content = file.read()
            logging.debug(
                "File {}\nExpected content: {}\nRead content: {}".format(
                    file_path, expected_content, read_content
                )
            )
            comparison = compare_two_text(expected_content, read_content)
            if comparison["same_text"]:
                print_green(f"Content of {file_path} -> OK")
            else:
                print_red(f"Content of {file_path} -> KO")
                print(
                    f"Diff between expected and read content of {file_path} :\n{comparison.get('diff', '')}"
                )

    else:
        print_red(f"{file_path} -> not found")


def create_expected_content_file3():
    """
    file3 is a copy of file2 that also contains 31 lines numeroted
    """
    expected_content_file3 = """Deuxième test de création de fichier.\nUtilisation d'un éditeur.\nC'est moins rapide mais ça fonctionne aussi.\n"""
    for i in range(1, 32):
        expected_content_file3 = expected_content_file3 + f"Line number {i+2}\n"
    return expected_content_file3


def check():
    # Check exercice1_a.txt
    folder = "/home/etudiant/exercice1"
    file1 = "exercice1_a.txt"
    file2 = "exercice1_b.txt"
    expected_content_file1 = """Premier test de création de fichier.\n"""
    expected_content_file2 = """Deuxième test de création de fichier.\nUtilisation d'un éditeur.\nC'est moins rapide mais ça fonctionne aussi."""
    if os.path.exists(folder):
        print_green(f"{folder} -> found")
        file_path = os.path.join(folder, file1)
        # Test file1 content
        check_content_of_file(
            file_path=file_path, expected_content=expected_content_file1
        )
        file_path = os.path.join(folder, file2)
        # Test file2 content
        check_content_of_file(
            file_path=file_path, expected_content=expected_content_file2
        )
    else:
        os.access(
            "/home/etudiant/exercice1/exo1.sh",
        )
        print(f"{colors['red']} {folder} -> not found {colors['reset']}")
    # Check bash script
    file_path = "/home/etudiant/exercice1/exo1.sh"
    if os.path.exists(file_path):
        print_green(f"{file_path} -> found")
        if os.access(file_path, os.X_OK):
            print_green(f"Execution access on {file_path} is OK")
        else:
            print_red(f"Execution access on {file_path} isn't set")
    else:
        print_red(f"{file_path} -> not found")

    # Check copy of file : there are two files with the same name {file2} but not in the same directory
    check_content_of_file(f"/home/etudiant/{file2}", create_expected_content_file3())


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # logging.info(
    #     "{}PROGRAM not finished yet. Don't use !!!{}".format(
    #         colors["red"], colors["reset"]
    #     )
    # )
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
    # print(create_expected_content_file3())
