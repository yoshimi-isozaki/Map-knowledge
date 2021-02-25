
sample_text = '緯度: 33.560544 経度: 130.387521'

lat_long = {} # latが緯度、longが経度
list = []

"""
for tmp in sample_text.split():
    if type(tmp) == "<class 'float'>":
        list.append(tmp)
print(list)
"""

for val in sample_text.split():
    try:
        val = float(val)
    except ValueError:
        val = None
    else:
        list.append(val)

print(list) #[33.560544, 130.387521]となる
lat_long['緯度'] = list[0]
lat_long['経度'] = list[1]
print(lat_long)


