import fcntl, os, pty, re, runpy, select, struct, subprocess, sys, termios, time
from types import SimpleNamespace

entry = sys.argv[1]
help_text = subprocess.check_output([entry, "--help"])
assert b"-help" in help_text and b"--huge" in help_text
for flag in ("-h", "-help"):
    assert subprocess.check_output([entry, flag]) == help_text
module = runpy.run_path(entry)
for cols, rows in [(16,8),(80,24),(150,52),(220,100),(300,12),(20,80)]:
    args = SimpleNamespace(huge=True,large=False,no_pot=False,dirt=False,leaves='classic')
    for seed in [1,12,41]:
        pot, frames=module['make_tree'](cols,rows,args,seed)
        cells=pot+[cell for frame in frames for cell in frame]
        assert all(0<=x<cols and 0<=y<rows for x,y,*_ in cells)
        if (cols,rows)==(150,52):
            xs,ys=zip(*[(x,y) for x,y,*_ in cells])
            assert max(xs)-min(xs)>0.90*cols and max(ys)-min(ys)>0.9*rows
        assert (pot,frames)==module['make_tree'](cols,rows,args,seed)
    args.dirt = True
    for large, huge in [(False, False),(True, False),(False, True)]:
        args.large, args.huge = large, huge
        pot, frames = module['make_tree'](cols,rows,args,41)
        assert not pot
        assert max(y for frame in frames for _,y,*_ in frame)==rows-4
        bands = module['soil'](cols,rows,41)
        for row in range(rows-2,rows+1):
            assert re.search(rf'\x1b\[{row};1H\x1b\[[0-9;]+m[ ·.,]{{{cols}}}(?=\x1b)', bands)
print('Layout, size bounds, reproducibility and terminal coverage passed')

def live(flags, loop=False):
    m,s=pty.openpty()
    def resize(rows,cols):
        fcntl.ioctl(s,termios.TIOCSWINSZ,struct.pack('HHHH',rows,cols,0,0))
    resize(8,16) if loop else resize(42,128)
    p=subprocess.Popen([entry,*flags],stdin=s,stdout=s,stderr=s,env={**os.environ,'TERM':'xterm-256color'})
    def capture(duration):
        output=b''
        end=time.monotonic()+duration
        while time.monotonic()<end:
            if select.select([m],[],[],0.025)[0]: output+=os.read(m,65536)
        return output
    try:
        output=capture(0.4)
        assert output.count(b'\x1b]4;')>=2 and b'\x1b[38;5;201m' in output
        if '--dirt' in flags:
            assert b'48;5;94;' in output and '╭'.encode() not in output
        if loop:
            end=time.monotonic()+10
            while output.count(b'\x1b[2J')<2 and time.monotonic()<end:
                output+=capture(0.15)
            assert output.count(b'\x1b[2J')>=2
        else:
            resize(6,10)
            assert b'Enlarge' in capture(0.16)
            resize(33,99)
            assert b'\x1b[2J' in capture(0.16)
        os.write(m,b'q')
        output+=capture(.18)
        assert p.wait(timeout=2)==0 and b'\x1b[?1049l' in output and b'\x1b]104;' in output
    finally:
        if p.poll() is None: p.kill(); p.wait()
        os.close(m); os.close(s)

live([])
live(['--large','--theme','ocean','--leaves','needle','--cycle','4','--no-pot','--dirt','--seed','19'])
live(['--huge','--dirt','--infinite','--theme','sakura','--wait','0'],True)
print('Live terminal growth, resize, looping, keypress and screen restoration passed')
