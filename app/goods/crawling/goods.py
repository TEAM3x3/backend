import os
import re
import urllib

from django.core.files import File
from django.db import DataError
from selenium.common.exceptions import NoSuchElementException

from config.settings.base import MEDIA_ROOT
from event.models import GoodsEventType


def get_data():
    from selenium import webdriver
    from goods.models import Goods
    from goods.models import Category
    from goods.models import Type
    from goods.models import GoodsType
    from goods.models import GoodsDetail
    from goods.models import GoodsExplain
    from goods.models import GoodsDetailTitle
    from event.models import MainEvent, MainEventType
    from goods.models import SaleInfo

    driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')

    all_goods_url_list = get_urls()

    type_name_list = get_type()
    category_list = get_categories()

    for category_index, category_urls in enumerate(all_goods_url_list):
        event_ins, created = MainEvent.objects.get_or_create(title=category_list[category_index])
        for type_index, type_urls in enumerate(category_urls):
            for index, url in enumerate(type_urls):
                try:
                    print(event_ins.title)
                    mainEvent_ins, __ = MainEventType.objects.get_or_create(
                        name=type_name_list[category_index][type_index],
                        event=event_ins
                    )
                    # print(mainEvent_ins.name)
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
                    sales_ins = None

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

                    # sale ins get
                    try:
                        sales_value = driver.find_element_by_xpath(
                            '//*[@id="sectionView"]/div/p[3]/span[1]/span[1]/span[2]').get_attribute('innerText')
                        discount_rate = int(re.search(r'\d+', sales_value).group())
                        sales_ins, __ = SaleInfo.objects.get_or_create(
                            discount_rate=discount_rate
                        )
                    except NoSuchElementException:
                        pass

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
                            # category=category_ins,
                            sales=sales_ins
                        )
                        created = True
                    print(goods_ins, created)

                    GoodsEventType.objects.get_or_create(
                        goods=goods_ins,
                        type=mainEvent_ins
                    )

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
                #                     # print(type_name_ins)
                # print(goods_ins)
                # goodstype_ins, created = GoodsType.objects.get_or_create(type=type_name_ins, goods=goods_ins)
                # print(goodstype_ins, created)
                except DataError:
                    continue


def crawling():
    get_data()


def get_urls():
    url_list = [
        [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=54199',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34171',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34475',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51911',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44680',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55919',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55918',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54179',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52609',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41024',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51932',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43934',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51609',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54622',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40874',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4961'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=30926',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41691',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51910',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29551',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43935',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26714',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41023',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45715',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56724',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54551',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36068',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49405',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27189',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51186',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53632',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37076']],

        [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=43726',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41135',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56722',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6176',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49694',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49695',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11212',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4768',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45296',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51031',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43351',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42991',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35315',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53568',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53564',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35481']],

        [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=43726',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41135',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56722',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6176',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49694',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49695',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11212',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4768',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45296',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51031',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43351',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42991',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35315',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53568',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53564',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35481'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=26587',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41135',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56722',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4475',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31390',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36543',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31392',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31391',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54071',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31389',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31388',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51271',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51031',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43351',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42991',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35315'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=54254',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53707',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53620',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53705',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53702',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53700',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53704',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48611',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48614',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45765',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34070',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34074',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34069',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34071',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34075',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53619']],

        [['https://www.kurly.com/shop/goods/goods_view.php?goodsno=52922',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6050',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4299',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49265',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47811',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13006',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6167',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44178',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31758',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29437',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29438',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42892',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42891',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54967',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4304',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49571'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=53178',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49698',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2718',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55620',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25705',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34010',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44523',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9984',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47649',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27902',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7388',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31100',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51900',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30766',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31388',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51572'],
         ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=54074',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52738',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50422',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48264',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25861',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54153',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31804',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6445',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56554',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31393',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49246',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49499',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27232',
          'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3748']]

    ]
    return url_list


def get_categories():
    category_list = ['매콤달콤 우리집 식탁', '아이들 입맛 책임질 간편식', '햅쌀로 즐기는 솥밥', '달걀 레시피 기획전']
    return category_list


def get_type():
    type_list = [
        ['매운맛', '달콤한맛'],
        ['간편식'],
        ['가을 소고기 무밥', '명란 버섯 솥밥', '반찬 & 주방용품'],
        ['에그 브런치', '에그 버거', '에그 키토김밥']
    ]
    return type_list
