# 必要なライブラリのインポート
from time import sleep
from bs4 import BeautifulSoup
import requests
import pandas as pd

# 変数urlにairdoorサイトのURLを格納する
url = 'https://airdoor.jp/list?si=d-141011-141020-141038-141046-141054-141062-141071-141089-141097-141101-141119-141127-141135-141143-141151-141160-141178-141186&p={}'

# 物件情報を格納するリストを初期化する
property_list = []

# ページ番号が1から3までの各ページに対してループ
for i in range(1, 4):
    target_url = url.format(i)  # ページ番号をURLに埋め込む
    r = requests.get(target_url)  # ページのHTMLデータを取得する
    sleep(1)  # SUUMOサーバーへの負荷を軽減する
    soup = BeautifulSoup(r.text, 'html.parser')  # BeautifulSoupでHTMLを解析する

    # 各物件情報を取得する
    contents = soup.find_all('div', class_='PropertyPanel_propertyPanel__MqCpF')

    # 各物件情報をループで取得する
    for content in contents:
        # 物件名
        buildingTitle = content.find('div', class_='PropertyPanelBuilding_buildingTitle__NbWmb').text
        # 住所
        buildingInformation = content.find('p', class_='is-mt5').text
        # 家賃
        rentPrice = content.find('div', class_='PropertyPanelRoom_rentPrice__HO4Jp').text
        # 部屋情報（号室、間取り、㎡、方角）
        roomDetail = content.find('span', class_='is-ml5').text

        # 取得した全ての情報を辞書に格納する
        property = {
            'Title': buildingTitle,
            'address': buildingInformation,
            'price': rentPrice,
            'room_detail': roomDetail,
        }

        # 取得した辞書をproperty_listに格納する
        property_list.append(property)

# 取得したリストをdfに格納
df = pd.DataFrame(property_list)

# dfをcsvに出力
df.to_csv('airdoor.csv', index=None, encoding='utf-8-sig')
