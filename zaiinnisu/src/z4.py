#!/usr/bin/python
# -*- coding: utf-8 -*-
from itertools import chain
from datetime import date
import calendar
import math
evaldatestring = "2021-02-08"  # 評価日の文字列。
init_inpatients = 0  # 評価日24時の在院患者数。
admissions_discharges = 0  # 評価日までの入退院数。
total_days = 0  # 評価日までののべ在院日数。
stay_length = 21 # 達成すべき平均在院日数。
total_beds = 64  # 病床数。
# 表の作成。
evaldate = date.fromisoformat(evaldatestring)  # 評価日のdateオブジェクト。
days = calendar.monthrange(evaldate.year, evaldate.month)[1] - evaldate.day + 1  # 残日数。
ds = days+1  # range stopに使用。
stay_length_limit = stay_length*1.1  # 変動範囲上限。3ヶ月10％
tables = []  # 表のリスト。
for c in range(total_beds*2):  # cはdummy。
	admissions_per_unit = 1  # 単位あたりの入院患者数。
	discharges_per_unit = 1  # 単位あたりの退院患者数。
	rows = [(f"入院{admissions_per_unit}人ずつ退院{discharges_per_unit}人ずつの場合 行: 入院 列: 退院  平均在院日数(全例転棟または1日入院の場合の平均在院日数)月末入院数",),
			("", *[f"{i}日間隔" for i in range(1, ds)])]  # 行のリスト。	
	for admission_interval in range(1, ds): # 入院間隔。行方向に展開。毎日、2日ごと、3日ごと、、、
		for discharge_interval in range(1, ds):  # 退院間隔。列方向に展開。毎日、2日ごと、3日ごと、、、
			cols = [f"{discharge_interval}日間隔"]  # １行あたりの列のリスト。
			inpatients = []  # １日あたりの入院患者数のリスト。
			for d in range(1, ds):  # 経過日数
				inpatients.append(admissions_per_unit*math.floor(d/admission_interval) - discharges_per_unit*math.floor(d/discharge_interval))  # １日患者数を取得。			
			if init_inpatients+min(inpatients)<0:  # 入院患者数合計が負になるときは結果なし。
				cols.append("")
			else:  # 実現可能なとき。
				new_admissions = admissions_per_unit*math.floor(days/admission_interval)  # 新規入院患者数。
				new_dsicharges = discharges_per_unit*math.floor(days/discharge_interval)  # 新規退院患者数。
				estimated_stay = "" if (ave:=(total_days+sum(inpatients))*2/(admissions_discharges+new_admissions+new_dsicharges))>stay_length_limit or ave==0 else ave  # 予測平均在院日数を取得。変動範囲上限を超えているときや0のときは空文字。
				estimated_stay2 = "" if (ave:= (total_days+sum(inpatients)+new_dsicharges)*2/(admissions_discharges+new_admissions+new_dsicharges))>stay_length_limit or ave==0 else ave   # 予測平均在院日数を取得(転棟)。転棟は転棟日ものべ日数に含まれる。
				if any((estimated_stay, estimated_stay2)):
					cols.append(f"{estimated_stay}({estimated_stay2}){inpatients[-1]}")  # 予測平均在院日数(転棟時または全例1日入院)最終入院患者数。
				else:
					cols.append("")
			if any(cols[1:]):
				rows.append(cols)
			else:  # 列の要素がすべて空文字なら表の作成終了。
				break
		else:
			continue
		break
	if rows[2:]:  # 表ができているとき。
		rows.append(("",))  # 空行を最後に追加。
		tables.append(rows)
		if len(tables)>1 or len(rows[2:])>3:  # 表が2個あるか、毎日、2日ごと、3日ごと、4日ごと、の入院間隔まで出力されているとき。
			break
	if admissions_per_unit<discharges_per_unit:  # 単位あたりの人数を退院の方から増やす。
		admissions_per_unit += 1
	else:
		discharges_per_unit += 1 
# 表の出力。
with open("output.csv", "a") as f:
	txt = "\n".join(f"{i}" for i in chain.from_iterable(tables))
	f.write(f"""\
評価日: {evaldatestring}	
評価日24時の在院患者数: {init_inpatients}
評価日までの入退院数: {admissions_discharges}	
評価日までののべ在院日数: {total_days}	
達成すべき平均在院日数: {stay_length}
病床数: {total_beds}
{txt}\
""")
