import subprocess
import secrets
import sys
import os


def install(package):
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}. Please install it manually.")


def check_virtual_env():
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Virtual environment detected. Continuing with setup...")
    else:
        print("WARNING: It's recommended to run this script in a virtual environment.")
        input("Press Enter to continue or Ctrl+C to abort...")


def generate_secret_key():
    return secrets.token_urlsafe(32)


def setup_django_environment():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ichikoto.settings')
    import django
    django.setup()


def run_migrations():
    try:
        call_command('migrate')
        print("Database migrations successfully applied.")
    except Exception as e:
        print(f"Failed to apply database migrations: {e}")


def main():
    # Check if running in a virtual environment
    check_virtual_env()

    # check for and create the .env file if it doesn't exist
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')

    if not os.path.exists(env_file_path):
        with open(env_file_path, 'w') as file:
            file.write('DEBUG=True\n')
            file.write('\n')
            file.write(f'SECRET_KEY="{generate_secret_key()}"\n')
            file.write('\n')
            file.write('OPENAI_API_KEY="YourAPIKeyHere"\n')
            file.write('OPENAI_API_MODEL="gpt-3.5-turbo"\n')
            file.write('\n')
            file.write('MAILJET_API_KEY="YourMailjetAPIKeyHere"\n')
            file.write('MAILJET_SECRET_KEY="YourMailjetSecretKeyHere"\n')
            file.write('MAILJET_SENDER_EMAIL="YourMailjetSenderEmailHere"\n')
            file.write('RECIPIENT_EMAIL="YourEmailHere"\n')
            file.write('# 0-11 ==> am\n')
            file.write('# 12-23 ==> pm\n')
            file.write('EMAIL_SCHEDULER_HOUR=12\n')
            file.write('EMAIL_SCHEDULER_MINUTES=0\n')
            file.write('\n')
            file.write('TARGET_LANGUAGE="Japenese"\n')

    # install required packages
    print("Installing required packages...")
    install("requests")
    install("python-dotenv")
    install("openai")

    setup_django_environment()
    run_migrations()

    print("Setup complete. Please check the .env file and update it with your settings.")


if __name__ == "__main__":
    main()
