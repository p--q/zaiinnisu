#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date
import calendar
import math
evaldatestring = "2021-2-8"  # 評価日の文字列。
inpatients = 0  # 評価日24時の在院患者数。
admissions_discharges = 0  # 評価日までの入退院数。
total_days = 0  # 評価日までののべ在院日数。
stay_length = 21 # 達成すべき平均在院日数。


evaldate = date.fromisoformat(evaldatestring)
days = calendar.monthrange(evaldate.year, evaldate.month)[1] - evaldate.day + 1  # 残日数。

admissions_per_unit = 1  # 単位あたりの入院患者数。
discharges_per_unit = 1  # 単位あたりの退院患者数。


for discharge_interval in range(1, days+1): # 退院間隔
	for admission_interval in range(1, days+1):  # 入院間隔




pnk = 0  # 当日の入院患者数。
ab = 0  # 前日までの入退院数合計。
zn = 0  # 前日までののべ在院日数。
rds = 31  # 当月の残日数。
a = 1  # 今後の1日あたりの入院数。
b = 1  # 今後の１日あたりの退院数。

cols = []
for bi in range(1, rds+1): # 退院間隔
	for ai in range(1,rds+1):  # 入院間隔
		cols.append("{}".format(bi-1))
		ps = []  # 1日あたりの入院患者数
		for d in range(1,rds+1):  # 経過日数
			ps.append(a*math.floor(d/ai) - b*math.floor(d/bi))  # １日患者数を取得。
		if pnk+min(ps)<0:  # 入院患者数合計が負になるとき。
			cols.append("")
		else:  # 実現可能なとき
			neoa = a*math.floor(rds/ai)  # 新規入院患者数。
			neob = b*math.floor(rds/bi)  # 新規退院患者数。
			z = (zn+sum(ps))*2/(ab+neoa+neob)  # 予測平均在院日数を取得。
			z2 = (zn+sum(ps)+neob)*2/(ab+neoa+neob)  # 予測平均在院日数を取得(転棟)。転棟は転棟日ものべ日数に含まれる。
			if z>21:
				cols.append("")
			else:
				if z2>21:
					cols.append(str(z))
				else:
					cols.append("{}({})".format(z,z2))
					

		  
		  
					
print("\n".join([",".join(map(str,i)) for i in totalt]))   
