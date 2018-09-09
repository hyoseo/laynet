from selenium import webdriver
import db
import datetime

NAVER_FINANCE_BASE_URL = 'http://finance.naver.com'
SISE_ENTRYJONGMOK_URL = '/sise/entryJongmok.nhn?&page=%d'
TRADING_TREND_URL = '/item/frgn.nhn?code=%s&page=%d'
ITEM_ANALYSIS_URL = '/item/coinfo.nhn?code=%s'

def scrape_kospi_top200(driver):
    ranking = 1

    kospiTop200 = []
    
    for i in range(1, 21):
        driver.get(NAVER_FINANCE_BASE_URL + SISE_ENTRYJONGMOK_URL % i)
        stocks = driver.find_elements_by_xpath('//a[@target="_parent"]')

        for stock in stocks:
            companyName = stock.text
            stockCode = stock.get_attribute('href')[-6:]
            
            kospiTop200.append({'ranking': ranking, 'companyName': companyName, 'stockCode': stockCode})

            ranking += 1

    for i in range(len(kospiTop200)):
        baseData = scrape_stock_base_data(driver, kospiTop200[i]['stockCode'])

        db.addOrUpdateKospi200(kospiTop200[i]['ranking'], kospiTop200[i]['companyName']
                               , kospiTop200[i]['stockCode'], baseData['marketSum'], baseData['askingPriceUnit'])

def scrape_stock_base_data(driver, stockCode):
    driver.get(NAVER_FINANCE_BASE_URL + ITEM_ANALYSIS_URL % stockCode)

    # 시가총액을 가져온다. 
    result = driver.find_elements_by_xpath('//em[@id="_market_sum"]')[0].text.split('조')

    marketSum = 0
    if len(result) > 1:
        marketSum = int(result[0] + result[1].lstrip().replace(',', '').rjust(4, '0') + '00000000')
    else:
        marketSum = int(result[0].replace(',', '') + '00000000')

    # 현재가를 가져온다.
    todayPrice = int(driver.find_elements_by_xpath('//p[@class="no_today"]')[0].text.replace('\n', '').replace(',',   ''))
        
    askingPriceUnit = 0
    if todayPrice < 1000:
        askingPriceUnit = 1
    elif todayPrice < 5000:
        askingPriceUnit = 5
    elif todayPrice < 10000:
        askingPriceUnit = 10
    elif todayPrice < 50000:
        askingPriceUnit = 50
    elif todayPrice < 100000:
        askingPriceUnit = 100
    elif todayPrice < 500000:
        askingPriceUnit = 500
    else:
        askingPriceUnit= 1000
    
    return {'marketSum': marketSum, 'askingPriceUnit': askingPriceUnit}

def scrape_stock_trade_page_numbers(driver, stockCode):
    driver.get(NAVER_FINANCE_BASE_URL + TRADING_TREND_URL % (stockCode, 1))

    return driver.find_elements_by_xpath('//div[@class="section inner_sub"]/table[@class="Nnavi"]/tbody/tr/td[not(@class)]')

def scrape_stock_trade_this_page(driver, stockCode, page):
    driver.get(NAVER_FINANCE_BASE_URL + TRADING_TREND_URL % (stockCode, page))

    return driver.find_elements_by_xpath('//div[@class="section inner_sub"]/table/tbody/tr[@onmouseover="mouseOver(this)"]')

def scrape_stock_trade(driver, companyName, stockCode):
    latestStockTrade = db.getLatestStockTrade(stockCode)
       
    pageNumbers = scrape_stock_trade_page_numbers(driver, stockCode)

    dayTradeList = []

    for i in range(1, min(4, 2+len(pageNumbers))):
        dayTrades = scrape_stock_trade_this_page(driver, stockCode, i)
            
        endOfTheLoop = False
            
        for dayTrade in dayTrades:
            dayTradeInfo = dayTrade.text.split()
            if len(dayTradeInfo) == 0:
                break

            tradeDate = datetime.datetime.strptime(dayTradeInfo[0], '%Y.%m.%d').date()

            # db에 저장된 데이터의 이후 데이터만 저장한다.
            if latestStockTrade and tradeDate <= latestStockTrade[2]:
                latestStockTrade[2] = latestStockTrade[2].strftime('%Y.%m.%d')
                dayTradeList.append([*latestStockTrade])#, 0, 'NONE']) #  0, 'NONE'은 임시로 추가
                endOfTheLoop = True
                break

            dayTradeList.append([companyName                                # [0] CompanyName
                                    , stockCode                                # [1] StockCode
                                    , dayTradeInfo[0]                          # [2] Date
                                    , int(dayTradeInfo[1].replace(',', ''))    # [3] Price
                                    , 0                                        # [4] Delta
                                    , 'NONE'                                   # [5] CurveType
                                    , int(dayTradeInfo[5].replace(',', ''))    # [6] InstitutionVolume
                                    , int(dayTradeInfo[6].replace(',', ''))])  # [7] ForeignersVolume        

        if endOfTheLoop:
            break

    # 액면분할 이후의 데이터만 저장한다.
    dayTradeList = delete_all_before_split_stock(dayTradeList)

    # 변곡점과 Delta값을 계산한다.
    update_curve_type_and_delta(dayTradeList)

    for i in reversed(range(len(dayTradeList))):
        db.addOrUpdateDayStockTrade(*dayTradeList[i])

def scrape_kospi_top200_stock_trade(driver):        
    kospiTop200 = db.getKospi200()
    if kospiTop200 == None:
        return None

    for company in kospiTop200:
        scrape_stock_trade(driver, company[1], company[2])

def update_kospi_top200_big_players_data():        
    kospiTop200 = db.getKospi200()
    if kospiTop200 == None:
        return None

    for company in kospiTop200:
        stockCode = company[2]
        db.updateBigPlayersData(stockCode)

def delete_all_before_split_stock(dayTradeList):
    PRICE = 3
    INSTITUTION_VOLUME = 6
    FOREIGNERS_VOLUME = 7
    
    for i in range(len(dayTradeList)):
        if dayTradeList[i][INSTITUTION_VOLUME] == 0 and dayTradeList[i][FOREIGNERS_VOLUME] == 0:
            if i == 0:
                return []
            elif dayTradeList[i-1][PRICE] * 2 < dayTradeList[i][PRICE]:
                return dayTradeList[:i]

    return dayTradeList

def update_curve_type_and_delta(dayTradeList):
    if len(dayTradeList) < 2:
        return

    PRICE = 3
    DELTA = 4
    CURVE_TYPE = 5

    for cur in reversed(range(len(dayTradeList)-1)):
        prev = cur+1
        if dayTradeList[prev][PRICE] < dayTradeList[cur][PRICE]:
            dayTradeList[cur][CURVE_TYPE] = 'UPWARD'
        elif dayTradeList[prev][PRICE] > dayTradeList[cur][PRICE]:
            dayTradeList[cur][CURVE_TYPE] = 'DOWNWARD'
        else:
            dayTradeList[cur][CURVE_TYPE] = dayTradeList[prev][CURVE_TYPE]

        dayTradeList[cur][DELTA] = dayTradeList[cur][PRICE] - dayTradeList[prev][PRICE]
        
        if dayTradeList[cur][CURVE_TYPE] != dayTradeList[prev][CURVE_TYPE]:
            if dayTradeList[prev][CURVE_TYPE] == 'UPWARD':
                dayTradeList[prev][CURVE_TYPE] = 'CURVE_HIGH'
            elif dayTradeList[prev][CURVE_TYPE] == 'DOWNWARD':
                dayTradeList[prev][CURVE_TYPE] = 'CURVE_LOW'
            else:
                dayTradeList[prev][CURVE_TYPE] = dayTradeList[cur][CURVE_TYPE]
    return

# 주식 호가 단위(10만원 이상은 500원씩)와 시총 대비 거래량 총 금액 비율도 중요하다.
# MAX치의 0.1%이다. 즉, ~1000원 미만 : 1원, ~5000원, ~10000원, ~50000원, ~100000원, ~500000원, 50만원 이상
# 즉, 비쌀 수록 단타에 유리하다.

# 변동폭 점수 알고리즘
# CurveDay간에 Delta 값을 구한다.
# 그 Delta값들의 절대값을 모두 합한 후 총 수로 나눈다. 그러면 변동폭 평균 값이 나온다.
# 이 평균 값으로 KOSPI 200 종목의 순위를 매기자.
# 이 Delta값은 Percentage로 해야 한다.
# CurveDay Delta 3%, CurveDady Delta -3% 이렇게 있으면 변동폭 평균은 3%가 된다.

# 변동빈도 점수 알고리즘
# 30일 기준으로 얼마나 자주 Curve가 반복되었는지 계산한다. 이는 C++로 만들어 놓은 것을 확인하자.

# 점수 순서는 변동빈도 > 변동폭 > 우상향 이 순서대로 하자.