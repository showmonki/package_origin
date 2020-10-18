# Change Log
## Scrapping code
|  Date   | Status  |#| Content  | Note  |
|  ----  | ----  | ----  | ----  | ----  |
| 2020/10/15  | Done | 1.| 封装为one_page函数，增加参数设定  | ---- |
|  | Done  | 2.|修改失败后第一次补爬loop逻辑| sleep仅设置在download发生时生效，df不应该再次被更新（产生重复值）|
|  | Done  | 3.|download function中回调部分设定次数限制| 避免过多自循环爬数  |
|  | Done  | 4.|storename换位置取店名| 无需两列数据，两列产生原因是因为店铺名包含搜索关键词 ， 原storename应该与storetype合并 |
|  | Done  | 5.|单页内爬取图片sleep时间减少为1秒| 单页内实际人工操作也不会花很长时间  |
|  | ----  | ---|---| ---  |
| 2020/10/18 | Done  | 翻页实现| 翻页function several_page |可控制选择max翻页页数
| TODO | --- | ---|验证码| ---  |
|  | ----  | ---|网速慢，图片加载问题| ---  |
## Model code