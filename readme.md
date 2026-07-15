# GKI KernelSU SUSFS
### Automated Kernel Build Repository for ReSukiSU

**Automated GKI Kernel Builds | Integrated ReSukiSU + SUSFS**

[![Release](https://img.shields.io/github/v/release/coolzyd9107/GKI_KernelSU_SUSFS?label=Release&style=flat-square&logo=github&logoColor=white&color=2ea44f)](https://github.com/ReSukiSU-GKI/GKI_KernelSU_SUSFS/releases)
[![Telegram](https://img.shields.io/static/v1?label=Telegram&message=Channel&color=0088cc)](https://t.me/ReSukiSUKernelBuilds)
[![ReSukiSU](https://img.shields.io/badge/ReSukiSU-Supported-5AA300?style=flat-square)](https://kernelsu.org/)
[![SUSFS](https://img.shields.io/badge/SUSFS-Integrated-E67E22?style=flat-square)](https://gitlab.com/simonpunk/susfs4ksu)

---

## ⚠️ Repository Disclaimer

1. This repository is a fork of [zzh20188/GKI_KernelSU_SUSFS](https://github.com/zzh20188/GKI_KernelSU_SUSFS/). Only minor updates and bug fixes have been applied here. For general builds, please consider using the upstream repository.

2. This repository only supports building kernels with **ReSukiSU**. Support for other KernelSU variants has been completely removed. If you need to build with other variants, please fork the upstream repository and build it yourself.

---

## ⚠️ Key Updates

> **Note:** OnePlus ColorOS 14 and 15 are currently not supported; flashing might require a factory reset to boot.

> **ReSukiSU:** ReSukiSU is updated more frequently than SukiSU. If SukiSU throws errors, try ReSukiSU. The default variant has been set to **ReSukiSU**.

> **rekernel (Beta):** Supported rekernel features.

---

## 🧪 Droidspaces Container Support (Experimental)

> **Experimental Feature:** Successful booting is not guaranteed. Make sure to back up your stock Boot image before flashing.
>
> **Tip:** The workflow uses the [Official Patches](https://github.com/ravindu644/Droidspaces-OSS/tree/main/Documentation/resources/kernel-patches/GKI) from [Droidspaces](https://github.com/ravindu644/Droidspaces-OSS). 

[Droidspaces](https://github.com/ravindu644/Droidspaces-OSS) is a lightweight Linux container tool that runs a full Linux environment on Android.

**Support range:** 5.10 / 5.15 / 6.1 / 6.6 / 6.12

**Usage:** When running the workflow manually, select the `Droidspaces` option.

---

## 🧪 Masquerade `/proc/config.gz` (Stock Config)

This is an advanced feature. The build automatically checks if `config/stock_defconfig` exists: if it does, it applies it; if not, it skips it.

**Usage:**
1. Ensure your device is currently running Stock ROM + Stock Kernel.
2. Obtain `/proc/config.gz` from the device.
3. Extract it, rename it to `stock_defconfig`, and commit it to the [`config/`](config/) directory of this repository.

The build process will automatically:
- Copy it to the kernel source: `$KERNEL_ROOT/common/arch/arm64/configs/stock_defconfig`
- Change the rule for `$(obj)/config_data` in `$KERNEL_ROOT/common/kernel/Makefile` to use your stock config instead.
- Make the output `/proc/config.gz` match your stock kernel config.
