import os
import secrets
import string
import sys
import subprocess

from dotenv import load_dotenv

load_dotenv()

REQUIRED_PW_VARS = (
    "DJANGO_SECRET_KEY",
    "DJANGO_SUPERUSER_PASSWORD",
    "YET_ANOTHER_SECRET_KEY",
)
OTHER_REQUIRED_VARS = (
    "DATABASE_URL",
    "REDIS_URL",
    "SOME_OTHER_VAR",
)


def generate_password(length: int = 64, special_chars: str = "!@#^*()") -> str:
    """
    Generate a random password with letters, digits, and special characters.

    :param length: Desired length of the password. Default = 64
    :param special_chars: Special characters to include in the password. Default = "!@#^*()"
    :return: A random password of the specified length.
    """
    alphabet = string.ascii_letters + string.digits + special_chars
    password = "".join(secrets.choice(alphabet) for _ in range(length))

    return password


def check_missing_vars(vars_: tuple[str, ...]) -> list[str]:
    """
    Checks if given variables are available.
    If not, print a list of missing variables.

    :param vars_: Tuple of required variables.
    :return: List of missing variables.
    """
    env_vars = os.environ.keys()
    missing_vars = [var for var in vars_ if var not in env_vars]

    if missing_vars:
        print("The following required variables are missing:")
        for var in missing_vars:
            print(f"- {var}")
        print()

    return missing_vars


def check_pw_vars(required_pw_vars: tuple[str, ...] = REQUIRED_PW_VARS) -> None:
    """
    Checks if required password variables are available.
    If not, generates them and adds them to the .env file.

    :param required_pw_vars: Tuple of required password variables.
    :return: None
    """
    missing_vars = check_missing_vars(required_pw_vars)

    if not missing_vars:
        return

    print("Generating missing password variables...")
    pw_vars = []
    for var in missing_vars:
        print(f"Generating password for {var}...")
        password = generate_password()
        pw_vars.append(f'{var}="{password}"\n')

    print("Writing password variables to .env file...")
    with open(".env", "a") as f:
        f.writelines(pw_vars)
    print()


def check_required_vars(required_vars: tuple[str, ...] = OTHER_REQUIRED_VARS) -> None:
    """
    Checks if required variables are available and not empty.
    If any variables are missing or empty print out the errors and exit the program.

    :param required_vars: Tuple of required variables.
    :return: None
    """
    missing_vars = check_missing_vars(required_vars)
    if missing_vars:
        sys.exit(1)

    empty_vars = [var for var in required_vars if not os.environ.get(var)]
    if empty_vars:
        print("The following required variables are empty:")
        for var in empty_vars:
            print(f"\t- {var}")
        sys.exit(1)

    print("All required variables are set and not empty.")


if __name__ == "__main__":
    check_pw_vars()
    check_required_vars()

    # Run the command specified in the compose.yml file
    command = sys.argv[1:]
    if command:
        subprocess.run(command)
