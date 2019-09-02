import os
import subprocess

def killRadio():
	p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
	out, err = p.communicate()
	for line in out.splitlines():
		if 'multimon-ng' in line:
			pid = int(line.split(None, 1)[0])
			os.kill(pid, 9)