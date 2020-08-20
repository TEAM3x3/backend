import os
import re
import time
import urllib

from django.core.files import File
from selenium.common.exceptions import NoSuchElementException

from config.settings import MEDIA_ROOT


def get_data():
    from selenium import webdriver
    from goods.models import Category
    from goods.models import Type
    from goods.models import GoodsType
    from goods.models import GoodsDetail
    driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')

    detail_page_list = []

    type_name_list = []
    category_name = '국 반찬 메인요리 할 차'
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
            print(text_one_title)
            print(text_one_context)
            print(text_one_description)
            print(category_ins)

            # 이미지 생성
            try:
                GOODS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'goods/{goods_title}/')
                if not os.path.exists(GOODS_IMAGE_DIR):
                    os.makedirs(GOODS_IMAGE_DIR, exist_ok=True)
                image_save_name = os.path.join(GOODS_IMAGE_DIR, f'{goods_title}_goods_image.jpg')
                urllib.request.urlretrieve(goods_image[1], image_save_name)

                f = open(os.path.join(GOODS_IMAGE_DIR, f'{image_save_name}'), 'rb')

                image_save_name2 = os.path.join(GOODS_IMAGE_DIR, f'{goods_title}_info_image.jpg')
                urllib.request.urlretrieve(info_image, image_save_name2)

                f2 = open(os.path.join(GOODS_IMAGE_DIR, f'{image_save_name2}'), 'rb')

                image_save_name3 = os.path.join(GOODS_IMAGE_DIR, f'{goods_title}_image_one.jpg')
                urllib.request.urlretrieve(image_one, image_save_name3)

                f3 = open(os.path.join(GOODS_IMAGE_DIR, f'{image_save_name3}'), 'rb')
            except FileNotFoundError:
                print(' 건너 뜁니다 !_________________________________________________')
                continue

            goods_ins, created = Goods.objects.get_or_create(
                img=File(f),
                info_img=File(f2),
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

                img_1=File(f3),
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
                goods_detail_ins, created = GoodsDetail.objects.get_or_create(
                    goods=goods_ins,
                    var_1_title=var_titles[0].get_attribute('innerText'),
                    var_1_desc=var_descs[0].get_attribute('innerText'),
                    var_2_title=var_titles[1].get_attribute('innerText'),
                    var_2_desc=var_descs[1].get_attribute('innerText'),
                    var_3_title=var_titles[2].get_attribute('innerText'),
                    var_3_desc=var_descs[2].get_attribute('innerText'),
                    var_4_title=var_titles[3].get_attribute('innerText'),
                    var_4_desc=var_descs[3].get_attribute('innerText'),
                    var_5_title=var_titles[4].get_attribute('innerText'),
                    var_5_desc=var_descs[4].get_attribute('innerText'),
                    var_6_title=var_titles[5].get_attribute('innerText'),
                    var_6_desc=var_descs[5].get_attribute('innerText'),
                    var_7_title=var_titles[6].get_attribute('innerText'),
                    var_7_desc=var_descs[6].get_attribute('innerText'),
                    var_8_title=var_titles[7].get_attribute('innerText'),
                    var_8_desc=var_descs[7].get_attribute('innerText'),
                )

            elif len(var_titles) == 10:
                GoodsDetail.objects.get_or_create(
                    goods=goods_ins,
                    var_1_title=var_titles[0].get_attribute('innerText'),
                    var_1_desc=var_descs[0].get_attribute('innerText'),
                    var_2_title=var_titles[1].get_attribute('innerText'),
                    var_2_desc=var_descs[1].get_attribute('innerText'),
                    var_3_title=var_titles[2].get_attribute('innerText'),
                    var_3_desc=var_descs[2].get_attribute('innerText'),
                    var_4_title=var_titles[3].get_attribute('innerText'),
                    var_4_desc=var_descs[3].get_attribute('innerText'),
                    var_5_title=var_titles[4].get_attribute('innerText'),
                    var_5_desc=var_descs[4].get_attribute('innerText'),
                    var_6_title=var_titles[5].get_attribute('innerText'),
                    var_6_desc=var_descs[5].get_attribute('innerText'),
                    var_7_title=var_titles[6].get_attribute('innerText'),
                    var_7_desc=var_descs[6].get_attribute('innerText'),
                    var_8_title=var_titles[7].get_attribute('innerText'),
                    var_8_desc=var_descs[7].get_attribute('innerText'),
                    var_9_title=var_titles[8].get_attribute('innerText'),
                    var_9_desc=var_descs[8].get_attribute('innerText'),
                    var_10_title=var_titles[9].get_attribute('innerText'),
                    var_10_desc=var_descs[9].get_attribute('innerText'),
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
