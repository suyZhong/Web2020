import argparse
from nltk import stem
import re


#only for test
diction = ['power', 'business', 'energy', 'contact', 'message', 'price', 'company', 'meeting', 'market', 'electricity',
'financial', 'offer', 'customers', 'issues', 'credit', 'service', 'office', 'address',
'employees', 'team', 'project', 'letter', 'transmission', 'management', 'president',
'plans','natural','signed','document','opportunity']


def parse_query(query):
    expression = query
    andPattern = re.compile(r'AND|\&')
    orPattern = re.compile(r'OR|\|')
    notPattern = re.compile(r'NOT|!')
    dictPattern = re.compile(r'[a-z]+')
    opPattern = re.compile(r'AND|OR|NOT|\&|\||!|\(|\)')
    result = []             # 结果列表
    stack = []  # 栈

    stemmer = stem.SnowballStemmer('english')

    priority = dict()
    priority['('] = priority[')'] = 0
    priority['&'] = 2
    priority['|'] = 1
    priority['!'] = 3

    # 这个步骤是做着做着觉得麻烦才加的。。。
    # 所以程序中，前半部分后半部分对符号的判断不一样
    expression = re.sub(andPattern, "&", expression)
    expression = re.sub(orPattern, "|", expression)
    expression = re.sub(notPattern, "!", expression)
    expression = re.sub(r' ', "", expression)
    while expression:
        if re.match(dictPattern, expression):      # 如果当前字符为数字那么直接放入结果列表
            result.append(stemmer.stem(
                re.match(dictPattern, expression).group(0)))
            expression = re.sub(dictPattern, "", expression, 1)
        elif re.match(opPattern, expression):                     # 如果当前字符为一切其他操作符
            if len(stack) == 0:   # 如果栈空，直接入栈
                stack.append(re.match(opPattern, expression).group(0))
                expression = re.sub(opPattern, "", expression, 1)
            elif re.match(r'\(', expression):   # 如果当前为（，直接入栈
                stack.append(re.match(r'\(', expression).group(0))
                expression = re.sub(r'\(', "", expression, 1)
            elif re.match(andPattern, expression):  # 或者为and
                stack.append(re.match(andPattern, expression).group(0))
                expression = re.sub(andPattern, "", expression, 1)
            elif re.match(r'\)', expression):     # 如果右括号则全部弹出（碰到左括号停止）
                t = stack.pop()
                while t != '(':
                    result.append(t)
                    t = stack.pop()
                expression = re.sub(r'\)', "", expression, 1)
            # 如果当前字符优先级比较低，则开始弹出
            elif priority[expression[0]] < priority[stack[-1]]:
                if stack.count('(') == 0:           # 如果有左括号，弹到左括号为止
                    while stack:
                        result.append(stack.pop())
                else:                               # 如果没有左括号，弹出所有
                    t = stack.pop()
                    while t != '(':
                        result.append(t)
                        t = stack.pop()
                    stack.append('(')
                stack.append(expression[0])
                expression = expression[1:]  # 把第一个删了
            else:
                stack.append(expression[0])  # 其余情况直接入栈
                expression = re.sub(opPattern, "", expression, 1)
        else:
            print("Your Bool is wrong")
    while stack:
        result.append(stack.pop())
    return result


def load_index(token, IndexPath):
    docList = []
    stemmer = stem.SnowballStemmer('english')
    f = open(IndexPath, "r")
    p = re.compile(str(stemmer.stem(token)))
    print(str(token))
    flag = 0
    for t in f:
        if re.match(p, t):
            print('success find ' + token + ' in invert index!')
            docListGap = t.split()[1:]
            flag = 1
            break
    if flag == 0:
        print("No "+token+"in index ")
    tmp = 0
    for num in range(len(docListGap)):
        tmp += int(docListGap[num])
        docList.append(tmp)
    f.close()
    return docList


def search(query, IndexPath):
    stack = []
    for word in query:
        if word.isalpha:
            stack.append(load_index(word, IndexPath))
        elif word is "|":
            result = boolNOT(stack.pop())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default="",
                        help='choose the input file!')
    parser.add_argument('--scan', action='store_true',
                        help='use keyboard input')

    path = "../output/index.txt"
    methods = parser.parse_args()
    query = "powerANDnaturalOR!businessANDmessage"
    listQuery = parse_query(query)
    # for token in diction:
        # docList = load_index(token, path)
        # print(docList)
    search(listQuery, path)
