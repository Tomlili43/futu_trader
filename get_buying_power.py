from futu import *
trd_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK, host='127.0.0.1', port=11111, security_firm=SecurityFirm.FUTUSECURITIES)
ret, data = trd_ctx.accinfo_query()
if ret == RET_OK:
    print(f"Maximum buying power {data['power'][0]}") 
    print(f"Short buying power {data['max_power_short'][0]}") 
    print(f"Cash buying power {data['net_cash_power'][0]}") 
else:
    print('accinfo_query error: ', data)
trd_ctx.close()  # Close the current connection
 