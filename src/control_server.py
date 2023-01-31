from src import etc_server
import sys
import linecache

def select_server():
    minecraft_server_list_txt_lines_count = sum([1 for _ in open('data/minecraft-list.txt', encoding="utf-8")])
    minecraft_server_dir_list_txt_lines_count = sum([1 for _ in open('data/minecraft-dir-list.txt', encoding="utf-8")])
    while True:
        choice_lines = input("サーバーを選んでください: ")
        if not choice_lines or not choice_lines.isdigit():
            continue
        if int(choice_lines) <= 0 or int(minecraft_server_dir_list_txt_lines_count) < int(choice_lines) - 1 or int(minecraft_server_list_txt_lines_count) < int(choice_lines):
            continue
        break
    return choice_lines

def run():
    print("サーバー起動モード")
    # txtファイルカウント
    minecraft_server_list_txt_lines_count = sum([1 for _ in open('data/minecraft-list.txt', encoding="utf-8")])
    minecraft_server_dir_list_txt_lines_count = sum([1 for _ in open('data/minecraft-dir-list.txt', encoding="utf-8")])

    if not minecraft_server_dir_list_txt_lines_count == minecraft_server_list_txt_lines_count:
        print("txtファイル同士の行数が一致しないため起動できません。")
        sys.exit(1)

    print("起動するサーバーを選んでください。")
    # サーバー情報を読み込む
    with open("data/minecraft-list.txt", "r", encoding="utf-8") as f:
        lines = f.read()
    print(lines)
    choice_lines = select_server()
    while True:
        choice_xms = input("Xms(最小メモリ)を入力してください(G) ※数字のみ: ")
        choice_xmx = input("Xmx(最大メモリ)を入力してください(G) ※数字のみ: ")
        mem_input = [str(choice_xms), str(choice_xmx)]
        for i in mem_input:
            if not i.isdigit():
                continue
            if int(i) < 1:
                continue
        break
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_lines)).replace('\n', '')
    print(path)

    start_jar = linecache.getline("data/"+path.replace('/', '-')+".txt", 3).replace('\n', '')
    etc_server.exec_java(path, start_jar, mem_input[0], mem_input[1], "")

def port():
    print("ポート変更モード")
    print("ポート変更するサーバーを選んでください。")
    with open("data/minecraft-list.txt", "r", encoding="utf-8") as f:
        lines = f.read()
    print(lines)
    choice_lines = select_server()
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_lines)).replace('\n', '')
    while True:
        input_port = input("変更先のポートを入力してください: ")
        if not input_port or not str.isnumeric(input_port):
                continue
        else:
            break
    etc_server.file_identification_rewriting(path+"/server.properties", "server-port=", "server-port="+input_port+"\n")
    print("ポート変更が完了しました")

def make_sh():
    print("sh-batファイルを作成するサーバーを選んでください")
    with open("data/minecraft-list.txt", "r", encoding="utf-8") as f:
        lines = f.read()
    print(lines)
    choice_lines = select_server()
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_lines)).replace('\n', '')
    while True:
        choice_xms = input("Xms(最小メモリ)を入力してください(G) ※数字のみ: ")
        choice_xmx = input("Xmx(最大メモリ)を入力してください(G) ※数字のみ: ")
        mem_input = [str(choice_xms), str(choice_xmx)]
        for i in mem_input:
            if not i.isdigit():
                continue
            if int(i) < 1:
                continue
        break
    start_jar = linecache.getline("data/"+path.replace('/', '-')+".txt", 3).replace('\n', '')
    file_name = ["start.sh", "start.bat"]
    for i in file_name:
        with open(path+"/"+i, 'w', encoding="utf-8") as f:
            print("echo Start!\njava -Xms"+mem_input[0]+"G -Xmx"+mem_input[1]+"G -jar "+start_jar, file=f)
    print("sh-batファイルを作成しました")

def main():
    while True:
        choice = input("\n管理モードを選択してください | Choose your management mode\n実行モード | runner mode（run）\nサーバーポート変更モード | edit server port mode（port）\nshとbatファイル作成モード | make sh file mode（sh or bat）\n戻る | Exit (exit)\n[R,P,S,B,E]：").lower()
        if choice in ["run", "ru", "r"]:
            run()
        elif choice in["port", "por", "po", "p"]:
            port()
        elif choice in["sh", "s"]:
            make_sh()
        elif choice in["bat", "ba", "b"]:
            make_sh()
        elif choice in["exit", "exi", "ex", "e"]:
            break
        else:
            print("その項目はありません。| There is no item for that.")
