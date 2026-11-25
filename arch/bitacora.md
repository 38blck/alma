# Arch BTW

### To-Do

- Documentar la instalación de nodejs.
- Investigar como funcionan los screen lockers.
- Hacer funcionar las mute keys.
- Crear una animación para cuando se haga un screenshot.
- Documentar la configuración del bluetooth.

### Índice

1. [Introducción](#introducción)
2. [Instalación minimalista](instalación-minimalista)
3. [Instalación de entorno gráfico](instalación-de-entorno-gráfico)
4. [Configuración y personalización](configuración-y-personalización)
5. [Conexión a GitHub con SSH](#conexión-a-github-con-ssh)
6. [Referencias](#referencias)

## Introducción

Esta bitácora es para documentar el proceso de configuración de Arch, desde la instalación de los paquetes base hasta la personalización de Qtile.

Un gran amigo me regaló una laptop que tenía arrumbada, se me ocurrió que con la fluidez y libertad de Linux podría sacarle el máximo provecho a esa computadora viejita. Ya sabes, el típico proyecto de revivir una máquina modesta de hace una década y ser completamente funcional en la actualidad con tareas que no sean tan demandantes (al mismo tiempo, ser un resistente a la obsolescencia programada).

Como me dijo mi abuelo alguna vez mientras se tomaba su cuarta caguama: La basura de un hombre, es el tesoro de otro.

**Especificaciones**:

- **CPU** AMD A9-9425, 2 núcleos a 3.1GHz.
- **GPU** AMD Radeon R5 (Integrada).
- **RAM** 1x4GB a 2400MHz.
- **HDD** 1TB a 5400RPM.

## Instalación minimalista

En una memoria USB monté el archivo .iso de Arch.

Entré a la Bios, comprobé dos cosas, que estuviera el UEFI Boot activado y el Secure Boot desactivado. Guardé los cambios, conecté la memoria y reinicié la computadora.

Inicié el Live-ISO desde el Boot Menu. Comprobé que si haya iniciado en modo UEFI y la arquitectura del CPU:

```text
# ls /sys/firmware/efi/efivars
# cat /sys/firmware/efi/fw_platform_size
```

Me conecté a internet usando el comando interactivo `iwctl`:

```text
[iwd]# device list
[iwd]# station <device_name> get-networks
[iwd]# station <device_name> connect <network_ssid>
[iwd]# exit
```

Comprobé la conexión a internet:

```text
# ping -c 4 archlinux.org
```

Sincronicé con mi zona horaria:

```text
# timedatectl set-timezone America/Mexico_City
# timedatectl
```

Particioné el disco con `fdisk`:

Device      | Size    | Type
------------|---------|--------------
/dev/sd*xn* | 1GB     | EFI System
/dev/sd*xn* | 4GB     | Swap
/dev/sd*xn* | Default | Root (x86_64)

Formateé las particiones:

```text
# mkfs.fat -F 32 /dev/sd<xn>
# mkswap /dev/sd<xn>
# mkfs.ext4 /dev/sd<xn>
```

Monté las particiones:

```text
# mount --mkdir /dev/sd<xn> /mnt/boot
# swapon /dev/sd<xn>
# mount /dev/sd<xn> /mnt
```

Restauré mi configuración de los mirrors usando `curl`:

```text
# curl -o /etc/pacman.d/mirrorlist https://raw.githubusercontent.com/38blck/alma/main/arch/mirrorlist
# pacman -Sy
```

Instalé los paquetes esenciales:

```text
# pacstrap -K /mnt base base-devel linux linux-firmware nano
```

Generé el archivo fstab:

```text
# genfstab -U /mnt >> /mnt/etc/fstab
```

Ingresé al sistema recién instalado:

```text
# arch-chroot /mnt
```

Ajusté la zona horaria:

```text
# ln -sf /usr/share/zoneinfo/America/Mexico_City /etc/localtime
# hwclock --systohc
```

Ajusté el idioma del sistema:

```text
# nano /etc/locale.gen
	Descomenté: en_US.UTF-8 UTF-8
# locale-gen
# nano /etc/locale.conf
	Escribí: LANG=en_US.UTF-8
```

Configuré la red:

```text
# pacman -S networkmanager
# nano /etc/hostname
	Escribí: <hostname>
# nano /etc/hosts
	Escribí:
		127.0.0.1	localhost
		::1			localhost
		127.0.1.1	<hostname>
# systemctl enable NetworkManager
```

Agregué mi usuario:

```text
# passwd
# useradd -m -G wheel <username>
# passwd <username>
# nano /etc/sudoers
	Descomenté: %wheel ALL=(ALL:ALL) ALL
```

Instalé Grub:

```text
# pacman -S amd-ucode grub efibootmgr
# mount --mkdir /dev/sd<xn> /boot/efi
# grub-install --target=x86_64-efi --bootloader-id=grub
# grub-mkconfig -o /boot/grub/grub.cfg
```
Reinicié para iniciar en el nuevo sistema:

```text
# exit
# umount -R /mnt
# reboot
```

## Instalación de entorno gráfico

Inicié sesión y me conecté a internet:

```text
$ nmcli device
$ nmcli device wifi list
$ nmcli device wifi connect <network_ssid> password <network_passwod> ifname <device_name>
```

Comprobé la conexión a internet:

```text
$ ping -c 4 archlinux.org
```

Instalé los paquetes base:

```text
$ sudo pacman -S xorg qtile alacritty firefox git neovim noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-hack-nerd dmenu
```

***Nota**: En la selección de dependencias de Firefox, escoger lib32-pipewire-jack*.

Reinicié otra vez y ejecuté el entorno gráfico:

```text
$ qtile start
```

## Configuración y personalización

Configuré algunos shortcuts que considero son funciones esenciales como manipular la salida de audio, tomar screenshots o ajustar el brillo de la pantalla. De igual forma, agregué widgets para mostrar el estado del sistema operativo.

Primero, instalé los paquetes necesarios:

```text
$ sudo pacman -S pipewire pipewire-alsa pipewire-jack alsa-utils grim slurp wl-clipboard brightnessctl python-iwlib
```

***Nota**: Para hacer capturas de pantalla antes se tiene que crear el directorio ~/Pictures/Screenshots*.

No hice la gran cosa. En [r/unixporn](https://www.reddit.com/r/unixporn) he visto arroces muy bonitos, obras de arte dignas de admirar, aunque quisiera hacer algo parecido no tengo el conocimiento ni las ganas de construir algo así. Por el momento me conformo con una estética apenas cambiada.

Restauré los dotfiles:

```text
$ curl -o ~/.bashrc https://raw.githubusercontent.com/38blck/alma/main/arch/.bashrc
$ curl --create-dirs -o ~/.Scripts/alacritty_prompt.sh https://raw.githubusercontent.com/38blck/alma/main/arch/scripts/alacritty_prompt.sh
$ curl --create-dirs -o ~/.Scripts/cprj.sh https://raw.githubusercontent.com/38blck/alma/main/arch/scripts/cprj.sh

$ curl --create-dirs -o ~/.config/alacritty/alacritty.toml https://raw.githubusercontent.com/38blck/alma/main/arch/alacritty.toml

$ curl --create-dirs -o ~/.config/qtile/config.py https://raw.githubusercontent.com/38blck/alma/main/arch/config.py
$ curl --create-dirs -o ~/Pictures/Wallpapers/edu-lins-pIe9a3CWB4A-unsplash.jpg https://raw.githubusercontent.com/38blck/alma/main/arch/wallpapers/edu-lins-pIe9a3CWB4A-unsplash.jpg

$ curl --create-dirs -o ~/.config/nvim/init.lua https://raw.githubusercontent.com/38blck/alma/main/arch/init.lua
```

***Nota**: Reinicié tantas veces la computadora que no sé hasta que punto esto sea un requisito**.

## Conexión a GitHub con SSH

Instalé el paquete:

```text
$ sudo pacman -S openssh
```

Generé una key en ~/.ssh:

```text
$ ssh-keygen -t ed25519 -C <github_email>
```

Inicié el ssh-agent:

```text
$ eval "$(ssh-agent -s)"
```

Agregué la key al ssh-agent:

```text
$ ssh-add ~/.ssh/id_ed25519
```

Creé una SSH Key en GitHub copiando el contenido del archivo ~/.ssh/id_ed25519.pub.

Comprobé la conexión:

```text
$ ssh -T git@github.com
```

Configuré la identidad de git:

```text
$ git config --global user.name <name>
$ git config --global user.email <github_email>
```

## Referencias

- ArchWiki. [Installation guide](https://wiki.archlinux.org/title/Installation_guide).
- [Qtile docs](https://docs.qtile.org/en/stable/).
- GitHub Docs. [Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).
