# ICS文件格式解析

最近写了一个生成ics文件的js脚本，过程中大致了解到了ics文件的基本格式，总结在此。







## ics文件结构

```ics
BEGIN:VCALENDAR
//日历本身头部信息

BEGIN:VTIMEZONE
//时区信息

BEGIN:STANDARD
//标准时信息
END:STANDARD

BEGIN:DAYLIGHT
//夏令时信息
END:DAYLIGHT

//时区信息结束
END:VTIMEZONE

//日程循环部分开始，多个日程会有很多个VEVENT的重复
BEGIN:VEVENT
//日程信息
END:VEVENT

BEGIN:VEVENT
//日程信息

BEGIN:VALARM
//提醒信息
END:VALARM

//日程信息结束
END:VEVENT
//....

//日历本身结束
END:VCALENDAR
```

需要注意的是，上面给出的空行是便于观察和学习ics文件结构，实际的ics文件中**不允许有空行**。

## 常用属性

以`X-`开头的属性为私有属性，不一定出现在ics规范中，但能在特定的日历中被识别使用。

以Apple日历导出的属性为例说明：

### VCALENDAR

一个ics文件由一个VCALENDAR结构组成。结构本身包含的属性有：

| 属性名 | 解释 | 典型值/示例值 |
| ----- | --- | ----- |
| METHOD | 公开/私密 | PUBLISH/PRIVATE |
| VERSION | ics版本信息，现在一般为2.0| 2.0 |
| X-WR-CALNAME | 日历名称 | 课表安排 |
| PRODID | 生成ics的程序信息 | -//Apple Inc.//Mac OS X 10.15.6//CN |
| X-WR-TIMEZONE | 时区信息 | Asia/Shanghai |
| CALSCALE | 历法 | GREGORIAN |

#### VTIMEZONE

| 属性名 | 解释 | 典型值/示例值 |
| ----- | --- | ----- |
| TZID | Time Zone Identifier 时区标识符 | Asia/Shanghai |

##### STANDARD

| 属性名 | 解释 | 典型值/示例值 |
| ----- | --- | ----- |
| TZOFFSETFROM | 和GMT的偏值（夏令时） | +0900 |
| RRULE | [重复规则](https://icalendar.org/iCalendar-RFC-5545/3-3-10-recurrence-rule.html) | FREQ=YEARLY;UNTIL=19910914T170000Z;BYMONTH=9; |
| BYDAY | 重复规则 | 3SU |
| DTSTART | 标准时开始时间 | 19890917T020000 |
| TZNAME | 时区名称 | GMT+8 |
| TZOFFSETTO | 和GMT的偏值（标准时间） | +0800 |

##### DAYLIGHT

在没有夏令时的地区，可以不加DAYLIGHT部分，但STANDARD里的RRULE和BYDAY需要删除。

| 属性名 | 解释 | 典型值/示例值 |
| ----- | --- | ----- |
| TZOFFSETFROM | 和GMT的偏值（夏令时） | +0900 |
| DTSTART | 夏令时开始时间 | 19890917T020000 |
| TZNAME | 时区名称 | GMT+8 |
| TZOFFSETTO | 和GMT的偏值（夏令时） | +0800 |
| RDATE |  | 19910414T020000 |

#### VEVENT

| 属性名 | 解释 | 典型值 |
| ----- | --- | ----- |
| TRANSP | 独占时间 | OPAQUE |
| SEQUENCE | 第几次修改事件 | 1 |
| CREATED | 创建日程时间 | 20200905T120042Z |
| DTSTAMP | 生成日程时间 | 20200905T120042Z |
| LAST-MODIFIED | 上次修改日程时间 | 20200905T120042Z |
| UID | GUID/UUID，日程唯一识别符，按照格式随机生成 | 66159abd-f4b9-477f-8eb8-4772eb9347e1 |
| SUMMARY | 日程名称 | 一个日程示例 by @Saafo |
| LOCATION | 日程地点 | 成都双流国际机场 |
| DESCRIPTION | 日程详细描述 | ics文件说明 from mintsky.xyz |
| DTSTART;TZID=Asia/Shanghai | 日程开始时间（上海时区） | 20200907T083000 |
| DTEND;TZID=Asia/Shanghai | 日程结束时间（上海时区） | 20200907T100500 |
| RRULE | 重复规则 | <放到后面专门讲> |

##### VALARM

| 属性名 | 解释 | 典型值 |
| ----- | --- | ----- |
| UID | GUID/UUID，提醒唯一识别符，按照格式随机生成 | 66159abd-f4b9-477f-8eb8-4772eb9347e1 |


## RRULE

Repeating Rule的规则不是一句话能说清的，所以放在这里单独讲。

DTSTART为循环起始时间，DTEND为第一次终止的时间，FREQ为循环频率（YEARLY, MONTHLY, DAILY），UNTIL为终止时间。更多详细的参数可以查看[文档](https://icalendar.org/iCalendar-RFC-5545/3-8-5-3-recurrence-rule.html)。

## 样例

本次写的仓库地址在[这里](https://github.com/Saafo/uestc-coursetable-parser)。语言为`JavaScript`。如果需要可以参考，如果有帮到你可以选择`Star`本仓库！