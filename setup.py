from src import main
import os
import sys
import platform
from thirdparty import els
import shutil
import time
import platform

autoer_text = ["----------------------------------------------\n|   ■■                                     ■■|", "|   ■■■             ■                      ■■|", "|   ■ ■            ■■                      ■■|", "|  ■  ■    ■   ■  ■■■■   ■■■    ■■■   ■ ■■ ■ |", "|  ■  ■    ■   ■   ■■   ■   ■  ■   ■  ■■   ■ |", "|  ■   ■   ■   ■   ■■   ■    ■ ■   ■■ ■    ■ |", "| ■■■■■■   ■   ■   ■■   ■    ■ ■■■■■■ ■    　|", "| ■    ■   ■   ■   ■■   ■    ■ ■      ■    　|", "| ■     ■  ■■  ■   ■■   ■   ■  ■   ■  ■    ■ |", "|■■     ■   ■■■■    ■■   ■■■    ■■■   ■    ■■|\n----------------------------------------------"]
def check(check, net):
    if not check:
        return

    if platform.system() == "Windows":
        for i in autoer_text:
            print(i)
            time.sleep(0.1)

    print("チェック中")
    ## pathの内容がなかったらエラーを出す系
    #print("File Check 1",end="")
    #path = ["", "data/config.ini"]
    #for i in path:
    #    print(".",end="")
    #    if not os.path.exists(i):
    #        print("Error!")
    #        print("\nError: File or directory does not exist\nNo folder or file found is => \n"+i)
    #        sys.exit(1)
    #print("OK!")
    # pathの内容がなかったら作成する系
    print("File Check",end="")
    path = ["data", "minecraft", "data/minecraft-list.txt", "data/minecraft-dir-list.txt"]
    path_attribute = ["dir", "dir", "file", "file"]
    for i in range(4):
        print(".",end="")
        if not os.path.exists(path[i]):
            print("-Create-",end="")
            if path_attribute[i] == "dir":
                os.mkdir(path[i])
            if path_attribute[i] == "file":
                f = open(path[i], 'w')
                f.write('')
                f.close()
    print("OK!")
    # ネットにつながっているか（pingで）を確認する
    if net:
        print("Network Check",end="")
        for i in range(3):
            print(".",end="")
            ping_result = els.check_ping("google.com","1")
        if ping_result:
            print("OK!")
        if not ping_result:
            print("Error!")
            print("ネットワークに繋がっていません | NetWork Is Unavailable")
            sys.exit(2)
    # javaが導入されているか？（pathが通っているか）
    print("Java Path",end="")
    if shutil.which('java') == None:
        print(".Error!")
        print("Javaが導入されていないか\nPath(環境変数)が通っていない、可能性があります。")
        sys.exit(2)
    print(".OK!")

    # Autoer!はPython 3.10以上でないと実行できないから3.10未満だったら終了させる
    for i in range(4):
        i = i + 1
        need_version = '3.10'
        now_version = platform.python_version()[0:i]
        if float(now_version) < float(need_version[0:i]):
            print(now_version)
            print("Error: Python versions prior to 3.10 are not available.")

if __name__ == "__main__":
    cmd_input = sys.argv
    if len(cmd_input) >= 2:
        if cmd_input[1] == "-notcheck":
            check_def = False
        else:
            check_def = True
    else:
        check_def = True
    if len(cmd_input) >= 3:
        if cmd_input[2, 3] == "-nonet":
            net = False
        else:
            net = True
    else:
        net = True
    check(check_def, net)
    print("Start!\n")
    main.run()
