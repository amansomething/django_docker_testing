import os
import secrets
import string
import subprocess
import sys
from typing import Union

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class RequiredPW(BaseModel):
    """
    Pydantic model for required password variables.

    :param name: Name of the environment variable. All caps, snake_case recommended.
    :param length: Desired length of the password. Default = 64
    :param special_chars: Special characters to allow in the password. Default = "!@#^*()"

    Example Definitions:
        RequiredPW(name="SECRET_KEY")
        RequiredPW(name="PASSWORD", length=16)
        RequiredPW(name="YET_ANOTHER_SECRET_KEY", special_chars="!@#^*()")
        RequiredPW(name="SuperCustom", length=128, special_chars="!")
    """
    name: str
    length: int = 64
    special_chars: str = "!@#^*()"


# See the RequiredPW class for details.
REQUIRED_PW_VARS = (
    RequiredPW(name="DJANGO_SECRET_KEY"),
    RequiredPW(name="DJANGO_SUPERUSER_PASSWORD", length=16),
    RequiredPW(name="YET_ANOTHER_SECRET_KEY"),
)
OTHER_REQUIRED_VARS = (
    "VAR_1",
    "VAR_2",
    "SOME_OTHER_VAR",
)
ENV_FILE = ".env"


def generate_password(length: int = 64, special_chars: str = "") -> str:
    """
    Generate a random password with letters, digits, and special characters.

    :param length: Desired length of the password. Default = 64
    :param special_chars: Special characters to include in the password. Default = ""
    :return: A random password of the specified length.
    """
    alphabet = string.ascii_letters + string.digits + special_chars
    password = "".join(secrets.choice(alphabet) for _ in range(length))

    return password


def check_pw_vars(
        required_pw_vars: tuple[RequiredPW] = REQUIRED_PW_VARS, env_file: str = ENV_FILE
) -> None:
    """
    Checks if required password variables are loaded.
    If not, generates them and adds them to the .env file.
    Prints out status messages as it goes.

    :param required_pw_vars: Tuple of RequiredPW variables to check.
    :param env_file: Env file name to write passwords to.
    :return: None
    """
    missing_vars = []
    for var in required_pw_vars:
        if not os.getenv(var.name):
            print(f"Missing required password variable: {var.name}")
            missing_vars.append(var)

    if not missing_vars:
        return

    print("\nGenerating missing password variables...")
    pw_vars = ["# Missing Required Passwords\n"]
    for var in missing_vars:
        print(f"Generating password for {var.name}...")
        password = generate_password(var.length, var.special_chars)
        pw_vars.append(f'{var.name}="{password}"\n')
    pw_vars.append("\n")

    print("\nAppending password variables to .env file...")
    with open(env_file, "a") as f:
        f.writelines(pw_vars)
    print("Done!\n")


def check_required_vars(
        required_vars: Union[list[str], tuple[str, ...]] = OTHER_REQUIRED_VARS,
        env_file: str = ENV_FILE,
) -> None:
    """
    Checks if required variables are available and not empty.
    If variable are missing:
        - Adds them to the .env file as empty strings.
        - Prints out a message to fill them out.
        - Exits the program.
    If variables are empty strings, prints out the errors and exits the program.
    Prints out status messages as it goes.

    :param required_vars: List or tuple of required variables to check.
    :param env_file: Env file name to write variables to.
    :return: None
    """
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            print(f"Missing required variable: {var}")
            missing_vars.append(var)

    if missing_vars:
        print("\nAppending missing variables to .env file...")
        required_vars = ["\n# Required Variables\n"]
        for var in missing_vars:
            required_vars.append(f'{var}=""\n')

        with open(env_file, "a") as f:
            f.writelines(required_vars)

        print("Done! Fill those out and re-run the script.")
        sys.exit(1)

    empty_vars = [var for var in required_vars if not os.environ.get(var)]
    if empty_vars:
        print("The following required variables are empty:")
        for var in empty_vars:
            print(f"- {var}")
        sys.exit(1)

    print("All required variables are set and not empty.")


if __name__ == "__main__":
    check_pw_vars()
    check_required_vars()

    # Run the command specified in the compose.yml file
    command = sys.argv[1:]
    if command:
        subprocess.run(command)
