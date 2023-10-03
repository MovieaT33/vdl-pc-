import os
import sys
import time
import getpass
import requests
import traceback


class LoginError(BaseException):
    ...


def clear() -> None:
    os.system("cls")


def main() -> None:
    print("Initialization program...")
    url = "https://movieat33.pythonanywhere.com"

    program_name = "vdc (pc)"
    full_program_name = "Virtual DataBase Console (PC)"
    version = "2.0.0"
    license_ = "GNU"
    program = f"program_name={program_name}&full_program_name={full_program_name}&version={version}&license={license_}"
    anim = "|/-\\"
    for i in range(20):
        element = anim[i % len(anim)]
        print(element, end="\r")
        time.sleep(0.1)
    clear()

    print(f"{full_program_name} {version}. {license_} license")
    print("Login")

    username = input("Username: ")
    user_password = getpass.getpass("Password: ")
    db_name = input("DataBase name: ")
    password = getpass.getpass("DataBase password: ")

    prefix = f"username={username}&user_password={user_password}&db_name={db_name}&password={password}"
    response = requests.get(f"{url}/api/v0/verification_password?{program}&{prefix}")
    if response.status_code != 200 or response.text != "Password correctly":
        raise LoginError(
            f"Status code isn't 200. Code: {response.status_code}"
        )
    clear()

    run = True
    while run:
        command = input(f"(vdc) \033[32m~\{os.getcwd()}\033[0m $ ")
        len_command_split = len(command.split())
        if 0 < len_command_split and command.lower().split()[0] == "exit":
            sys.exit()
        if 0 < len_command_split and command.lower().split()[0] == "login":
            with open(__file__, "r", encoding="utf-8") as file:
                exec(file.read(), globals(), locals())
        if 0 < len_command_split and command.lower().split()[0] == "clear":
            clear()
            continue

        if command.find("?") == -1:
            full_url = f"{url}{command}?{program}&{prefix}"
        else:
            full_url = f"{url}{command}&{program}&{prefix}"

        print(full_url)

        try:
            response = requests.get(full_url)
            print(f"{response.text}\n{response.status_code}")
            continue
        except Exception as error:
            print("".join(traceback.format_exception(type(error), error, error.__traceback__)))
        except BaseException as error:
            print("".join(traceback.format_exception(type(error), error, error.__traceback__)))
        if command.split()[0] == "cd":
            os.chdir(" ".join(command.split()[1:]))
            continue
        if command.split()[0] == "info":
            print(globals())
            print(locals())
            continue
        os.system(command)


if __name__ == "__main__":
    main()
    print("Program finished")
