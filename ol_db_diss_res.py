########################################################################
##   Restore_hot_database_backup.sh      ##
##   edited by Wang Xiaoyun                  ##
##        2016-7-6                           ##
#########################################################################

import pexpect 
import os
import time
import glob
import pwd
os.environ["ORACLE_HOME"]="/data1/ora11g/product/11.2.0/dbhome_1"
os.environ["LD_LIBRARY_PATH"]=os.getenv("ORACLE_HOME")+"/lib"
os.environ["ORACLE_SID"]="ORACLE_SID"
os.environ["ORACLE_USER"]="ora11g"
os.unsetenv('TWO_TASK')
os.environ["PATH"] += os.pathsep + os.getenv('ORACLE_HOME')+"/bin"+os.pathsep+os.getenv('ORACLE_HOME')+"/OPatch"
BACKUP_DATE = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
RMAN_LOG_FILE = "/data1/backup/logs/resdbbac_"+BACKUP_DATE+".log"
BACKUP_DIR = "/data1/backup/"
os.system('export ORACLE_SID=OWSSHS10')
os.system('echo "-----------------'+BACKUP_DATE+'-----------------">'+RMAN_LOG_FILE)
os.system('echo "ORACLE_SID: '+os.getenv("ORACLE_SID")+'">>'+RMAN_LOG_FILE)
os.system('echo "ORACLE_HOME: '+os.getenv("ORACLE_HOME")+'">>'+RMAN_LOG_FILE)
os.system('echo "ORACLE_USER: '+os.getenv("ORACLE_USER")+'">>'+RMAN_LOG_FILE)
os.system('echo "==========================================" >>'+RMAN_LOG_FILE)
os.system('echo "RESTORE DATABASE BEGIN......" >>'+RMAN_LOG_FILE)
os.system('echo "                   " >>'+RMAN_LOG_FILE)
os.system('chmod 666 '+RMAN_LOG_FILE)

newsp = sorted(glob.glob(BACKUP_DIR+"level_cont_spfile*"), key=os.path.getctime)[-1]
print('restore control file found :'+newsp );
print('RMAN starting...');

child = pexpect.spawn('rman TARGET sys/passwd@ORACLE_SID nocatalog msglog '+RMAN_LOG_FILE+' append',timeout=9000)
child.expect ('RMAN>')
child.sendline ('shutdown immediate')
child.expect ('RMAN>')
child.sendline ('startup nomount')
child.expect ('RMAN>')
print('restore controlfile from "'+newsp+'";')
child.sendline('restore controlfile from "'+newsp+'";')
child.expect ('RMAN>')
child.sendline ('alter database mount;')
#child.expect ('RMAN>')
#child.sendline('CATALOG START WITH "/data1/backup/";')
#index = child.expect (['(enter YES or NO)?','no files found to be unknown to the database'])
#if (index ==0):
	child.sendline('YES')
#else:
#	os.system('echo "------- No catalog backupfile found ----- " >>'+RMAN_LOG_FILE)
child.expect ('RMAN>')
child.sendline()
child.expect ('RMAN>')
print ('RESTORE DATABSE ....')
child.sendline ('RESTORE DATABASE;')
child.expect ('RMAN>')
child.sendline()
child.expect ('RMAN>')
print ('RESTROE DATABAE DONE...')
print ('RECOVER DATABASE ...')
child.sendline('RECOVER DATABASE;')
child.expect ('RMAN>')
child.sendline()
child.expect ('RMAN>')
child.sendline()
print ('RECOVER DATABASE DONE....')
child.expect ('RMAN>')
child.sendline()
child.expect ('RMAN>')
child.sendline()
child.expect ('RMAN>')
child.sendline()
child.expect ('RMAN>')
child.sendline('alter database open resetlogs;')
child.expect ('RMAN>')
child.sendline()
child.expect ('RMAN>')
child.sendline()

print("database open done.")
child.sendline('exit')


os.system('echo "  ====   script endding            ====      " >>'+RMAN_LOG_FILE)
BACKUP_DATE = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
os.system('echo "-----------------'+BACKUP_DATE+'-----------------">>'+RMAN_LOG_FILE)

