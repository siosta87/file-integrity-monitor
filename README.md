# File Integrity Monitor

A Python lab that uses SHA-256 hashes to detect changes in a local directory.

## Included files

- [fim.py](fim.py): baseline creation and monitoring loop
- [monitored_files](monitored_files): sample directory to monitor
- [baseline.json](baseline.json): stored hashes; regenerate for your own local files

## Requirements

Python 3. No third-party packages are required.

## Run

Open a terminal in this repository directory. Initialize the baseline from the files currently in monitored_files:

```console
python fim.py --init
```

Start monitoring:

```console
python fim.py
```

In a separate terminal or editor, create, edit, or delete a test file in monitored_files. The script checks about every two seconds and prints alerts. Press Ctrl+C to stop.

## How it works

The script recursively calculates SHA-256 hashes and compares them with baseline.json. It reports new, modified, and deleted files.

## Important limitations

- The baseline is updated after each observed change. This is a rolling change monitor, not a permanently trusted reference.
- The baseline is stored beside the script without tamper protection.
- Paths are relative to the terminal working directory.
- Missing-file handling is included, but permission failures and malformed baseline JSON need more robust handling.
- No timestamps or durable alert report are produced by the monitoring alerts.
- No automated tests or captured run results are included.

The previous README described a different log-analysis project. This README now matches fim.py.
