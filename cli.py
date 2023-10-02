import sys, os, json, subprocess
from argparse import ArgumentParser

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__ + os.sep + "src")


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