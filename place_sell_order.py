from futu import *
from utilts.encrypt import decrypt

PASSWORD = os.environ.get('FUTU_PASSWORD')
############################ 全局变量设置 ############################
FUTUOPEND_ADDRESS = '127.0.0.1'  # Futu OpenD 监听地址
FUTUOPEND_PORT = 11111  # Futu OpenD 监听端口

TRADING_ENVIRONMENT = TrdEnv.REAL  # 交易环境：真实 / 模拟
TRADING_MARKET = TrdMarket.HK  # 交易市场权限，用于筛选对应交易市场权限的账户
TRADING_PWD = decrypt(PASSWORD)  # 交易密码，用于解锁交易
TRADING_PERIOD = KLType.K_1M  # 信号 K 线周期
TRADING_SECURITY = 'HK.09988'  # 交易标的

trade_context = OpenSecTradeContext(filter_trdmarket=TRADING_MARKET, host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT, security_firm=SecurityFirm.FUTUSECURITIES)  # 交易对象，根据交易品种修改交易对象类型

# get open order from futu
def get_open_order():
    ret, data = trade_context.order_list_query()
    if ret == RET_OK:
        if data.shape[0] > 0:  # If the order list is not empty
            print(data[['code', 'price', 'qty']])
    else:
        print('order_list_query error: ', data)
    trade_context.close()

# get order status from futu
def get_order_status(order_id):
    ret, data = trade_context.order_list_query(order_id=order_id)
    if ret == RET_OK:
        print(data)
        print(data['order_status'][0])  # Get the order ID of the placed order
        print(data['order_status'].values.tolist())  # Convert to list
    else:
        print('place_order error: ', data)
    trade_context.close()


def place_order(price,qyt,trd_side=TrdSide.BUY):
    if unlock_trade():
        ret, data = trade_context.place_order(price=price, qty=qyt, 
                                              code=TRADING_SECURITY, trd_side=trd_side,
                                                order_type=OrderType.NORMAL, trd_env=TRADING_ENVIRONMENT,
                                                )
        if ret == RET_OK:
            print(data[['price', 'qty']])
        else:
            print('place_order error: ', data)
    trade_context.close()

# 解锁交易
def unlock_trade():
    if TRADING_ENVIRONMENT == TrdEnv.REAL:
        ret, data = trade_context.unlock_trade(TRADING_PWD)
        if ret != RET_OK:
            print('解锁交易失败：', data)
            return False
        print('解锁交易成功！')
    return True

############################ 填充以下函数来完成您的策略 ############################
# 策略启动时运行一次，用于初始化策略
def on_init():
    # 解锁交易（如果是模拟交易则不需要解锁）
    if not unlock_trade():
        return False
    print('************  策略开始运行 ***********')
    return True

def get_five_min_low():
    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data, page_req_key = quote_ctx.request_history_kline(TRADING_SECURITY,ktype='K_DAY', start=start, end=end, max_count=5) # 5 per page, request the first page
    if ret == RET_OK:
        max_close = data['close'].max() # The minimum closing price of the first page
        print(f"max_close: {max_close}")
    else:
        print('error:', data)
    quote_ctx.close() # After using the connection, remember to close it to prevent the number of connections from running out
    return max_close

# get position then sell price at buying price *1.04
def get_position():
    ret, data = trade_context.position_list_query()
    if ret == RET_OK:
        if data.shape[0] > 0:  # If the position list is not empty
            # print stock name qty cost_price market_val
            print(data[['stock_name', 'qty', 'cost_price', 'market_val']])
            return data['cost_price'][0]
    else:
        print('position_list_query error: ', data)
if __name__ == '__main__':
    buying_price = get_position()
    place_order(buying_price*1.04,200,trd_side=TrdSide.SELL)
    # place_order(get_five_min_low(),200,trd_side=TrdSide.SELL)