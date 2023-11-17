from futu import *
trd_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK, host='127.0.0.1', port=11111, security_firm=SecurityFirm.FUTUSECURITIES)
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

ret, data = trd_ctx.acctradinginfo_query(trd_env=TrdEnv.REAL, order_type=OrderType.NORMAL, code='HK.09988', price=88)
if ret == RET_OK:
    print(data)
    print(data['max_cash_and_margin_buy'][0])  # Get maximum quantity that can be bought on margin
else:
    print('acctradinginfo_query error: ', data)
trd_ctx.close()  # Close the current connection
