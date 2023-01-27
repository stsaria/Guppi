from src import make_server
import configparser
import sys

ini = configparser.ConfigParser()
ini.read('data/config.ini', 'UTF-8')
def run():
    print("Autoer! Name "+ini['autoer_info']['codename'])
    print("Version "+ini['autoer_info']['version'])
    while True:
        choice = input("\nモードを選択してください | Specify mode\nサーバー作成モード | make mode（make）\nサーバー管理モード | control mode（control）\n[M,C]：").lower()
        if choice in ["make", "mak", "ma", "m"]:
            make_server.make()
        elif choice in["control", "contro", "contr", "cont", "con", "co", "c"]:
            pass
        else:
            print("その項目はありません。| There is no item for that.")

if __name__ == "__main__":
    cmd_input = sys.argv
    if len(cmd_input) >= 2:
        if cmd_input[1] == "-direct":
            run()
