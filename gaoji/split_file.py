# coding=utf-8

def splitfile(filename, sizelimit, forline=True):
    size = 0
    i = 1
    out = open("%s.%d" % (filename, i), 'w')
    for line in open(filename):
        size = size + 1 if forline else size + len(line)
        if size > sizelimit:
            size = 1 if forline else len(line)
            out.close()
            i += 1
            out = open("%s.%d" % (filename, i), 'w')
        out.write(line)
    out.close()


if __name__ == '__main__':
    filename = input("请输入要分隔的文件名:")
    forline = input("输入数字0按行分隔，输入其它按大小分隔(请输入:)")
    forline = (int(forline) == 0)
    sizelimit = int(input("请输入分割子文件的大小(或行数):"))
    splitfile(filename, sizelimit, forline)
