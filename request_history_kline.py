from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start='2019-09-11', end='2019-09-18', max_count=5) # 5 per page, request the first page
if ret == RET_OK:
    print(data)
    print(data['code'][0]) # Take the first stock code
    print(data['close'].values.tolist()) # The closing price of the first page is converted to a list
else:
    print('error:', data)
while page_req_key != None: # Request all results after
    print('*************************************')
    ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start='2019-09-11', end='2019-09-18', max_count=5,page_req_key=page_req_key) # Request the page after turning data
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
print('All pages are finished!')
quote_ctx.close() # After using the connection, remember to close it to prevent the number of connections from running out
