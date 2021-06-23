
# Instali Miriadan plennodon en senregila Raspberry Pi

Traduko el la gvidilo de Rikard Wissing. Origina anglalingva instrukcio troviĝas [ĉi tie](https://github.com/rikardwissing/raspberry-pi-xmy-full-node/blob/main/README.md). Samloke troveblas liaj elŝutaĵoj.

![image](https://user-images.githubusercontent.com/22580571/119530875-b6ca2a80-bd83-11eb-8648-0b2c5251037e.png)

Ĉi tiu instrukcio helpos vin aranĝi kaj instali Miriadan plennodon en Raspberry Pi dekomence ĝisfine.

### Aparataro

Eku akirante la necesajn konsistaĵojn

• Raspberry Pi de minimume 512 MB je RAM (tamen rekomendindas 2 GB)

• SD-karto de 16 GB aŭ plie kiu konformu je via selekto de Raspberry Pi (Mia nuna aparato uzas ĉirkaŭ 10 gigabajtojn, do 16-gigabajta SD-karto dume taŭgas, sed poste ĝi povus esti tro malgranda pro kreskado de blokĉeno)

• Elektro-adaptilo por Raspberry Pi

• Mojosa kesto por ĉio. Konsideru la subajn 3D-printeblaĵojn (opcie)

• “Sense HAT" por ĉarma lumspektaklo (opcie)

Verkante ĉi instrukcion mi testis ĝin en “Raspberry Pi 4” de 4 GB je RAM kun 16-gigabajta SD-karteto. Tiu tuta aranĝo kostis ĉirkaŭ 50 dolarojn. Depost tiam mi testis ĝin sukcesege en aliaj pli malmultekostaj modeloj. Kontrolu la subajn tabelojn por koni ĉiujn testitajn aparatojn.

### Testitaparatoj

#### Nunaj modeloj

| Aparato                | RAM*  | CPU*       | Proksimuma kosto | Noto                                                                                            |
| ---------------------- | ----- | ---------- | ---------------: | ------------------------------------------------------------------------------------------------|
| Raspberry Pi 4 Modelo B| 4GB   | 4x1.5GHz   | $50              | Senprobleme, ĝi glate funkcias. Rekomendinde!                                                   |
| Raspberry Pi Zero W    | 512MB | 700MHz     | $15              | Observu sube la instrukcion por ARM v6. Programtradukado kaj sinkronigo daŭras ĉirkaŭ du tagojn |

#### Malnovaj modeloj

| Aparato                | RAM*  | CPU*       | Proksimuma kosto | Noto                                                                                            |
| ---------------------- | ----- | ---------- | ---------------: | ------------------------------------------------------------------------------------------------|
| Raspberry Pi 3 Model B | 1GB   | 4x1.2GHz   | Neaplikeble      | Ĝi bezonas permutaĵon (Swap) sed funkcias grandioze                                             |
| Raspberry Pi 1 Model B | 512MB | 700MHz     | Neaplikeble      | Observu subela instrukciojn por ARM v6. Programtradukado kaj sinkronigo daŭras ĉirkau du tagojn | |


* Labormemoro (RAM)
* Ĉefprocesoro (CPU)

### Pretigu SD-karton

Antaŭ kiam startigi la aparaton ni bezonas pretigi la SD-karton.

1. Elŝutu “Raspberry Pi Imager” el https://www.raspberrypi.org/software/
2. Muntu la SD-karton en via komputilo
3. Lanĉu “Raspberry Pi Imager” kaj instalu “Raspberry Pi OS Lite” en via SD-karto
4. Malfermu la SD-karton en via dosierfoliumilo (eble vi bezonos remunti la SD-karton por ĝin aperigi)
5. Se vi planas defore mastrumi la aparaton, vi bezonos krei malplenan dosieron nomendan `ssh` en la SD-karto
6. Se vi volas la aparaton konektota al vifio, vi devas krei dosieron nomendan wpa_supplicant.conf en la SD-karto. Poste algluu la sekvan kodon en ĝi (anstataŭigante `RET-NOMO` kaj `RET-PASVORTO` per viaj vifiaj nomo kaj pasvorto):
   ```
   country=US
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1

   network={
       ssid="RET-NOMO"
       psk="RET-PASVORTO"
   }
   ```
Memoru ke kelkaj modeloj de la aparato, ekzemple “Pi 1” kaj “Pi Zero W”, nur rekonas sendratajn retojn de 2.4 gigahercoj

7. Konservu la dosieron kaj demetu la SD-karton
8. Muntu la SD-karton en la Raspberry Pi kaj startigu la aparaton
9. Post kiam la aparato startos, vi estu kapabla eĥosondi ĝin per la komando `ping raspberrypi`

Gratulon! Vi nun havas vian Raspberry Pi agordita, funkcianta kaj konektita al interreto.

### Defore kontroli la aparaton

Ĉi tiu elpaŝo estas opcia kaj ĝi nur bezonatas se vi ne volas konekti la aparaton al klavaro kaj ekrano. Ĉi tiu instrukcio fariĝis ankaŭ por la specifa kazo se vi havas SSH-klienton disponeblan en via terminalo. Vi povus uzi aliajn SSH-klientojn kaj adapti la instrukcion por ili.

1. Certiĝu ke vi observis la instrukcion pri kiel aktivigi sekurŝelon (SSH) en la antaŭa fazo, pretigante la SD-karton
2. Malfermu terminalon
3. Aliru la aparaton uzante `ssh pi@raspberrypi` (pi estas la uzantnomo, tial la pi@)
4. Uzu la pasvorton `raspberry` kiam ĝi estos postulata
5. Nun aperu ĉi tio aŭ similaĵo: `pi@raspberrypi:~ $`

Vi estas nun sukcese ensalutinta en la Raspberry Pi ekde alia komputilo, kaj ĉio pretas nun por instali Miriadon. Grandioza laboro!

### Instali kaj startigi Myriadcoin Core

#### Aŭtomata instalo

1. Rulu `wget -qO- https://github.com/rikardwissing/raspberry-pi-xmy-full-node/archive/refs/heads/main.tar.gz | tar xzfv -`
2. Sekve `rulu sudo raspberry-pi-xmy-full-node-main/auto-install` (legu la specialan instrukcion se vi uzas ARM v6)
3. Vi povus kontroli la protokolplenumadon, rulante `tail -f myriadcoind.log`
4. Por kontroli procezojn kaj retstatistikojn vi povas uzi bashtop, lanĉante `bashtop-master/bashtop`
 
#### Speciala instrukcio por ĉefprocesoroj ARM v6 (Raspberry Pi Zero aŭ Pi 1)

Se vi havas aparaton kun ĉefprocesoro ARM v6 (kiel Pi Zero aŭ Pi 1), vi bezonos ruli `sudo raspberry-pi-xmy-full-node-main/run-detached auto-install-arm6` (tio kompilos Miriadon el ties fonto). Ĝi plenumiĝos en malkroĉita ekrano, do por kontroli la progreson vi bezonos ordoni `sudo screen -r` (malligu ĝin el la ekrano per Stirklavo+A d).

Bashtop estas tro procesorintensa por tiaj aparatoj, tial la skripto anstataŭe instalas `htop`. Simple lanĉu htop por kontroli procezojn.

#### Permana instalo

(Permana instalo ne funkcias en Raspberry Pi Zero aŭ 1, observu la procedon de aŭtomata instalo por tiaj aparatoj)

1. Elŝutu kaj elĉerpu Myriadcoin Core: `mkdir -p myriadcoin && wget -qO- https://github.com/myriadteam/myriadcoin/releases/download/v0.18.1.0/myriadcoin-0.18.1.0-arm-linux-gnueabihf.tar.gz | tar xzfv - -C myriadcoin --strip-components=1`
2. Kreu dosierujon por la Miriada blokĉeno: `mkdir myriadcoin-data`
3. Malfermu tekstredaktilon por krei servon `nano myriadcoin.service` kaj kopiu la sekvan kodon en ĝi:

```
[Unit]
Description=Myriadcoin
After=network.target

[Service]
ExecStart=/home/pi/myriadcoin/bin/myriadcoind -datadir=/home/pi/myriadcoin-data -debuglogfile=/home/pi/myriadcoind.log -rpcpassword=rpc -port=10888 -disablewallet -listen -discover -upnp
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Se vi rulas en aparato kun malmulta labormemoro (RAM), eble indus provi pligrandigi la permutaĵon (swap-dosiero) aŭ testi per la sekvaj agordoj `-blocksonly -maxmempool=100 -dbcache=20 -maxorphantx=10 -maxsigcachesize=4 -rpcthreads=1`

4. Konservu la dosieron kunpremante Stirklavon+O (certiĝu ke la dosiero konservata nomiĝas `myriadcoin.service`)
5. Fermu la tekstredaktilon per Stirklavo+X
6. Kreu simbolan ligilon de la servo: `sudo ln -s /home/pi/myriadcoin.service /etc/systemd/system/myriadcoin.service`
7. Startigu la servon: `sudo systemctl start myriadcoin`
8. Certiĝu ke ĝi aktivas per la komando `htop`
9. Fermu htop per Stirklavo+C
10. Aktivigu la servon tiel ke ĝi startos ĉiufoje kiam la aparato ŝaltiĝos `sudo systemctl enable myriadcoin`
11. Laŭvole vi povus kontroli la protokolplenumadon per `tail -f myriadcoind.log`

Se via reta enkursigilo (router) akceptas UPnP, Miriado malfermos la ĝustajn konektejojn kaj igos vian nodon publika. Se vi rimarkos ke post ĝisdatiĝo ĝi ankoraŭ ne estas publika, vi eble bezonos agordi vian enkursigilon permane por resendi la TCP-pordon 10888 al la aparato.

### Krome

#### 3D-printaĵoj

En la dosierujo `extra/3d_prints` troveblas ĉarmaj Miriadmarkaj kestoj por Raspberry Pi.

Ili estas modifitaj versioj de la dizajnoj de [Malalo](https://www.thingiverse.com/thing:3723561) kaj [Make](https://www.thingiverse.com/thing:1173084).

| Device                 | Image | Note  |
| ---------------------- | ----- | ----- |
| Raspberry Pi 3         | <img src="https://user-images.githubusercontent.com/22580571/121495503-f3c82b00-c9d9-11eb-8b5b-25fdfccab756.jpg" width="150"> | La ĉarman lumspektaklon provizas la skripto de "Sense HAT". Prilegu pli sube. |
| Raspberry Pi Zero      | <img src="https://user-images.githubusercontent.com/22580571/121494123-c0d16780-c9d8-11eb-8297-277815b6c40c.jpg" width="150"> | Jen la plej ĉarma aĵo iam ekzistinta, ĉu ne? |

### Sense HAT

Se vi havas “Sense HAT” mi verkis skripton kiu montras la logotipon de Miriado kaj blinkas laŭ variaj koloroj kiam nova bloko trovitas. [Spektu ĝin funkciantan ĉi tie.](https://imgur.com/5Wl1JRo)

1. Akiru “Sense HAT” (https://www.raspberrypi.org/products/sense-hat/)
2. Rulu `sudo raspberry-pi-xmy-full-node-main/install-sense-hat`

### Algoritmoj kaj ties koloroj:

| Algo      | Koloro          |
| --------- | -------------- |
| SHA256D   | ![#71DD96](https://via.placeholder.com/15/71DD96/000000?text=+) `#71DD96 (113, 221, 150)` |
| Scrypt    | ![#FD951E](https://via.placeholder.com/15/FD951E/000000?text=+) `#FD951E (253, 149, 30)`  |
| Groestl   | ![#FDEF41](https://via.placeholder.com/15/FDEF41/000000?text=+) `#FDEF41 (253, 239, 65)`  |
| ~~Skein~~ (ne plu uzata) | ![#F6BEBE](https://via.placeholder.com/15/F6BEBE/000000?text=+) `#F6BEBE (246, 108, 190)` |
| ~~Qubit~~ (ne plu uzata) | ![#83E9ED](https://via.placeholder.com/15/83E9ED/000000?text=+) `#83E9ED (131, 233, 237)` |
| Yescrypt  | ![#86B7F0](https://via.placeholder.com/15/86B7F0/000000?text=+) `#86B7F0 (134, 183, 240)` |
| Argon2d   | ![#AF48DA](https://via.placeholder.com/15/AF48DA/000000?text=+) `#AF48DA (175, 72, 218)`  |

Tradukite de Spirajn

MMcFd23Np1ZritkFDv8PYEowjAMzLZYUdR
