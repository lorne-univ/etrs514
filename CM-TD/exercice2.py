#!/usr/bin/env python3

import os
import argparse
import logging
import subprocess
import signal
import shutil
import difflib
import sys
import pwd
import spwd


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
    pass


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


def check_user_exists(user_name):
    """
    This check the existence of the user in the /etc/passwd
    """
    try:
        pwd.getpwnam(user_name)
    except KeyError:
        print_red(f"{user_name} doesn't exists")
        exit(1)
    print_green(f"{user_name} exists")


def check_user_password_set(user_name):
    try:
        shadow_password = spwd.getspnam(user_name).sp_pwdp
        logging.debug("{}".format(shadow_password))
    except PermissionError:
        print_red("The program exerice2.py must be started as root. use sudo")
        exit(1)
    except KeyError:
        print_red(f"no password found for {user_name}")
        exit(1)
    if shadow_password != "!!":
        print_green(f"{user_name} has a password")
    else:
        print_red(f"no password found for {user_name}")
        exit(1)


def check_step1():
    """
    Check if user1 exists
    """
    check_user_exists("user1")
    check_user_password_set("user1")


def check_step2():
    pass


def check_step3():
    logging.debug("3")


def check_all():
    logging.debug("all")


def check(step):
    steps = {
        "step1": check_step1,
        "step2": check_step2,
        "step3": check_step3,
        "all": check_all,
    }
    steps.get(step, check_all)()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info(
        "{}PROGRAM not finished yet. Don't use !!!{}".format(
            colors["red"], colors["reset"]
        )
    )
    parser = argparse.ArgumentParser(
        prog="exerice 2",
        description="Programme de tests et d'initialisation de l'exerice 2 du module ETRS514_TRI",
    )
    parser.add_argument(
        "action",
        choices=["init", "check"],
        help="Two possible actions : check (check your work) or init (initialize environment). ",
    )
    parser.add_argument("--step", help="wich step do you want to check or initialize")

    args = parser.parse_args()
    action = vars(args)["action"]
    step = vars(args).get("step", None)
    if step is None:
        print(
            f"You didn't enter a step to check or init. You can do it : \nexercice2 check --step step1."
        )
    if action == "init":
        init()
    elif action == "check":
        check(step)
    # print(create_expected_content_file3())
