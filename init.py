import sys

from divaautobackup2 import DivaAutoBackup


if __name__ == "__main__":
    app = DivaAutoBackup()
    
    sys.exit(app.run())