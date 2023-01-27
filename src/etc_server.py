from urllib.request import Request, urlopen
import urllib

# マインクラフトのバージョン別のダウンロードURLが書いている配列
minecraft_download_link_list = [
    'https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar', #1.16.5
    'https://launcher.mojang.com/v1/objects/0a269b5f2c5b93b1712d0f5dc43b6182b9ab254e/server.jar', #1.17
    'https://launcher.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar', #1.17.1
    'https://launcher.mojang.com/v1/objects/3cf24a8694aca6267883b17d934efacc5e44440d/server.jar', #1.18
    'https://launcher.mojang.com/v1/objects/125e5adf40c659fd3bce3e66e67a16bb49ecc1b9/server.jar', #1.18.1
    'https://launcher.mojang.com/v1/objects/c8f83c5655308435b3dcf03c06d9fe8740a77469/server.jar', #1.18.2
    'https://launcher.mojang.com/v1/objects/e00c4052dac1d59a1188b2aa9d5a87113aaf1122/server.jar', #1.19
    'https://piston-data.mojang.com/v1/objects/8399e1211e95faa421c1507b322dbeae86d604df/server.jar', #1.19.1
    'https://piston-data.mojang.com/v1/objects/f69c284232d7c7580bd89a5a4931c3581eae1378/server.jar', #1.19.2
    'https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar' #1.19.3
]

# ファイルに書き込む関数
def file_write(file, text):
    f = open(file, 'w')
    f.write(text)
    f.close()

# 続行・同意するか確認する関数
def input_yes_no(text):
    while True:
        choice = input(text)
        if choice in ["yes", "ye", "y"]:
            return True
        elif choice in ["no", "n"]:
            return False
# 普通にダウンロードする関数
def download(url, save_name):
    urllib.request.urlretrieve(url, save_name)
# テキストに書き込むダンロード関数（ユーザーエージェント偽装済み）
def download_text(url, file_name):
    # そのままだとurllib.error.HTTPError: HTTP Error 403: Forbiddenでコケるからユーザーエージェントを偽装
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = Request(url, headers=headers)
    html = urlopen(request).read()
    html = html.decode('utf-8')
    # ファイル書き込み(server.properties)
    file = open(file_name, mode='w')
    file.write(str(html))
    file.close()

# 曜日と月を3文字に変換する関数
def setting_week_day_or_month(dt_now):
    # 月をmatch.caseで設定する(3文字)
    match dt_now.strftime('%m'):
        case "01": month="Jan"
        case "02": month="Feb"
        case "03": month="Mar"
        case "04": month="Apr"
        case "05": month="May"
        case "06": month="Jun"
        case "07": month="Jul"
        case "08": month="Aug"
        case "09": month="Sep"
        case "10": month="Oct"
        case "11": month="Nov"
        case "12": month="Dec"
    # 曜日をmatch.caseで設定する(3文字)
    match dt_now.weekday():
        case 0: day_of_week="Sun"
        case 1: day_of_week="Mon"
        case 2: day_of_week="Tue"
        case 3: day_of_week="Wed"
        case 4: day_of_week="Thu"
        case 5: day_of_week="Fri"
        case 6: day_of_week="Sat"
    return month,day_of_week

def select_minecraft_version_line_conversion(input_version, new_version, output):
    match input_version:
        case "1.19.3": minecraft_server_link_lines = 9
        case "1.19.2": minecraft_server_link_lines = 8
        case "1.19.1": minecraft_server_link_lines = 7
        case "1.19": minecraft_server_link_lines   = 6
        case "1.18.2": minecraft_server_link_lines = 5
        case "1.18.1": minecraft_server_link_lines = 4
        case "1.18": minecraft_server_link_lines   = 3
        case "1.17.1": minecraft_server_link_lines = 2
        case "1.17": minecraft_server_link_lines   = 1
        case "1.16.5": minecraft_server_link_lines = 0
        case _:
            while True:
                if output:
                    problem_text = "そのバージョンは存在しないまたは、全角などで書いている可能性があります\nデフォルトだと"+new_version+"(最新)が適用されます。\nただし、これを決めるのは責任者（親やサーバー管理者など）です。\nもし、このような管理者などがいた場合には、その人の指示に従うのが望ましいと思われます。\n変更したい場合はY(Yes)・デフォルトのバージョン["+new_version+"]に設定したい場合はN(No)を選択してください。\n[Y/n]: "
                    choice = input("インストール中に問題が発生しました\n内容:\n"+problem_text).lower()
                    if choice in ["yes", "ye", "y"]:
                        return True, True, ""
                    elif choice in ["no", "n"]:
                        minecraft_server_link_lines = 9
                        return True, False, minecraft_download_link_list[minecraft_server_link_lines]
                    else:
                        continue
                # outputがFalse(エラーが表示されない)引数で呼び出したときの処理
                elif not output:
                    return True

    if output:
        return False, False, minecraft_download_link_list[minecraft_server_link_lines]
    # outputがFalseだったときの処理
    elif not output:
        return False
    else:
        return False, False, minecraft_download_link_list[minecraft_server_link_lines]

# 特定の文字列の行を書き換える関数
def replace_func(fname, replace_set):
    target, replace = replace_set

    with open(fname, 'r') as f1:
        tmp_list =[]
        for row in f1:
            if row.find(target) != -1:
                tmp_list.append(replace)
            else:
                tmp_list.append(row)

    with open(fname, 'w') as f2:
        for i in range(len(tmp_list)):
            f2.write(tmp_list[i])

# ↑を呼び出す関数
def file_identification_rewriting(file_name, before, after):
    replace_setA = (before, after) # (検索する文字列, 置換後の文字列)
    # call func
    replace_func(file_name, replace_setA)
