# morning-babyni

Morning to my baby ni from Wechat Public Tester or PushDeer or PushPlus by Github action.

And you can customize the template on the platform, My template is in [template.md](template.md).

Setup your `environment variables` and `cron` in your repo action secrets, see in [morning.yml](.github/workflows/action.yml)

## Wechat Public Tester

Get your `APP_ID`,`APP_SECRET`,`TEMPLATE_ID` and etc from [here](https://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index)

1. Login to get `APP_ID` and `APP_SECRET`.
2. Add your template in the platform and get the `TEMPLATE_ID`.
3. Scan the QR code to add your wechat account to the test group and get user's `USER_ID`. You can add multiple user's `USER_ID` by separate them by comma.

## PushDeer

Download and install the app, then add your `PUSHKEY` to the environment variables.

### iOS14+

![](doc/image/clipcode.png)

Iphone (iOS 14+) users can scan the QR code to launch the PushDeer app. Alternatively, they can download the app from the *App Store*.

> Note: Do not install PushDeer self-hosted version.

### MacOS 11+

Mac 11+ users can download the app from the *app Store.app*.

### Android

Android users can download the app test version from ([GitHub](https://github.com/easychen/pushdeer/releases/tag/android1.0alpha)|[Gitee](https://gitee.com/easychen/pushdeer/releases/android1.0alpha))。

## PushPlus

Get your `PUSHPLUS_TOKENS` from [here](https://www.pushplus.plus/push1.html)

## Run in local

Run by Python in local:

```shell
export APP_ID='xxxxx'
export APP_SECRET='xxxxxxx'
export TEMPLATE_ID='xxxxxx'
export USER_IDS='xxxx,yyyy'
export NAMES='koda,koni'
export LOVE_DATE='2016-11-29'
export BIRTHDAY='1997-10-03'
export CITY='上海'
export PROVINCE='上海'
export PUSHDEER_PUSHKEYS='xxxxxx'
export PUSHPLUS_TOKENS='xxxxxx'
pip install -r requirements.txt && python morning.py --channel='all'
```
