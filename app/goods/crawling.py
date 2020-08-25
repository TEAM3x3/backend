import os
import re
import urllib

from django.core.files import File
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

    detail_page_list = get_urls()

    type_name_list = get_type()
    category_name = get_categories()

    for index, lst in enumerate(detail_page_list):
        category_ins, __ = Category.objects.get_or_create(name=category_name[index])

        for detail_index, url in enumerate(lst):
            print(category_ins.name)
            type_name_ins, __ = Type.objects.get_or_create(
                name=type_name_list[index][detail_index],
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


def crawling():
    get_data()


def get_categories():
    category_list = [
        '채소',
        '과일·견과·쌀',
        '수산·해산·건어물',
        '정육·계란',
        '국·반찬·메인요리',
        '샐러드·간편식',
        '면·양념·오일',
        '음료·우유·떡·간식',
        '베이커리·치즈·델리',
        '건강식품',
        '생활용품·리빙',
        '뷰티·바디케어',
        '주방용품',
        '가전제품',
        '베이비·키즈',
        '반려동물'
    ]
    return category_list


def get_type():
    type_list = [
        ['기본채소', '쌈·샐러드·간편채소', '브로콜리·특수채소', '콩나물·버섯류', '시금치·부추·나물', '양파·마늘·생강·파', '파프리카·피망·고추'],
        ['제철과일', '국산과일', '수입과일', '냉동·건과일', '견과류', '쌀·잡곡'],
        ['생선류', '오징어·낙지·문어', '새우·게·랍스터', '해산물·조개류', '수산가공품', '김·미역·해조류', '건어물·다시팩'],
        ['소고기', '돼지고기', '계란류', '닭·오리고기', '양념육·돈까스', '양고기'],
        ['국·탕·찌개', '밑반찬', '김치·장아찌·젓갈', '두부·어묵·부침개', '햄·소시지·통조림', '메인요리'],
        ['샐러드·도시락', '간편식·냉동식품', '밥류·면식품·즉석식품', '선식·시리얼·그래놀라', '만두·튀김·떡볶이', '죽·스프'],
        ['파스타·면류', '밀가루·가루·믹스', '향신료·소스·드레싱', '양념·액젓·장류', '소금·설탕·식초·꿀', '식용유·참기름·오일'],
        ['생수·음료·주스', '커피·차', '우유·두유·요거트', '아이스크림', '떡·한과', '간식·과자·쿠키', '초콜릿·젤리·캔디'],
        ['식빵·빵류', '잼·버터·스프레드', '케이크·파이·디저트', '치즈', '건조육', '올리브·피클·델리'],
        ['건강즙·건강음료', '홍삼·인삼·꿀', '영양제', '유산균', '건강분말·건강환', '유아동'],
        ['휴지·티슈·위생용품', '세제·청소용품', '화훼·인테리어소품', '의약외품·마스크', '생활잡화·문구'],
        ['스킨케어', '구강·면도', '바디·제모', '헤어케어', '미용기기·소품'],
        ['주방소모품', '주방·조리도구', '냄비·팬류', '식기류', '컵·와인잔·사케잔', '차·커피도구'], ['주방가전', '생활가전'],
        ['분유·간편 이유식', '이유식 재료', '유아·어린이 음식', '간식·음료·건강식품', '유아용품·젖병·식기류', '기저귀·물티슈', '목욕·세제·위생용품',
         '유아스킨·구강케어'],
        ['강아지 간식', '강아지 주식', '고양이 간식', '고양이 주식', '반려동물 용품']
    ]
    return type_list


def get_urls():
    url_list = [
        [
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=26448',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30781',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26451',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1385',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49246',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49921',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27232',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30735',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=70',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=96',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31391',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53498',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49248',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49499',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49920',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3469'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=26448',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49246',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27232',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=70',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=96',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53498',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31395',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54661',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54657',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=69',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50692',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54660',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=97',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50690',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27233',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43350'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=1385',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48835',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45384',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=98',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=32142',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1074',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48834',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30612',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48833',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50252',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2718',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30610',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38267',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36662',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=5755',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48838'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=37313',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42793',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11099',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36686',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36692',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53479',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=453',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55689',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12656',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30793',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9213',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3326',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43548'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=49921',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31391',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31393',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49634',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31389',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31390',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36543',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31392',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31388',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54584',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49922',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36542',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27488',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13338',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10322',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54586'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=43350',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36663',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3188',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42665',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31114',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2657',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53318',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41303',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1278',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=512',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41305',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1712',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41302'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=26451',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49248',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49920',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3469',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49252',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42157',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49247',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6117',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54885',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2811',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50697',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27461',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27166',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27771',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42788',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51425'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=30781',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30735',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49499',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1350',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27769',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27770',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27768',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7027',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6792',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=304',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49251',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40987',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27767',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42790',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55104',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41022']
        ],

        [
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=1391',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54074',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29524',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27202',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53512',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45277',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47711',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45300',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52957',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50422',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43698',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48540',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53513',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26587',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3446',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37914'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=1391',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53512',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47711',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45300',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43698',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48540',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53513',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43697',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37066',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=5451',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13611',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35952',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53508',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52832',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51705',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51305'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=29565',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10870',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4289',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10316',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9985',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13275',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30143',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55383',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49889',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25418',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26401',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34038',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48538',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48686',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41122',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9465'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=54074',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29524',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42356',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29629',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31379',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37257',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34930',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42444',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13127',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54153',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56554',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37254',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4297',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44640',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37114',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4705'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=34322',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49995',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37627',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13474',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31659',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29386',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42439',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43508',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13272',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25954',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42444',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42919',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49136',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54466',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53621',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44754'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=27202',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52957',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26587',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37914',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12973',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11540',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34124',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48263',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35003',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54411',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6807',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55123',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35000',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37053',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52475',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4475'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=45277',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50422',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3446',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37914',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50056',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4778',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25861',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26854',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52202',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53702',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45278',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55130',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25862',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9879',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44113',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12986'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=50362',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30822',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51727',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42283',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51709',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51729',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27311',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9878',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51710',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27500',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43351',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3673',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9877',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27211',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51728',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53268']
        ],
        [
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=29850',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50290',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26847',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25888',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44534',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34943',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41405',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38008',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51264',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25443',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36067',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29849',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47857',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47858',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1224',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37880'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=57308',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56504',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55949',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55946',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54880',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54450',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54451',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54452',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54447',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54448',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54438',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54430',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54434',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54436',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54437',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54397'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=55460',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55459',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56511',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56509',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55175',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54225',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54224',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54223',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54189',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54065',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54064',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54060',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54054',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52346',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51687',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51606'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=48529',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51888',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51890',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51889',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53113',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50569',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48168',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41405',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41404',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40907',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38008',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37933',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34943',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34030',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31279',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31278'],

            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=55917',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55916',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56012',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56440',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55672',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55821',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55820',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55819',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55459',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55460',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55304',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55298',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55297',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54879',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54502',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54889'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=51308',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51307',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51306',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43800',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43799',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43796',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41741',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41740',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35943',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35942',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31195',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31193',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26205']
        ],
        [
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=50290',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25888',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27202',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48639',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52131',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42765',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30068',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11633',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53794',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6503',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26566',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31864',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27606',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52957',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54583',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3664'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=48639',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42765',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11633',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48646',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48745',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51186',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53979',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1235',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53932',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48746',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38126',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48260',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49761',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55073',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41783',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44756'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=53794',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54583',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48528',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48023',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11284',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41439',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40874',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53071',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36962',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36460',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36694',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26557',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53795',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49949',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49954',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52487'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=52957',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26587',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10142',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26690',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26687',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6807',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26688',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7222',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52959',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52958',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4475',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10141',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48187',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41256',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7225',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42292'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=30068',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53794',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6503',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3664',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4180',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38249',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38297',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12973',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34568',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54557',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52323',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36455',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48192',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53795',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40508',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29881'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=52131',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26566',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27606',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1680',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11540',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3535',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48706',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29534',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13002',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54502',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52924',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11473',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40500',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55496',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27609',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10899'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=50290',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25888',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27202',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31864',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30594',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=5051',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27013',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40874',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=32137',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36694',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50567',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43904',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53486',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52237',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31491',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54888']
        ],
        [
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=48639',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52812',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31466',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37555',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31454',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9467',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1269',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36731',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26926',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31188',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6477',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35376',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42730',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44505',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26232',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1277'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=31466',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37555',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31454',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1269',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36731',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26926',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42730',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44505',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4504',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54833',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37061',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27812',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36698',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51641',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48517',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36554'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=26232',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36145',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4237',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4365',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54699',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13521',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45187',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4402',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4364',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42865',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34364',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45186',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29847',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49724',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37363',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42862'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=31466',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31454',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9467',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36731',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31188',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6477',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35376',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1277',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36150',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41172',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36962',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13463',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40908',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36866',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49453',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49787'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=48639',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52812',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31466',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36972',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26061',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12949',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48049',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41875',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52907',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4393',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41230',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27461',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12950',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4546',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34971',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41256'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=11475',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35040',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1737',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=551',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47787',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44470',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13725',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49766',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54185',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52771',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26292',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53904',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27694',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35037',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1688',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35043'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=325',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=343',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55518',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6331',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4517',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31651',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30776',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48274',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=355',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55520',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34441',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36753',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49237',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40973',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=342',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=8908']
        ],
        [
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=56621',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56324',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42489',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49703',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3417',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40710',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55242',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53293',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52365',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54665',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52912',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54632',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31481',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54621',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54620',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54604'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=56121',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56124',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56127',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56130',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56131',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55413',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55412',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55258',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55398',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55397',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55266',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55265',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34162',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55442',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56181',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55317'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=55564',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55561',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55914',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54878',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54383',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54379',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54212',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55247',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53915',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52824',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53217',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53215',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53214',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54665',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38253',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51475'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=56165',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54576',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55897',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55894',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56286',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55602',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56251',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56225',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56008',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56004',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55271',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55146',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55458',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53377',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53376',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55442'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=56230',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55548',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55525',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56654',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52337',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52333',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55076',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55077',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55428',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54621',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54620',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54174',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53662',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55484',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51830',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53732']
        ],
        [
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=52096',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11021',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52682',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49159',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31986',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47787',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51185',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50910',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37040',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42143',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42152',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=39502',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26292',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44335',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45462',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55718'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=52096',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11021',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52682',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31986',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37040',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42152',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=39502',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26292',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42658',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54721',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51600',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36208',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55439',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54454',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51216',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31064'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=51215',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34287',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26348',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26349',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26376',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41742',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49460',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13152',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27921',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45157',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45158',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27922',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45743',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55855',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40664',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53291'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=49159',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44335',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34287',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49724',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37363',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51509',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53833',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50288',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=48619',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44097',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47564',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55381',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47965',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50289',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43713',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26610'],

        ],

        [
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=7646',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41824',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7645',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54422',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52230',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52767',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51152',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49665',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55322',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53143',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7592',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52760',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55372',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34947',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37494',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13721'],
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
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51528',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49324',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56003',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53127',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53148',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10990',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54201',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53903',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56097',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9706'],
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
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55994']
        ],
        [
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=35741',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54216',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37343',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11160',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54215',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=40084',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37522',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12651',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52269',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35469',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35669',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52469',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35751',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53452',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53328',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54214'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=35741',
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
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=12605']
        ],
        [
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=50880',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53374',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55112',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51434',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51885',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50417',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54489',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49271',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=56579',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51510',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55358',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54956',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53797',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52862',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54426',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50187'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=49271',
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
        ],
        [
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=27876',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26448',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29524',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26451',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25888',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27232',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3748',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=70',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=96',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36067',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3469',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7414',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11633',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11248',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=69',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=98'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=30138',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=5999',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37196',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37167',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29711',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27247',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36325',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35894',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37144',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7475',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41923',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7477',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25966',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27874',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52612',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36239'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=50692',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1733',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50697',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50693',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25369',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=2758',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36688',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43351',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29441',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26170',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=603',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3282',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34456',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41146',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=34461',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13272'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=25888',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36067',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11633',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11248',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6905',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11540',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=3535',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37066',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=4432',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10142',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27013',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35393',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54502',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=13766',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36694',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30085'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=3748',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7414',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=601',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1691',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27758',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26232',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=11021',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=31253',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27362',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=30222',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9796',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44542',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=38224',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=1289',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35963',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=6105'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=53252',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7356',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53251',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35026',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35842',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36385',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54946',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54940',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54939',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41923',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54950',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45173',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55112',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43755',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54931',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=54945'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=12419',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51318',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51685',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51321',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7486',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52218',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52222',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=36847',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42952',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=7350',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9270',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=9269',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=42948',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43603',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44282',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44144'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=45367',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=43736',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41920',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26286',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55052',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55055',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45374',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45149',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53127',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51315',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=27827',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55797',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53237',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=26289',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55802',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55041'],
            ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=7499',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52760',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35026',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52761',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52756',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51193',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=25363',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55867',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45378',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52766',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44409',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=55866',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50357',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45373',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53782',
             'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45375']
        ],
    ]
    return url_list
