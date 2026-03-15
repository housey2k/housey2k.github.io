---
layout: post
title: "Reverse engineering of a NT98321BG DVR"
date: 2026-03-15
---

Soo this project is pretty simple, I was working on a DVR and the original goal was to run DOOM on it but I didn't have success trying to compile code for it, but I managed to edit scripts and even change the boot logo to my own. This is some research I did earlier, I'm just pasting it here with little change:

"This DVR is based on a NT98321BG SoC running Linux, I already did a lot of research on the firmware and I wrote scripts to unpack and repack the firmware, and allow me to edit the linux system in a simple folder format.

It originally runs an app called Sofia that handles all hardware stuff through HDAL and gives you a display to record, save recordings to USB, rewatch from HDD, change settings, etc

When Linux boots it runs a shell script at `/etc/init.d/rcS`, I tried editing it and had success doing changes like adding delays, removing or adding commands. I tried to access devices like `/dev/fb0` (which is mentioned on the main application Sofia), and `/dev/sda` (it's the name that shows when you go to the export video app and need to select a USB drive, they didn't have the effort of putting a nice name on it).
These devices apparently don't exist at boot since trying to call a script at sda or DDing into fb0 won't do anything. There is no UART logs even thought ttyS0 console is set at U-Boot. Apparently not even the serial devices are created by the linux kernel since writing a script to loop through all tty devices didn't work.

I have checked and there is a file called modules.tar.lzma inside the "usr" partition, the rcS script calls a script called `loadmod`, this script uncompresses the file and runs a script called `vg_boot.sh`, this script goes through every `.ko` file and runs insmod to load them into the kernel.
Taking a closer look at Sofia with Ghidra I have seen many references to HDMI and CVBS stuff while looking for a framebuffer, apparently a lot of the setup or driver communication is done by the application, I believe this was done on purpose to make it harder to write custom apps.
After a lot of searching, I managed to get my hands in several SDKs and documentation and have nearly 7GB of compressed files about this chip, on the documents I found something called "HDAL", that must be a fancy name for HAL, and the function names that I've seen on there match exactly the function names on ghidra, I couldn't find the compilers needed, but since it's just Linux ELF and hopefully build an application, so maybe we could work around it since we don't need to compile the whole kernel and BLs"

So this is my research, it was pretty early but was a good foundation. After looking around more, I confirmed that the DVR requires HDAL to work, the linux kernel is crude and doesn't do shit, the drivers also don't do shit when loaded into the kernel, we need to talk to the drivers so they start working, I don't see a reason for that besides making RE harder by not giving you a shell, LCD, or anything. Below there is an image from the SDK docs showing the boot chain, the most critical parts are `/mnt/mtd/vg_boot.sh` call that does `insmod`, and `module_init&` that runs HDAL code to initialize stuff, then give you a framebuffer and a shell, I can't call this vg_boot thing because it is contained inside Sofia, so it does the initialization and goes straight into the app.

![Boot Chain Image](/post_img/NT9832x_SDK_Boot.png)

These are the partitions on my firmware dump:
"custom": Strings for language, images for app personalization, firmware version, etc (all by branding, not changeable by a normal user)
"logo": Images for U-Boot logo and Sofia boot logo
"romfs": Linux Kernel
"usr": Sofia app compressed, Squirrel scripts, drivers compressed
"web": HTML files, not sure where they are used

More research is available on [Recessim Wiki](https://wiki.recessim.com/view/NT98321BG)
If you find this toolchain, please contact me through E-Mail or discord (brennomaturino2@gmail.com or @brennomaturino1)