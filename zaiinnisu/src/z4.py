#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date
import calendar
import math
evaldatestring = "2021-2-8"  # 評価日の文字列。
init_inpatients = 0  # 評価日24時の在院患者数。
admissions_discharges = 0  # 評価日までの入退院数。
total_days = 0  # 評価日までののべ在院日数。
stay_length = 21 # 達成すべき平均在院日数。
total_beds = 64  # 病床数。

evaldate = date.fromisoformat(evaldatestring)
days = calendar.monthrange(evaldate.year, evaldate.month)[1] - evaldate.day + 1  # 残日数。


	admissions_per_unit = 1  # 単位あたりの入院患者数。
	discharges_per_unit = 1  # 単位あたりの退院患者数。
	cols = []  # １行あたりの列のリスト。
	rows = []  # 行のリスト。
	for admission_interval in range(1, days+1): # 入院間隔。行方向に展開。
		for discharge_interval in range(1, days+1):  # 退院間隔。列方向に展開。
			inpatients = []  # １日あたりの入院患者数のリスト。
			for d in range(1, days+1):  # 経過日数
				inpatients.append(admissions_per_unit*math.floor(d/admission_interval) - discharges_per_unit*math.floor(d/discharge_interval))  # １日患者数を取得。			
			if init_inpatients+min(inpatients)<0:  # 入院患者数合計が負になるときは結果なし。
				cols.append("")
			else:  # 実現可能なとき。
				new_admissions = admissions_per_unit*math.floor(days/admission_interval)  # 新規入院患者数。
				new_dsicharges = discharges_per_unit*math.floor(days/discharge_interval)  # 新規退院患者数。
				estimated_stay = (total_days+sum(inpatients))*2/(admissions_discharges+new_admissions+new_dsicharges)  # 予測平均在院日数を取得。
				estimated_stay2 = (total_days+sum(inpatients)+new_dsicharges)*2/(admissions_discharges+new_admissions+new_dsicharges)   # 予測平均在院日数を取得(転棟)。転棟は転棟日ものべ日数に含まれる。
				if estimated_stay>stay_length:  # 目標平均在院日数未達のとき。
					cols.append("")
				else:  # 全員退院で目標達成のとき。
					if estimated_stay2>stay_length:  # 全員転棟では未達のとき。
						cols.append(f"{estimated_stay}(){inpatients[-1]}")  # 予測平均在院日数(転棟時)最終入院患者数。
					else:
						cols.append(f"{estimated_stay}({estimated_stay2}){inpatients[-1]}")  # 予測平均在院日数(転棟時)最終入院患者数。	
			if any(cols):
				rows.append(cols)
			else:  # 列の要素がすべて空文字なら計算終了。
				break
		else:
			continue
		break



		
print("\n".join([",".join(map(str,i)) for i in totalt]))   
