import os
import subprocess

from dbBackup.dbConnectionData import DB_USER, DB_PASS, DB_NAME


errors_whitelist = ['mysql: [Warning] Using a password on the command line interface can be insecure.\r\n',
                    'mysqldump: [Warning] Using a password on the command line interface can be insecure.\r\n']

CURRENT_PATH = os.path.dirname(__file__)
DB_BACKUP_FILE_PATH = os.path.normpath(os.path.join(CURRENT_PATH, "db_backup.sql"))



def export_db_to_backup():
    cmd_line = f"mysqldump -u {DB_USER} --password={DB_PASS} --databases {DB_NAME} > {DB_BACKUP_FILE_PATH}"
    sqldump_process = subprocess.Popen(cmd_line,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True)

    stdout, stderr = sqldump_process.communicate()
    stdout, stderr = stdout.decode(), stderr.decode()
    _handle_stdout_stderr(cmd_line, stdout, stderr)


def update_db_from_backup():
    cmd_line = f"mysql -u {DB_USER} --password={DB_PASS} --database={DB_NAME} < {DB_BACKUP_FILE_PATH}"
    sqldump_process = subprocess.Popen(cmd_line,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True)

    stdout, stderr = sqldump_process.communicate()
    stdout, stderr = stdout.decode(), stderr.decode()
    _handle_stdout_stderr(cmd_line, stdout, stderr)


def _handle_stdout_stderr(cmd_line, stdout, stderr):
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
    # update_db_from_backup()
    export_db_to_backup()
