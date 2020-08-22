import os
import re
import urllib

from django.core.files import File
from selenium.common.exceptions import NoSuchElementException

from config.settings.base import MEDIA_ROOT


def get_data():
    from selenium import webdriver
    from goods.models import Category
    from goods.models import Type
    from goods.models import GoodsType
    from goods.models import GoodsDetail
    from goods.models import GoodsExplain

    driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')

    detail_page_list = [
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=1391',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53512',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47711',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45300',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48540',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43698',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53513',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43699',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43697',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53884',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37066',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13611',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=5451',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51705',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53508',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35952'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=29565',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10870',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53934',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4289',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10316',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48536',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9985',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13275',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49889',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55383',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25418',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34038',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26401',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48538',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48686',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9465'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=29524',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54074',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42356',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29629',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31379',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37257',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34930',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13127',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42444',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54153',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48171',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37254',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4297',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37114',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50941',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4705'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=34322',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37627',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49139',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49135',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13474',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29386',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43508',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13272',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25954',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54466',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42444',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49136',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53621',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41980',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48534',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41612'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=27202',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52957',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53856',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37914',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12973',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35003',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11540',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48263',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34124',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52956',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6807',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54411',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35000',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55123',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52475',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37053'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=45277',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50422',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37914',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3446',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50056',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4778',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25861',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26854',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53702',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52202',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45278',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55130',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34250',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25862',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9879',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44113'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=50362',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30822',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51727',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51709',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42283',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27311',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9878',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51729',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51710',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27500',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43351',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9877',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3673',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27211',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51728',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9758']]

    type_name_list = ['생선류', '오징어·낙지·문어', '새우·게·랍스터', '해산물·조개류', '수산가공품', '김·미역·해조류', '건어물·다시팩']
    category_name = '수산·해산·건어물'
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
            try:
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
            except NoSuchElementException:
                pass

            try:
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
            except NoSuchElementException:
                pass

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
            print(text__title)
            print(text__context)
            print(text__description)
            print(category_ins)

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

            goods_ins, created = Goods.objects.get_or_create(
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
            print(goods_ins, created)

            goods_explain, created = GoodsExplain.objects.get_or_create(
                img=File(extra_image),
                text_title=text__title,
                text_context=text__context,
                text_description=text__description,

                goods=goods_ins,
            )
            print('goods_explain, created', goods_explain, created)

            # 디테일 정보
            var_titles = driver.find_elements_by_xpath('//*[@id="goods-infomation"]/table/tbody/tr/th')
            var_descs = driver.find_elements_by_xpath('//*[@id="goods-infomation"]/table/tbody/tr/td')
            # print('var_titles>>>>>>>>>>>>>>>>>.', var_titles)
            # print('var_descs >>>>>>>>>>>>>>>>>>', var_descs)
            if len(var_titles) >= 1:
                for var_detail_title, var_detail_desc in zip(var_titles, var_descs):
                    # print(var_detail_title.get_attribute('innerText'))
                    # print(var_detail_desc.get_attribute('innerText'), '\n')
                    detail_ins, created = GoodsDetail.objects.get_or_create(
                        detail_title=var_detail_title.get_attribute('innerText'),
                        detail_desc=var_detail_desc.get_attribute('innerText'),
                        goods=goods_ins,
                    )
                    # print('goods_detail_ins, created', detail_ins, created)
            # 타입 명시
            # print(type_name_ins)
            # print(goods_ins)
            goodstype_ins, created = GoodsType.objects.get_or_create(type=type_name_ins, goods=goods_ins)
            # print(goodstype_ins, created)


def crawling():
    get_data()
