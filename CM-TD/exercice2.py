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
import crypt


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


def remove_user(username):
    """
    Delete/remove a user from the system
    user : user name
    """
    print(f"Removing {username}")
    process = subprocess.run(
        ["sudo", "/usr/sbin/userdel", "-r", username], capture_output=True
    )
    if process.returncode != 0:
        print(f"Error when removing {username}")
        print(f"remove_user {username} stderr :{process.stderr}")


def remove_grp(group_name):
    """
    Remove the group named grp
    grp_name : group_name
    """
    print(f"Removing {group_name}")
    process = subprocess.run(
        ["sudo", "/usr/sbin/groupdel", group_name], capture_output=True
    )
    if process.returncode != 0:
        print(f"Error when removing group {group_name}")
        print(f"remove_grp {group_name} stderr : {process.stderr}")


def add_grp(group_name):
    """
    Remove the group named grp
    grp_name : group_name
    """
    print(f"Add {group_name}")
    process = subprocess.run(
        ["sudo", "/usr/sbin/groupadd", group_name], capture_output=True
    )
    if process.returncode != 0:
        print(f"Error when adding group {group_name}")
        print(f"add_grp {group_name} stderr : {process.stderr}")


def add_line_to_file_as_user(file_name, line, as_user, as_group):
    """
    Add a line to a file as user
    line : the content you want to add at the end of the file
    as_user: username
    """
    print(f"Try Write {line } in {file_name} as {as_user}")
    uid = pwd.getpwnam(as_user).pw_uid
    gid = grp.getgrnam(as_group).gr_gid
    try:
        logging.debug("Changing user uid")
        os.setegid(gid)
        os.seteuid(uid)
    except PermissionError:
        print("Start again the program using sudo.")
        return
    try:
        with open(file_name, "a") as file:
            file.write(f"{line}\n")
            file.close()
    except PermissionError as p:
        print_red(f"{as_user} doesn't have the permission to write in {file_name}")
        print(f"{p}")
        return
    print_green(f"Successfull write in {file_name} as {as_user}.")
    uid = pwd.getpwnam("etudiant").pw_uid


def add_file(file_name, as_user, content=None, permissions=None):
    """
    Removes a file and recreates it
    file_name :
    as_user :
    content : file content ["", ""]
    permissions : {"owner" : root ,"group":root :, "mode": "0777" }
    """
    print(f"Recreating {file_name}")
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
        except PermissionError:
            print("Permission Error, retry using sudo")
            exit(1)

    process = subprocess.run(
        ["sudo", "-u", as_user, "touch", file_name], capture_output=True
    )
    if process.returncode != 0:
        print(f"Problème dans la création du fichier {file_name}")
        print(f"Try again using sudo")
        print(f"add_file {file_name} stderr : {process.stderr}")
        print(f"Try again using sudo")
        exit(1)
    if content is not None:
        print(f"Adding {content} to {file_name}")
        with open(file_name, "a") as file1:
            file1.writelines(content)
            file1.close()
    if permissions is not None:
        os.chmod(file_name, int(permissions["mode"], 8))


def remove_folder(folder):
    """
    Remove completely, folder, subfolder(s) and file(s)
    """
    print(f"Removing {folder}")
    if os.path.exists(folder):
        try:
            shutil.rmtree(folder)
        except PermissionError:
            print(f"Error when removing {folder}")
            print("Start the command using sudo")


def add_user(username, password):
    print(f"Adding user : {username} with password : {password}")
    password = crypt.crypt(password, "22")
    process = subprocess.run(["adduser", "-p", password, username], capture_output=True)

    if process.returncode != 0:
        if "already exists" in process.stderr.decode("utf-8"):
            print(f"{username} already exists")
        else:
            print(f"Problème dans la création de l'utilisateur {username}")
            print(f"add_user {username} stderr : {process.stderr}")
            print(f"Try again using sudo")


def remove_user_from_all_group(username):
    """
    Remove the user from all secondary group
    """
    print(f"Remove user {username} from all secondary groups.")
    process = subprocess.run(["usermod", "-G", "", username], capture_output=True)

    if process.returncode != 0:
        print(f"Error when reinit group for user {username}")
        print(f"remove_user_from_all_group {username} stderr : {process.stderr}")
        print(f"Try again using sudo")


def add_user_to_group(username, group):
    """
    Add a user to a secondary group
    usernane : the username
    group : the group to which the user will be added
    """
    print(f"Add user {username} to secondary group {group}.")
    process = subprocess.run(["usermod", "-aG", group, username], capture_output=True)

    if process.returncode != 0:
        print(f"Error adding {username} to group {group}")
        print(f"add_user_to_group {username} stderr : {process.stderr}")
        print(f"Try again using sudo")


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
        print_red(f"{file} doesn't exist")
        return False


def check_user_exists(username):
    """
    This check the existence of the user in the /etc/passwd
    """
    try:
        pwd.getpwnam(username)
    except KeyError:
        print_red(f"{username} doesn't exists")
        exit(1)
    print_green(f"{username} exists")


def check_user_password_set(username):
    try:
        shadow_password = spwd.getspnam(username).sp_pwdp
        logging.debug("{}".format(shadow_password))
    except PermissionError:
        print_red("Restart the verification as root, using sudo")
        exit(1)
    except KeyError:
        print_red(f"no password found for {username}")
        exit(1)
    if shadow_password != "!!":
        print_green(f"{username} has a password")
    else:
        print_red(f"no password found for {username}")
        exit(1)


def check_permissions(file, expected_permission):
    """
    file : path of the file
    expected_permission : {"owner" : root ,"group":root :, "mode": "0777" }
    return : True or False
    """
    try:
        statinfo = os.stat(file)
    except FileNotFoundError:
        print_red(f"{file} not found")
        exit(1)
    except PermissionError:
        print_red(
            f"You don't have the permission to access the file!\nTry starting the verification using *sudo*."
        )
        exit(1)
    owner = pwd.getpwuid(statinfo.st_uid).pw_name
    if owner == expected_permission["owner"]:
        group = grp.getgrgid(statinfo.st_gid).gr_name
        if group == expected_permission["group"]:
            # We focus only on the ISUID/ISGID/ISVTX and owner and group and other permissions [-4:]
            mode = oct(statinfo.st_mode)[-4:]
            if check_mode(mode, expected_permission["mode"]):
                print_green(
                    f"{file} -> Permissions : owner, group_owner and mode are correct"
                )
                return True
            else:
                print_red(
                    f"{file} mode is not correct.\nExpected:\t{expected_permission['mode']}\nCurrent:\t{mode}\nIf a \"!\" remplaces a number in the expected_mode. You can put what you want for this number.\n"
                )
                return
        else:
            print_red(
                f"{file} group owner is not correct.\nExpected group :{expected_permission['group']}\nCurrent group :{group}\n"
            )
    else:
        print_red(
            f"{file} owner is not correct.\nExpected owner:{expected_permission['owner']}\nCurrent owner:{owner}\n"
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


def check_mode(current_mode, expected_mode):
    """
    Check the mode of a file
    Exemple current_mode=0777, expected_mode=07!7 -> Return True
    """
    for i, char in enumerate(current_mode):
        if char != expected_mode[i] and expected_mode[i] != "!":
            return False
    return True


def init_step0():
    """
    Remove user1 add during step1
    """
    print("Nothing to do")


def init_step1():
    """
    Remove user1 add during step1
    """
    remove_user("user1")


def init_step2():
    """ """
    folder = "/projet1"
    remove_folder(folder)
    add_user("user1", "user1")


def init_step3():
    """
    Removing and recreating /projet1
    Removing user2
    Removing and recreating /projet1/user1.txt
    Removing user2
    """
    folder = "/projet1"
    print("Removing and recreating /projet1")
    remove_folder(folder)
    try:
        os.makedirs(folder)
    except PermissionError:
        print("Start the command using sudo")
        exit(1)

    print(f"Changing permission on /projet1 - Add 777")
    os.chmod(folder, 0o0777)
    # Creating /projet1/user1.txt
    file = "/projet1/user1.txt"
    add_file(file, "user1", "Premier test de user1.")
    remove_user("user2")


def init_step4():
    """ """
    remove_user("intrus")
    add_user("user2", "user2")
    add_file(
        "/projet1/user2.txt",
        "user2",
        ["Premier test de user2.\n", "Deuxième test de user1."],
        {"owner": "user2", "group": "user2", "mode": "0646"},
    )
    add_file(
        "/projet1/user1.txt",
        "user1",
        ["Premier test de user1.\n", "Deuxième test de user2."],
        {"owner": "user1", "group": "user1", "mode": "0646"},
    )


def init_step5():
    """
    Initialize step5
    """
    remove_user("intrus")
    add_file(
        "/projet1/user2.txt",
        "user2",
        ["Premier test de user2.\n", "Deuxième test de user1."],
        {"owner": "user2", "group": "user2", "mode": "0646"},
    )
    add_file(
        "/projet1/user1.txt",
        "user1",
        ["Premier test de user1.\n", "Deuxième test de user2."],
        {"owner": "user1", "group": "user1", "mode": "0646"},
    )
    remove_grp("projet1")
    remove_user_from_all_group("user1")
    remove_user_from_all_group("user2")


def init_step6():
    """
    Initialize step6
    """
    add_user("intrus", "intrus")
    folder = "/projet1"
    print("Removing and recreating /projet1")
    remove_folder(folder)
    try:
        os.makedirs(folder)
    except PermissionError:
        print("Start the command using sudo")
        exit(1)
    print(f"Changing permission on /projet1 - Add 770")
    os.chmod(folder, 0o0770)
    add_grp("projet1")
    print(f"Changing group owner on /projet1 - projet1")
    shutil.chown("/projet1", "root", "projet1")

    add_user_to_group("user1", "projet1")
    add_user_to_group("user2", "projet1")
    add_file(
        "/projet1/user2.txt",
        "user2",
        ["Premier test de user2.\n", "Deuxième test de user1."],
        {"owner": "user2", "group": "user2", "mode": "0646"},
    )
    add_file(
        "/projet1/user1.txt",
        "user1",
        ["Premier test de user1.\n", "Deuxième test de user2."],
        {"owner": "user1", "group": "user1", "mode": "0646"},
    )
    add_file(
        "/projet1/user1b.txt",
        "user1",
        "",
        {"owner": "user1", "group": "user1", "mode": "0664"},
    )


def init_all():
    """ """
    print("This will reinit all the exercice")
    ans = input("Do you want to continuer ? Y/N")
    if ans == "Y" or ans == "y":
        remove_user("intrus")
        remove_user("user1")
        remove_user("user2")
        remove_grp("projet1")
        remove_folder("/projet1")
    else:
        exit(1)


def init(step):
    """
    To initialize the VM, remove content
    step : the step to initialize
    """
    steps = {
        "step1": init_step1,
        "step2": init_step2,
        "step3": init_step3,
        "step4": init_step4,
        "step5": init_step5,
        "step6": init_step6,
        "all": init_all,
    }
    steps.get(step, init_all)()


def check_step1():
    """
    Check if user1 exists
    """
    check_user_exists("user1")
    check_user_password_set("user1")


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
    print("****************************************************************")
    print("To check this step, all the previous steps must have been done.")
    print("****************************************************************\n")
    check_user_in_group("projet1", "user1")
    check_user_in_group("projet1", "user2")
    folder = "/projet1"
    check_permissions(folder, {"owner": "root", "group": "projet1", "mode": "0770"})
    file = "user1.txt"
    check_permissions(
        f"{folder}/{file}", {"owner": "user1", "group": "projet1", "mode": "0660"}
    )
    file = "user2.txt"
    check_permissions(
        f"{folder}/{file}", {"owner": "user2", "group": "projet1", "mode": "0660"}
    )
    file = "user1b.txt"
    check_permissions(
        f"{folder}/{file}", {"owner": "user1", "group": "user1", "mode": "0664"}
    )


def check_step6():
    file = "/projet1/user1c.txt"
    if os.path.exists("/projet1/user1c.txt"):
        check_permissions(file, {"owner": "user1", "group": "user1", "mode": "0660"})
        add_line_to_file_as_user(
            "/projet1/user1c.txt", "Test de user2", "user2", "projet1"
        )
    else:
        print_red("You must create /projet1/user1c.txt as user1")


def check_all():
    print("You must enter a step to check.")


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
        "step6": check_step6,
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
