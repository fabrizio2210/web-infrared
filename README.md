Istruzioni:
http://www.raspberrypiwiki.com/index.php/Raspberry_Pi_IR_Control_Expansion_Board

istruzioni piu' recenti, ma con pin sbagliati:
https://mariodivece.com/blog/2018/03/11/using-lirc-on-the-pi

istruzioni abbastanza complete:
https://gist.github.com/prasanthj/c15a5298eb682bde34961c322c95378b

Sintesi:
vi /boot/config.txt
vi /etc/modules
vi /etc/lirc/lircd.conf
reboot

per registrare:
irrecord -d /dev/lirc0 -k
