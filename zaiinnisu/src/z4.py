#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date
import calendar
import math
evaldatestring = "2021-02-03"  # 評価日の文字列。
init_inpatients = 2  # 評価日24時の在院患者数。
admissions_discharges = 13  # 評価日までの入退院数。
total_days = 216  # 評価日までののべ在院日数。
stay_length = 21 # 達成すべき平均在院日数。
total_beds = 64  # 病床数。
# 表の作成。
evaldate = date.fromisoformat(evaldatestring)  # 評価日のdateオブジェクト。
days = calendar.monthrange(evaldate.year, evaldate.month)[1] - evaldate.day  # 残日数。
ds = days + 1  # range stopに使用。
stay_length_limit = stay_length*1.1  # 変動範囲上限。3ヶ月10％
tables = []  # 表のリスト。
headerrow = f',{",".join(f"{i}日間隔" for i in range(1, ds))}'  # 表のヘッダー行。
for c in range(total_beds*2):  # cはdummy。
	admissions_per_unit = 1  # 単位あたりの入院患者数。
	discharges_per_unit = 1  # 単位あたりの退院患者数。
	rows = []  # 行のリスト。	
	for admission_interval in range(1, ds): # 入院間隔。行方向に展開。毎日、2日ごと、3日ごと、、、		
		cols = [f"{admission_interval}日間隔"]  # １行あたりの列のリスト。
		for discharge_interval in range(1, ds):  # 退院間隔。列方向に展開。毎日、2日ごと、3日ごと、、、
			inpatients = []  # １日あたりの入院患者数のリスト。
			for d in range(1, ds):  # 経過日数
				p = init_inpatients + admissions_per_unit*int(d/admission_interval) - discharges_per_unit*int(d/discharge_interval)  # １日患者数を取得。初期値+累積入院数-累積退院数。		
				if p<0:  # 入院患者数が負になる日がある場合は結果なし。
					cols.append("")
					break
				else:
					inpatients.append(p)	
			else:  # 実現可能なとき。
				new_discharges = discharges_per_unit*int(days/discharge_interval)  # 予測退院患者数。
				new_admissions_discharges = admissions_discharges + admissions_per_unit*int(days/admission_interval) + new_discharges  # 予測新入退院数。
				new_total_days = total_days+sum(inpatients)  # 予測のべ在院日数。
				estimated_stay = "-" if (ave:= math.ceil(new_total_days*2/new_admissions_discharges))>stay_length_limit or ave==0 else f"{ave}日"  # 予測平均在院日数を取得。変動範囲上限を超えているときや0のときは結果を出力しない。
				estimated_stay2 = "-" if (ave:= math.ceil((new_total_days+new_discharges)*2/new_admissions_discharges))>stay_length_limit or ave==0 else f"{ave}日"   # 予測平均在院日数を取得(転棟)。転棟は転棟日ものべ日数に含まれる。
				if any((estimated_stay!="-", estimated_stay2!="-")):
					cols.append(f"{estimated_stay}({estimated_stay2}){inpatients[-1]}人")  # 予測平均在院日数(全例転棟時または1日入院)最終入院患者数。
				else:
					cols.append("")
		if any(cols[1:]):
			rows.append(",".join(cols))  # 列の文字列をすべて結合して行に追加。
		else:  # 列の要素がすべて空文字なら表の作成終了。
			break
	if rows:  # 表ができているとき。
		tablerows = [f"入院{admissions_per_unit}人ずつ退院{discharges_per_unit}人ずつの場合 行:入院 列:退院  平均在院日数と月末入院数 ()内は全例転棟または1日入院の場合", headerrow] # 行のリスト。	
		tablerows += rows
		tablerows.append("")  # 空行を最後に追加。
		tables.append("\n".join(tablerows))
		if len(tables)>1 or len(rows)>3:  # 表が2個あるか、毎日、2日ごと、3日ごと、4日ごと、の入院間隔まで出力されているとき。
			break
	if admissions_per_unit<discharges_per_unit:  # 単位あたりの人数を退院の方から増やす。
		admissions_per_unit += 1
	else:
		discharges_per_unit += 1 
# 表の出力。
with open("output.csv", "a") as f:  # 追記でファイルを開く。
	tabletxt = "\n".join(tables)
	print(tabletxt)
	f.write(f'''\
評価日: {evaldatestring}	
評価日24時の在院患者数: {init_inpatients}人
評価日までの入退院数: {admissions_discharges}	
評価日までののべ在院日数: {total_days}日	
達成すべき平均在院日数: {stay_length}日
病床数: {total_beds}ベッド
{tabletxt}\
''')
