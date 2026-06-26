from ftplib import FTP
from pathlib import Path
import time,os
from config import *
from utils import ping,save,now

files=list(Path("../Jogos").glob("*"))
if not files:
    print("Coloque arquivos na pasta ../Jogos");raise SystemExit
print("Arquivos:")
for i,f in enumerate(files,1): print(f"{i} - {f.name}")
idx=int(input("Escolha: "))-1
reps=int(input("Repeticoes: "))
arq=files[idx]
csv="../Resultados/ftp.csv"

for n in range(1,reps+1):
    print(f"\nTeste {n}/{reps}")
    p,l=ping(PS3_IP)
    ftp=FTP(PS3_IP,timeout=30)
    ftp.login(FTP_USER,FTP_PASSWORD)
    ftp.cwd(REMOTE_DIR)
    total=os.path.getsize(arq)
    sent=[0]
    def cb(block):
        sent[0]+=len(block)
        pct=sent[0]/total*100
        print(f"\r{pct:6.2f}% ",end="")
    ini=time.perf_counter()
    with open(arq,"rb") as f:
        ftp.storbinary(f"STOR {arq.name}",f,8192,callback=cb)
    t=time.perf_counter()-ini
    ftp.quit()
    thr=round((total/1024/1024*8)/t,2)
    print(f"\nTempo {t:.2f}s Throughput {thr} Mbps")
    save(csv,[now(),arq.name,round(t,2),thr,p,l])
print("\nConcluido.")
