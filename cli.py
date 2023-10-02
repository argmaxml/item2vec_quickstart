import sys, os, json, subprocess
from argparse import ArgumentParser
from pathlib import Path
from decouple import config

__dir__ = Path(__file__).absolute().parent.parent
sys.path.append(str(__dir__ / "src"))


def shell(cmd):
    """Run bash command"""
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")
    return stdout, stderr
  
  
def main(args):
    """Empty main function"""
    return 0


if __name__ == "__main__":
    argparse = ArgumentParser()
    argparse.add_argument('--input', default='/', type=str, help='input dir')
    sys.exit(main(argparse.parse_args()))