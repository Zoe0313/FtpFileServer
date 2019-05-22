"""
obj = Array(ctype,data)
功能:开辟共享内存空间
参数:ctype 表示共享内存数据类型
    data 整数则表示开辟空间的大小,其他数据类型
返回值:共享内存对象
"""

import multiprocessing
import os

# 创建共享内存
# 共享内存开辟5个整型列表空间
#shm = multiprocessing.Array('i', 5)

# 共享内存初始化数据[1,2,3]
shm = multiprocessing.Array('i', [1,2,3])

def fun():
    # 共享内存对象可迭代
    print(os.getpid())
    for i in shm:
        print(i, end=" ")
    print()
    #修改共享内存
    shm[1] = 200

p = multiprocessing.Process(target=fun)
p.start()
p.join()

print(os.getpid())
for i in shm:
    print(i, end=" ")