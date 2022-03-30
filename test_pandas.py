import pandas as pd

tent_view = "result_tent.csv"
battle_ship_view = "battle_ship_view.csv"

a = pd.read_csv(tent_view)
a.columns = ['id','time','memory','game','algorithm','level']
a.drop('id', axis=1, inplace=True) 

print(a)