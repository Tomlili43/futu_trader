from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

ret, data = quote_ctx.get_market_snapshot(['HK.09988'])
if ret == RET_OK:
    last_price = data['last_price'][0]  # 最新价格
    print(last_price)

else:
    print('can not get latest price', data)
quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽
