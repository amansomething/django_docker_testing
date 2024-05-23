# TODO: Use dotenv to handle reading the .env file.
# TODO: Check that required vars aren't empty and a reasonable length.

import os
import secrets
import string
import sys


def generate_password(length: int = 64, special_chars: str = "!@#^*()") -> str:
    """
    Generate a random password with letters, digits, and special characters.

    :param length: Desired length of the password. Default = 64
    :param special_chars: Special characters to include in the password. Default = "!@#^*()"
    :return: A random password of the specified length.
    """
    alphabet = string.ascii_letters + string.digits + special_chars
    password = "".join(secrets.choice(alphabet) for i in range(length))

    return password


def create_env_file(env_file: str = ".env") -> None:
    """
    Creates a .env file if it does not already exist.

    :param env_file: The name of the .env file. Default = ".env"
    :return: None
    """
    if not os.path.exists(env_file):
        print(f"Creating {env_file}...")
        with open(env_file, "w") as f:
            f.write("")
    else:
        print(f"{env_file} already exists.")


def read_env_file(env_file: str = ".env") -> str:
    """
    Reads the contents of a .env file and returns it as a string.
    Uses the create_env_file function to create the .env file if it does not exist.

    :param env_file: Name of the .env file. Default = ".env"
    :return: Contents of the .env file.
    """
    create_env_file(env_file)

    with open(env_file, "r") as f:
        env_vars = f.read()

    return env_vars


def check_pw_vars(env_vars: str, required_pw_vars: tuple) -> None:
    """
    Checks if required password variables are set in the .env file.
    If not, adds them to the .env file.

    :param env_vars: Contents of the .env file.
    :param required_pw_vars: Tuple of required password variables.
    :return: None
    """
    # Check if required password variables are in the .env file
    pw_vars = []
    for var in required_pw_vars:
        if var not in env_vars:
            print(f"Generating password for {var}...")
            password = generate_password()
            line = f'{var}="{password}"\n'
            pw_vars.append(line)

    # Add any missing variables to the .env file.
    if pw_vars:
        with open(".env", "a") as f:
            f.writelines(pw_vars)
        print("Passwords added to .env file.")
    else:
        print("All required passwords are present in the .env file.")


def check_other_required_vars(env_vars: str, required_vars: tuple) -> None:
    """
    Checks if other required variables are set in the .env file.
    If not, exit the program.

    :param env_vars: Contents of the .env file.
    :param required_vars: Tuple of required  variables.
    :return: None
    """
    error = False
    for var in required_vars:
        if var not in env_vars:
            print(f"ERROR: {var} is not set in the .env file.")
            error = True

    if error:
        sys.exit(1)


def main():
    required_pw_vars = (
        "DJANGO_SECRET_KEY",
        "ANOTHER_SECRET_KEY",
        "YET_ANOTHER_SECRET_KEY",
    )
    required_vars = (
        "DATABASE_URL",
        "REDIS_URL",
        "SOME_OTHER_VAR",
    )

    env_vars = read_env_file()
    check_pw_vars(env_vars, required_pw_vars)
    check_other_required_vars(env_vars, required_vars)


if __name__ == "__main__":
    main()
