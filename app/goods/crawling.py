import os
import re
import urllib

from django.core.files import File
from django.db import DataError
from selenium.common.exceptions import NoSuchElementException

from config.settings.base import MEDIA_ROOT


def get_data():
    from selenium import webdriver
    from goods.models import Goods
    from goods.models import Category
    from goods.models import Type
    from goods.models import GoodsType
    from goods.models import GoodsDetail
    from goods.models import GoodsExplain
    from goods.models import GoodsDetailTitle

    driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')

    all_goods_url_list = get_urls()

    type_name_list = get_type()
    category_list = get_categories()

    for category_index, category_urls in enumerate(all_goods_url_list):
        category_ins, created = Category.objects.get_or_create(name=category_list[category_index])
        for type_index, type_urls in enumerate(category_urls):
            for index, url in enumerate(type_urls):
                try:
                    print(category_ins.name)
                    type_name_ins, __ = Type.objects.get_or_create(
                        name=type_name_list[category_index][type_index],
                        category=category_ins
                    )
                    print(type_name_ins.name)
                    driver.get(url)
                    driver.implicitly_wait(10)
                    print('------------------------------------------- start ----------------------')
                    # 안전빵
                    transfer = None
                    packing = None
                    goods_origin = None
                    goods_each = None
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
                            '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[1]/dd').get_attribute(
                            'innerText')
                        # print('goods_each', goods_each)
                    elif '배송구분' in goods_each_innerText:
                        transfer = driver.find_element_by_xpath(
                            '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[1]/dd').get_attribute(
                            'innerText')
                        # print('transfer', transfer)

                    goods_each_weight = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[2]/dd').get_attribute('innerText')
                    # print('goods_each_weight', goods_each_weight)

                    # 배송 구분 또는 포장 타입
                    try:
                        transfer_innerText = driver.find_element_by_xpath(
                            '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[3]/dt').get_attribute(
                            'innerText')
                        if '배송구분' in transfer_innerText:
                            transfer = driver.find_element_by_xpath(
                                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[3]/dd').get_attribute(
                                'innerText')
                            # print('transfer', transfer)
                        elif '포장타입' in transfer_innerText:
                            packing = driver.find_element_by_xpath(
                                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[3]').get_attribute(
                                'innerText')
                            # print('packing', packing)
                    except NoSuchElementException:
                        pass

                    try:
                        goods_origin_innerText = driver.find_element_by_xpath(
                            '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[4]/dt').get_attribute(
                            'innerText')
                        # print(goods_origin_innerText)
                        if '원산지' in goods_origin_innerText:
                            goods_origin = driver.find_element_by_xpath(
                                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[4]/dd').get_attribute(
                                'innerText')
                            # print('goods_origin', goods_origin)
                        elif '포장타입' in goods_origin_innerText:
                            packing = driver.find_element_by_xpath(
                                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[4]/dd').get_attribute(
                                'innerText')
                            # print('transfer', packing)
                    except NoSuchElementException:
                        pass

                    # 포장 정보 또는 알레르기
                    try:
                        goods_packing_innerText = driver.find_element_by_xpath(
                            '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[5]/dt').get_attribute(
                            'innerText')
                        if '포장' in goods_packing_innerText:
                            packing = driver.find_element_by_xpath(
                                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[5]/dd').get_attribute(
                                'innerText')
                            # print('packing', packing)
                        elif '알레르기' in goods_packing_innerText:
                            allergy = driver.find_element_by_xpath(
                                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[5]/dd').get_attribute(
                                'innerText')
                            # print('allergy', allergy)
                    except NoSuchElementException:
                        packing = None
                        allergy = None

                    # 안내사항, 유통기한, 안내사항
                    try:
                        goods_info_innerText = driver.find_element_by_xpath(
                            '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dt').get_attribute(
                            'innerText')
                        if '안내' in goods_info_innerText:
                            info = driver.find_element_by_xpath(
                                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dd').get_attribute(
                                'innerText')
                            # print('info', info)
                        elif '유통기한' in goods_info_innerText:
                            expiration = driver.find_element_by_xpath(
                                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dd').get_attribute(
                                'innerText')
                            # print('expiration', expiration)
                        elif '알레르기정보' in goods_info_innerText:
                            allergy = driver.find_element_by_xpath(
                                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dd').get_attribute(
                                'innerText')
                            # print('allergy', allergy)
                    except NoSuchElementException:
                        info = None
                        expiration = None
                        allergy = None

                    try:
                        image_one = driver.find_element_by_xpath(
                            '/html/body/div/div[2]/div[2]/div/div[3]/div/div[1]/div/div/div[1]/img').get_attribute(
                            'src')
                    # print('image_one', image_one)
                    except NoSuchElementException:
                        print('----------------------건너 뜁니다!!!')
                        continue

                    text__title = driver.find_element_by_xpath(
                        '//*[@id="goods-description"]/div/div[1]/div[2]/h3/small').get_attribute('innerText')
                    # print('text__title', text__title)

                    text__context_dummy = driver.find_element_by_xpath(
                        '//*[@id="goods-description"]/div/div[1]/div[2]/h3').get_attribute('innerText')

                    text__context_dummy = text__context_dummy.split('\n')
                    text__context = ''
                    for i in text__context_dummy[1:]:
                        text__context += i + ' '
                    # print('text__context', text__context)

                    text__description = driver.find_element_by_xpath(
                        '//*[@id="goods-description"]/div/div[1]/div[2]/p').get_attribute('innerText')
                    # print('text__description', text__description)
                    try:
                        check_point_image = driver.find_element_by_xpath(
                            '//*[@id="goods-description"]/div/div/div/div/img').get_attribute('src')
                        # pri nt('check_point_image', check_point_image)
                    except NoSuchElementException:
                        check_point_image = None

                    info_image = driver.find_element_by_xpath(
                        '//*[@id="goods_pi"]/p/img').get_attribute('src')
                    # print('info_image', info_image)

                    # print(goods_image[1])
                    # print(info_image)
                    # print(goods_title)
                    # print(short_desc)
                    # print(result)
                    # print(goods_each)
                    # print(goods_each_weight)
                    # print(transfer)
                    # print(packing)
                    # print(goods_origin)
                    # print(allergy)
                    # print(info)
                    # print(expiration)
                    #
                    # print(image_one)
                    # print(text__title)
                    # print(text__context)
                    # print(text__description)
                    # print(category_ins)

                    # 이미지 생성
                    try:
                        GOODS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'goods/{goods_title}/')
                        if not os.path.exists(GOODS_IMAGE_DIR):
                            os.makedirs(GOODS_IMAGE_DIR, exist_ok=True)
                        image_save_name = os.path.join(GOODS_IMAGE_DIR, f'{goods_title}_goods_image.jpg')
                        urllib.request.urlretrieve(goods_image[1], image_save_name)

                        main_image = open(os.path.join(GOODS_IMAGE_DIR, f'{image_save_name}'), 'rb')

                        image_save_name2 = os.path.join(GOODS_IMAGE_DIR, f'{goods_title}_info_image.jpg')
                        urllib.request.urlretrieve(info_image, image_save_name2)

                        info_image = open(os.path.join(GOODS_IMAGE_DIR, f'{image_save_name2}'), 'rb')

                        image_save_name3 = os.path.join(GOODS_IMAGE_DIR, f'{goods_title}_image_one.jpg')
                        urllib.request.urlretrieve(image_one, image_save_name3)

                        extra_image = open(os.path.join(GOODS_IMAGE_DIR, f'{image_save_name3}'), 'rb')
                    except FileNotFoundError:
                        print(' 건너 뜁니다 !_________________________________________________')
                        continue
                    print('File')
                    print(File(main_image))
                    try:
                        goods_ins = Goods.objects.get(title=goods_title, price=result)
                        created = False

                    except Goods.DoesNotExist:
                        goods_ins = Goods.objects.create(
                            img=File(main_image),
                            info_img=File(info_image),
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
                            category=category_ins,
                        )
                        created = True
                    print(goods_ins, created)

                    goods_explain, created = GoodsExplain.objects.get_or_create(
                        img=File(extra_image),
                        text_title=text__title,
                        text_context=text__context,
                        text_description=text__description,

                        goods=goods_ins,
                    )
                    # print('goods_explain, created', goods_explain, created)

                    # 디테일 정보
                    var_titles = driver.find_elements_by_xpath('//*[@id="goods-infomation"]/table/tbody/tr/th')
                    var_descs = driver.find_elements_by_xpath('//*[@id="goods-infomation"]/table/tbody/tr/td')
                    # print('var_titles>>>>>>>>>>>>>>>>>.', var_titles)
                    # print('var_descs >>>>>>>>>>>>>>>>>>', var_descs)
                    if len(var_titles) >= 1:
                        for var_detail_title, var_detail_desc in zip(var_titles, var_descs):
                            detail_goods_title_ins, created = GoodsDetailTitle.objects.get_or_create(
                                title=var_detail_title.get_attribute('innerText')
                            )
                            # print(var_detail_title.get_attribute('innerText'))
                            # print(var_detail_desc.get_attribute('innerText'), '\n')
                            detail_ins, created = GoodsDetail.objects.get_or_create(
                                detail_title=detail_goods_title_ins,
                                detail_desc=var_detail_desc.get_attribute('innerText'),
                                goods=goods_ins,
                            )
                            # print('goods_detail_ins, created', detail_ins, created)
                    # 타입 명시
                    # print(type_name_ins)
                    # print(goods_ins)
                    goodstype_ins, created = GoodsType.objects.get_or_create(type=type_name_ins, goods=goods_ins)
                    # print(goodstype_ins, created)
                except DataError:
                    continue


def crawling():
    get_data()


def get_urls():
    url_list = [
        # [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=26448',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49246',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27232',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30559',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=70',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=96',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53498',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31395',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54661',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54657',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26450',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=69',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50692',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54660',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=97',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50690'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=1385',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48835',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45384',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=98',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48845',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1366',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=32142',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=647',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=252',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1074',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48834',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27319',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30612',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48833',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56655',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=102'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=1364',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37313',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=319',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27164',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42793',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11099',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1070',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1067',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36686',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=434',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53478',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36692',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53479',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10534',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=332',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=318'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=38300',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=94',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49921',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31391',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31393',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38301',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49634',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31389',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31390',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36543',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31392',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3784',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31388',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54584',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49922',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36542'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=718',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=149',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43350',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36663',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3188',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7364',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1735',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42665',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31114',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2657',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53318',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26472',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41303',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41304',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1278',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=512'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=27318',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26451',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27320',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49248',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49920',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3469',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49252',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42157',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49247',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=95',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41020',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6117',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54885',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2811',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1734',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50697'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=30781',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30735',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49499',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1350',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27769',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27770',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27768',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7027',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6792',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=304',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49251',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40987',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27767',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42790',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55104',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41022']],
        # [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=38256',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27611',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38123',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3741',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52556',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27228',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29439',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=8772',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7187',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52555',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56015',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55694',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6426',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3690',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=57098',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54482'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=53164',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=99',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38256',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29438',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51900',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30766',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3380',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29437',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38123',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49265',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36814',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=100',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3741',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52556',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53495',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3125'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=491',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31441',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=267',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36748',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31882',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27611',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=330',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31443',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=79',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31442',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49846',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35693',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49628',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35954',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26576',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30849'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=3389',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3393',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54840',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=39670',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4182',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3644',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49256',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4824',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51353',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54884',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45840',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35702',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54843',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11319',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54842',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6576'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=54492',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54490',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54491',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27971',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54496',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36934',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9502',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50258',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54494',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52368',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51672',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37513',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12471',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27970',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1238',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50260'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=3173',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1363',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25578',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4278',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31424',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1248',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51034',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1358',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7002',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51037',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45607',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51036',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37790',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1646',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49132',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26044']],
        # [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=1391',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53512',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47711',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45300',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43698',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48540',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53513',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43697',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53884',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37066',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=5451',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13611',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35952',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53508',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52832',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51705'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=29565',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51757',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10870',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53934',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4289',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48536',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10316',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9985',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13275',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30143',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55383',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49889',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29562',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25418',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26401',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34038'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=54074',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29524',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42356',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29629',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31379',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37257',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55131',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34930',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42444',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13127',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54153',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56554',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37254',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4297',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44640',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37114'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=34322',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49995',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37627',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49139',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49135',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13474',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31658',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31659',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29386',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42439',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43508',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13272',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25954',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42444',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42919',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49136'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=27202',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52957',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26587',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37914',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12973',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11540',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34124',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48263',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35003',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54411',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6807',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52956',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55123',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35000',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37053',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52475'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=50422',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3446',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37914',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50056',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4778',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25861',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26854',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52202',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53702',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45278',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55130',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34250',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25862',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9879',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44113',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12986'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=50362',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30822',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51727',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42283',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51709',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51729',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27311',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9878',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51710',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27500',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43351',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3673',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9877',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27211',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51728',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53268']],
        # [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=57308',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=57310',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56504',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55966',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55949',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55946',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55674',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55673',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54880',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54447',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54438',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54430',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54434',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54436',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54437',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54397'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=55460',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55459',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56512',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56511',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56509',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55175',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54225',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54224',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54223',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54189',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54065',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54064',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54063',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54062',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54060',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54054'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=48529',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51888',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51890',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51889',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53113',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50569',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48168',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41405',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41404',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41773',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41772',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41764',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40907',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38290',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38008',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37933'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=55295',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54190',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54067',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54191',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50290',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52477',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52101',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52100',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51141',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49822',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48567',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48566',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48565',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48564',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48563',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47887'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=55917',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55916',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56012',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56440',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55672',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55821',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55820',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55819',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55459',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55460',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55304',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55298',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55297',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54879',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54502',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54889'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=51308',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51307',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51306',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47720',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43800',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43799',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43796',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41741',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41740',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36445',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35943',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35942',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31195',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31193',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26205',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6152']],
        # [
        #     ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=48639',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42765',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11633',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48646',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48745',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53979',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1235',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53932',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48746',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38126',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53733',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48260',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49761',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55073',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41783',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44756'],
        #     ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=53794',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54583',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48018',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=32289',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48528',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48023',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11284',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41439',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=32292',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40874',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53071',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36962',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36460',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36694',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26557',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53795'],
        #     [
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52957',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26587',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10142',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54983',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26690',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26687',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48571',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6807',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26688',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52956',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7222',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52959',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52958',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45566',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4475',
        #         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10141'],
        #     ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=51488',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51489',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30068',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53794',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6503',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=5474',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3664',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4180',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6482',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38249',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38297',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12973',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13709',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54560',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34568',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6481'],
        #     ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=52131',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49239',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26566',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27606',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1680',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31351',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11540',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3535',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=341',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48706',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29534',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13002',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54502',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52924',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11473',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43023'],
        #     ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=50290',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25888',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27202',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31864',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30594',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=5051',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27013',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40874',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=32137',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36694',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50567',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43904',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53486',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52237',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31491',
        #      'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13402']],
        # [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=9669',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49301',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48499',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42318',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42019',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42846',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52807',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41351',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35919',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31078',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54555',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41057',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41353',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47999',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48513',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44581'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=27449',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43337',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50290',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26847',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35970',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44534',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48310',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52203',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48186',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51264',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49819',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25443',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41697',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52644',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42765',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52635'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=25689',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48639',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9755',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10146',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41350',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11248',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26926',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41728',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31706',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9224',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3490',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54588',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41057',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53787',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41044',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47867'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=42479',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6081',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1229',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11151',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53378',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1305',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53379',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6572',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26436',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31973',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26937',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9619',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54699',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7664',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27687',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52526'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=27876',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50290',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29682',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31377',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11236',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6905',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4570',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34557',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52324',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50834',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54545',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31645',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31956',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9421',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34558',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7226'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=2749',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13266',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43576',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55571',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1227',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11230',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36742',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35939',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10354',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41620',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11229',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9534',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11223',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35940',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11225',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11226']],
        # [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=53977',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31466',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37555',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31454',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1269',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36731',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26926',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42730',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44505',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4504',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54833',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37061',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27812',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36698',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51641',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48517'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=26232',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36145',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4237',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4365',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54699',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13521',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45187',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4402',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4364',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42865',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34364',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45186',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29847',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49724',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37363',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42862'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=31466',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31454',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9467',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36731',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31188',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6477',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35376',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1277',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36150',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41172',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36962',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13463',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40908',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36866',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49453',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49787'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=48639',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52812',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31466',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36972',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26061',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12949',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48049',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41875',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52907',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4393',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41230',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27461',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12950',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4546',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34971',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41256'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=11475',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35040',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52136',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1737',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=551',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47787',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44470',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13725',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49766',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54185',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52771',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26292',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53904',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27694',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35037',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1688'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=325',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=343',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55518',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6331',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4517',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31651',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30776',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48274',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=355',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55520',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34441',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36753',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49237',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40973',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=342',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=8908']],
        # [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=4497',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27520',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35470',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36820',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52096',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31431',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38305',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54604',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30569',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53097',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1234',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54320',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9713',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35425',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47863',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26820'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=49857',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48752',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38168',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52819',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52365',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40752',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31482',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43583',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38159',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34162',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37246',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26518',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55258',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38275',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37633',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49419'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=48086',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48666',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3702',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44571',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3071',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=8844',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35448',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31154',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34152',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34748',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45156',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49727',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47640',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41247',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12993',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7540'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=9413',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55487',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13500',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27191',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49544',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53014',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44737',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51333',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53852',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13628',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4190',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53102',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48004',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56324',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=32123',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55485'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=55242',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48236',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50530',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52014',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52673',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4570',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54238',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29710',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51338',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34997',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35846',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35494',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50842',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50864',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31420',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52015'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=42479',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50530',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26746',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38276',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52573',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6081',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31464',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54020',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9884',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53773',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3643',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12291',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4278',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55010',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43922',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54150'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=40710',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42109',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55428',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42099',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42506',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1289',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51310',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4920',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40442',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50336',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42308',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43116',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49988',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25785',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50479',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27342']],
        # 빵
        # [
            # [
             # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54967',
             # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55984',
             #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55983',
             # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55982',
             # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55500',
             # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55144',
             # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55143',
             # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54647',
             # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54648',
             # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53986',
             # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53987',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53988',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53989',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53990',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53991',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53992'],
            # ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=55397',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55398',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53376',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53377',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54213',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55483',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53847',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54116',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54629',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54631',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54595',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55219',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55223',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55238',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55237',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55232'],
            # ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=56859',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55274',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55503',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55502',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55501',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54139',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54041',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54040',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54039',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54137',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49726',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9371',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54404',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54151',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54980',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53746'],
            # ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=56319',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56318',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56591',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56588',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56194',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56193',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56192',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53588',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53587',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54509',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54508',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55684',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55685',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54119',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48664',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55678'],
            # ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=56012',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53944',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53879',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53878',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53586',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51575',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51578',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51576',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51577',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49774',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49775',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49776',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49777',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49778',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44658',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44656'],
            # ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=48664',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53878',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53879',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53944',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48038',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48037',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48036',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48035',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48034',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45246',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45244',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44469',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44468',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44467',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44466',
            #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44465']],
        # heath food
        # [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=52096',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11021',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52682',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31986',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37040',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42152',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=39502',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26292',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42658',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54721',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51600',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36208',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55439',
        #   'https://www.kurly.com/shop/goods/goods_view.php?&goodsno=31986',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51216',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31064'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=47787',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45462',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26039',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52665',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41272',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47788',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31684',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25774',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48569',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31488',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41269',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43945',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25684',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45658',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52667',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26439'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=51185',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50910',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42143',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55718',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51144',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47890',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26596',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54082',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47889',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47894',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51146',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51600',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50391',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42144',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52890',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55411'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=51215',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34287',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26348',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26349',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26376',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41742',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49460',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13152',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27921',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45157',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45158',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27922',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45743',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55855',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40664',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53291'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=49159',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44335',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34287',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49724',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37363',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51509',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53833',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50288',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48619',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44097',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47564',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55381',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47965',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50289',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43713',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26610'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=11021',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42152',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31684',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53287',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26349',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35688',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26376',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41742',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53288',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41071',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43909',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44317',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27922',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35687',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44316',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53290']],
        # 생활
        # [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=42552',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49360',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36174',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45698',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37522',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40737',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45697',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10725',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27892',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53449',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49364',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49665',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48867',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53450',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45696',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37520'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=12922',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12927',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42842',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54215',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52380',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43736',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53452',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13413',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25561',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53328',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51507',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51758',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13318',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55027',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12926',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53234'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=32028',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54414',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53487',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10703',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52592',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50035',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54513',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54514',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55136',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50025',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26793',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52970',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55139',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55135',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53491',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10310'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=52099',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53870',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36600',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55864',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55863',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54898',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50496',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55322',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55759',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50513',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56499',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34233',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55199',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41825',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54897',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34230'],
        #  ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=54216',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37343',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35751',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40666',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35186',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30577',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54414',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54459',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55735',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53606',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56003',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54844',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54847',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49071',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42887',
        #   'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49042']],
        # 뷰티
        [[
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51152',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54905',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55063',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50345',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54907',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52234',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54730',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54906',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53043',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55811',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51764',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51765',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51166',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51157',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55359'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=7646',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7645',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52767',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55322',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7592',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52760',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13721',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41482',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13574',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53558',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41452',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51194',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26825',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52761',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51192',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53011'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=41824',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53143',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34947',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37494',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40745',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37500',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29381',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51528',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49324',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56003',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53127',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53148',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10990',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54201',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53903',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56097'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=54422',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30290',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55363',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37484',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42261',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55797',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54912',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54910',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53124',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51195',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42735',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51746',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52750',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55798',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52747',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43277'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=49665',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55372',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50345',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34949',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55375',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34950',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26286',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49663',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56003',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7380',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26289',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50346',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56033',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55593',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55592',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55994']],
        # 주방
        [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=35741',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54216',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37343',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11160',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54215',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40084',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37522',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12651',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35469',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35669',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35751',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53452',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53328',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54214',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7634',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37520'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=55739',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50984',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26143',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26120',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26115',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50975',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51352',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35775',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52689',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50555',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26118',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56257',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38199',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52473',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52463',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27274'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=48296',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54748',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48300',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38199',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53415',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12938',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56367',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34731',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48947',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53414',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55985',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55017',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53421',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38289',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25916',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53411'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=52469',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53170',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44690',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27157',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31496',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55993',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44687',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42681',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55330',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54402',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52984',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54475',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29548',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29581',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43243',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49852'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=52269',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42691',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53710',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30883',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53709',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53708',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52442',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53426',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31083',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50663',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36528',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52422',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36085',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9605',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10989',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9597'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=40751',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35244',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30883',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31083',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50660',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9597',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6529',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9606',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9610',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30880',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9609',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42433',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30743',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9607',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12604',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12605']],
        # 가전
        [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=49271',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56579',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55358',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50187',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54250',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52685',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50515',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51140',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51198',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42978',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49601',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6529',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51798',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50129',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51199',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55356'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=50880',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53374',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55112',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51434',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51885',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50417',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54489',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52855',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51510',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54956',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53797',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52862',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54426',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49088',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52554',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48812']],
        # 베이비 없음
        # 반려
        [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=35328',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38207',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53715',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48200',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36713',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36639',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34855',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52378',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51089',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52788',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53998',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48312',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34816',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51088',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53717',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=32354'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=30936',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54802',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51083',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42236',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30935',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54798',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36030',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36628',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36631',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54807',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54810',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30992',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51082',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34882',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37587',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48041'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=35328',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53715',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34855',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51088',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53717',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37459',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49870',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49606',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51390',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30911',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55751',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37328',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48201',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48194',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30912',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30901'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=54795',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30861',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30978',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54788',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49333',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49336',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54826',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49343',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54828',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54829',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36585',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54827',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49342',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49327',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49339',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36574'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=55861',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36981',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51989',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53724',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55757',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51108',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36982',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49613',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50677',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52952',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49863',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52777',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51107',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50827',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53158',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51110']]]
    return url_list


def get_categories():
    category_list = [
        # '채소',
        # '과일·견과·쌀',
        # '수산·해산·건어물',
        # '정육·계란',
        # '국·반찬·메인요리',
        # '샐러드·간편식',
        # '면·양념·오일',
        # '음료·우유·떡·간식',
        # '베이커리·치즈·델리',
        # '건강식품',
        # '생활용품·리빙',
        '뷰티·바디케어',
        '주방용품',
        '가전제품',
        # '베이비·키즈',
        '반려동물'
    ]
    return category_list


def get_type():
    type_list = [
        # ['기본채소',
        #  '쌈·샐러드·간편채소',
        #  '브로콜리·특수채소',
        #  '콩나물·버섯류',
        #  '시금치·부추·나물',
        #  '양파·마늘·생강·파',
        #  '파프리카·피망·고추'],
        # ['제철과일', '국산과일', '수입과일', '냉동·건과일', '견과류', '쌀·잡곡'],
        # [
        #     '생선류', '오징어·낙지·문어', '새우·게·랍스터', '해산물·조개류', '수산가공품',
        #     '김·미역·해조류', '건어물·다시팩'],
        # [
        #     '소고기',
        #     '돼지고기', '계란류', '닭·오리고기', '양념육·돈까스', '양고기'],
        # ['국·탕·찌개', '밑반찬', '김치·장아찌·젓갈', '두부·어묵·부침개', '햄·소시지·통조림', '메인요리'],
        # ['샐러드·도시락', '간편식·냉동식품', '밥류·면식품·즉석식품', '선식·시리얼·그래놀라', '만두·튀김·떡볶이', '죽·스프'],
        # ['파스타·면류', '밀가루·가루·믹스', '향신료·소스·드레싱', '양념·액젓·장류', '소금·설탕·식초·꿀', '식용유·참기름·오일'],
        # ['생수·음료·주스', '커피·차', '우유·두유·요거트', '아이스크림', '떡·한과', '간식·과자·쿠키', '초콜릿·젤리·캔디'],
        # ['식빵·빵류', '잼·버터·스프레드', '케이크·파이·디저트', '치즈', '건조육', '올리브·피클·델리'],
        # ['건강즙·건강음료', '홍삼·인삼·꿀', '영양제', '유산균', '건강분말·건강환', '유아동'],
        # ['휴지·티슈·위생용품', '세제·청소용품', '화훼·인테리어소품', '의약외품·마스크', '생활잡화·문구'],
        ['스킨케어', '구강·면도', '바디·제모', '헤어케어', '미용기기·소품'],
        ['주방소모품', '주방·조리도구', '냄비·팬류', '식기류', '컵·와인잔·사케잔', '차·커피도구'],
        ['주방가전', '생활가전'],
        # ['분유·간편 이유식', '이유식 재료', '유아·어린이 음식', '간식·음료·건강식품', '유아용품·젖병·식기류', '기저귀·물티슈', '목욕·세제·위생용품',
        #  '유아스킨·구강케어'],
        ['강아지 간식', '강아지 주식', '고양이 간식', '고양이 주식', '반려동물 용품']]
    return type_list


# def get_delivery():
#     from selenium import webdriver
#
#
#     driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')
#
#     driver.get('https://www.kurly.com/shop/board/view.php?id=notice&no=64')
#
#     address_img = driver.find_element_by_xpath('//*[@id="noticeView"]/div/a/img').get_attribute('src')
#
#     GOODS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'goods/address/')
#     if not os.path.exists(GOODS_IMAGE_DIR):
#         os.makedirs(GOODS_IMAGE_DIR, exist_ok=True)
#     # image_save_name = os.path.join(GOODS_IMAGE_DIR, f'address_image.jpg')
#     # urllib.request.urlretrieve(address_img, image_save_name)
#     #
#     # deli_image = open(os.path.join(GOODS_IMAGE_DIR, f'{image_save_name}'), 'rb')
#
#     # deli_ins = DeliveryInfo.objects.create(address_img=File(deli_image))
#     deli_ins = DeliveryInfo.objects.first()
#     images = driver.find_elements_by_xpath('//*[@id="noticeView"]/div/img')
#     for index, img in enumerate(images):
#         img = img.get_attribute('src')
#         image_save_name = os.path.join(GOODS_IMAGE_DIR, f'image_{index}.jpg')
#         urllib.request.urlretrieve(img, image_save_name)
#
#         image = open(os.path.join(GOODS_IMAGE_DIR, f'{image_save_name}'), 'rb')
#
#         DeliveryInfoImage.objects.create(
#             image=File(image),
#             info=deli_ins,
#         )
