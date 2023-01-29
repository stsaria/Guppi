from src import main
import os
import sys
import platform
from src import etc_server
from thirdparty import els
import shutil

def check():
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
    print("OK!")
    # pathの内容がなかったら作成する系
    print("File Check 1",end="")
    path = ["data", "data/config.ini", "minecraft", "data/minecraft-list.txt", "data/minecraft-dir-list.txt"]
    path_attribute = ["dir", "file", "dir", "file", "file"]
    for i in range(5):
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
    print("Network Check",end="")
    for i in range(3):
        print(".",end="")
        ping_result = els.check_ping("google.com","1")
    if ping_result:
        print("OK!")
    if not ping_result:
        print("Error!")
        print("ネットワークに繋がっていません | NetWork Is Unavailable")
        print("ネットに繋がっていない又はファイアーウォールなどで\n接続できない設定になっている可能性があります\nWifiなどの設定を見直す・ネットワーク管理者などに接続を許可する\nなどで解決してください。\nYou may not be connected to the internet or\nit may be set to not be able to connect due to a firewall\nReview the Wi-Fi settings or allow the network administrator to connect\n.")
        if etc_server.input_yes_no("以上のことからこのまま続行するのは推奨されませんが\n続行することもできます\nただし、これによるサーバー作成の失敗などには責任は負いません\nFor the reasons above, we do not recommend continuing at this point. \nYou can continue\nHowever, we are not responsible for server creation failures caused by this. \n"):
            print("-Pass-")
    # javaが導入されているか？（pathが通っているか）
    print("Java Path",end="")
    if shutil.which('java') == None:
        print(".Error!")
        print("Javaが導入されていないか\nPath(環境変数)が通っていない、可能性があります。")
        sys.exit(2)
    print(".OK!")

    # Autoer!は3.10以上でないと実行できないから3.10未満だったら終了させる
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
            pass
        else:
            check()
    else:
        check()
    print("Start!\n")
    main.run()
