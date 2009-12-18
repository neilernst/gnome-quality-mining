from names import Taxonomy
import subprocess
t = Taxonomy()
for sign in t.get_signified():
    wordlist =  t.get_signifiers(sign)
    for word in wordlist:
        p = subprocess.Popen(["perl", "typo.pl", word], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) 
        (out, err) = p.communicate()
        print out
        # print word