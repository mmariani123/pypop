import subprocess
import hashlib
import pytest

def test_AlleleColon():
    process=subprocess.Popen(
        ['./bin/pypop.py', '-m', '-c', './tests/data/Test_Allele_Colon_HardyWeinberg.ini', './tests/data/Test_Allele_Colon_HardyWeinberg.pop'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
    process.communicate()
    exit_code = process.wait()  # wait until script completed

    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("Test_Allele_Colon_HardyWeinberg-out.txt", 'rb').read()).hexdigest() == '86b09eb23ac6a17eaa6aaa498b552e3f'

