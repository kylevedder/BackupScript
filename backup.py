import shutil
import os
import sys
import datetime


class c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


VERSION = "0.0.1"
HEADER = """Welcome to Backup Script v{0}! Sorry for all the bugs!
 ____________________        _____________
|      |             |      ||           ||
|      |           _ |      ||           ||
|------|          | `-._|\  ||           ||
|      |          |       \ ||___________||
|      |          |    _  / |   _______   |
|------|------.---|_.-' |/  |  |    __ |  |
|      |      |      |      |  |   |__||  |
|______|______|______|      '--|_______|--'

""".format(
    VERSION)

# Backup drive
BACKUP_DRIVE = "/media/kyle/Pepper (1TB)/"

# Locations to place backups
PUSH_LOCATION = "Backups/"

# Locations to pull from
PULL_LOCATIONS = [
    ("/home/kyle/scripts/", "scripts"),
    ("/home/kyle/.thunderbird", "thunderbird"),
    ("/home/kyle/code/", "code"),
    ("/home/kyle/Music/", "Music"),
    ("/home/kyle/Documents/", "Documents"),
    ("/home/kyle/.ssh/", "ssh")
]


def main():
    printc(HEADER, c.HEADER)

    # check drive exists
    if(not os.path.exists(BACKUP_DRIVE)):
        printc("Backup Drive \"{0}\" not found!".format(BACKUP_DRIVE), c.FAIL)
        sys.exit(-1)

    setup()

    # Push each directory
    cleanCopy = True
    for locationTuple in PULL_LOCATIONS:
        pullLoc = locationTuple[0]
        pushDir = locationTuple[1]

        # check pull location exists
        if(not os.path.exists(pullLoc)):
            printc("Pull location \"{0}\" not found!".format(pullLoc), c.FAIL)
            sys.exit(-1)

        pushLocFrmt = BACKUP_DRIVE + PUSH_LOCATION + pushDir + "/" + \
            getBackupDirectory(pushDir)

        # push location already exists
        if(os.path.exists(pushLocFrmt)):
            printc("Push location \"{0}\" already exists!".format(
                pushLocFrmt), c.FAIL)
            sys.exit(-1)

        printc(("Backing up \"{0}\"...\n Size: %0.1f MB" %
                sizeFolder(pullLoc)).format(pullLoc))
        copyStatus = copyDirectory(pullLoc, pushLocFrmt)
        if(not copyStatus):
            cleanCopy = false

    if(cleanCopy):
        printc("Backup complete!", c.OKGREEN)
    else:
        printc("Backup finished with errors.", c.WARNING)


def setup():
    if(not os.path.exists(BACKUP_DRIVE + PUSH_LOCATION)):
        printc("Push location \"{0}\" not found, creating...".format(
            PUSH_LOCATION), c.WARNING)
        os.makedirs(BACKUP_DRIVE + PUSH_LOCATION)
    else:
        printc("Push location \"{0}\" found...".format(
            PUSH_LOCATION), c.OKBLUE)

# Folder size in MN


def sizeFolder(folder):
    folder_size = 0
    for (path, dirs, files) in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            if(not os.path.islink(filename)):
                folder_size += os.path.getsize(filename)
    return (folder_size / (1024 * 1024.0))


def getBackupDirectory(baseDirectory):
    date = datetime.datetime.now().strftime('%Y-%m-%d_%H%M')
    return (baseDirectory + "_{0}").format(date)


def copyDirectory(src, dst):
    if(not os.path.exists(dst)):
        shutil.copytree(src, dst, True)
        return True
    else:
        printc("Push folder \"{0}\" already exists!".format(dst), c.FAIL)
        return False


def printc(str, color=""):
    print(color + str + c.ENDC)

if __name__ == '__main__':
    main()
