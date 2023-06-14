import paramiko
import time

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.db import connections
from django.conf import settings
from django.utils.timezone import make_aware
from django.utils import timezone
from .models import Device, Log

curs = connections['kb_a'].cursor()

def home(request):
    curs = connections['kb_a'].cursor()
    if request.method == "POST" and request.POST['submit'] == "Refresh":
        id_h = request.POST['hp']
        
        curs.execute("SELECT mc_id FROM `hn_mach` WHERE hn_id = '"+id_h+"'")
        id_m = curs.fetchone()
        id_m = str(id_m[0])
        
        curs.execute("SELECT ip FROM `machine` WHERE id = '"+id_m+"'")
        ips = curs.fetchone()
        ip = ips[0]
        
        curs.execute("SELECT user FROM `machine` WHERE id = '"+id_m+"'")
        users = curs.fetchone()
        user = users[0]
        
        curs.execute("SELECT AES_DECRYPT(DES_DECRYPT(DECODE(passw,'pass'),'pass'),'pass') from machine where id='"+id_m+"'")
        passws = curs.fetchone()
        passw = passws[0]
        
        curs.execute("SELECT r_user FROM `machine` WHERE id = '"+id_m+"'")
        r_users = curs.fetchone()
        r_user = r_users[0]
        
        curs.execute("SELECT AES_DECRYPT(DES_DECRYPT(DECODE(r_pass,'pass'),'pass'),'pass') from machine where id='"+id_m+"'")
        r_passs = curs.fetchone()
        r_pass = r_passs[0]
        
        curs.execute("SELECT type FROM `hn_mach` WHERE hn_id = '"+id_h+"'")
        htyp = curs.fetchone()
        
        chk = "systemctl status "
        
        condat = str()
        stat = "inactive"
        st = "stopped"
        
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip,
                               username=r_user, password=r_pass)
            conn = ssh_client.invoke_shell()
            sttm = ""
            
            while True:
                if conn.recv_ready():
                    condat += conn.recv(65535).decode()
                else:
                    continue
                if condat.endswith('$ '):
                    conn.send("sudo -s" + "\n")
                    time.sleep(1)
                elif condat.find('try again') != -1:
                    stat = "active"
                    break
                elif condat.endswith(': '):
                    conn.send(passw + "\n")
                    time.sleep(1)
                elif condat.endswith('# '):
                    stat = "active"
                    break
                
            condat = ""
                
            conn.send(chk + htyp[0] + "\n")
            time.sleep(1)
            condat += conn.recv(65535).decode()
            conn.send("q" + "\n")
            time.sleep(1)
            condat += conn.recv(65535).decode()
            
            if condat.find('active (running)') != -1:
                st = "running"
            else:
                st = "stopped"
            
            ssh_client.close()
            
        except Exception as e:
            stat = "inactive"
        
        curs.execute("UPDATE machine SET status = '"+stat+"' WHERE machine.id = '"+id_m+"'")
        curs.fetchall()
        
        curs.execute("UPDATE honeypot SET service = '"+st+"' WHERE honeypot.id = '"+id_h+"'")
        curs.fetchall()
    
        all_device = Device.objects.all()
        devices = Device.objects.all()
        last_event = Log.objects.all().order_by('-id')[:10]
        
        curs.execute('select * from hn_mach')
        dat = curs.fetchall()
        
        sttm = ""
        
        if dat == [[]]:
            sttm = "There is no honeypot installed, deploy a new one...."
        else:
            sttm = ""
        context = {
            'all_device': len(all_device),
            'last_event': last_event,
            'devices': devices,
            'dat': dat,
            'sttm': sttm
        }
        
        curs.close()

        return render(request, 'home.html', context)
        
    else:
        all_device = Device.objects.all()
        devices = Device.objects.all()
        last_event = Log.objects.all().order_by('-id')[:10]
        
        curs.execute('select * from hn_mach')
        dat = curs.fetchall()
        
        sttm = ""
        
        if dat == [[]]:
            sttm = "There is no honeypot installed, deploy a new one...."
        else:
            sttm = ""
        context = {
            'all_device': len(all_device),
            'last_event': last_event,
            'devices': devices,
            'dat': dat,
            'sttm': sttm
        }
        
        curs.close()

        return render(request, 'home.html', context)

def log(request):
    curs = connections['kb_a'].cursor()
    log_text = Log.objects.all()

    context = {
        'logs': log_text
    }
    
    curs.close()

    return render(request, 'log.html', context)


def deploy(request):
    curs = connections['kb_a'].cursor()
    if request.method == "POST" and request.POST['submit'] == "Submit":
        result = []
        error  = []
        other_command = request.POST['other_command'].splitlines()
        
        id_m = request.POST['mc']
        if id_m != '':
            curs.execute("SELECT ip FROM `machine` WHERE id = '"+id_m+"'")
            ips = curs.fetchone()
            ip = ips[0]
            curs.execute("SELECT platform FROM `machine` WHERE id = '"+id_m+"'")
            platform = curs.fetchone()
            platform = str(platform[0])
            curs.execute("SELECT user FROM `machine` WHERE id = '"+id_m+"'")
            users = curs.fetchone()
            user = users[0]
            curs.execute("SELECT AES_DECRYPT(DES_DECRYPT(DECODE(passw,'pass'),'pass'),'pass') from machine where id='"+id_m+"'")
            passws = curs.fetchone()
            passw = passws[0]
            curs.execute("SELECT r_user FROM `machine` WHERE id = '"+id_m+"'")
            r_users = curs.fetchone()
            r_user = r_users[0]
            curs.execute("SELECT AES_DECRYPT(DES_DECRYPT(DECODE(r_pass,'pass'),'pass'),'pass') from machine where id='"+id_m+"'")
            r_passs = curs.fetchone()
            r_pass = r_passs[0]
        else:
            name = request.POST['name']
            loc = request.POST['loc']
            platform = request.POST['platform']
            ip = request.POST['ip']
            user = request.POST['user']
            passw = request.POST['passw']
            r_user = request.POST['r_user']
            r_pass = request.POST['r_pass']
        
        ttoken = request.POST['ttoken']
        hname = request.POST['hname']
        htyp = request.POST['htyp']
        a_start = request.POST['a_start']
        
        if htyp != "0":
            curs.execute("select script from repository where type='packages' and os='any' and label='"+htyp+"'")
            pkg = curs.fetchall()
            curs.execute("select script from repository where type='install' and os='any' and label='"+htyp+"'")
            comm = curs.fetchall()
            curs.execute("select script from repository where type='packages' and os='"+platform+"' and label='"+htyp+"'")
            addi = curs.fetchall()
            curs.execute("select script from repository where type='additional' and os='any' and label='"+htyp+"'")
            jlog = curs.fetchall()
            curs.execute("select script from repository where type='services' and os='any' and label='"+htyp+"'")
            serv = curs.fetchall()
            curs.execute("select script from repository where type='start' and os='any' and label='"+htyp+"'")
            strt = curs.fetchall()
            curs.execute("select script from repository where type='additional' and os='any' and label='telegraf'")
            tgraf = curs.fetchall()
            stt = "0"
            servi = "stopped"
            ins = "INSERT INTO `honeypot` (`id`, `name`, `type`, `m_id`, `created`, `updated`, `status`, `service`) VALUES (NULL, '"
            sep = "', '"
            chk = "systemctl status "
            
            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=ip,
                                   username=r_user, password=r_pass)
                conn = ssh_client.invoke_shell()
                
                def step1():
                    condat = str()
                    while True:
                        if conn.recv_ready():
                            condat += conn.recv(65535).decode()
                        else:
                            continue
                        if condat.endswith('$ '):
                            conn.send("sudo -s" + "\n")
                            time.sleep(1)
                        elif condat.find('try again') != -1:
                            condat += "Machine (root) username or password has been changed"
                            break
                        elif condat.endswith(': '):
                            conn.send(passw + "\n")
                            time.sleep(1)
                        elif condat.endswith('# '):
                            break
                    return condat
                
                def step2():
                    condat = str()
                    for cmd in pkg:
                        conn.send(cmd[0] + "\n")
                        time.sleep(1)
                        while True:
                            if conn.recv_ready():
                                condat += conn.recv(65535).decode()
                            else:
                                continue
                            if condat.endswith('# '):
                                break
                    if addi != [[]]:
                        for addt in addi:
                            conn.send(addt[0] + "\n")
                            time.sleep(1)
                            while True:
                                if conn.recv_ready():
                                    condat += conn.recv(65535).decode()
                                else:
                                    continue
                                if condat.endswith('# '):
                                    break
                        return condat
                    else:
                        return condat
                    
                def step3():
                    condat = str()
                    curs.execute("select script from repository where type='setup' and label='"+htyp+"'")
                    setup = curs.fetchall()
                    conn.send(setup[0][0] + "\n")
                    time.sleep(1)
                    while True:
                        if conn.recv_ready():
                            condat += conn.recv(65535).decode()
                        else:
                            continue
                        if condat.endswith('# '):
                            break
                    conn.send("echo 'next'" + "\n")
                    time.sleep(1)
                    condat += conn.recv(65535).decode()
                    return condat
                
                def step4():
                    condat = str()
                    for cmmd in comm:
                        conn.send(cmmd[0] + "\n")
                        time.sleep(1)
                        while True:
                            if conn.recv_ready():
                                condat += conn.recv(65535).decode()
                            else:
                                continue
                            if condat.endswith('# '):
                                break
                    conn.send("echo 'next'" + "\n")
                    condat += conn.recv(65535).decode()
                    return condat
                
                def step5():
                    condat = str()
                    for jlogg in jlog:
                        conn.send(jlogg[0] + '\n')
                        time.sleep(1)
                        while True:
                            if conn.recv_ready():
                                condat += conn.recv(65535).decode()
                            else:
                                continue
                            if condat.endswith('# '):
                                break
                    conn.send("echo 'next'" + "\n")
                    condat += conn.recv(65535).decode()
                    return condat
                
                def step6():
                    condat = str()
                    for srv in serv:
                        conn.send(srv[0] + "\n")
                        time.sleep(1)
                        while True:
                            if conn.recv_ready():
                                condat += conn.recv(65535).decode()
                            else:
                                continue
                            if condat.endswith('# '):
                                break
                    if a_start == "0":
                        return condat
                    elif a_start == "a_start":
                        for st in strt:
                            conn.send(st[0] + "\n")
                            time.sleep(1)
                            while True:
                                if conn.recv_ready():
                                    condat += conn.recv(65535).decode()
                                else:
                                    continue
                                if condat.endswith('# '):
                                    break
                        return condat
                
                def step7():
                    condat = str()

                    for tg in tgraf:
                        conn.send(tg[0] + '\n')
                        time.sleep(1)
                        while True:
                            if conn.recv_ready():
                                condat += conn.recv(65535).decode()
                            else:
                                continue
                            if condat.endswith('# '):
                                break
                    conn.send("echo 'next'" + "\n")
                    condat += conn.recv(65535).decode()
                    return condat
                
                result.append(htyp)
                
                s1 = step1()
                time.sleep(1)
                stt = "1"
                s2 = step2()
                time.sleep(1)
                stt = "2"
                s3 = step3()
                time.sleep(1)
                stt = "3"
                s4 = step4()
                time.sleep(1)
                stt = "4"
                s5 = step5()
                time.sleep(1)
                stt = "5"
                s6 = step6()
                time.sleep(1)
                conn.send(chk + htyp + "\n")
                time.sleep(1)
                s6 += conn.recv(65535).decode()
                conn.send("q" + "\n")
                time.sleep(1)
                s6 += conn.recv(65535).decode()
                if s6.find('active (running)') != -1:
                    servi = "running"
                else:
                    servi = "stopped"                
                
                stt = "6"
                
                result.append(s1)
                result.append(s2)
                result.append(s3)
                result.append(s4)
                result.append(s5)
                result.append(s6)
                
                if ttoken != '' and stt == "6":
                    s7 = step7()
                    time.sleep(1)
                    result.append(s7)
                elif ttoken == '':
                    result.append("Telegraf token not specified")
                else:
                    result.append("Honeypot installation contain error")
                
                if id_m != '' and stt == "6":
                    curs.execute(ins+hname+sep+htyp+sep+id_m+"', current_timestamp(), current_timestamp(), '"+stt+sep+servi+"')")
                    curs.fetchall()
                
                log = Log(target=ip, action="Verify Configuration",
                          status="Installation Succeed", time=make_aware(datetime.now()), messages="Nice Run")
                log.save()
                
            except Exception as e:
                result.append(e)
                for i in range (0,7):
                    result.append("Unable to execute step")
                log = Log(target=ip, action="Verify Configuration",
                          status="Installation Error", time=make_aware(datetime.now()), messages="Error Detected")
                log.save()
            
            ssh_client.close()
            curs.close()
            return render(request, 'verify_result.html', {'result': result}) 
            
    elif request.method == "POST" and request.POST['submit'] == "Refresh":
        id_m = request.POST['mc']
        ip  = curs.execute("SELECT ip FROM `machine` WHERE id = '"+id_m+"'")
        ip = curs.fetchone()
        user = curs.execute("SELECT user FROM `machine` WHERE id = '"+id_m+"'")
        user = curs.fetchone()
        passw = curs.execute("SELECT AES_DECRYPT(DES_DECRYPT(DECODE(passw,'pass'),'pass'),'pass') from machine where id='"+id_m+"'")
        passw = curs.fetchone()
        r_user = curs.execute("SELECT r_user FROM `machine` WHERE id = '"+id_m+"'")
        r_user = curs.fetchone()
        r_pass = curs.execute("SELECT AES_DECRYPT(DES_DECRYPT(DECODE(r_pass,'pass'),'pass'),'pass') from machine where id='"+id_m+"'")
        r_pass = curs.fetchone()
        
        stat = "inactive"
        
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip[0],
                               username=r_user[0], password=r_pass[0])
            conn = ssh_client.invoke_shell()
            sttm = ""
            
            condat = str()
            while True:
                if conn.recv_ready():
                    condat += conn.recv(65535).decode()
                else:
                    continue
                if condat.endswith('$ '):
                    conn.send("sudo -s" + "\n")
                    time.sleep(1)
                elif condat.endswith(': '): 
                    conn.send(passw[0] + "\n")
                    time.sleep(1)
                elif condat.endswith('# '):
                    stat = "active"
                    break
                elif condat.find('try again') != -1:
                    stat = "incorrect machine (root) username/password"
                    break
            
            ssh_client.close()
            
        except Exception as e:
            stat = "inactive"
        
        curs.execute("UPDATE machine SET status = '"+stat+"' WHERE machine.id = '"+id_m+"'")
        curs.fetchall()
        devices = Device.objects.all()
        all_device = Device.objects.all()
        last_event = Log.objects.all().order_by('-id')[:10]
        curs.execute('select * from machine')
        dat = curs.fetchall()
        
        if dat == [[]]:
            sttm = "There is no machine saved, add a new one...."
        else:
            sttm = ""
        context = {
            'all_device': len(all_device),
            'last_event': last_event,
            'devices': devices,
            'dat': dat,
            'stat': stat,
            'sttm': sttm,
            'mode': 'Verify Config'
        }
        
        curs.close()
        
        return render(request, 'deploy.html', context)
    
    elif request.method == "POST" and request.POST['submit'] == "Save":
        name = request.POST['name']
        loc = request.POST['loc']
        platform = request.POST['platform']
        if platform == "ubuntu-18":
            platform = "Ubuntu 18.04 or below"
        elif platform == "ubuntu+20":
            platform = "Ubuntu 20.04 and above"
        ip  = request.POST['ip']
        user  = request.POST['user']
        passw   = request.POST['passw']
        r_user  = request.POST['r_user']
        r_pass   = request.POST['r_pass']
        ins = "INSERT INTO `machine` (`id`, `name`, `location`, `platform`, `ip`, `user`, `passw`, `r_user`, `r_pass`, `status`) VALUES (NULL, '"
        sep = "', '"
        stat = "inactive"
        
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip,
                               username=r_user, password=r_pass)
            conn = ssh_client.invoke_shell()
            sttm = ""
            
            condat = str()
            
            while True:
                if conn.recv_ready():
                    condat += conn.recv(65535).decode()
                else:
                    continue
                if condat.endswith('$ '):
                    conn.send("sudo -s" + "\n")
                    time.sleep(1)
                elif condat.endswith(': '):
                    conn.send(passw + "\n")
                    time.sleep(1)
                elif condat.endswith('# '):
                    stat = "active"
                    break
                elif condat.find('try again') != -1:
                    stat = "incorrect machine (root) username/password"
                    break
            
            ssh_client.close()
            
        except Exception as e:
            stat = "machine state is inactive"
        
        if stat == "active":
            curs.execute(ins+name+sep+loc+sep+platform+sep+ip+sep+user+"', ENCODE(DES_ENCRYPT(AES_ENCRYPT('"+passw+"','pass'),'pass'),'pass'), '"+r_user+"', ENCODE(DES_ENCRYPT(AES_ENCRYPT('"+r_pass+"','pass'),'pass'),'pass'), '"+stat+"')")
            curs.fetchall()
            sttm = "Machine saved successfully"
        else:
            sttm = "Cannot save new machine because "+stat

        devices = Device.objects.all()
        all_device = Device.objects.all()
        last_event = Log.objects.all().order_by('-id')[:10]
        curs.execute('select * from machine')
        dat = curs.fetchall()
        
        if dat == [[]]:
            sttm += "\nThere is no machine saved, add a new one...."
        else:
            sttm+= "\n"
        
        context = {
            'all_device': len(all_device),
            'last_event': last_event,
            'devices': devices,
            'dat': dat,
            'stat': stat,
            'sttm': sttm,
            'mode': 'Verify Config'
        }
        
        curs.close()
        
        return render(request, 'deploy.html', context)

    else:
        devices = Device.objects.all()
        all_device = Device.objects.all()
        last_event = Log.objects.all().order_by('-id')[:10]
        curs.execute('select * from machine')
        dat = curs.fetchall()
        
        sttm = ""
        
        if dat == [[]]:
            sttm = "There is no machine saved, add a new one...."
        else:
            sttm = ""
        context = {
            'all_device': len(all_device),
            'last_event': last_event,
            'devices': devices,
            'dat': dat,
            'sttm': sttm,
            'mode': 'Verify Config'
        }
        
        curs.close()
        
        return render(request, 'deploy.html', context)
        

def about(request):
    return render(request, 'about.html')

def verify_result(request):
    return render(request, 'verify_result.html')