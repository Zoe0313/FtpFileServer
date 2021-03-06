"""
前情回顾
1.threading创建线程
    Thread()创建线程对象
    start()启动线程
    join()回收线程
2.线程对象属性
3.自定义线程类
    继承 Thread
    重写__init__和run
4.线程同步互斥
    通信：全局变量
    同步互斥方法：Event Lock
    死锁：多个线程因为资源的争夺造成锁混乱，无法继续执行，是不想看到的
        延迟处理
        使用RLock
5.GIL问题：线程效率低
"""