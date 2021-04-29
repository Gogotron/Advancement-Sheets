import gspread
import gspread_formatting as fmt
from parser import ids

KEY = "1mLAinsgATj7ef6C3XOc8OMHYynUjBqOWkjCGdf5NIiU"
CREDENTIALS_PATH = "./"

gc = gspread.service_account(filename=CREDENTIALS_PATH+"credentials.json")
sh = gc.open_by_key(KEY)
page = sh.sheet1

green = fmt.Color(0.72,0.88,0.80)
red = fmt.Color(0.96,0.78,0.76)

adv_names = list(ids.keys())

def col_to_a1(col):
	return gspread.utils.rowcol_to_a1(1,col)[:-1]

def clear():
	page.delete_rows(1,page.row_count-1)
	page.clear()
	fmt.get_conditional_format_rules(page).clear()

def titles():
	page.insert_row(["","Nombre total"]+adv_names)

def values(advancements):
	rows = []
	for player in sorted(advancements):
		bools = [int(advancements[player][i]) for i in adv_names]
		rows.append([player,sum(bools)]+bools)
	page.insert_rows(rows,row=2)

def apply_format():
	page.format("B1:1",{"textRotation":{"angle":45}})
	page.format(f"B2:B{page.row_count}",{"horizontalAlignment":"CENTER"})
	rules = fmt.get_conditional_format_rules(page)

	rule = fmt.ConditionalFormatRule(
		ranges=[fmt.GridRange.from_a1_range(f"C2:{col_to_a1(len(ids)+2)}",page)],
		booleanRule=fmt.BooleanRule(
			condition=fmt.BooleanCondition("NUMBER_EQ",['1']),
			format=fmt.CellFormat(textFormat=fmt.textFormat(foregroundColor=green),backgroundColor=green)
			)
	)
	rules.append(rule)

	rule = fmt.ConditionalFormatRule(
		ranges=[fmt.GridRange.from_a1_range("C2:{col_to_a1(len(ids)+2)}",page)],
		booleanRule=fmt.BooleanRule(
			condition=fmt.BooleanCondition("NUMBER_EQ",['0']),
			format=fmt.CellFormat(textFormat=fmt.textFormat(foregroundColor=red),backgroundColor=red)
			)
	)
	rules.append(rule)

	rule = fmt.ConditionalFormatRule(
		ranges=[fmt.GridRange.from_a1_range(f"B2:B{page.row_count}",page)],
		gradientRule=fmt.GradientRule(
			minpoint=fmt.InterpolationPoint(
				color=fmt.Color(1,1,1),
				type="MIN"
				),
			maxpoint=fmt.InterpolationPoint(
				color=fmt.Color(0,1,0),
				type="MAX"
				),
			)
	)
	rules.append(rule)

	rules.save()

	fmt.set_column_width(page,"A",150)
	fmt.set_column_width(page,"B",50)
	fmt.set_column_width(page,f"C:{col_to_a1(len(ids)+2)}",30)
	if page.col_count<len(ids)+3:
		page.insert_cols([[]],col=page.col_count)
	fmt.set_column_width(page,f"{col_to_a1(len(ids)+3)}",70)


def write_sheet(advancements):
	clear()
	titles()
	values(advancements)
	apply_format()
