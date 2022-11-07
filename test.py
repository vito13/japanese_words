from collections import namedtuple
City = namedtuple('City', 'name country population coordinates')	# 参数是类名，另一个是类的各个字段的名字
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))	# 创建对象
print(tokyo)	# 访问
tokyo.population = 100
print(tokyo.population)
print(tokyo.coordinates)
print(tokyo[1])
print(City._fields)	# _fields 属性是一个包含这个类所有字段名称的元组。


LatLong = namedtuple('LatLong', 'lat long')
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
delhi = City._make(delhi_data)	# 用_make()通过接受一个可迭代对象来生成这个类的一个实例，它的作用跟City(*delhi_data)是一样的

print(delhi._asdict())	#_asdict()把具名元组以collections.OrderedDict的形式返回，下面是迭代每一项
for key, value in delhi._asdict().items():
	print(key + ':', value)