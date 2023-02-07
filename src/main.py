from src import make_server
from src import control_server
import sys

version = "Pre/0.0.5-alpha"
codename = "Guppi"

def run():
    print("Autoer! Name "+codename)
    print("Version "+version)
    print("このプログラムは、まだ”アルファ版”です。\nなにか不具合があった場合には、GithubのIssueでお伝え下さい。")
    print("Github : https://github.com/solothunder-autoer/Guppi")
    while True:
        choice = input("\nモードを選択してください | Specify mode\nサーバー作成モード | make mode（make）\nサーバー管理モード | control mode（control）\n終了 | Exit (exit) \n[M,C,E]：").lower()
        if choice in ["make", "mak", "ma", "m"]:
            make_server.make()
        elif choice in["control", "contro", "contr", "cont", "con", "co", "c"]:
            control_server.main()
        elif choice in["exit", "exi", "ex", "e"]:
            break
        else:
            print("その項目はありません。| There is no item for that.")

if __name__ == "__main__":
    cmd_input = sys.argv
    if len(cmd_input) >= 2:
        if cmd_input[1] == "-direct":
            run()
