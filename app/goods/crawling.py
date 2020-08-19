import re
import time

from selenium.common.exceptions import NoSuchElementException


def get_data():
    from selenium import webdriver
    from goods.models import Category
    from goods.models import Type
    from goods.models import GoodsType
    from goods.models import GoodsDetail
    driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')

    detail_page_list = [
        [
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26448',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49246',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27232',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=70',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=96',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53498',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54657',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31395',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54661',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=97',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50692',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=69',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37789',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50690',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54660',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=333',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27233',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26450',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43350',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31100',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37654',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49635',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37314',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50691',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49253',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44270',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49841',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3440',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36963',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54671',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53298',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52615',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51486',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3110',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50694',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3115',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50693',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38031',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49840',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36964',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51700',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50696',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52614',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49264',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54662',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27165',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48526',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48527',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38029',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38028',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3328',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50698',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55707',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30768',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42159',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51487',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41303',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37987',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48555',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41304',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52391',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36499',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55380',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47869',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38032',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41305',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38030',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48281',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55377',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41302',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55379',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55378',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43408',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48007'],
            # [
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1385',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48835',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=98',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1366',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45384',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48845',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=647',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1074',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=252',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=102',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1079',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=32142',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34133',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=177',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36965',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30612',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1072',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27319',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50252',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48834',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51953',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48833',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38267',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2718',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37934',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1078',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30610',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1076',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=5755',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36662',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42332',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48838',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=334',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36689',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1733',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1075',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11437',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36687',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27169',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=522',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56655',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42158',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42154',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=151',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7334',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50305',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36688',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35520',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7878',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1073',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34456',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50884',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53055',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50883',
            #     'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7301',

            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4176',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34461',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7299',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34278',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52398',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48837',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13278',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3320',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2658',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34455',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=454',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31369',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36690',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48840',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=5160',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45387',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48836',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36607',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45386',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26811',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48842',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48844',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36691',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9214'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=1364',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37313',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1083',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=319',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50688',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27164',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1067',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1070',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11099',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42793',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36686',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7300',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36692',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10534',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53479',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53478',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52853',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2882',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=332',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=318',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=453',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12656',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30793',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9213'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=38300',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=94',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49921',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31391',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31393',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38301',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49634',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31390',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31389',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36543',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31392',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3784',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31388',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54584',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49922',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36542',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27728',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27488',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10322',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54586',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27298',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51271',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27729',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10323',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10326',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10324',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10325',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27187',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7667'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=718',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=149',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43350',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36663',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3188',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7363',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42665',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31114',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2657',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26472',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53318',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41303',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41304',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1278',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=512',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41305',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41302'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=27318',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26451',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49248',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3469',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49920',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=95',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49252',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41020',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49247',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42157',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6117',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54885',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1734',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2811',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42160',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27166',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40984',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27771',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27461',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50697',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36664',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42788',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45605',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37669',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51425',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44660'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=30781',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30735',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49499',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1350',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7027',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27769',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27768',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27770',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55100',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6792',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=304',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40987',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49251',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27767',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55104',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51408',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41022',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=508',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51407',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50914',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=641']
    ]

    type_name_list = [
        # '기본채소',
        '쌈·샐러드·간편채소',
        '브로콜리·특수채소',
        '콩나물·버섯류',
        '시금치·부추·나물',
        '양파·마늘·생강·파',
        '파프리카·피망·고추']
    category_name = '채소'
    category_ins, __ = Category.objects.get_or_create(name=category_name)
    from goods.models import Goods
    for lst, type_name in zip(detail_page_list, type_name_list):
        type_name_ins, __ = Type.objects.get_or_create(
            name=type_name
        )
        for url in lst:
            driver.get(url)
            driver.implicitly_wait(10)
            print('------------------------------------------- start ----------------------')
            # 안전빵
            transfer = None
            packing = None
            goods_origin = None
            allergy = None
            info = None
            expiration = None
            print(url)
            # print('type_name', type_name)
            goods_image = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]').get_attribute('style')
            goods_image = goods_image.split('"')
            # print('goods_image', goods_image[1])

            goods_title = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/p[1]/strong').get_attribute('innerText')
            # print('goods_title', goods_title)

            short_desc = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/p[1]/span[2]').get_attribute('innerText')
            # print('short_desc', short_desc)

            try:
                # 미 할인 상품
                goods_price = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/p[2]/span[1]/span/span').get_attribute(
                    'innerText')
            except NoSuchElementException:
                # 할인 상품
                goods_price = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/p[3]/span[1]/span[1]/span[1]').get_attribute(
                    'innerText')

            price = re.findall('\d+', goods_price)
            result = ''
            for value in price:
                result += value
            # print('price result', result)

            goods_each_innerText = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[1]/dt').get_attribute('innerText')
            if '판매단위' in goods_each_innerText:
                goods_each = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[1]/dd').get_attribute('innerText')
                # print('goods_each', goods_each)
            elif '배송구분' in goods_each_innerText:
                transfer = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[1]/dd').get_attribute('innerText')
                # print('transfer', transfer)

            goods_each_weight = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[2]/dd').get_attribute('innerText')
            # print('goods_each_weight', goods_each_weight)

            # 배송 구분 또는 포장 타입
            transfer_innerText = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[3]/dt').get_attribute('innerText')
            if '배송구분' in transfer_innerText:
                transfer = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[3]/dd').get_attribute('innerText')
                # print('transfer', transfer)
            elif '포장타입' in transfer_innerText:
                packing = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[3]').get_attribute('innerText')
                # print('packing', packing)

            goods_origin_innerText = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[4]/dt').get_attribute('innerText')
            # print(goods_origin_innerText)
            if '원산지' in goods_origin_innerText:
                goods_origin = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[4]/dd').get_attribute('innerText')
                # print('goods_origin', goods_origin)
            elif '포장타입' in goods_origin_innerText:
                packing = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[4]/dd').get_attribute('innerText')
                # print('transfer', packing)

            # 포장 정보 또는 알레르기
            try:
                goods_packing_innerText = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[5]/dt').get_attribute('innerText')
                if '포장' in goods_packing_innerText:
                    packing = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[5]/dd').get_attribute('innerText')
                    # print('packing', packing)
                elif '알레르기' in goods_packing_innerText:
                    allergy = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[5]/dd').get_attribute('innerText')
                    # print('allergy', allergy)
            except NoSuchElementException:
                packing = None
                allergy = None

            # 안내사항, 유통기한, 안내사항
            try:

                goods_info_innerText = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dt').get_attribute('innerText')
                if '안내' in goods_info_innerText:
                    info = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dd').get_attribute('innerText')
                    # print('info', info)
                elif '유통기한' in goods_info_innerText:
                    expiration = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dd').get_attribute('innerText')
                    # print('expiration', expiration)
                elif '알레르기정보' in goods_info_innerText:
                    allergy = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dd').get_attribute('innerText')
                    # print('allergy', allergy)
            except NoSuchElementException:
                info = None
                expiration = None
                allergy = None

            try:
                image_one = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[3]/div/div[1]/div/div/div[1]/img').get_attribute('src')
            # print('image_one', image_one)
            except NoSuchElementException:
                print('----------------------건너 뜁니다!!!')
                continue

            text_one_title = driver.find_element_by_xpath(
                '//*[@id="goods-description"]/div/div[1]/div[2]/h3/small').get_attribute('innerText')
            # print('text_one_title', text_one_title)

            text_one_context_dummy = driver.find_element_by_xpath(
                '//*[@id="goods-description"]/div/div[1]/div[2]/h3').get_attribute('innerText')

            text_one_context_dummy = text_one_context_dummy.split('\n')
            text_one_context = ''
            for i in text_one_context_dummy[1:]:
                text_one_context += i + ' '
            # print('text_one_context', text_one_context)

            text_one_description = driver.find_element_by_xpath(
                '//*[@id="goods-description"]/div/div[1]/div[2]/p').get_attribute('innerText')
            # print('text_one_description', text_one_description)
            try:
                check_point_image = driver.find_element_by_xpath(
                    '//*[@id="goods-description"]/div/div/div/div/img').get_attribute('src')
                # pri nt('check_point_image', check_point_image)
            except NoSuchElementException:
                check_point_image = None

            info_image = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[3]/div/div[2]/div/p/img').get_attribute('src')
            # print('info_image', info_image)

            print(goods_image[1])
            print(info_image)
            print(goods_title)
            print(short_desc)
            print(result)
            print(goods_each)
            print(goods_each_weight)
            print(transfer)
            print(packing)
            print(goods_origin)
            print(allergy)
            print(info)
            print(expiration)

            print(image_one)
            print(text_one_title)
            print(text_one_context)
            print(text_one_description)
            print(category_ins)

            goods_ins, created = Goods.objects.get_or_create(
                img=goods_image[1],
                info_img=info_image,
                title=goods_title,
                short_desc=short_desc,
                price=result,
                each=goods_each,
                weight=goods_each_weight,
                transfer=transfer,
                packing=packing,
                origin=goods_origin,
                allergy=allergy,
                info=info,
                expiration=expiration,

                img_1=image_one,
                text_1_title=text_one_title,
                text_1_context=text_one_context,
                text_1_description=text_one_description,
                category=category_ins,
            )
            print(goods_ins, created)

            # 디테일 정보
            var_titles = driver.find_elements_by_xpath('//*[@id="goods-infomation"]/table/tbody/tr/th')
            var_descs = driver.find_elements_by_xpath('//*[@id="goods-infomation"]/table/tbody/tr/td')

            # for index, desc in enumerate(var_descs):
            #     title = var_titles[index].get_attribute('innerText')
            # print(title)
            # print(desc.get_attribute('innerText'), '\n')
            # print(len(var_titles))
            if len(var_titles) == 0:
                pass
            elif len(var_titles) == 8:
                GoodsDetail.objects.create(
                    goods=goods_ins,
                    var_1_title=var_titles[0],
                    var_1_desc=var_descs[0],
                    var_2_title=var_titles[1],
                    var_2_desc=var_descs[1],
                    var_3_title=var_titles[2],
                    var_3_desc=var_descs[2],
                    var_4_title=var_titles[3],
                    var_4_desc=var_descs[3],
                    var_5_title=var_titles[4],
                    var_5_desc=var_descs[4],
                    var_6_title=var_titles[5],
                    var_6_desc=var_descs[5],
                    var_7_title=var_titles[6],
                    var_7_desc=var_descs[6],
                    var_8_title=var_titles[7],
                    var_8_desc=var_descs[7],
                )
            elif len(var_titles) == 10:
                GoodsDetail.objects.create(
                    goods=goods_ins,
                    var_1_title=var_titles[0],
                    var_1_desc=var_descs[0],
                    var_2_title=var_titles[1],
                    var_2_desc=var_descs[1],
                    var_3_title=var_titles[2],
                    var_3_desc=var_descs[2],
                    var_4_title=var_titles[3],
                    var_4_desc=var_descs[3],
                    var_5_title=var_titles[4],
                    var_5_desc=var_descs[4],
                    var_6_title=var_titles[5],
                    var_6_desc=var_descs[5],
                    var_7_title=var_titles[6],
                    var_7_desc=var_descs[6],
                    var_8_title=var_titles[7],
                    var_8_desc=var_descs[7],
                    var_9_title=var_titles[8],
                    var_9_desc=var_descs[8],
                    var_10_title=var_titles[9],
                    var_10_desc=var_descs[9],
                )
            # else:
            # for index in range(len(var_titles)):

            # 타입 명시
            print(type_name_ins)
            print(goods_ins)
            goodstype_ins, created = GoodsType.objects.get_or_create(type=type_name_ins, goods=goods_ins)
            print(goodstype_ins, created)


def crawling():
    get_data()
