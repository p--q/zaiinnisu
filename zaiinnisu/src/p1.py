#!/opt/libreoffice7.1/program/python
# -*- coding: utf-8 -*-
from datetime import date
import calendar
import math
evaldatestring = "2021-02-03"  # 評価日の文字列。
init_inpatients = 0  # 評価日24時の在院患者数。
admissions_discharges = 0  # 評価日までの入退院数。
total_days = 0  # 評価日までののべ在院日数。
stay_length = 21 # 達成すべき平均在院日数。
total_beds = 64  # 病床数。
average_inpatients = 50  # 目標平均入院患者数。達成できなければ自動的に下げていく。
maxresult = 10
# シミュレート
maxresult -= 1
outputs = []
evaldate = date.fromisoformat(evaldatestring)  # 評価日のdateオブジェクト。
days = calendar.monthrange(evaldate.year, evaldate.month)[1] - evaldate.day  # 残日数。
ds = days + 1  # range stopに使用。
stay_length_limit = stay_length*1.1  # 変動範囲上限。3ヶ月10％
admissions_per_unit = 1  # 単位あたりの入院患者数。
discharges_per_unit = 1  # 単位あたりの退院患者数。

for t in range(average_inpatients+1)[::-1]:
	for c in range(total_beds*2):  # cはdummy。
		for admission_interval in range(1, ds)[::-1]: # 入院間隔。毎日、2日ごと、3日ごと、、、を逆順にループ。		
			for discharge_interval in range(1, ds)[::-1]:  # 退院間隔。毎日、2日ごと、3日ごと、、、を逆順にループ。		
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
					estimated_stay = "-" if (ave:= math.ceil(new_total_days*2/new_admissions_discharges))>stay_length_limit or ave==0 else f"{ave}日"  # 予測平均在院日数を取得。変動範囲上限を超えているときや0のときは結果を出力しない。
					estimated_stay2 = "-" if (ave:= math.ceil((new_total_days+new_discharges)*2/new_admissions_discharges))>stay_length_limit or ave==0 else f"{ave}日"   # 予測平均在院日数を取得(転棟)。転棟は転棟日ものべ日数に含まれる。
					if any((estimated_stay!="-", estimated_stay2!="-")):
						if (avep:=round(sum(inpatients)/days,1))>=t and avep<t+1:
							outputs.append(f"{admissions_per_unit},{admission_interval},{discharges_per_unit},{discharge_interval},{estimated_stay},{estimated_stay2},{avep}")
							if len(outputs)>maxresult:
								break
			else:
				continue
			break
		else:
			if admissions_per_unit<discharges_per_unit:  # 単位あたりの人数を退院の方から増やす。
				admissions_per_unit += 1
			else:
				discharges_per_unit += 1 		
			continue
		break		
	else:
		continue
	break
# 結果の出力。		
with open("output.csv", "w") as f:  # ファイルを開く。
	tabletxt = "\n".join(outputs)
	print(tabletxt)
	f.write(f'''\
評価日: {evaldatestring}	
評価日24時の在院患者数: {init_inpatients}人
評価日までの入退院数: {admissions_discharges}	
評価日までののべ在院日数: {total_days}日	
達成すべき平均在院日数: {stay_length}日
病床数: {total_beds}ベッド
目標平均入院患者数: {average_inpatients}
この人数を,この日数間隔で入院させ,この人数を,この日数間隔で退院させたとき,平均在院日数,全例転棟か1日入院の場合,平均入院患者数
{tabletxt}\
''')