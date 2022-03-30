import pandas as pd

tent_view = "result_tent.csv"
battle_ship_view = "result_battleship.csv"

a = pd.read_csv(tent_view)
a.columns = ['id','time','memory','game','algorithm','level']
a.drop('id', axis=1, inplace=True) 

b = pd.read_csv(battle_ship_view)
b.columns = ['id','time','memory','game','algorithm','level']
b.drop('id', axis=1, inplace=True) 

print(a)
print(b)