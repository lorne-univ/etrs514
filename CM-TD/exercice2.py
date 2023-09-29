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
import grp
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


def init_step0():
    """
    Remove user1 add during step1
    """
    pass


def init_step1():
    """
    Remove user1 add during step1
    """
    process = subprocess.run(
        ["sudo", "/usr/sbin/userdel", "-r", "user1"], capture_output=True
    )
    if process.returncode != 0:
        logging.info("init_step1 : {}".format(process.stderr.decode("utf-8")))


def init_step2():
    """ """
    pass


def init_step3():
    """ """
    pass


def init_all():
    """ """
    pass


def init(step):
    """
    To initialize the VM, remove content
    step : the step to initialize
    """
    steps = {
        "step1": init_step1,
        "step2": init_step2,
        "step3": init_step3,
        "all": init_all,
    }
    steps.get(step, init_all)()


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


def check_file_exist(file):
    """
    Check if a file exists.
    file : path of the file
    """
    if os.path.exists(file):
        print_green(f"{file} exists")
        return True
    else:
        print_green(f"{file} doesn't exist")
        return False


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


def check_mode(current_mode, expected_mode):
    """
    Check the mode of a file
    Exemple current_mode=0777, expected_mode=07!7 -> Return True
    """
    for i, char in enumerate(current_mode):
        if char != expected_mode[i] and expected_mode[i] != "!":
            return False
    return True


def check_permissions(file, expected_permission):
    """
    file : path of the file
    expected_permission : {"owner" : root ,"group":root :, "mode": "0777" }
    return : True or False
    """
    statinfo = os.stat(file)
    owner = pwd.getpwuid(statinfo.st_uid).pw_name
    if owner == expected_permission["owner"]:
        group = grp.getgrgid(statinfo.st_gid).gr_name
        if group == expected_permission["group"]:
            # We focus only on the ISUID/ISGID/ISVTX and owner and group and other permissions [-4:]
            mode = oct(statinfo.st_mode)[-4:]
            if check_mode(mode, expected_permission["mode"]):
                print_green(
                    f"{file} -> Permissions owner, group_owner and mode are correct"
                )
                return True
            else:
                print_red(
                    f"{file} mode is not correct.\nExpected:\t{expected_permission['mode']}\nCurrent:\t{mode}\nIf a \"!\" remplaces a number in the expected_mode. You can put what you want for this number."
                )
                return
        else:
            print_red(
                f"{file} group owner is not correct.\nExpected:{expected_permission['group']}\nCurrent:{group}"
            )
    else:
        print_red(
            f"{file} owner is not correct.\nExpected:{expected_permission['owner']}\nCurrent:{owner}"
        )
    return False


def check_group_exists(group_name):
    """
    Check if a group exists
    """
    try:
        grp.getgrnam(group_name)
        print_green(f"{group_name} exists.")
    except KeyError:
        print_red(f"{group_name} doesn't exist.")
        exit(1)


def check_user_in_group(group_name, user):
    """
    Test if user belongs to a posix group
    Return True or False
    """
    try:
        group_infos = grp.getgrnam(group_name)
        if user in group_infos.gr_mem:
            print_green(f"{user} in group {group_name}.")
            return True
        else:
            print_red(f"{user} not in group {group_name}.")
            return False
    except KeyError:
        print_red(f"{group_name} doesn't exist.")
        exit(1)


def check_step2():
    """
    Check if folder /projet1 exists
    Check permissions on /projet1 root root rwx???rwx
    Check if file /projet1/use1.txt exists

    """
    folder = "/projet1"
    if os.path.exists(folder):
        print_green(f"{folder} exists")
        # Check permission
        check_permissions(folder, {"owner": "root", "group": "root", "mode": "07!7"})
        file1 = "/projet1/user1.txt"
        if os.path.exists(file1):
            print_green(f"{file1} exists")
            check_permissions(
                file1, {"owner": "user1", "group": "user1", "mode": "0644"}
            )
            check_content_of_file(file1, "Premier test de user1.")
        else:
            print_red(f"{file1} not presents")

    else:
        print_red(f"{folder} not found")


def check_step3():
    """
    Essai de partage en local de fichiers ou de dossiers
    """
    check_user_exists("user2")
    check_user_password_set("user2")
    file1 = "/projet1/user2.txt"
    if check_file_exist(file1):
        check_permissions(file1, {"owner": "user2", "group": "user2", "mode": "06!6"})
        check_content_of_file(file1, "Premier test de user2.\nDeuxième test de user1.")
    file1 = "/projet1/user1.txt"
    if check_file_exist(file1):
        check_permissions(file1, {"owner": "user1", "group": "user1", "mode": "06!6"})
        check_content_of_file(file1, "Premier test de user1.\nDeuxième test de user2.")


def check_step4():
    """
    Un intrus arrive à écrire dans un des fichiers
    """
    check_user_exists("intrus")
    check_user_password_set("intrus")
    file1 = "/projet1/user2.txt"
    check_content_of_file(
        file1, "Premier test de user1.\nDeuxième test de user2.\nAccès par instrus."
    )


def check_step5():
    """
    Création d'un groupe projet1 et placement des permissions sur le dossier et les fichiers
    """
    check_user_in_group("projet1", "user1")
    check_user_in_group("projet1", "user2")


def check_all():
    logging.debug("all")


def check(step):
    """
    Check if the student made a good job
    step : step1, step2
    """
    steps = {
        "step1": check_step1,
        "step2": check_step2,
        "step3": check_step3,
        "step4": check_step4,
        "step5": check_step5,
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
        if action == "init":
            print(
                f"You didn't enter a step to init.\All the step will be initialized\nIf you to initialize a step you can do it :\nexercice2 check --step step1."
            )
            ans = input("Are you sure you want to initialize all ?Y/N")
            if ans == "Y" or ans == "y":
                init("all")
            else:
                exit(0)
        elif action == "check":
            print(
                f"You didn't enter a step to init.\All the step will be initialized\nIf you to initialize a step you can do it :\nexercice2 check --step step1."
            )
            ans = input("Are you sure you want to initialize all ?Y/N")
            if ans == "Y" or ans == "y":
                check("all")
            else:
                exit(0)
    else:
        if action == "init":
            init(step)
        elif action == "check":
            check(step)
