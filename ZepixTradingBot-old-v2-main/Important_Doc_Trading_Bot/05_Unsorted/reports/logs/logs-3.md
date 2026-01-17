Microsoft Windows [Version 10.0.20348.4294]
(c) Microsoft Corporation. All rights reserved.

C:\Users\Administrator>cd ZepixTradingBot-New-v2

C:\Users\Administrator\ZepixTradingBot-New-v2>python src/main.py --host 0.0.0.0 --port 80
Config loaded - MT5 Login: 308646228, Server: XMGlobal-MT5 6
==================================================
ZEPIX TRADING BOT v2.0
==================================================
Starting server on 0.0.0.0:80
Features enabled:
+ Fixed lot sizes
+ Re-entry system
+ SL hunting protection
+ 1:1.5 Risk-Reward
+ Progressive SL reduction
==================================================
←[32mINFO←[0m:     Started server process [←[36m4596←[0m]
←[32mINFO←[0m:     Waiting for application startup.
SUCCESS: MT5 connection established
Account Balance: $8970.50
Account: 308646228 | Server: XMGlobal-MT5 6
SUCCESS: Trend manager set in Telegram bot
SUCCESS: Trading engine initialized successfully
SUCCESS: Price monitor service started
SUCCESS: Profit booking manager initialized
SUCCESS: Telegram bot polling started
←[32mINFO←[0m:     Application startup complete.
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://0.0.0.0:80←[0m (Press CTRL+C to quit)
Webhook received: {
  "type": "entry",
  "symbol": "EURUSD",
  "signal": "buy",
  "tf": "5m",
  "price": 1.1,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'entry', 'symbol': 'EURUSD', 'signal': 'buy', 'tf': '5m', 'price': 1.1, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
ERROR: Order failed: Invalid stops (Error code: 10016)
Request details: Symbol=EURUSD, Lot=0.05, Price=1.16355, SL=1.085, TP=1.1225
ERROR: Order failed: Invalid stops (Error code: 10016)
Request details: Symbol=EURUSD, Lot=0.05, Price=1.16355, SL=1.098, TP=1.103
2025-11-13 21:38:16 - src.managers.dual_order_manager - ERROR - ERROR: Both orders failed: EURUSD BUY
WARNING: Dual order error: Order A failed: MT5 order placement failed
WARNING: Dual order error: Order B failed: MT5 order placement failed
←[32mINFO←[0m:     127.0.0.1:51393 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
←[32mINFO←[0m:     120.76.250.13:35996 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
Webhook received: {
  "type": "entry",
  "symbol": "EURUSD",
  "signal": "buy",
  "tf": "5m",
  "price": 1.1,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'entry', 'symbol': 'EURUSD', 'signal': 'buy', 'tf': '5m', 'price': 1.1, 'strategy': 'ZepixPremium'}
ERROR: Duplicate alert detected
←[32mINFO←[0m:     3.110.221.62:51398 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
SUCCESS: Mode set to AUTO for XAUUSD 5m
SUCCESS: Trend updated: XAUUSD 5m -> BEARISH (MANUAL)
SUCCESS: Mode set to AUTO for XAUUSD 5m
←[32mINFO←[0m:     188.166.16.179:54933 - "←[1mGET /admin/config.php HTTP/1.0←[0m" ←[31m404 Not Found←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
←[32mINFO←[0m:     5.187.35.21:59740 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.32.218.31:51696 - "←[1mHEAD /Core/Skin/Login.aspx HTTP/1.1←[0m" ←[31m404 Not Found←[0m
Webhook received: {
  "type": "entry",
  "symbol": "XAUUSD",
  "signal": "buy",
  "tf": "1h",
  "price": 4179.095,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'entry', 'symbol': 'XAUUSD', 'signal': 'buy', 'tf': '1h', 'price': 4179.095, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
ERROR: Trend not aligned for LOGIC3: {'1d': 'NEUTRAL', '1h': 'BEARISH'}
←[32mINFO←[0m:     52.32.178.7:31422 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
Webhook received: {
  "type": "trend",
  "symbol": "XAUUSD",
  "signal": "bull",
  "tf": "15m",
  "price": 4179.095,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'trend', 'symbol': 'XAUUSD', 'signal': 'bull', 'tf': '15m', 'price': 4179.095, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
SUCCESS: Trend updated: XAUUSD 15m -> BULLISH (AUTO)
←[32mINFO←[0m:     34.212.75.30:26520 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
Webhook received: {
  "type": "entry",
  "symbol": "XAUUSD",
  "signal": "buy",
  "tf": "15m",
  "price": 4179.095,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'entry', 'symbol': 'XAUUSD', 'signal': 'buy', 'tf': '15m', 'price': 4179.095, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
ERROR: Trend not aligned for LOGIC2: {'1h': 'BEARISH', '15m': 'BULLISH'}
←[32mINFO←[0m:     52.32.178.7:56522 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
←[32mINFO←[0m:     103.252.89.75:51026 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     64.62.197.2:40056 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     64.62.197.15:59113 - "←[1mGET /favicon.ico HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     64.62.197.2:47926 - "←[1mGET /geoserver/web/ HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     213.209.157.254:41452 - "←[1mGET /.git/config HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     165.154.204.47:34784 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     51.158.54.10:61001 - "←[1mGET / HTTP/1.0←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     87.236.176.22:38761 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.32.218.31:39406 - "←[1mHEAD /Core/Skin/Login.aspx HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     92.60.40.229:56073 - "←[1mGET /.env HTTP/1.1←[0m" ←[31m404 Not Found←[0m
Webhook received: {
  "type": "trend",
  "symbol": "XAUUSD",
  "signal": "bear",
  "tf": "5m",
  "price": 4183.81,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'trend', 'symbol': 'XAUUSD', 'signal': 'bear', 'tf': '5m', 'price': 4183.81, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
SUCCESS: Trend updated: XAUUSD 5m -> BEARISH (AUTO)
←[32mINFO←[0m:     34.212.75.30:28062 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
←[32mINFO←[0m:     206.168.34.200:19974 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     206.168.34.200:18042 - "←[1mPRI %2A HTTP/2.0←[0m" ←[31m404 Not Found←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
←[33mWARNING←[0m:  Invalid HTTP request received.
←[32mINFO←[0m:     206.168.34.200:59812 - "←[1mGET /wiki HTTP/1.1←[0m" ←[31m404 Not Found←[0m
Webhook received: {
  "type": "entry",
  "symbol": "XAUUSD",
  "signal": "sell",
  "tf": "5m",
  "price": 4176.685,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'entry', 'symbol': 'XAUUSD', 'signal': 'sell', 'tf': '5m', 'price': 4176.685, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
ERROR: Trend not aligned for LOGIC1: {'1h': 'BEARISH', '15m': 'BULLISH'}
←[32mINFO←[0m:     34.212.75.30:27280 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mPOST /cgi-bin/../../../../../../../../../../bin/sh HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mPOST /cgi-bin/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/bin/sh HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mPOST /hello.world?%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mPOST /?%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /vendor/phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /vendor/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /vendor/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /vendor/phpunit/phpunit/LICENSE/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /vendor/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /lib/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /lib/phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /lib/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /lib/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /lib/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /www/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /ws/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /yii/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /zend/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /ws/ec/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /V2/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /tests/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /test/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /testing/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /api/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /demo/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /cms/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /crm/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /admin/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /backup/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /blog/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /workspace/drupal/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /panel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /public/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /apps/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /app/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /index.php?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=Hello HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /public/index.php?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=Hello HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /index.php?lang=../../../../../../../../usr/local/lib/php/pearcmd&+config-create+/&/<?echo(md5("hi"));?>+/tmp/index1.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /index.php?lang=../../../../../../../../tmp/index1 HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.36.107.228:57486 - "←[1mGET /containers/json HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mPOST /cgi-bin/../../../../../../../../../../bin/sh HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mPOST /cgi-bin/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/bin/sh HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mPOST /hello.world?%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mPOST /?%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /vendor/phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /vendor/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /vendor/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /vendor/phpunit/phpunit/LICENSE/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /vendor/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /lib/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /lib/phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /lib/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /lib/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /lib/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /www/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /ws/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /yii/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /zend/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /ws/ec/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /V2/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /tests/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /test/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /testing/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /api/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /demo/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /cms/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /crm/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /admin/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /backup/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /blog/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /workspace/drupal/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /panel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /public/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /apps/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /app/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /index.php?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=Hello HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /public/index.php?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=Hello HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /index.php?lang=../../../../../../../../usr/local/lib/php/pearcmd&+config-create+/&/<?echo(md5("hi"));?>+/tmp/index1.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /index.php?lang=../../../../../../../../tmp/index1 HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     82.66.241.245:38924 - "←[1mGET /containers/json HTTP/1.1←[0m" ←[31m404 Not Found←[0m
Webhook received: {
  "type": "trend",
  "symbol": "XAUUSD",
  "signal": "bull",
  "tf": "5m",
  "price": 4190.025,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'trend', 'symbol': 'XAUUSD', 'signal': 'bull', 'tf': '5m', 'price': 4190.025, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
SUCCESS: Trend updated: XAUUSD 5m -> BULLISH (AUTO)
←[32mINFO←[0m:     52.32.178.7:56558 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
←[32mINFO←[0m:     205.210.31.34:53654 - "←[1mGET / HTTP/1.0←[0m" ←[31m404 Not Found←[0m
Webhook received: {
  "type": "entry",
  "symbol": "XAUUSD",
  "signal": "buy",
  "tf": "5m",
  "price": 4197.865,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'entry', 'symbol': 'XAUUSD', 'signal': 'buy', 'tf': '5m', 'price': 4197.865, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
ERROR: Trend not aligned for LOGIC1: {'1h': 'BEARISH', '15m': 'BULLISH'}
←[32mINFO←[0m:     52.32.178.7:50792 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
←[32mINFO←[0m:     205.210.31.129:57594 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
←[32mINFO←[0m:     91.232.238.112:61001 - "←[1mGET / HTTP/1.0←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     118.123.1.32:37890 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     118.123.1.32:37892 - "←[1mGET /visitors_online HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     118.123.1.32:37896 - "←[1mGET /getServerConfig HTTP/1.1←[0m" ←[31m404 Not Found←[0m
Webhook received: {
  "type": "entry",
  "symbol": "XAUUSD",
  "signal": "sell",
  "tf": "5m",
  "price": 4202.74,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'entry', 'symbol': 'XAUUSD', 'signal': 'sell', 'tf': '5m', 'price': 4202.74, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
ERROR: Trend not aligned for LOGIC1: {'1h': 'BEARISH', '15m': 'BULLISH'}
←[32mINFO←[0m:     52.32.178.7:54034 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
←[32mINFO←[0m:     59.88.153.247:46038 - "←[1mPOST /GponForm/diag_Form?images/ HTTP/1.1←[0m" ←[31m404 Not Found←[0m
Webhook received: {
  "type": "trend",
  "symbol": "XAUUSD",
  "signal": "bear",
  "tf": "5m",
  "price": 4200.235,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'trend', 'symbol': 'XAUUSD', 'signal': 'bear', 'tf': '5m', 'price': 4200.235, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
SUCCESS: Trend updated: XAUUSD 5m -> BEARISH (AUTO)
←[32mINFO←[0m:     52.32.178.7:25210 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
Webhook received: {
  "type": "trend",
  "symbol": "XAUUSD",
  "signal": "bear",
  "tf": "15m",
  "price": 4188.295,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'trend', 'symbol': 'XAUUSD', 'signal': 'bear', 'tf': '15m', 'price': 4188.295, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
SUCCESS: Trend updated: XAUUSD 15m -> BEARISH (AUTO)
←[32mINFO←[0m:     52.32.178.7:48078 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
←[32mINFO←[0m:     93.174.93.12:60000 - "←[1mGET / HTTP/1.0←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.32.218.31:50900 - "←[1mHEAD /Core/Skin/Login.aspx HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     213.209.157.254:53916 - "←[1mGET /.git/index HTTP/1.1←[0m" ←[31m404 Not Found←[0m
SUCCESS: Trend updated: XAUUSD 1d -> BEARISH (MANUAL)
SUCCESS: Mode set to AUTO for XAUUSD 1d
←[32mINFO←[0m:     185.180.140.118:60313 - "←[1mGET /sitecore/shell/sitecore.version.xml HTTP/1.1←[0m" ←[31m404 Not Found←[0m
Webhook received: {
  "type": "entry",
  "symbol": "XAUUSD",
  "signal": "sell",
  "tf": "1h",
  "price": 4178.16,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'entry', 'symbol': 'XAUUSD', 'signal': 'sell', 'tf': '1h', 'price': 4178.16, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
SUCCESS: Order placed successfully: Ticket #472956057
SUCCESS: Order placed successfully: Ticket #472956062
←[32mINFO←[0m:     52.32.178.7:53094 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
Webhook received: {
  "type": "entry",
  "symbol": "XAUUSD",
  "signal": "sell",
  "tf": "15m",
  "price": 4178.16,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'entry', 'symbol': 'XAUUSD', 'signal': 'sell', 'tf': '15m', 'price': 4178.16, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
SUCCESS: Order placed successfully: Ticket #472956068
SUCCESS: Order placed successfully: Ticket #472956069
←[32mINFO←[0m:     52.32.178.7:53100 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
Auto-reconciliation: Position 472956062 already closed in MT5
SUCCESS: Position 472956062 already closed (not found in MT5)
Trade Closed: XAUUSD SELL
   Entry: 4178.16000 -> Close: 4179.82500
   Pips: -166.5 | PnL: $-8.33
   Reason: MT5_AUTO_CLOSED
Auto-reconciliation: Position 472956069 already closed in MT5
SUCCESS: Position 472956069 already closed (not found in MT5)
Trade Closed: XAUUSD SELL
   Entry: 4178.16000 -> Close: 4179.47500
   Pips: -131.5 | PnL: $-6.58
   Reason: MT5_AUTO_CLOSED
2025-11-14 06:32:19 - src.managers.profit_booking_manager - WARNING - Chain PROFIT_XAUUSD_f5a06d56 has missing order: 472956062 (check 1/3)
2025-11-14 06:32:19 - src.managers.profit_booking_manager - WARNING - Chain PROFIT_XAUUSD_123b5cc2 has missing order: 472956069 (check 1/3)
2025-11-14 06:33:19 - src.managers.profit_booking_manager - WARNING - Marking chain PROFIT_XAUUSD_f5a06d56 as STALE - all orders missing after 3 checks
2025-11-14 06:33:19 - src.managers.profit_booking_manager - WARNING - Marking chain PROFIT_XAUUSD_123b5cc2 as STALE - all orders missing after 3 checks
←[32mINFO←[0m:     20.65.194.88:38808 - "←[1mGET /actuator/health HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.32.218.31:42466 - "←[1mHEAD /Core/Skin/Login.aspx HTTP/1.1←[0m" ←[31m404 Not Found←[0m
Webhook received: {
  "type": "entry",
  "symbol": "XAUUSD",
  "signal": "buy",
  "tf": "5m",
  "price": 4178.91,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'entry', 'symbol': 'XAUUSD', 'signal': 'buy', 'tf': '5m', 'price': 4178.91, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
SUCCESS: Position 472956057 closed successfully
Error: 'RiskManager' object has no attribute 'remove_closed_trade'
←[32mINFO←[0m:     34.212.75.30:52258 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
←[33mWARNING←[0m:  Invalid HTTP request received.
←[32mINFO←[0m:     45.82.78.100:39382 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     93.123.109.22:51036 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     93.123.109.22:51036 - "←[1mGET /favicon.ico HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     34.52.204.70:56804 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     43.153.9.143:35076 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mPOST /cgi-bin/../../../../../../../../../../bin/sh HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mPOST /cgi-bin/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/bin/sh HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mPOST /hello.world?%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mPOST /?%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /vendor/phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /vendor/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /vendor/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     3.131.215.38:45630 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /vendor/phpunit/phpunit/LICENSE/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /vendor/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /lib/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /lib/phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /lib/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /lib/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /lib/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /www/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /ws/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /yii/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /zend/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /ws/ec/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /V2/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /tests/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /test/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /testing/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /api/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /demo/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /cms/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /crm/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /admin/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /backup/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /blog/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /workspace/drupal/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /panel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /public/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /apps/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /app/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /index.php?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=Hello HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /public/index.php?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=Hello HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /index.php?lang=../../../../../../../../usr/local/lib/php/pearcmd&+config-create+/&/<?echo(md5("hi"));?>+/tmp/index1.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /index.php?lang=../../../../../../../../tmp/index1 HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     158.220.115.215:57026 - "←[1mGET /containers/json HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     3.131.215.38:45792 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
←[33mWARNING←[0m:  Invalid HTTP request received.
←[33mWARNING←[0m:  Invalid HTTP request received.
←[32mINFO←[0m:     87.121.84.52:45564 - "←[1mGET / HTTP/1.0←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     87.120.191.6:40704 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.252.89.75:58756 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.32.218.31:46346 - "←[1mHEAD /Core/Skin/Login.aspx HTTP/1.1←[0m" ←[31m404 Not Found←[0m
Auto-reconciliation: Position 472956068 already closed in MT5
SUCCESS: Position 472956068 already closed (not found in MT5)
Trade Closed: XAUUSD SELL
   Entry: 4178.16000 -> Close: 4155.34500
   Pips: 2281.5 | PnL: $114.08
   Reason: MT5_AUTO_CLOSED
Webhook received: {
  "type": "entry",
  "symbol": "XAUUSD",
  "signal": "sell",
  "tf": "5m",
  "price": 4153.02,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'entry', 'symbol': 'XAUUSD', 'signal': 'sell', 'tf': '5m', 'price': 4153.02, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
SUCCESS: Order placed successfully: Ticket #473160889
SUCCESS: Order placed successfully: Ticket #473160893
←[32mINFO←[0m:     52.32.178.7:35160 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
SUCCESS: Position 473160893 closed successfully
Trade Closed: XAUUSD SELL
   Entry: 4153.02000 -> Close: 4150.83500
   Pips: 218.5 | PnL: $10.93
   Reason: PROFIT_BOOKING
SUCCESS: Order placed successfully: Ticket #473161454
SUCCESS: Order placed successfully: Ticket #473161460
SUCCESS: Position 473161454 closed successfully
Trade Closed: XAUUSD SELL
   Entry: 4150.76000 -> Close: 4148.93500
   Pips: 182.5 | PnL: $9.13
   Reason: PROFIT_BOOKING
SUCCESS: Position 473161460 closed successfully
Trade Closed: XAUUSD SELL
   Entry: 4150.76000 -> Close: 4148.98000
   Pips: 178.0 | PnL: $8.90
   Reason: PROFIT_BOOKING
SUCCESS: Order placed successfully: Ticket #473163059
SUCCESS: Order placed successfully: Ticket #473163065
SUCCESS: Order placed successfully: Ticket #473163072
SUCCESS: Order placed successfully: Ticket #473163081
Auto-reconciliation: Position 473163059 already closed in MT5
SUCCESS: Position 473163059 already closed (not found in MT5)
Trade Closed: XAUUSD SELL
   Entry: 4148.74000 -> Close: 4142.68500
   Pips: 605.5 | PnL: $30.28
   Reason: MT5_AUTO_CLOSED
Auto-reconciliation: Position 473163065 already closed in MT5
SUCCESS: Position 473163065 already closed (not found in MT5)
Trade Closed: XAUUSD SELL
   Entry: 4148.74000 -> Close: 4143.84500
   Pips: 489.5 | PnL: $24.47
   Reason: MT5_AUTO_CLOSED
Auto-reconciliation: Position 473163072 already closed in MT5
SUCCESS: Position 473163072 already closed (not found in MT5)
Trade Closed: XAUUSD SELL
   Entry: 4148.74000 -> Close: 4143.61500
   Pips: 512.5 | PnL: $25.62
   Reason: MT5_AUTO_CLOSED
Auto-reconciliation: Position 473163081 already closed in MT5
SUCCESS: Position 473163081 already closed (not found in MT5)
Trade Closed: XAUUSD SELL
   Entry: 4148.74000 -> Close: 4143.98000
   Pips: 476.0 | PnL: $23.80
   Reason: MT5_AUTO_CLOSED
2025-11-14 11:17:29 - src.managers.profit_booking_manager - WARNING - Chain PROFIT_XAUUSD_34892f04 has missing order: 473163059 (check 1/3)
2025-11-14 11:17:29 - src.managers.profit_booking_manager - WARNING - Chain PROFIT_XAUUSD_34892f04 has missing order: 473163065 (check 1/3)
2025-11-14 11:17:29 - src.managers.profit_booking_manager - WARNING - Chain PROFIT_XAUUSD_34892f04 has missing order: 473163072 (check 1/3)
2025-11-14 11:17:29 - src.managers.profit_booking_manager - WARNING - Chain PROFIT_XAUUSD_34892f04 has missing order: 473163081 (check 1/3)
2025-11-14 11:18:29 - src.managers.profit_booking_manager - WARNING - Marking chain PROFIT_XAUUSD_34892f04 as STALE - all orders missing after 3 checks
←[32mINFO←[0m:     146.70.188.181:37163 - "←[1mGET /.git/config HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     146.70.188.181:39535 - "←[1mGET /.env HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     146.70.188.181:42016 - "←[1mGET /.env.production HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     148.135.254.180:60781 - "←[1mGET /.env HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     148.135.254.180:42929 - "←[1mPOST / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
Webhook received: {
  "type": "bias",
  "symbol": "XAUUSD",
  "signal": "bear",
  "tf": "1h",
  "price": 4133.18,
  "strategy": "ZepixPremium"
}
ALERT: Received alert: {'type': 'bias', 'symbol': 'XAUUSD', 'signal': 'bear', 'tf': '1h', 'price': 4133.18, 'strategy': 'ZepixPremium'}
SUCCESS: Alert validation successful
SUCCESS: Trend updated: XAUUSD 1h -> BEARISH (AUTO)
←[32mINFO←[0m:     34.212.75.30:56982 - "←[1mPOST /webhook HTTP/1.1←[0m" ←[32m200 OK←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
Auto-reconciliation: Position 473160889 already closed in MT5
SUCCESS: Position 473160889 already closed (not found in MT5)
Trade Closed: XAUUSD SELL
   Entry: 4153.02000 -> Close: 4130.15000
   Pips: 2287.0 | PnL: $114.35
   Reason: MT5_AUTO_CLOSED
←[32mINFO←[0m:     18.207.144.231:39622 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mPOST /cgi-bin/../../../../../../../../../../bin/sh HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mPOST /cgi-bin/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/bin/sh HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mPOST /hello.world?%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mPOST /?%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /vendor/phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /vendor/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /vendor/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /vendor/phpunit/phpunit/LICENSE/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /vendor/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /lib/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /lib/phpunit/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /lib/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /lib/phpunit/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /lib/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /www/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /ws/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /yii/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /zend/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /ws/ec/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /V2/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /tests/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /test/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /testing/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /api/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /demo/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /cms/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /crm/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /admin/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /backup/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /blog/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /workspace/drupal/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /panel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /public/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /apps/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /app/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /index.php?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=Hello HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /public/index.php?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=Hello HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /index.php?lang=../../../../../../../../usr/local/lib/php/pearcmd&+config-create+/&/<?echo(md5("hi"));?>+/tmp/index1.php HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /index.php?lang=../../../../../../../../tmp/index1 HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     103.143.11.97:51464 - "←[1mGET /containers/json HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.32.218.31:40556 - "←[1mHEAD /Core/Skin/Login.aspx HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
←[32mINFO←[0m:     103.252.89.75:50256 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     51.158.54.10:61001 - "←[1mGET / HTTP/1.0←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     101.32.218.31:32918 - "←[1mHEAD /Core/Skin/Login.aspx HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
←[32mINFO←[0m:     103.252.89.75:37614 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     20.168.107.40:39402 - "←[1mGET /druid/index.html HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
←[32mINFO←[0m:     87.120.191.6:45590 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     87.120.191.6:45606 - "←[1mDELETE / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     87.120.191.6:33708 - "←[1mTRACE / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[33mWARNING←[0m:  Invalid HTTP request received.
←[32mINFO←[0m:     101.32.218.31:51588 - "←[1mHEAD /Core/Skin/Login.aspx HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     43.163.206.70:33884 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     119.28.140.106:48460 - "←[1mGET / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     91.232.238.112:61001 - "←[1mGET / HTTP/1.0←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     179.61.245.83:50351 - "←[1mGET /.env HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     179.61.245.83:34517 - "←[1mPOST / HTTP/1.1←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     131.196.48.84:61001 - "←[1mGET /admin/config.php HTTP/1.0←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     91.232.238.153:61001 - "←[1mGET /admin/config.php HTTP/1.0←[0m" ←[31m404 Not Found←[0m
←[32mINFO←[0m:     Shutting down
←[32mINFO←[0m:     Waiting for application shutdown.
Trading bot shutting down...
←[32mINFO←[0m:     Application shutdown complete.
←[32mINFO←[0m:     Finished server process [←[36m4596←[0m]

C:\Users\Administrator\ZepixTradingBot-New-v2>