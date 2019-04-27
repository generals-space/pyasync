import pathlib
import time

def writefile(i):
    filepath = 'data/{:d}'.format(i)
    filecontent = 'hello world for the {:d} times'.format(i)
    file = open(filepath, 'w')
    file.write(filecontent)
    file.close()

## 创建存储目录
p = pathlib.Path('data')
if not p.exists(): p.mkdir()

start = time.time()
for i in range(10000): writefile(i)
end = time.time()

print('cost %f' % (end - start))
