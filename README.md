# Automatic Backups with Python

## How to use config.php
Yo need create a config.py into conf/ directory.

```
{
  "artegrafico.net": {
    "ftp": "ftp.artegrafico.net",
    "user": "user",
    "passwd": "pass",
    "backup_dir": "uploads/",
    "tmp_dir": "./tmp/",
    "log_dir": "./logs/backups.log",
    "backup": {
      "directories": "conf/, .test/",
      "files": "tmp/test_file1.txt, tmp/test_file2.txt"
    }
  }
}
```