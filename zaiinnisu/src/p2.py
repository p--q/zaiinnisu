#!/opt/libreoffice7.1/program/python
# -*- coding: utf-8 -*-
from datetime import date
from operator import itemgetter
import calendar
import math
evaldatestring = "2021-02-03"  # 評価日の文字列。
init_inpatients = 21  # 評価日24時の在院患者数。
admissions_discharges = 219  # 評価日までの入退院数。
total_days = 2247  # 評価日までののべ在院日数。
stay_length_limit = 21 # 達成すべき平均在院日数。
total_beds = 64  # 病床数。
admissions_per_unit_max = 5  # 単位あたりの最大入院数。
discharges_per_unit_max = 5  # 単位あたりの最大退院数。
# シミュレート
outputs = []
evaldate = date.fromisoformat(evaldatestring)  # 評価日のdateオブジェクト。
days = calendar.monthrange(evaldate.year, evaldate.month)[1] - evaldate.day  # 残日数。
ds = days + 1  # range stopに使用。
admissions_per_unit = 1  # 単位あたりの入院患者数。
discharges_per_unit = 1  # 単位あたりの退院患者数。
while True:
	for admission_interval in range(1, ds): # 入院間隔。行方向に展開。毎日、2日ごと、3日ごと、、、		
		flg = True  # この入院間隔で結果がでたら倒すフラグ。
		for discharge_interval in range(1, ds):  # 退院間隔。列方向に展開。毎日、2日ごと、3日ごと、、、
			inpatients = []  # １日あたりの入院患者数のリスト。
			for d in range(1, ds):  # 経過日数
				p = init_inpatients + admissions_per_unit*int(d/admission_interval) - discharges_per_unit*int(d/discharge_interval)  # １日患者数を取得。初期値+累積入院数-累積退院数。		
				if p<0 or p>total_beds:  # 入院患者数が負かベッド数以上になる日がある場合は結果なし。
					break
				else:
					inpatients.append(p)	
			else:  # 実現可能なとき。
				new_discharges = discharges_per_unit*int(days/discharge_interval)  # 予測退院患者数。
				new_admissions_discharges = admissions_discharges + admissions_per_unit*int(days/admission_interval) + new_discharges  # 予測新入退院数。
				new_total_days = total_days+sum(inpatients)  # 予測のべ在院日数。
				estimated_stay = "" if (ave:= math.ceil(new_total_days*2/new_admissions_discharges))>stay_length_limit or ave==0 else ave  # 予測平均在院日数を取得。変動範囲上限を超えているときや0のときは結果を出力しない。
				estimated_stay2 = "" if (ave:= math.ceil((new_total_days+new_discharges)*2/new_admissions_discharges))>stay_length_limit or ave==0 else ave  # 予測平均在院日数を取得(転棟)。転棟は転棟日ものべ日数に含まれる。
				if any((estimated_stay, estimated_stay2)):
					outputs.append((admissions_per_unit, admission_interval, discharges_per_unit, discharge_interval, estimated_stay, estimated_stay2, new_total_days, new_admissions_discharges, " ".join(map(str, inpatients))))
					flg = False
		if flg:  # 退院間隔を変えても結果がでないときはもうこの入院間隔では計算しない。
			break
	if admissions_per_unit<discharges_per_unit:  # 単位あたりの人数を退院の方から増やす。ベッド数以上の入退院数のときは終了。
		if (admissions_per_unit:= admissions_per_unit+1)>admissions_per_unit_max or admissions_per_unit>total_beds:
			break
	else:
		if (discharges_per_unit:= discharges_per_unit+1)>discharges_per_unit_max or discharges_per_unit>total_beds:
			break	
outputs.sort(key=itemgetter(6), reverse=True)  # のべ在院日数の降順でソート。		
# 結果の出力。		
with open("output.csv", "w") as f:  # ファイルを開く。
	tabletxt = "\n".join(",".join(map(str, i)) for i in outputs)
	print(tabletxt)
	f.write(f'''\
評価日: {evaldatestring}	
評価日24時の在院患者数: {init_inpatients}人
評価日までの入退院数: {admissions_discharges}	
評価日までののべ在院日数: {total_days}日	
達成すべき平均在院日数: {stay_length_limit}日
病床数: {total_beds}ベッド
この人数を,この日数間隔で入院させ,この人数を,この日数間隔で退院させたとき,平均在院日数,全例転棟か1日入院の場合,のべ在院日数,入退院数, 日々の入院患者数
{tabletxt}\
''')		

