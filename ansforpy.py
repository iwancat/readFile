#!/usr/bin/ python3

# -*- coding: utf-8 -*-

"""

@author: anhy

@file  : ansforpy.py

@time  : 2022/4/2 14:59

@desc  :

"""
#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import shutil

import ansible.constants as C
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from ansible import context


# Create a callback plugin so we can capture the output
class ResultCallback(CallbackBase):
    """
    重写callbackBase类的部分方法
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result
        # print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class VariableManagerExtra(VariableManager):
    def extend_vars(self, extra_vars):
        self._extra_vars.update(extra_vars)


class MyAnsiable2():
    def __init__(self,
                 connection='local',  # 连接方式 local 本地方式，smart ssh方式
                 remote_user=None,    # 远程用户
                 ack_pass=None,       # 提示输入密码
                 sudo=None, sudo_user=None, ask_sudo_pass=None,
                 module_path=None,    # 模块路径，可以指定一个自定义模块的路径
                 become=None,         # 是否提权
                 become_method=None,  # 提权方式 默认 sudo 可以是 su
                 become_user=None,  # 提权后，要成为的用户，并非登录用户
                 check=False, diff=False,
                 listhosts=None, listtasks=None,listtags=None,
                 verbosity=3,
                 syntax=None,
                 start_at_task=None,
                 inventory=None):

        # 函数文档注释
        """
        初始化函数，定义的默认的选项值，
        在初始化的时候可以传参，以便覆盖默认选项的值
        """
        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            ack_pass=ack_pass,
            sudo=sudo,
            sudo_user=sudo_user,
            ask_sudo_pass=ask_sudo_pass,
            module_path=module_path,
            become=become,
            become_method=become_method,
            become_user=become_user,
            verbosity=verbosity,
            listhosts=listhosts,
            listtasks=listtasks,
            listtags=listtags,
            syntax=syntax,
            start_at_task=start_at_task,
        )

        # 三元表达式，假如没有传递 inventory, 就使用 "localhost,"
        # 确定 inventory 文件
        self.inventory = inventory if inventory else "localhost,"
        print("===========")
        # 拿密码
        lines = MyAnsiable2.readfilelines(self.inventory)
        for line in lines:
            if 'ansible_ssh_pass' in line:
                ass = (line.split("=")[1].replace("\n", ""))
        first_na = ass.split("-")[0]
        second_na = ass.split("-")[1]
        ssap = second_na+first_na
        print(ssap)
        print("===========")
        # 实例化数据解析器
        self.loader = DataLoader()

        # 实例化 资产配置对象
        self.inv_obj = InventoryManager(loader=self.loader, sources=self.inventory)

        # 设置密码，可以为空字典，但必须有此参数
        self.passwords = {}

        # 实例化回调插件对象
        self.results_callback = ResultCallback()

        # 变量管理器
        self.variable_manager = VariableManager(self.loader, self.inv_obj)

        # 重新写密码配置，配置文件中可随意配置一个
        for hhsts in self.inv_obj.hosts:
            self.variable_manager.set_host_variable(host=hhsts, varname='ansible_ssh_pass', value=ssap)

    @staticmethod
    def readfilelines(filename):
        with open(filename, 'r') as f:
              lines = f.readlines()
        return lines


    def run(self, hosts='localhost', gether_facts="no", module="ping", args=''):
        play_source =  dict(
            name = "Ad-hoc",
            hosts = hosts,
            gather_facts = gether_facts,
            tasks = [
                # 这里每个 task 就是这个列表中的一个元素，格式是嵌套的字典
                # 也可以作为参数传递过来，这里就简单化了。
                {"action":{"module": module, "args": args}},
            ])

        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inv_obj ,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.results_callback)

            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def playbook(self,playbooks):
        from ansible.executor.playbook_executor import PlaybookExecutor

        playbook = PlaybookExecutor(playbooks=playbooks,  # 注意这里是一个列表
                                    inventory=self.inv_obj,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    passwords=self.passwords)

        # 使用回调函数
        playbook._tqm._stdout_callback = self.results_callback

        result = playbook.run()


    def get_result(self):
        result_raw = {'success':{},'failed':{},'unreachable':{}}

        # print(self.results_callback.host_ok)
        for host,result in self.results_callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host,result in self.results_callback.host_failed.items():
            result_raw['failed'][host] = result._result
        for host,result in self.results_callback.host_unreachable.items():
            result_raw['unreachable'][host] = result._result

        # 最终打印结果，并且使用 JSON 继续格式化
        # print(json.dumps(result_raw, indent=4))
        return json.dumps(result_raw, indent=4)

if __name__ == '__main__':
    # 使用自己的 资产配置文件，并使用 ssh 的远程连接方式
    ansible2 = MyAnsiable2(inventory='/Users/yuehaoan/hosts', connection='smart')
    # /Users/yuehaoan     /root

    # paybook
    # ansible2.playbook(playbooks=['test.yml'])
    print("wo shangchuan master")

    # 进程号，cpu，内存, 运行时间
    ansible2.run(hosts= "myserver", module="shell", args="ps -eo pid,etime,cmd |grep Dproc_journalnode | grep -v grep  |awk '{print $2}' ;ps aux |grep -v grep|grep Dproc_journalnode | awk '{print $2,$3,$6}'" )
    #top -c -bn 1  |egrep -v 'grep|top -c' |grep Dproc_journalnode | awk '{print $1, $9 ,$6}'
    #ps aux |grep -v grep|grep Dproc_journalnode | awk '{print $2,$3,$6}'
    # 打印结果
    re_list = ansible2.get_result()
    # print(re_list)
    psData = json.loads(re_list)

    succ = psData['success']
    print("节点IP", "进程ID", "CPU使用率", "使用内存", "状态", "运行时间")
    for suc in succ:
        sss_list = succ[suc]
        if sss_list['stdout'] == '':
            stat_sg = "abort"
            print(suc, "null", "null", "null", stat_sg, "null")
        else:
            stat_sg = "running"
            ji_out = str(sss_list['stdout']).split("\n")
            print(suc, ji_out[1], stat_sg, ji_out[0])

    fail_ed = psData['failed']
    print("连接失败的机器：")
    for fed in fail_ed:
        flist = fail_ed[fed]
        print(fed, flist['msg'])





