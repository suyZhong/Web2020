import argparse
import re

def get_query(query, invertIndex):
    andPattern = re.compile(r'AND|\&')
    orPattern = re.compile(r'OR|\|')
    notPattern = re.compile(r'NOT|!')
    dictPattern = re.compile(r'[a-z]+')

    while query:
        print(123)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default="", help='choose the input file!')
    parser.add_argument('--scan', action='store_true', help='use keyboard input')

    methods = parser.parse_args()
    while methods.file:
        print(123)
    print(323)

