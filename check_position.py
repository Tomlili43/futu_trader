from futu import *
trd_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK,host='127.0.0.1', port=11111, security_firm=SecurityFirm.FUTUSECURITIES)
ret, data = trd_ctx.position_list_query()
if ret == RET_OK:
    if data.shape[0] > 0:  # If the position list is not empty
        print(data['stock_name'][0])  # Get the first stock name of the holding position
        print(data['qty'][0])
        print(data['cost_price'][0])
        print(data['market_val'][0])
else:
    print('position_list_query error: ', data)
trd_ctx.close()  # Close the current connection

