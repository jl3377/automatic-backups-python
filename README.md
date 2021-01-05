# Automatic Backups with Python.

## How to make and use the config file.
You need create a config.py into conf/ directory.
This script, can copy multiple directories and files into a selected ftp.

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

## not much more to say.
## log file, how to use.
