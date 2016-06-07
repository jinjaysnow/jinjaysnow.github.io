# -*- coding:utf-8 -*-
u"""Lamport全局快照"""
from multiprocessing import Process, Manager, Pipe

token = "I am a token"

# 全局状态，in-x表示消息在x中
manager = Manager()
global_state = manager.dict()
global_state["p"] = None        # 进程1的状态，初始为空，可选状态<空，in-p>
global_state["q"] = None        # 进程2的状态，初始为空，可选状态<空，in-q>
global_state["c1"] = None       # 通道c1的状态，初始为空，可选状态<空，in-c1>
global_state["c2"] = None       # 通道c2的状态，初始为空，可选状态<空，in-c2>
global_state["start"] = False   # 是否开启消息循环
global_state["stop"] = False    # 停止循环
global_state['state1'] = 0
global_state['state2'] = 0

snap_num = 101  # 快照开始的state标记


def proc1(pipe1, pipe2, global_state):
    u"""进程1"""
    while True:
        # 消息到达后，发送并更改状态
        if global_state["p"] == "in-p":
            pipe1.send(token)
            if global_state['state1'] == snap_num:   # 进程1状态为101，发送消息完毕后开始快照，停止所有进程
                global_state['start'] = False
                global_state['stop'] = True
            # 发送消息后，进程p状态改变，通道c1的状态改变
            global_state["p"] = None
            global_state["c1"] = "in-c1"
        # 状态为None，且消息循环已经开始，等待通道c2的消息
        elif global_state["p"] is None and global_state["c2"] == "in-c2" and global_state['start'] and not global_state['stop']:
            # 为空状态时，等待从c2接收消息，除非停止
            if pipe2.recv():
                # 接收成功
                global_state['state1'] += 1
                global_state['p'] = "in-p"
                global_state['c2'] = None
        if global_state['stop']:
            break


def proc2(pipe1, pipe2, global_state):
    u"""进程2"""
    # 进程1最先拥有消息
    while True:
        # 消息到达后，发送并更改状态
        if global_state["q"] == "in-q":
            pipe2.send(token)
            # 发送消息后，进程p状态改变，通道c1的状态改变
            global_state["q"] = None
            global_state["c2"] = "in-c2"
        # 状态为None，且消息循环已经开始，等待通道c2的消息
        elif global_state["q"] is None and global_state['c1'] == "in-c1" and global_state['start'] and not global_state['stop']:
            # 为空状态时，从c1接收消息，除非停止
            if pipe1.recv():
                # 接收成功
                global_state['state2'] += 1
                global_state['q'] = "in-q"
                global_state['c1'] = None
        if global_state['stop']:
            break


# 构建管道
pipe1 = Pipe()
pipe2 = Pipe()

# 创建进程
p1 = Process(target=proc1, args=(pipe1[0], pipe2[1], global_state, ))
p2 = Process(target=proc2, args=(pipe1[1], pipe2[0], global_state, ))

# 进程1先发送消息
global_state['p'] = "in-p"
global_state['start'] = True

p1.start()
p2.start()
p1.join()
p2.join()

# 输出结果
print "process1: ", global_state['p'], " state: ", global_state['state1']
print "channal1: ", global_state["c1"]
print "process2: ", global_state['q'], " state: ", global_state['state1']
print "channal2: ", global_state["c2"]
