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

def place_order(price,qyt,trd_side=TrdSide.BUY):
    if unlock_trade():
        ret, data = trade_context.place_order(price=price, qty=qyt, 
                                              code=TRADING_SECURITY, trd_side=trd_side,
                                                order_type=OrderType.NORMAL, trd_env=TRADING_ENVIRONMENT,
                                                )
        if ret == RET_OK:
            print(data)
            print(data['order_id'][0])  # Get the order ID of the placed order
            print(data['order_id'].values.tolist())  # Convert to list
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
    start = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data, page_req_key = quote_ctx.request_history_kline(TRADING_SECURITY,ktype='K_1M', start=end, end=end, max_count=100) # 5 per page, request the first page
    if ret == RET_OK:
        min_close = data['close'].min() # The minimum closing price of the first page
        print(f"min_close: {min_close}")
    else:
        print('error:', data)
    quote_ctx.close() # After using the connection, remember to close it to prevent the number of connections from running out
    return min_close

if __name__ == '__main__':
    # place_order(get_five_min_low(),200,trd_side=TrdSide.BUY)
    get_five_min_low()