from futu import *
from utilts.encrypt import decrypt

PASSWORD = os.environ.get('FUTU_PASSWORD')

############################ 全局变量设置 ############################
FUTUOPEND_ADDRESS = '127.0.0.1'  # Futu OpenD 监听地址
FUTUOPEND_PORT = 11111  # Futu OpenD 监听端口

TRADING_ENVIRONMENT = TrdEnv.SIMULATE  # 交易环境：真实 / 模拟
TRADING_MARKET = TrdMarket.HK  # 交易市场权限，用于筛选对应交易市场权限的账户
TRADING_PWD = decrypt(PASSWORD)  # 交易密码，用于解锁交易
TRADING_PERIOD = KLType.K_1M  # 信号 K 线周期
TRADING_SECURITY = 'HK.00700'  # 交易标的
FAST_MOVING_AVERAGE = 1  # 均线快线的周期
SLOW_MOVING_AVERAGE = 3  # 均线慢线的周期

quote_context = OpenQuoteContext(host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT)  # 行情对象
trade_context = OpenSecTradeContext(filter_trdmarket=TRADING_MARKET, host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT, security_firm=SecurityFirm.FUTUSECURITIES)  # 交易对象，根据交易品种修改交易对象类型
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

def on_tick():
    pass

# 展示订单回调
def show_order_status(data):
    order_status = data['order_status'][0]
    order_info = dict()
    order_info['代码'] = data['code'][0]
    order_info['价格'] = data['price'][0]
    order_info['方向'] = data['trd_side'][0]
    order_info['数量'] = data['qty'][0]
    print('【订单状态】', order_status, order_info)

# 订单状态有变化时运行一次
def on_order_status(data):
    if data['code'][0] == TRADING_SECURITY:
        show_order_status(data)

# 委托成交有变化时运行一次
def on_fill(data):
    pass

class OnTickClass(TickerHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        # on_tick()
        ret_code, data = super(OnTickClass,self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("TickerTest: error, msg: %s"% data)
            return RET_ERROR, data
        print("TickerTest ", data) # TickerTest's own processing logic
        return RET_OK, data

class OnOrderClass(TradeOrderHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret, data = super(OnOrderClass, self).on_recv_rsp(rsp_pb)
        if ret == RET_OK:
            on_order_status( data)

class OnFillClass(TradeDealHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret, data = super(OnFillClass, self).on_recv_rsp(rsp_pb)
        if ret == RET_OK:
            on_fill(data)


# 主函数
if __name__ == '__main__':
    # 初始化策略
    if not on_init():
        print('策略初始化失败，脚本退出！')
        quote_context.close()
        trade_context.close()
    else:
        # 设置回调
        quote_context.set_handler(OnTickClass())
        trade_context.set_handler(OnOrderClass())
        trade_context.set_handler(OnFillClass())

        # 订阅标的合约的 逐笔，K 线和摆盘，以便获取数据
        quote_context.subscribe(code_list=[TRADING_SECURITY], subtype_list=[SubType.TICKER, SubType.ORDER_BOOK, TRADING_PERIOD])
