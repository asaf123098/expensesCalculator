import os
import subprocess
from configparser import ConfigParser

errors_whitelist = ['mysql: [Warning] Using a password on the command line interface can be insecure.\r\n']

CURRENT_PATH = os.path.dirname(__file__)
CONF_FILE_PATH = os.path.normpath(os.path.join(CURRENT_PATH, "..", 'conf.ini'))
DB_BACKUP_FILE_PATH = os.path.normpath(os.path.join(CURRENT_PATH, "db_backup.sql"))

parser = ConfigParser()
parser.read(CONF_FILE_PATH)
DB_NAME = parser.get("DatabaseData", 'DBName')
DB_USER = parser.get("DatabaseData", 'DBRootUser')
DB_PASS = parser.get("DatabaseData", 'DBPass')

def update_db_from_backup():
    cmd_line = f"mysql -u {DB_USER} --password={DB_PASS} --database={DB_NAME} < {DB_BACKUP_FILE_PATH}"
    sqldump_process = subprocess.Popen(cmd_line,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True)

    stdout, stderr = sqldump_process.communicate()
    stdout, stderr = stdout.decode(), stderr.decode()
    _handle_stdout_stderr(cmd_line, stderr, stdout)


def _handle_stdout_stderr(cmd_line, stderr, stdout):
    if stderr:
        for err in errors_whitelist:
            if err == stderr:
                break
        else:
            raise Exception(stderr)
    if "Usage:" in stdout:
        print(f"Given command - {cmd_line}")
        raise Exception(stdout)
    print(stdout)


if __name__ == "__main__":
    update_db_from_backup()