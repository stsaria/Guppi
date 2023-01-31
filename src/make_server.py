import os
import sys
import datetime
from thirdparty import const
from src import etc_server
import configparser
import shutil

new_version = "1.19.3"

class InputInfoClass:
    def __init__(self):
        self.name = ""
        self.version = ""
        self.port = ""
        self.local_jar = False
        self.local_jar_mode = 0
        self.local_jar_file = ""
        self.attribute = ""
        self.start_jar_file = ""

class LocalJarFileClass:
    def __init__(self):
        self.install_jar_file = ""

# 入力関数
def input_server_info():
    name = input("サーバーの名前を入力してください：")
    while True:
        input_choice_text = "\n[Nでスキップできます。]サーバーのjarを持っている場合などではjarを読み込むことができます。\n例えば：Forgeをインストールしたい場合はM(mod)を選択してください。\n普通のjarファイル（spigotなど）を読み込む場合はY(Yes)を選択してください。"
        #if ini['autoer_info']['language'] == "en-us":
        #    input_choice_text = "[input `N` is skip]If you have the server jar you can load the jar file. \nFor example: If you want to install Forge, select M(mod). \nSelect Y (Yes) if you want to load a normal jar file (such as spigot)."
        choice = input(input_choice_text+"[Y/N/M]：").lower()
        # yes(普通ローカルjarモード)の動作
        if choice in ["yes", "ye", "y"]:
            local_jar = True
            local_jar_mode = 1
            while True:
                input_jar_file = input("ファイルのファイル場所＋/ファイルの名前を記入してください\n例[/home/solo/Desktop/server_jar/my_server_jar.jar]：")
                if not os.file.exists(input_jar_file):
                    print("ファイルが存在しません")
                    continue
                local_jar_file = input_jar_file
                version = ""
                break
            break
        # mod(Forgeモード)の動作
        elif choice in ["mod", "mo", "m"]:
            local_jar = True
            local_jar_mode = 2
            while True:
                input_jar_file_install = input("インストール用jarファイルのファイル場所＋/ファイルの名前を記入してください\n例[/home/solo/Desktop/server_jar/forge_install.jar]：")
                if not os.path.exists(input_jar_file_install):
                    print("ファイルが存在しません")
                    continue
                local_jar_file = input_jar_file_install
                version = ""
                break
            break
        elif choice in ["no", "n"]:
            local_jar = True
            local_jar_mode = 0
            local_jar_file = "nofile"
            version = input("サーバーのバージョンを入力してください：")
            break
        print("その項目は存在しません")
    while True:
        port = input("ポートを入力してください：")
        if not port or not str.isnumeric(port):
            continue
        else:
            break
    # server_add_or_one_more = input("作成方法を選んでください\nadd:すぐに作成する\nplural:もう一つ作成する\n（注意：未入力・それ以外の場合はaddになります）\n選択してください[A/p]：").lower()
    server_add_or_one_more = "add"
    if not name:
        name = "デフォルト（未入力）"
    if not port or not str.isnumeric(port):
        port = "25565"
    if int(port) < 0 or int(port) > 65535:
        port = "25565"
    if server_add_or_one_more in ["add", "ad", "a"]:
        return True, name, version, port, local_jar, local_jar_mode, local_jar_file
    elif server_add_or_one_more in ["plural", "plura", "plur", "plu", "pl", "p"]:
        return False, name, version, port, local_jar, local_jar_mode, local_jar_file
    else:
        return True, name, version, port, local_jar, local_jar_mode, local_jar_file
#　作成関数
def make():
    print("\n作成モード")
    # サーバー作成　ループ処理
    server_count = 1
    while True:
        server = InputInfoClass()
        # print(server_count,"個目")
        input_choice = input_server_info()
        server.name = input_choice[1]
        server.version = input_choice[2]
        server.port = input_choice[3]
        server.local_jar = input_choice[4]
        server.local_jar_mode = input_choice[5]
        server.local_jar_file = input_choice[6]
        exec("server_"+str(server_count)+" = server")
        if input_choice[0]:
            break
        # 複数の設定にしたらcountを増やしてスキップ
        elif not input_choice[0]:
            server_count = server_count + 1
            continue
    # EULA同意画面
    choice = etc_server.input_yes_no("\nEULA・ソフトウェア利用許諾契約に同意しますか？\nMinecraftのEULAに関してはこちらをご覧ください\nhttps://www.minecraft.net/ja-jp/eula\nYes Noで選択してください[Y/n]：")
    # for文で回数分作成
    for i in range(server_count):
        i = i + 1
        dt_now = datetime.datetime.now()
        const.minecraft_dir = "minecraft/minecraft-"+dt_now.strftime('%Y-%m-%d-%H-%M-%S-%f')
        os.mkdir(const.minecraft_dir)
        # execでclassの変数をserver_?をserverに格納
        exec("server = server_"+str(i))
        print(server.name)
        detailed_day = etc_server.setting_week_day_or_month(dt_now)
        if server.local_jar:
            local_jar = LocalJarFileClass()
            # もし通常のローカルJarモードだった処理
            if server.local_jar_mode == 1:
                server.attribute = "local-jar"
                server.version = "unknown"
                shutil.copy(server.local_jar_file, const.minecraft_dir+"/server.jar")
                server.start_jar_file = "server.jar"
            elif server.local_jar_mode == 2:
                server.attribute = "local-jar-mod"
                server.version = "unknown"
                # 入力されたファイル（名）をlocal_jarのクラス
                local_jar.install_jar_file = os.path.basename(server.local_jar_file)
                # forgeのインストーラーの最後の文字 -installer(インストール用プログラムを意味する)を消してサーバー起動用jarの名前にする
                server.start_jar_file = local_jar.install_jar_file.replace('-installer', '')
                shutil.copy(server.local_jar_file, const.minecraft_dir+"/"+local_jar.install_jar_file)
            else:
                server.attribute = "default-jar"
                # try文でダウンロード時に不都合（ネットワーク未接続など）が発生したときの例外処理ができるようにする
                try:
                    while True:
                        minecraft_jar_version = etc_server.select_minecraft_version_line_conversion(server.version, new_version, True)
                        # 入力したバージョンがcase内に存在しないとき（default）の処理
                        if minecraft_jar_version[1]:
                            while True:
                                server.version = input("バージョンを入力してください：")
                                # ”再入力”したバージョンがcase内に存在するか確認する処理
                                minecraft_jar_version = etc_server.select_minecraft_version_line_conversion(server.version, new_version, False)
                                # 入力したバージョンがcase内に存在しないとき（default）の処理
                                if minecraft_jar_version:
                                    continue
                                # case内に存在するときの処理
                                else:
                                    break
                        else:
                            break
                    # マイクラjarファイルダウンロード
                    etc_server.download(minecraft_jar_version[2], const.minecraft_dir+"/server.jar")
                    server.start_jar_file = "server.jar"
                # ダウンロード時の例外処理
                except Exception as e:
                    print("ダウンロードでエラーが発生しました。\nエラー内容\n"+str(e))
                    sys.exit(1)
        # eula.txtファイル上書き
        etc_server.write_file(const.minecraft_dir+"/eula.txt", "#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n#"+detailed_day[1]+" "+detailed_day[0]+" "+dt_now.strftime('%d')+" "+dt_now.strftime('%H:%M:%S')+" "+str(dt_now.tzinfo)+" "+dt_now.strftime('%Y')+"\neula="+str(choice))
        # server.propertiesをダウンロードする
        etc_server.download_text("https://server.properties/",const.minecraft_dir+"/server.properties")
        # server.propertiesのポート設定欄を変更する
        etc_server.file_identification_rewriting(const.minecraft_dir+"/server.properties", "server-port=", "server-port="+server.port+"\n")
        # server.propertiesのmotdをサーバー名に変更する
        etc_server.file_identification_rewriting(const.minecraft_dir+"/server.properties", "motd=", "motd="+server.name+"\n")
        if server.local_jar_mode == 2:
            etc_server.exec_java(const.minecraft_dir, local_jar.install_jar_file, "1", "1", "--installServer")
        # minecraft-list.txtの行数のカウント
        minecraft_server_list_txt_lines_count = sum([1 for _ in open('data/minecraft-list.txt', encoding="utf-8")])

        # サーバーリスト編集
        with open('data/minecraft-list.txt', 'a', encoding="utf-8") as f:
            print("["+str(minecraft_server_list_txt_lines_count + 1)+"] Server name: "+server.name+" | Creation time: "+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')[:-3]+" | Server Version (Local Jar is Unknown): "+server.version+" | Minecraft Server Directory: "+const.minecraft_dir+"/", file=f)
        with open('data/minecraft-dir-list.txt', 'a', encoding="utf-8") as f:
            print(const.minecraft_dir, file=f)
        # サーバーディレクトリに管理用iniファイルを作成
        with open("data/"+const.minecraft_dir.replace('/', '-')+".txt", 'w', encoding="UTF-8") as f:
            print(server.version+"\n"+server.attribute+"\n"+server.start_jar_file, file=f)
    print("インストールが終わりました\n管理（Control）から実行できます。")

if __name__ == "__main__":
    # Q.FastServer?
    # A.No. This is GuppiServer
    # ?.Audio

    cmd_input = sys.argv
    if len(cmd_input) >= 2:
        if cmd_input[1] == "-fast-make":
            make()
