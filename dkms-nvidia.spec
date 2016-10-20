%global privlibs             libGLESv1_CM_nvidia
%global privlibs %{privlibs}|libGLESv2_nvidia
%global privlibs %{privlibs}|libGLX_nvidia
%global privlibs %{privlibs}|libEGL_nvidia
%global privlibs %{privlibs}|libnvidia-eglcore
%global privlibs %{privlibs}|libnvidia-glsi
%global privlibs %{privlibs}|libnvidia-glcore
%global privlibs %{privlibs}|libnvidia-tls
%global privlibs %{privlibs}|libglx
%global privlibs %{privlibs}|libnvidia-fatbinaryloader
%global privlibs %{privlibs}|libnvidia-ptxjitcompiler
%global privlibs %{privlibs}|libvdpau_nvidia
%global privlibs %{privlibs}|libnvidia-compiler
%global privlibs %{privlibs}|libnvidia-opencl
%global __requires_exclude ^(%{privlibs})\\.so
%global __provides_exclude ^(%{privlibs})\\.so

Name:           dkms-nvidia
Version:        367.57
Release:        1%{?dist}
Summary:        NVIDIA display driver kernel module

License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html
Source0:        ftp://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-no-compat32.run
Source1:        blacklist-nouveau.conf
Source2:        10-nvidia-xorg-modules.conf

ExclusiveArch:  x86_64
BuildRequires:  nvidia-common
Requires:       dkms
Requires:       nvidia-modprobe

%description
This package contains NVIDIA kernel modules wrapped for the DKMS framework.


%package        -n nvidia-driver-nvml
Summary:        The NVIDIA Management Library
Requires:       nvidia-common

%description    -n nvidia-driver-nvml
A C-based API for monitoring and managing various states of the NVIDIA GPU
devices. NVIDIA Management Library (NVML) provides a direct access to the
queries and commands exposed via nvidia-smi.


%package        -n nvidia-smi
Summary:        NVIDIA System Management Interface program
Requires:       nvidia-driver-nvml%{?_isa} = %{version}-%{release}
Requires:       nvidia-common

%description    -n nvidia-smi
The application nvidia-smi is the NVIDIA System Management Interface for
management and monitoring functionality.


%package        -n nvidia-driver-bugreport
Summary:        NVIDIA bug reporting tool
Requires:       nvidia-common

%description    -n nvidia-driver-bugreport
This package provides system information collecting script along with NVIDIA's
tool for collecting internal GPU state.


%package        -n nvidia-driver-cuda
Summary:        Runtime support for CUDA applications
Requires:       nvidia-common

%description    -n nvidia-driver-cuda
These libraries provide runtime support for CUDA (high-performance computing on
the GPU) applications. The additional NVIDIA CUDA Video Decoder (NVCUVID)
library provides an interface to hardware video decoding capabilities on NVIDIA
GPUs with CUDA.


%package        -n nvidia-driver-nvenc
Summary:        The NVENC Video Encoding library
Requires:       nvidia-driver-cuda%{?_isa} = %{version}-%{release}
Requires:       nvidia-common

%description    -n nvidia-driver-nvenc
The NVENC Video Encoding library provides an interface to video encoder
hardware on supported NVIDIA GPUs.


%package        -n nvidia-driver-nvfbcopengl
Summary:        Framebuffer Capture and Inband Frame Readback libraries
Requires:       nvidia-driver-nvenc%{?_isa} = %{version}-%{release}
Requires:       nvidia-common

%description    -n nvidia-driver-nvfbcopengl
This package provides private APIs only available to approved partners for use
in remote graphics scenarios.

%package        -n nvidia-driver-vdpau
Summary:        NVIDIA implementation of VDPAU
Requires:       libvdpau%{?_isa}
Requires:       nvidia-common

%description    -n nvidia-driver-vdpau
The NVIDIA implementation of Video Decode and Presentation API for Unix-like
systems


%package        -n nvidia-driver-opencl
Summary:        NVIDIA vendor installable client driver
Requires:       opencl-icd-loader%{?_isa}
Requires:       nvidia-driver-cuda%{?_isa} = %{version}-%{release}
Requires:       nvidia-common

%description    -n nvidia-driver-opencl
This package provides the NVIDIA vendor installable client driver (ICD).


%package        -n nvidia-driver-cfg
Summary:        A library to query the GPUs in the system
Requires:       nvidia-common

%description    -n nvidia-driver-cfg
Optional library which is needed by nvidia-xconfig to query the GPUs in the
system.


%package        -n nvidia-driver-xorg
Summary:        NVIDIA OpenGL X11 display driver files
Requires:       glvnd-libGL%{?_isa}
Requires:       glvnd-libGLES%{?_isa}
Requires:       glvnd-libGLX%{?_isa}
Requires:       glvnd-libEGL%{?_isa}
Requires:       xorg-x11-server-Xorg
Requires:       nvidia-common

%description    -n nvidia-driver-xorg
This package contains an X driver, which is needed by the X server to use your
NVIDIA hardware along with GLX extension and hardware-accelerated OpenGL
implementation libraries.


%package        -n nvidia-driver-doc
Summary:        NVIDIA documentation
Requires:       nvidia-common
BuildArch:      noarch

%description    -n nvidia-driver-doc
Documentation files.


%prep
chmod +x %{SOURCE0}
sh %{SOURCE0} --extract-only --target %{name}-%{version}


%build


%install
rm -rf %{buildroot}

# This handles leftovers
mkdir -p %{buildroot}/_/
cp -rv %{name}-%{version}/* %{buildroot}/_/

# Prepare directories
install -d %{buildroot}%{_usrsrc}/nvidia-%{version}/
install -d %{buildroot}%{_prefix}/lib/modprobe.d/
install -d %{buildroot}%{_sysconfdir}/OpenCL/vendors/
install -d %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/
install -d %{buildroot}%{_datadir}/nvidia/
install -d %{buildroot}%{_nvidia_bindir}/
install -d %{buildroot}%{_nvidia_libdir}/
install -d %{buildroot}%{_nvidia_lib32dir}/
install -d %{buildroot}%{_nvidia_docdir}/%{name}-%{version}/
install -d %{buildroot}%{_nvidia_mandir}/man1/
install -d %{buildroot}%{_nvidia_libdir}/xorg/modules/drivers/
install -d %{buildroot}%{_nvidia_libdir}/xorg/modules/extensions/
# path seems to be hardcoded
install -d %{buildroot}%{_datadir}/nvidia/

pushd %{name}-%{version}

# DKMS
sed -e 's;__VERSION_STRING;%{version};' \
    -e 's;__JOBS;4;' \
    -e 's;__EXCLUDE_MODULES;;' \
    -e 's;__DKMS_MODULES;'\
'BUILT_MODULE_NAME[0]=nvidia\n'\
'DEST_MODULE_LOCATION[0]="/kernel/drivers/video"\n'\
'BUILT_MODULE_NAME[1]=nvidia-uvm\n'\
'DEST_MODULE_LOCATION[1]="/kernel/drivers/video"\n'\
'BUILT_MODULE_NAME[2]=nvidia-modeset\n'\
'DEST_MODULE_LOCATION[2]="/kernel/drivers/video"\n'\
'BUILT_MODULE_NAME[3]=nvidia-drm\n'\
'DEST_MODULE_LOCATION[3]="/kernel/drivers/video";' \
    -i kernel/dkms.conf
cp -rf kernel/* %{buildroot}%{_usrsrc}/nvidia-%{version}/
rm -rf %{buildroot}/_/kernel/

install -p -m644 %{SOURCE1} %{buildroot}%{_prefix}/lib/modprobe.d/

# NVML
install -p -m755 libnvidia-ml.so.%{version} %{buildroot}%{_nvidia_libdir}/

rm -f %{buildroot}/_/libnvidia-ml.so.%{version}

ln -s libnvidia-ml.so.%{version} %{buildroot}%{_nvidia_libdir}/libnvidia-ml.so.1

# smi
install -p -m755 nvidia-smi      %{buildroot}%{_nvidia_bindir}/
install -p -m644 nvidia-smi.1.gz %{buildroot}%{_nvidia_mandir}/man1/

rm -f %{buildroot}/_/{nvidia-smi,nvidia-smi.1.gz}

# bug-report
install -p -m755 nvidia-debugdump     %{buildroot}%{_nvidia_bindir}/
install -p -m755 nvidia-bug-report.sh %{buildroot}%{_nvidia_bindir}/

rm -f %{buildroot}/_/{nvidia-debugdump,nvidia-bug-report.sh}

# CUDA
install -p -m755 nvidia-cuda-mps-control      %{buildroot}%{_nvidia_bindir}/
install -p -m755 nvidia-cuda-mps-server       %{buildroot}%{_nvidia_bindir}/
install -p -m644 nvidia-cuda-mps-control.1.gz %{buildroot}%{_nvidia_mandir}/man1/

rm -f %{buildroot}/_/nvidia-cuda-mps-{control,control.1.gz,server}

install -p -m755 libcuda.so.%{version}                   %{buildroot}%{_nvidia_libdir}/
install -p -m755 libnvidia-fatbinaryloader.so.%{version} %{buildroot}%{_nvidia_libdir}/
install -p -m755 libnvidia-ptxjitcompiler.so.%{version}  %{buildroot}%{_nvidia_libdir}/
install -p -m755 libnvcuvid.so.%{version}                %{buildroot}%{_nvidia_libdir}/

rm -f %{buildroot}/_/libcuda.so.%{version}
rm -f %{buildroot}/_/libnvidia-fatbinaryloader.so.%{version}
rm -f %{buildroot}/_/libnvidia-ptxjitcompiler.so.%{version}
rm -f %{buildroot}/_/libnvcuvid.so.%{version}

ln -s libcuda.so.%{version}    %{buildroot}%{_nvidia_libdir}/libcuda.so.1
ln -s libnvcuvid.so.%{version} %{buildroot}%{_nvidia_libdir}/libnvcuvid.so.1

# NVENC
install -p -m755 libnvidia-encode.so.%{version} %{buildroot}%{_nvidia_libdir}/

rm -f %{buildroot}/_/libnvidia-encode.so.%{version}

ln -s libnvidia-encode.so.%{version} %{buildroot}%{_nvidia_libdir}/libnvidia-encode.so.1

# nvfbcopengl
install -p -m755 libnvidia-fbc.so.%{version} %{buildroot}%{_nvidia_libdir}/
install -p -m755 libnvidia-ifr.so.%{version} %{buildroot}%{_nvidia_libdir}/

rm -f %{buildroot}/_/{libnvidia-fbc.so.%{version},libnvidia-ifr.so.%{version}}

ln -s libnvidia-fbc.so.%{version} %{buildroot}%{_nvidia_libdir}/libnvidia-fbc.so.1
ln -s libnvidia-ifr.so.%{version} %{buildroot}%{_nvidia_libdir}/libnvidia-ifr.so.1

# VDPAU
install -p -m 0755 libvdpau_nvidia.so.%{version} %{buildroot}%{_nvidia_libdir}/

rm -f %{buildroot}/_/libvdpau_nvidia.so.%{version}

ln -s libvdpau_nvidia.so.%{version} %{buildroot}%{_nvidia_libdir}/libvdpau_nvidia.so
ln -s libvdpau_nvidia.so.%{version} %{buildroot}%{_nvidia_libdir}/libvdpau_nvidia.so.1

# OpenCL
install -p -m644 nvidia.icd %{buildroot}%{_sysconfdir}/OpenCL/vendors/

rm -f %{buildroot}/_/nvidia.icd

install -p -m755 libnvidia-compiler.so.%{version} %{buildroot}%{_nvidia_libdir}/
install -p -m755 libnvidia-opencl.so.%{version}   %{buildroot}%{_nvidia_libdir}/

rm -f %{buildroot}/_/{libnvidia-compiler.so.%{version},libnvidia-opencl.so.%{version}}

ln -s libnvidia-opencl.so.%{version} %{buildroot}%{_nvidia_libdir}/libnvidia-opencl.so.1

# cfg
install -p -m755 libnvidia-cfg.so.%{version} %{buildroot}%{_nvidia_libdir}/

rm -f %{buildroot}/_/libnvidia-cfg.so.%{version}

ln -s libnvidia-cfg.so.%{version} %{buildroot}%{_nvidia_libdir}/libnvidia-cfg.so.1

# xorg
install -p -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/
install -p -m644 nvidia-drm-outputclass.conf \
    %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/10-nvidia-drm-outputclass.conf

rm -f %{buildroot}/_/nvidia-drm-outputclass.conf

install -p -m755 nvidia_drv.so        %{buildroot}%{_nvidia_libdir}/xorg/modules/drivers/
install -p -m755 libglx.so.%{version} %{buildroot}%{_nvidia_libdir}/xorg/modules/extensions/

rm -f %{buildroot}/_/nvidia_drv.so
rm -f %{buildroot}/_/libglx.so.%{version}

ln -s libglx.so.%{version} \
    %{buildroot}%{_nvidia_libdir}/xorg/modules/extensions/libglx.so

install -p -m755 libGLESv1_CM_nvidia.so.%{version} %{buildroot}%{_nvidia_libdir}/
install -p -m755 libGLESv2_nvidia.so.%{version}    %{buildroot}%{_nvidia_libdir}/
install -p -m755 libGLX_nvidia.so.%{version}       %{buildroot}%{_nvidia_libdir}/
install -p -m755 libEGL_nvidia.so.%{version}       %{buildroot}%{_nvidia_libdir}/
install -p -m755 libnvidia-eglcore.so.%{version}   %{buildroot}%{_nvidia_libdir}/
install -p -m755 libnvidia-glsi.so.%{version}      %{buildroot}%{_nvidia_libdir}/
install -p -m755 libnvidia-glcore.so.%{version}    %{buildroot}%{_nvidia_libdir}/
install -p -m755 tls/libnvidia-tls.so.%{version}   %{buildroot}%{_nvidia_libdir}/

rm -f %{buildroot}/_/libGLESv1_CM_nvidia.so.%{version}
rm -f %{buildroot}/_/libGLESv2_nvidia.so.%{version}
rm -f %{buildroot}/_/libGLX_nvidia.so.%{version}
rm -f %{buildroot}/_/libEGL_nvidia.so.%{version}
rm -f %{buildroot}/_/libnvidia-eglcore.so.%{version}
rm -f %{buildroot}/_/libnvidia-glsi.so.%{version}
rm -f %{buildroot}/_/libnvidia-glcore.so.%{version}
rm -f %{buildroot}/_/tls/libnvidia-tls.so.%{version}

ln -s libGLESv1_CM_nvidia.so.%{version} %{buildroot}%{_nvidia_libdir}/libGLESv1_CM_nvidia.so.1
ln -s libGLESv2_nvidia.so.%{version}    %{buildroot}%{_nvidia_libdir}/libGLESv2_nvidia.so.2
ln -s libGLX_nvidia.so.%{version}       %{buildroot}%{_nvidia_libdir}/libGLX_nvidia.so.0
ln -s libEGL_nvidia.so.%{version}       %{buildroot}%{_nvidia_libdir}/libEGL_nvidia.so.0

install -p -m644 nvidia-application-profiles-%{version}-key-documentation %{buildroot}%{_datadir}/nvidia/
install -p -m644 nvidia-application-profiles-%{version}-rc %{buildroot}%{_datadir}/nvidia/

rm -f %{buildroot}/_/nvidia-application-profiles-%{version}-rc
rm -f %{buildroot}/_/nvidia-application-profiles-%{version}-key-documentation

# doc
cp -pr html/ LICENSE NVIDIA_Changelog README.txt \
    %{buildroot}%{_nvidia_docdir}/%{name}-%{version}/

rm -rf %{buildroot}/_/html/
rm -f %{buildroot}/_/{LICENSE,NVIDIA_Changelog,README.txt}

popd

# manual cleanup
# provided by mesa
rm -f %{buildroot}/_/{gl.h,glext.h,glx.h,glxext.h}
# provided by opencl-icd-loader
rm -f %{buildroot}/_/libOpenCL.so.1.0.0
# provided by glvnd
rm -f %{buildroot}/_/libEGL.so.1
rm -f %{buildroot}/_/libGL.la
rm -f %{buildroot}/_/libGL.so.1.0.0
rm -f %{buildroot}/_/libGLX.so.0
rm -f %{buildroot}/_/libGLdispatch.so.0
rm -f %{buildroot}/_/libOpenGL.so.0
rm -f %{buildroot}/_/libGLESv1_CM.so.1
rm -f %{buildroot}/_/libGLESv2.so.2
rm -f %{buildroot}/_/libGL.so.%{version}
rm -rf %{buildroot}/_/libglvnd_install_checker/
# provided by nvidia-settings
rm -f %{buildroot}/_/libnvidia-gtk2.so.%{version}
rm -f %{buildroot}/_/libnvidia-gtk3.so.%{version}
rm -f %{buildroot}/_/nvidia-settings{,.1.gz,.desktop,.png}
# provided by nvidia-modprobe
rm -f %{buildroot}/_/nvidia-modprobe{,.1.gz}
# provided by nvidia-persistenced
rm -f %{buildroot}/_/nvidia-persistenced{,-init.tar.bz2,.1.gz}
# provided by nvidia-xconfig
rm -f %{buildroot}/_/nvidia-xconfig{,.1.gz}
# TLS garbage
rm -f %{buildroot}/_/libnvidia-tls.so.%{version}
rm -f %{buildroot}/_/tls_test{,_dso.so}
# didn't figured out how to use that
rm -f %{buildroot}/_/libnvidia-wfb.so.%{version}
# no wayland ATM
rm -f %{buildroot}/_/libnvidia-egl-wayland.so.%{version}
# no vulkan ATM
rm -f %{buildroot}/_/nvidia_icd.json
# installer
rm -f %{buildroot}/_/nvidia-installer{,.1.gz}
rm -f %{buildroot}/_/makeself-help-script.sh
rm -f %{buildroot}/_/makeself.sh
rm -f %{buildroot}/_/mkprecompiled
rm -f %{buildroot}/_/pkg-history.txt
rm -rf %{name}-%{version}


%files
%{_prefix}/lib/modprobe.d/blacklist-nouveau.conf
%{_usrsrc}/nvidia-%{version}/

%files -n nvidia-driver-nvml
%{_nvidia_libdir}/libnvidia-ml.so.*

%files -n nvidia-smi
%{_nvidia_bindir}/nvidia-smi
%{_nvidia_mandir}/man1/nvidia-smi.1.gz

%files -n nvidia-driver-bugreport
%{_nvidia_bindir}/nvidia-debugdump
%{_nvidia_bindir}/nvidia-bug-report.sh

%files -n nvidia-driver-cuda
%{_nvidia_bindir}/nvidia-cuda-mps-control
%{_nvidia_bindir}/nvidia-cuda-mps-server
%{_nvidia_libdir}/libcuda.so.*
%{_nvidia_libdir}/libnvidia-fatbinaryloader.so.*
%{_nvidia_libdir}/libnvidia-ptxjitcompiler.so.*
%{_nvidia_libdir}/libnvcuvid.so.*
%{_nvidia_mandir}/man1/nvidia-cuda-mps-control.1.gz

%files -n nvidia-driver-nvenc
%{_nvidia_libdir}/libnvidia-encode.so.*

%files -n nvidia-driver-nvfbcopengl
%{_nvidia_libdir}/libnvidia-fbc.so.*
%{_nvidia_libdir}/libnvidia-ifr.so.*

%files -n nvidia-driver-vdpau
%{_nvidia_libdir}/libvdpau_nvidia.so
%{_nvidia_libdir}/libvdpau_nvidia.so.*

%files -n nvidia-driver-opencl
%{_sysconfdir}/OpenCL/vendors/nvidia.icd
%{_nvidia_libdir}/libnvidia-compiler.so.*
%{_nvidia_libdir}/libnvidia-opencl.so.*

%files -n nvidia-driver-cfg
%{_nvidia_libdir}/libnvidia-cfg.so.*

%files -n nvidia-driver-xorg
%config %{_sysconfdir}/X11/xorg.conf.d/*.conf
%{_nvidia_libdir}/xorg/
%{_nvidia_libdir}/libGLESv1_CM_nvidia.so.*
%{_nvidia_libdir}/libGLESv2_nvidia.so.*
%{_nvidia_libdir}/libGLX_nvidia.so.*
%{_nvidia_libdir}/libEGL_nvidia.so.*
%{_nvidia_libdir}/libnvidia-eglcore.so.%{version}
%{_nvidia_libdir}/libnvidia-glsi.so.%{version}
%{_nvidia_libdir}/libnvidia-glcore.so.%{version}
%{_nvidia_libdir}/libnvidia-tls.so.%{version}
%dir %{_datadir}/nvidia/
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-rc
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-key-documentation

%files -n nvidia-driver-doc
%{_nvidia_docdir}/%{name}-%{version}/


%pre
# workaround upgrade from failing 349.16 for now
# TODO: remove this later
if [ $1 -gt 1 ]; then
    dkms remove --quiet --module nvidia -v 349.16 --all --rpm_safe_upgrade || :
fi

%preun
dkms remove --quiet --module nvidia -v %{version} --all --rpm_safe_upgrade || :

%posttrans
dkms add --quiet --module nvidia -v %{version} --rpm_safe_upgrade
dkms build --quiet --module nvidia -v %{version}
dkms install --quiet --force --module nvidia -v %{version}
exit 0

%post -n nvidia-driver-nvml -p /sbin/ldconfig
%postun -n nvidia-driver-nvml -p /sbin/ldconfig

%post -n nvidia-driver-cuda -p /sbin/ldconfig
%postun -n nvidia-driver-cuda -p /sbin/ldconfig

%post -n nvidia-driver-nvenc -p /sbin/ldconfig
%postun -n nvidia-driver-nvenc -p /sbin/ldconfig

%post -n nvidia-driver-nvfbcopengl -p /sbin/ldconfig
%postun -n nvidia-driver-nvfbcopengl -p /sbin/ldconfig

%post -n nvidia-driver-vdpau -p /sbin/ldconfig
%postun -n nvidia-driver-vdpau -p /sbin/ldconfig

%post -n nvidia-driver-opencl -p /sbin/ldconfig
%postun -n nvidia-driver-opencl -p /sbin/ldconfig

%post -n nvidia-driver-cfg -p /sbin/ldconfig
%postun -n nvidia-driver-cfg -p /sbin/ldconfig

%post -n nvidia-driver-xorg -p /sbin/ldconfig
%postun -n nvidia-driver-xorg -p /sbin/ldconfig


%changelog
* Thu Oct 20 2016 Jajauma's Packages <jajauma@yandex.ru> - 367.57-1
- Update to latest upstream version

* Fri Oct 07 2016 Jajauma's Packages <jajauma@yandex.ru> - 367.44-1
- Public release
