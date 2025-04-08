# 使用python的selenium库进行数据抓取 (Используйте библиотеку селена Python для понимания данных)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import re
import csv

# 启动浏览器 (Начните браузер)
driver = webdriver.Edge()
# 最大化浏览器窗口 (Максимизировать окно браузера)
driver.maximize_window()
# 访问网址 (Посетите URL)
driver.get('https://www.wildberries.ru')
time.sleep(5)
# 通过CSS选择器查找元素，输入关键字后回车 (Найдите элемент через селектор CSS, введите ключевое слово после ввода ключевого слова)
# 点击搜索框，确保它可见 (Щелкните поле поиска, чтобы убедиться, что он может быть виден)
search_box = driver.find_element(By.CSS_SELECTOR, '#searchInput')
search_box.click()
# 输入搜索词 (Введите поисковые слова)
search_box.send_keys('Товары для домашних животных')
# 回车搜索 (Вернуть поиск)
search_box.send_keys(Keys.ENTER)
time.sleep(30)

# 滚动页面函数,javascript (Функция поверхности катящейся страницы, JavaScript)
def drop_down():
  for x in range(15):
    js = "window.scrollBy(0, " + str(x * 200) + ");"
    driver.execute_script(js)
    time.sleep(1)


def find_lis():
  drop_down()
  # 最大尝试次数
  max_attempts = 15000
  attempts = 0
  while attempts < max_attempts:
    try:
      # 获取所有商品数据对应标签 (Получите соответствующий тег всех данных продукта)
      list_a = driver.find_elements(By.CLASS_NAME, 'product-card__wrapper')
      print("检测到目标元素")
      print(len(list_a))
      if len(list_a) <= 120:
        time.sleep(30)
        print("检测到目标元素，但不符合要求")
        # 刷新页面
        driver.refresh()
        print("页面已刷新")
        return find_lis()
      else:
        # 找到目标元素后返回
        print("目标元素符合要求")
        return list_a
    except NoSuchElementException:
      print("未检测到目标元素，正在尝试重新检索...")
      # 可以根据需要调整等待时间
      time.sleep(30)
      # 刷新页面
      driver.refresh()
      #attempts += 1
      return find_lis()
  print("达到最大尝试次数，未能找到价格元素")
  # 返回是否找到了价格元素的状态
  return None


# 创建一个空列表用于存储商品数据 (Создайте пустой список для хранения данных о продукте)
commodity_data = []

def get_commodity_info():
    # 获取所有商品数据对应标签 (Получите соответствующий тег всех данных продукта)
    #lis = driver.find_elements(By.CLASS_NAME, 'product-card__wrapper')
    lis = find_lis()
    # for循环遍历 (для прохождения)
    for li in lis:
      price_element = li.find_element(By.CLASS_NAME, 'price__lower-price').text
      #price_element = find_price() # 价格
      # 使用正则表达式匹配数字部分 (Используйте соответствующие номера регулярного выражения)
      price = re.sub(r'\D', '', price_element)

      brand = li.find_element(By.CLASS_NAME, 'product-card__brand-container').text  # 品牌

      # 在商品卡片元素中查找商品链接元素 (Найдите элемент ссылки продукта в элементе карты продукта)
      product_elements = li.find_elements(By.CLASS_NAME, 'product-card__link')
      # 遍历商品链接元素列表 (Пересечение списка элементов ссылки продукта)
      for index, product_element in enumerate(product_elements):
        # 获取商品链接 (Получите ссылку на продукт)
        product_link = product_element.get_attribute("href")
        # 打开新标签页 (Откройте новую вкладку)
        driver.execute_script("window.open('', '_blank');")
        # 获取窗口句柄 (Получить ручку окон)
        windows = driver.window_handles
        # 切换窗口，windows[-1]最右边窗口 (Переключение окна, Windows [-1] в дальнем правом окне)
        driver.switch_to.window(windows[-1])
        # 在新窗口打开商品链接 (Откройте ссылку продукта в новом окне)
        driver.get(product_link)
        driver.implicitly_wait(3)

      title = driver.find_element(By.CLASS_NAME, 'product-page__title').text  # 标题 (заголовок)
      count_element = driver.find_element(By.CLASS_NAME, 'product-review__count-review').text  # 评论 (Комментарий)
      # 使用正则表达式匹配数字部分 (Используйте регулярные выражения, чтобы соответствовать количественной части)
      count = re.sub(r'\D', '', count_element)
      rating = driver.find_element(By.CLASS_NAME, 'product-review__rating').text  # 评分 (счет)

      # 打开商品详情信息 (Откройте информацию о деталях продукта)
      driver.find_element(By.CLASS_NAME, 'product-page__btn-detail').click()
      time.sleep(1)

      # 创建空列表 (Создать пустой список)
      th_list = []
      td_list = []
      # 遍历详细信息 (Подробная информация)
      Lis_info = driver.find_elements(By.CLASS_NAME, 'product-params__row')
      for li_th in Lis_info:
        # 题目 (тема)
        th_element = li_th.find_element(By.CLASS_NAME, 'product-params__cell-decor')
        th_text = th_element.text
        # 将文本追加到相应的列表中 (Добавить текст в соответствующий список)
        th_list.append(th_text)
      for li_td in Lis_info:
        # 内容 (содержание)
        td_element = li_td.find_element(By.CSS_SELECTOR, 'td.product-params__cell')
        td_text = td_element.text
        # 将文本追加到相应的列表中 (Добавить текст в соответствующий список)
        td_list.append(td_text)
      # 使用zip函数将两组列表合并为字典 (Используйте функцию ZIP, чтобы объединить две группы в словарь)
      dict_info = dict(zip(th_list, td_list))

      dit_commodity_data = {
        'title': title,
        'brand': brand,
        'price': price,
        'count': count,
        'rating': rating,
        'info_dict': dict_info
      }
      print(title, brand, price, count, rating, dict_info)
      time.sleep(1)
      # 关闭窗口 (закройте окно)
      driver.close()
      driver.switch_to.window(windows[0])
      # 将商品数据添加到列表中 (Добавить данные продукта в список)
      commodity_data.append(dit_commodity_data)
      # 在每次循环结束时清空列表 (Очистить список в конце каждого цикла)
      th_list.clear()
      td_list.clear()

      # 将商品数据保存到CSV文件中 (Сохранить данные продукта в файле CSV)
      csv_file_path = 'wildberries宠物用品数据.csv'
      csv_columns = ['title', 'brand', 'price', 'count', 'rating', 'info_dict']

      with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for data in commodity_data:
          writer.writerow(data)





#翻页 (Страницы)
'''for page in range(1,61):'''
for page in range(1,61):
  # 等待元素加载 (Нагрузка элемента ожидания)
  driver.implicitly_wait(5)
  find_lis()
  time.sleep(1)
  get_commodity_info()
  driver.implicitly_wait(10)
  # 点击下一页 (Нажмите на следующую страницу)
  # driver.find_element(By.CSS_SELECTOR, '.pagination-next').click()
  next_page_button = driver.find_element(By.CSS_SELECTOR, '.pagination-next')
  driver.execute_script("arguments[0].click();", next_page_button)

# 关闭浏览器 (Закрыть браузер)
driver.quit()

print(f"数据已保存到'wildberries宠物用品数据'文件中")







