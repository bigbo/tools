#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
# subwork

__author__   ="tommy (bychyahoo@gamil.com)"
__date__     ="2009-01-06 16:33"
__copyright__="Copyright 2009 tudou, Inc"
__license__  ="Td, Inc"
__version__  ="0.1"

import os
import time
import signal
import tempfile
import traceback
import subprocess

#此包对于进行shell命令的延时处理使用的是非多线程机制(相对EasyProcess这个python包),使用所有包和函数均为python基本包,显示的封装成两个函数,解决的问题是新增命令超时的设置方法,解决了其他方法的僵尸进程的问题.
#
#1.shell_2_tty(_cmd=cmds, _cwd=None, _timeout=10*60)
#_cmd 是要执行的外面命令行，要是一个 list， 如果是str，shell=True，会启动一个新的shell去干活的，这样，不利于进程的控制
#_cwd 是执行这个命令行前，cd到这个路径下面，这个，对我的用应很重要，如果不需要可以用默认值
#_timeout 这个是主角，设置超时时间（秒单位），从真重执行命令行开始计时，墙上时间超过 _timeout后，父进程会kill掉子进程，回收资源，并避免产生 zombie(僵尸进程)并将调用的命令行输出，直接输出到stdout,即是屏幕的终端上,(如果对输出比较讨厌，可以将 stdout = open("/dev/null", "w"), stderr=open("/dev/null"),等等)
#
#2.shell_2_tempfile(_cmd=cmds, _cwd=None, _timeout=10)
#类同1，主要是增加，对命令行的输出，捕获，并返回给父进程，留作分析


__all__ = ["subwork", "trace_back", "os", "time", "traceback", "subprocess", "signal"]

def trace_back():
    try:
        type, value, tb = sys.exc_info()
        return str(''.join(traceback.format_exception(type, value, tb)))
    except:
        return ''

def getCurpath():
    try:
        return os.path.normpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    except:
        return

class subwork:
    """add timeout support!
    if timeout, we SIGTERM to child process, and not to cause zombie process safe!
    """
    def __init__(self, stdin=None, stdout=None, stderr=None, cmd=None, cwd=None, timeout=5*60*60):
        """default None
        """
        self.cmd       = cmd
        self.Popen     = None
        self.pid       = None
        self.returncode= None
        self.stdin     = None
        self.stdout    = stdout
        self.stderr    = stderr
        self.cwd       = cwd
        self.timeout   = int(timeout)
        self.start_time= None
        self.msg       = ''

    def send_signal(self, sig):
        """Send a signal to the process
        """
        os.kill(self.pid, sig)

    def terminate(self):
        """Terminate the process with SIGTERM
        """
        self.send_signal(signal.SIGTERM)

    def kill(self):
        """Kill the process with SIGKILL
        """
        self.send_signal(signal.SIGKILL)

    def wait(self):
        """ wait child exit signal,
        """
        self.Popen.wait()

    def free_child(self):
        """
        kill process by pid
        """
        try:
            self.terminate()
            self.kill()
            self.wait()
        except:
            pass

    def run(self):
        """
        run cmd
        """
        print "[subwork]%s" % split_cmd(self.cmd)
        code = True
        try:
            self.Popen = subprocess.Popen(args=split_cmd(self.cmd), stdout=self.stdout, stderr=self.stderr, cwd=self.cwd)
            self.pid   = self.Popen.pid
            self.start_time = time.time()
            while self.Popen.poll() == None and (time.time() - self.start_time) < self.timeout :
                time.sleep(1)
                #print "running... %s, %s, %s" % (self.Popen.poll(), time.time() - self.start_time, self.timeout)
        except:
            self.msg += trace_back()
            self.returncode = -9998
            code = False
            print "[subwork]!!error in Popen"
        # check returncode
        if self.Popen.poll() == None: # child is not exit yet!
            self.free_child()
            self.returncode = -9999
        else:
            self.returncode = self.Popen.poll()
        # return
        return {"code":code,\
                "msg":self.msg,\
                "req":{"returncode":self.returncode},\
                }

def split_cmd(s):
    """
    str --> [], for subprocess.Popen()
    """
    SC = '"'
    a  = s.split(' ')
    cl = []
    i = 0
    while i < len(a) :
        if a[i] == '' :
            i += 1
            continue
        if a[i][0] == SC :
            n = i
            loop = True
            while loop:
                if a[i] == '' :
                    i += 1
                    continue
                if a[i][-1] == SC :
                    loop = False
                    m = i
                i += 1
            #print a[n:m+1]
            #print ' '.join(a[n:m+1])[1:-1]
            cl.append((' '.join(a[n:m+1]))[1:-1])
        else:
            cl.append(a[i])
            i += 1
    return cl

def check_zero(dic=None):
    """
    check returncode is zero
    """
    if not isinstance(dic, dict):
        raise TypeError, "dist must be a Distribution instance"
    print "returncode :", int(dic["req"]["returncode"])
    if int(dic["req"]["returncode"]) == 0:
        return True, dic["msg"]
    else:
        return False, dic["msg"]


def shell_2_tty(_cmd=None, _cwd=None, _timeout=5*60*60):
    """
    """
    try:
        shell=subwork(cmd=_cmd, stdout=None, stderr=None, cwd=_cwd, timeout=_timeout)
        return check_zero(shell.run())
    except:
        return False, trace_back()

def shell_2_tempfile(_cmd=None, _cwd=None, _timeout=5*60*60):
    """
    to collect out-string by tempfile
    """
    try:
        try:
            fout=tempfile.TemporaryFile()
            ferr=tempfile.TemporaryFile()
            shell=subwork(cmd=_cmd, stdout=fout, stderr=ferr, cwd=_cwd, timeout=_timeout)
            req=check_zero(shell.run())
            # get media info from tmp_out
            fout.seek(0)
            out=fout.read()
            if not out:
                ferr.seek(0)
                out=ferr.read()
            #
            return req[0], str(out)
        finally:
            fout.close()
            ferr.close()
    except:
        return False, trace_back()

#---------------------------------------------
# main-test
#---------------------------------------------
if __name__ == '__main__' :
    pass
    cmds = "ping www.google.cn"
    cmds = "ls -la"
    #print shell_2_tty(_cmd=cmds, _cwd=None, _timeout=10)
    print shell_2_tempfile(_cmd=cmds, _cwd=None, _timeout=10)
    print "\nexit!"
    time.sleep(60)
