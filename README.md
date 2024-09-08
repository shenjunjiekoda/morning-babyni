# morning-babyni

Morning to my baby ni from Wechat Public Tester by Github action.

Get your `APP_ID`,`APP_SECRET`,`TEMPLATE_ID` and etc from [here](https://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index)

And you can customize the template on the platform, My template is in [template.md](template.md).

Setup your `environment variables` and `cron` in your repo action secrets, see in [morning.yml](.github/workflows/action.yml)

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
pip install -r requirements.txt && python morning.py
```
