import subprocess,os,csv
from datetime import datetime
def ping(ip):
 r=subprocess.run(["ping",ip,"-n","10"],capture_output=True,text=True,encoding="cp850",errors="ignore")
 avg=loss=""
 for l in r.stdout.splitlines():
  if "Média" in l or "Media" in l: avg=l.split("=")[-1].replace("ms","").strip()
  if "Perdidos" in l: loss=l.split("(")[-1].split("%")[0]
 return avg,loss
def save(csvfile,row):
 new=not os.path.exists(csvfile)
 with open(csvfile,"a",newline="",encoding="utf8") as f:
  w=csv.writer(f)
  if new:w.writerow(["Data","Arquivo","Tempo(s)","Throughput(Mbps)","Ping(ms)","Perda(%)"])
  w.writerow(row)
def now(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
