The [Linux startup process](https://en.wikipedia.org/wiki/Linux_startup_process) goes through several stages before reaching the final [graphical or multi-user target](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/sect-managing_services_with_systemd-targets). The initramfs stage occurs just before the root file system is mounted. Dracut is a tool that is used to manage the initramfs. The dracut emergency shell is an interactive mode that can be initiated while the initramfs is loaded.

This article will show how to use the dracut command to modify the initramfs. Some basic troubleshooting commands that can be run from the dracut emergency shell will also be demonstrated.
## **The InitRAMFS**
[Initramfs](https://en.wikipedia.org/wiki/Initial_ramdisk) stands for Initial Random-Access Memory File System. On modern Linux systems, it is typically stored in a file under the /boot directory. The kernel version for which it was built will be included in the file name. A new initramfs is generated every time a new kernel is installed.

![](Aspose.Words.dbbb0a0d-68da-4bf9-be8a-f07824c81d71.001.jpeg)**A Linux Boot Directory**

By default, Fedora keeps the previous two versions of the kernel and its associated initramfs. This default can be changed by modifying the value of the *installonly\_limit* setting the /etc/dnf/dnf.conf file.

You can use the *lsinitrd* command to list the contents of your initramfs archive:

![](Aspose.Words.dbbb0a0d-68da-4bf9-be8a-f07824c81d71.001.jpeg)**The LsInitRD Command**

The above screenshot shows that my initramfs archive contains the *nouveau* GPU driver. The *modinfo* command tells me that the nouveau driver supports several models of NVIDIA video cards. The *lspci* command shows that there is an NVIDIA GeForce video card in my computer’s PCI slot. There are also several basic Unix commands included in the archive such as *cat* and *cp*.

By default, the initramfs archive only includes the drivers that are needed for your specific computer. This allows the archive to be smaller and decreases the time that it takes for your computer to boot.
## **The Dracut Command**
The *dracut* command can be used to modify the contents of your initramfs. For example, if you are going to move your hard drive to a new computer, you might want to temporarily include all drivers in the initramfs to be sure that the operating system can load on the new computer. To do so, you would run the following command:

\# dracut --force --no-hostonly

The *force* parameter tells dracut that it is OK to overwrite the existing initramfs archive. The *no-hostonly* parameter overrides the default behavior of including only drivers that are germane to the currently-running computer and causes dracut to instead include all drivers in the initramfs.

By default dracut operates on the initramfs for the currently-running kernel. You can use the *uname* command to display which version of the Linux kernel you are currently running:

$ uname -r

5.0.5-200.fc29.x86\_64

Once you have your hard drive installed and running in your new computer, you can re-run the dracut command to regenerate the initramfs with only the drivers that are needed for the new computer:

\# dracut --force

There are also parameters to add arbitrary drivers, dracut modules, and files to the initramfs archive. You can also create configuration files for dracut and save them under the /etc/dracut.conf.d directory so that your customizations will be automatically applied to all new initramfs archives that are generated when new kernels are installed. As always, check the man page for the details that are specific to the version of dracut you have installed on your computer:

$ man dracut
## **The Dracut Emergency Shell**
![](Aspose.Words.dbbb0a0d-68da-4bf9-be8a-f07824c81d71.001.jpeg)**The Dracut Emergency Shell**

Sometimes something goes wrong during the initramfs stage of your computer’s boot process. When this happens, you will see “Entering emergency mode” printed to the screen followed by a shell prompt. This gives you a chance to try and fix things up manually and continue the boot process.

As a somewhat contrived example, let’s suppose that I accidentally deleted an important kernel parameter in my boot loader configuration:

\# sed -i 's/ rd.lvm.lv=fedora\/root / /' /boot/grub2/grub.cfg

The next time I reboot my computer, it will seem to hang for several minutes while it is trying to find the root partition and eventually give up and drop to an emergency shell.

From the emergency shell, I can enter *journalctl* and then use the **Space** key to page down though the startup logs. Near the end of the log I see a warning that reads “/dev/mapper/fedora-root does not exist”. I can then use the *ls* command to find out what does exist:

\# ls /dev/mapper

control  fedora-swap

Hmm, the fedora-root LVM volume appears to be missing. Let’s see what I can find with the lvm command:

\# lvm lvscan

`  `ACTIVE            '/dev/fedora/swap' [3.85 GiB] inherit

`  `inactive          '/dev/fedora/home' [22.85 GiB] inherit

`  `inactive          '/dev/fedora/root' [46.80 GiB] inherit

Ah ha! There’s my root partition. It’s just inactive. All I need to do is activate it and exit the emergency shell to continue the boot process:

\# lvm lvchange -a y fedora/root

