import sys
import datetime
import subprocess
import time
import os
from constants import *



def PlayAndWait(macro, timeout_seconds = 30, var1 = '-', var2 = '-', var3 = '-', path_downloaddir = None, path_autorun_html = None, browser_path = None):

    assert os.path.exists(path_downloaddir)
    assert os.path.exists(path_autorun_html)
    assert os.path.exists(browser_path)
    
    log = 'log_' + datetime.datetime.now().strftime('%m-%d-%Y_%H_%M_%S') + '.txt'
    
    path_log = os.path.join(path_downloaddir, log)

    
    args = r'file:///' + path_autorun_html + '?macro=' + macro + '&cmd_var1=' + var1 + '&cmd_var2=' + var2 + '&cmd_var3=' + var3 + '&closeKantu=0&direct=1&savelog=' + log
    
    proc = subprocess.Popen([browser_path, args])
    
    status_runtime = 0   
    
    print("Log File will show up at " + path_log)
    
    while(not os.path.exists(path_log) and status_runtime < timeout_seconds):
        print("Waiting for macro to finish, seconds=%d" % status_runtime)
        time.sleep(1)
        status_runtime = status_runtime + 1
    
    if status_runtime < timeout_seconds:
        with open(path_log) as f:
            status_text = f.readline()
        
        status_init = 1 if status_text.find('Status=OK') != -1 else -1        
        
    else:
        status_text = "Macro did not complete within the time given: %d" % timeout_seconds
        status_init = -2
        proc.kill()
        
    print(status_text)
    proc.kill()
    sys.exit(status_init)


if __name__ == '__main__':
    PlayAndWait(kantuScript, timeout_seconds = 120, path_downloaddir = kantuDownload, path_autorun_html = kantuAutoRun, browser_path=kantuFirefoxPath)

    #PlayAndWait('DemoAutofill', timeout_seconds = 35, path_downloaddir = r'C:\Downloads\\', path_autorun_html = r'M:\pyscript\cmdlinetest.html', browser_path=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
   
    
    
    
