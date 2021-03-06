from selenium import webdriver
import db
import datetime

NAVER_FINANCE_BASE_URL = 'http://finance.naver.com'
SISE_ENTRYJONGMOK_URL = '/sise/entryJongmok.nhn?&page=%d'
TRADING_TREND_URL = '/item/frgn.nhn?code=%s&page=%d'
ITEM_ANALYSIS_URL = '/item/coinfo.nhn?code=%s'
SISE_KOSPI_URL = '/sise/sise_index_day.nhn?code=KOSPI&page=%d'

# https://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI&page=1

def scrape_kospi_price(driver):
    latestTradeDate = db.getLatestKospiTradeDate()
    if latestTradeDate == None:
        latestTradeDate = (datetime.date.today() - datetime.timedelta(days=360))
    
    latestTradeDate -= datetime.timedelta(days=1)
    latestTradeDate = latestTradeDate.strftime('%Y.%m.%d')

    updateCompleted = False
    page = 1    
    while updateCompleted == False:
        driver.get(NAVER_FINANCE_BASE_URL + SISE_KOSPI_URL % page)
        kospiTrades = driver.find_elements_by_xpath('//table[starts-with(@summary, "일별 시세표")]/tbody/tr/td[@class="date" or @class="rate_down" or @class="number_1"]')
        #kospiPrice = driver.find_elements_by_xpath('//table[starts-with(@summary, "일별 시세표")]/tbody/tr/td[@class="date"]/following-sibling::*[1]')

        for oneTrade in range(0, int(len(kospiTrades) / 6)):
            i = oneTrade * 6

            tradeDate = kospiTrades[i].text
            if tradeDate <= latestTradeDate:
                updateCompleted = True
                break

            price             = float(kospiTrades[i+1].text.replace(',', ''))
            delta             = float(kospiTrades[i+2].text.replace(',', ''))
            percentage        = float(kospiTrades[i+3].text[:len(kospiTrades[i+3].text)-1])
            volume            = int(kospiTrades[i+4].text.replace(',', ''))
            TradeMoneyMillion = int(kospiTrades[i+5].text.replace(',', ''))

            if percentage < 0:
                delta = -delta

            db.addKospiTrade(tradeDate, price, delta, percentage, volume, TradeMoneyMillion)

        page += 1

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

    exKospiTop200 = db.getExKospi200()
    if exKospiTop200 == None:
        return None

    exKospiTop200Map = {}
    for exKospi in exKospiTop200:
        exKospiTop200Map[exKospi[1]] = exKospi[0]

    for stockCode, companyName in exKospiTop200Map.items():
        scrape_stock_trade(driver, companyName, stockCode)

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

def get_today_recommendation_list(baseDate, baseDays):
    kospiTop200 = db.getKospi200()
    if kospiTop200 == None:
        return None
    
    baseInfList = []

    theDate = baseDate - datetime.timedelta(days=baseDays)
    for company in kospiTop200:
        stockCode = company[2]

        bigPlayerData = db.getBigPlayersDataAfterTheDate(stockCode, theDate)
        if bigPlayerData == None:
            continue

        # Curve 마지막 날짜를 주어서 그 이후에 어떤식으로 주가가 진행되었는지 가져온다.
        sumAfterCurve = 0
        stockTrade = db.getStockTradeAfterTheDate(stockCode, bigPlayerData[0][2])
        for trade in stockTrade:
            sumAfterCurve += trade[6] + trade[7]

        sumCurveHighVolume = 0
        sumCurveLowVolume = 0

        compareValue = 0 if 'CURVE_HIGH' == bigPlayerData[0][3] else 1

        for i in range(len(bigPlayerData)):
            if i % 2 == compareValue:
                sumCurveHighVolume += bigPlayerData[i][6]
            else:
                sumCurveLowVolume += bigPlayerData[i][6]

        # 상승폭과 하락폭이 엇비슷한지 계산한다.
        curveSimilarValue = calculate_similar_value(sumCurveHighVolume, sumCurveLowVolume)
        curveSuperiority = calculate_superiority(sumCurveHighVolume, sumCurveLowVolume)

        # 현재까지 포함하여 계산한다.
        if stockTrade[0][5] == 'DOWNWARD':
            sumCurveLowVolume += sumAfterCurve
        else:
            sumCurveHighVolume += sumAfterCurve

        currentSimilarValue = calculate_similar_value(sumCurveHighVolume, sumCurveLowVolume)
        # 판 것과 산 것의 양 차이가 많이 났다가 줄어 드는 것은 원하는 현상이 아니다.
        # 줄어 든게 더 줄어 들기 보단 줄어 들었으니 늘어날 확률이 높다.
        if curveSimilarValue < currentSimilarValue:
            continue;

        # 차이가 너무 미세한 것은 투자 가치가 없다.
        curveCurrentSimilarDiff = round(abs(curveSimilarValue-currentSimilarValue),2)
        if curveCurrentSimilarDiff < 0.03:
            continue;

        currentSuperiority = calculate_superiority(sumCurveHighVolume, sumCurveLowVolume)
        # 현재 상태가 HIGH_BIG인 것은 제외한다. 기준 기간동안 판 것보다 더 샀다는 것이므로 팔 확률이 높다.
        if currentSuperiority == 'HIGH_BIG':
            continue;
           
        # HIGH_BIG -> LOW_BIG으로 바꼈고 그 차이가 큰 것을 찾자. 그 차이가 크고 LOW_BIG이 1에 가까울 수록 산 만큼 팔았다는 것이다.
        # 반대로 LOW_BIG이 1과 멀수록 산 것보다 훨씬 많이 팔았다는 것이다.
        baseInfList.append((company[1], stockCode, baseDate, baseDays, stockTrade[0][3], len(bigPlayerData), curveSimilarValue, curveSuperiority, currentSimilarValue, currentSuperiority, baseDate))

    return baseInfList#sorted(sorted(baseInfList, key=lambda baseInf : baseInf[3], reverse=True), key=lambda baseInf : baseInf[7], reverse=True)

def update_today_recommendation_stock():
    baseDate = db.getLatestStockScrapingDate()
    if baseDate == None:
        return None

    for stock in get_today_recommendation_list(baseDate, 15):
        db.addTodayRecommendation(*stock)

    for stock in get_today_recommendation_list(baseDate, 30):
        db.addTodayRecommendation(*stock)

    return
def calculate_superiority(a, b):
    a = abs(a)
    b = abs(b)

    return 'LOW_BIG' if a < b else 'HIGH_BIG'

def calculate_similar_value(a, b):
    a = abs(a)
    b = abs(b)

    return round((a / b if a < b else b / a), 2)

def update_past_recommendation_results():
    pastStocks = db.getPastRecommendation()
    kospiTrades = {}

    for kospiTrade in db.getKospiTradeAfterFirstRecommendation():
        kospiTrades[kospiTrade[0]] = kospiTrade[1:len(kospiTrade)]

    lastSearchDate = datetime.date.today()

    for pastStock in pastStocks:
        stockCode = pastStock[1]
        baseDate = pastStock[2]
        searchDate = pastStock[11]

        stockTrade = db.getStockTradeAfterTheDate(stockCode, searchDate)
        if stockTrade == None:
            continue

        minRate = db.getMaxPercentageAfterRecommendation(stockCode, baseDate)
        if minRate == None:
            minRate = 2.9 # 최소 3% 이상

        stockTrade.reverse()
        for trade in stockTrade:
            delta = trade[3] - pastStock[4]
            incRate = round((delta / pastStock[4]) * 100, 1)
            if incRate <= minRate:
                continue

            tradeDate = trade[2]

            minRate = incRate

            kospiChangeRate = round(((kospiTrades[tradeDate][0] - kospiTrades[baseDate][0]) / kospiTrades[baseDate][0]) * 100, 1)

            #diffDays = (trade[2] - pastStock[2]).days
            #annualYeild = round((360 / diffDays) * incRate, 1)

            #(@companyName, @stockCode, @baseDate, @period, @basePrice, @successDate, @successPrice)
            db.addPastRecommendationResults(pastStock[0], stockCode, baseDate, pastStock[3], pastStock[4], tradeDate, trade[3], kospiChangeRate)

            
        db.updatePastRecommendationSearchDate(pastStock[1], baseDate, pastStock[3], lastSearchDate)

    return

# 주식 호가 단위(10만원 이상은 500원씩)와 시총 대비 거래량 총 금액 비율도 중요하다.
# MAX치의 0.1%이다. 즉, ~1000원 미만 : 1원, ~5000원, ~10000원, ~50000원, ~100000원, ~500000원, 50만원 이상
# 즉, 비쌀 수록 단타에 유리하다.

# 변동폭 점수 알고리즘
# CurveDay간에 Delta 값을 구한다.
# 그 Delta값들의 절대값을 모두 합한 후 총 수로 나눈다. 그러면 변동폭 평균 값이 나온다.
# 이 평균 값으로 KOSPI 200 종목의 순위를 매기자.
# 이 Delta값은 Percentage로 해야 한다.
# CurveDay Delta 3%, CurveDay Delta -3% 이렇게 있으면 변동폭 평균은 3%가 된다.

# 변동빈도 점수 알고리즘
# 30일 기준으로 얼마나 자주 Curve가 반복되었는지 계산한다. 이는 C++로 만들어 놓은 것을 확인하자.

# 점수 순서는 변동빈도 > 변동폭 > 우상향 이 순서대로 하자.