echo off
lpfg.exe lsystem.l view.v anim.a material.mat functions.fset -c
time /t
echo Run 00
lpfg.exe lsystem.l view.v anim.a material.mat functions.fset -dll lsys.dll -b
time /t
echo Run 01
lpfg.exe lsystem.l view.v anim.a material.mat functions.fset -dll lsys.dll -b
time /t
echo Run 02
lpfg.exe lsystem.l view.v anim.a material.mat functions.fset -dll lsys.dll -b
time /t
echo Run 03
lpfg.exe lsystem.l view.v anim.a material.mat functions.fset -dll lsys.dll -b
time /t
echo Run 04
lpfg.exe lsystem.l view.v anim.a material.mat functions.fset -dll lsys.dll -b
time /t
echo Run 05
lpfg.exe lsystem.l view.v anim.a material.mat functions.fset -dll lsys.dll -b
time /t
