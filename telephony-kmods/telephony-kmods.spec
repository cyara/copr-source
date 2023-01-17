# Define the kmod package name here.
%define kmod_name		dahdi-linux

%define dahdi_version           3.2.0
%define wanpipe_version         7.0.34

# If kmod_kernel_version isn't defined on the rpmbuild line, define it here.
%if 0%{?el8}
%{!?kmod_kernel_version: %define kmod_kernel_version 4.18.0-425.10.1.el8_7}
%endif

%if 0%{?el9}
%{!?kmod_kernel_version: %define kmod_kernel_version 5.14.0-70.13.1.el9_0} 
%endif

Name:		telephony-kmods
Version:	1.0
Release:	9%{?dist}
Summary:	Telephony kernel modules
License:	GPLv2
URL:		http://www.kernel.org/

# Sources
Source0:	dahdi-linux-complete-%{dahdi_version}+%{dahdi_version}.tar.gz
Source1:	ftp://ftp.sangoma.com/wanpipe-%{wanpipe_version}.tgz
Patch1:		wanpipe-7.0.34-state.patch

ExclusiveArch:	x86_64

# Source code patches

%define findpat %( echo "%""P" )
%define __find_requires /usr/lib/rpm/redhat/find-requires.ksyms
%define __find_provides /usr/lib/rpm/redhat/find-provides.ksyms
%define dup_state_dir %{_localstatedir}/lib/rpm-state/kmod-dups
%define kver_state_dir %{dup_state_dir}/kver
%define kver_state_file %{kver_state_dir}/%{kmod_kernel_version}.%{_arch}
%define debug_package %{nil}

%global _use_internal_dependency_generator 0
%global kernel_source() %{_usrsrc}/kernels/%{kmod_kernel_version}.%{_arch}

BuildRequires:	elfutils-libelf-devel
BuildRequires:	kernel-devel = %{kmod_kernel_version}
BuildRequires:  kernel-modules = %{kmod_kernel_version}
BuildRequires:	kernel-abi-stablelists
BuildRequires:	kernel-rpm-macros
BuildRequires:	redhat-rpm-config
Requires:	kmod-dahdi == %{dahdi_version}
Requires:	kmod-wanpipe == %{wanpipe_version}

%description
This package provides the dahdi and wanpipe kernel module(s).  Due to wanpipe's
unique design, they have to be built together


%package -n kmod-dahdi
Version:        %{dahdi_version}
Summary:        DAHDI telephony interface kernel modules

Provides:	kernel-modules >= %{kmod_kernel_version}.%{_arch}
Provides:	kmod-dahdi = %{?epoch:%{epoch}:}%{dahdi_version}-%{release}

Requires(post):	%{_sbindir}/weak-modules
Requires(postun):	%{_sbindir}/weak-modules
Requires:	kernel >= %{kmod_kernel_version}
Requires:	kernel-firmware

%description -n kmod-dahdi
This package provides the dahdi kernel module(s).
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.


%package -n kmod-wanpipe
Version:        %{wanpipe_version}
Summary:        Sangoma WANPIPE package for Linux. This contains the kernel modules for Linux.

Provides:       kernel-modules >= %{kmod_kernel_version}.%{_arch}
Provides:       kmod-wanpipe = %{?epoch:%{epoch}:}%{wanpipe_version}-%{release}

Requires(post): %{_sbindir}/weak-modules
Requires(postun):       %{_sbindir}/weak-modules
Requires:       kernel >= %{kmod_kernel_version}
Requires:	kernel-firmware

%description -n kmod-wanpipe
Linux Drivers for Sangoma AFT Series of cards and S Series of Cards.

This package contains kernel modules for Linux.
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.


%prep
%setup -c -a 1
%patch1 -p1

echo "override dahdi * weak-updates/dahdi" > dahdi-linux-complete-%{dahdi_version}+%{dahdi_version}/linux/kmod-dahdi.conf
echo "override wanpipe * weak-updates/wanpipe" > wanpipe-%{wanpipe_version}/kmod-wanpipe.conf

%build
cd dahdi-linux-complete-%{dahdi_version}+%{dahdi_version}/linux
KVERS=%{kmod_kernel_version}.%{_arch} %{__make} modules

whitelist="/lib/modules/kabi-current/kabi_stablelist_%{_target_cpu}"
for modules in $( find . -name "*.ko" -type f -printf "%{findpat}\n" | sed 's|\.ko$||' | sort -u ) ; do
	# update greylist
	nm -u ./$modules.ko | sed 's/.*U //' |  sed 's/^\.//' | sort -u | while read -r symbol; do
		grep -q "^\s*$symbol\$" $whitelist || echo "$symbol" >> ./greylist
	done
done
sort -u greylist | uniq > greylist.txt

export DAHDI_DIR="$(pwd)"
cd ../../wanpipe-%{wanpipe_version}
KVER=%{kmod_kernel_version}.%{_arch} %{__make} DAHDI_DIR=$DAHDI_DIR all_kmod_dahdi

whitelist="/lib/modules/kabi-current/kabi_whitelist_%{_target_cpu}"
for modules in $( find . -name "*.ko" -type f -printf "%{findpat}\n" | sed 's|\.ko$||' | sort -u ) ; do
        # update greylist
        nm -u ./$modules.ko | sed 's/.*U //' |  sed 's/^\.//' | sort -u | while read -r symbol; do
                grep -q "^\s*$symbol\$" $whitelist || echo "$symbol" >> ./greylist
        done
done
sort -u greylist | uniq > greylist.txt


%install
cd dahdi-linux-complete-%{dahdi_version}+%{dahdi_version}/linux
KVERS=%{kmod_kernel_version}.%{_arch} DESTDIR=%{buildroot} %{__make} install-modules install-firmware install-xpp-firm

mkdir -p %{buildroot}%{_defaultdocdir}/kmod-dahdi-%{dahdi_version}
%{__install} -m 0644 greylist.txt %{buildroot}%{_defaultdocdir}/kmod-dahdi-%{dahdi_version}/
mkdir -p %{buildroot}%{_sysconfdir}/depmod.d
%{__install} -m 0644 kmod-dahdi.conf %{buildroot}%{_sysconfdir}/depmod.d

cd ../../wanpipe-%{wanpipe_version}
KVER=%{kmod_kernel_version}.%{_arch} DESTDIR=%{buildroot} %{__make} install_kmod
mkdir -p %{buildroot}/lib/modules/%{kmod_kernel_version}.%{_arch}/wanpipe
find %{buildroot}/lib/modules/%{kmod_kernel_version}.%{_arch}/kernel -iname '*.ko' -exec sh -c 'mv "{}" "%{buildroot}/lib/modules/%{kmod_kernel_version}.%{_arch}/wanpipe/$(basename {})"' ';'
rm -rf %{buildroot}/lib/modules/%{kmod_kernel_version}.%{_arch}/kernel
mkdir -p %{buildroot}%{_defaultdocdir}/kmod-wanpipe-%{wanpipe_version}
%{__install} -m 0644 greylist.txt %{buildroot}%{_defaultdocdir}/kmod-wanpipe-%{wanpipe_version}/
%{__install} -m 0644 kmod-wanpipe.conf %{buildroot}%{_sysconfdir}/depmod.d

# strip the modules(s)
find %{buildroot} -type f -name \*.ko -exec %{__strip} --strip-debug \{\} \;

# remove generated crap
rm -f %{buildroot}/lib/modules/%{kmod_kernel_version}.%{_arch}/modules.*

# Move firmware to /usr/lib
mkdir -p %{buildroot}/usr/lib
mv %{buildroot}/lib/firmware %{buildroot}/usr/lib/


%post -n kmod-dahdi
modules=( $(find /lib/modules/%{kmod_kernel_version}.%{_arch}/dahdi | grep '\.ko$') )
printf '%s\n' "${modules[@]}" | %{_sbindir}/weak-modules --add-modules --no-initramfs

mkdir -p "%{kver_state_dir}"
touch "%{kver_state_file}"

exit 0


%post -n kmod-wanpipe
modules=( $(find /lib/modules/%{kmod_kernel_version}.%{_arch}/wanpipe | grep '\.ko$') )
printf '%s\n' "${modules[@]}" | %{_sbindir}/weak-modules --add-modules --no-initramfs

mkdir -p "%{kver_state_dir}"
touch "%{kver_state_file}"

exit 0


%preun -n kmod-dahdi
if rpm -q --filetriggers kmod 2> /dev/null| grep -q "Trigger for weak-modules call on kmod removal"; then
	mkdir -p "%{kver_state_dir}"
	touch "%{kver_state_file}"
fi

mkdir -p "%{dup_state_dir}"
rpm -ql kmod-dahdi-%{dahdi_version}-%{release}.%{_arch} | grep '\.ko$' > "%{dup_state_dir}/rpm-kmod-dahdi-modules"


%preun -n kmod-wanpipe
if rpm -q --filetriggers kmod 2> /dev/null| grep -q "Trigger for weak-modules call on kmod removal"; then
        mkdir -p "%{kver_state_dir}"
        touch "%{kver_state_file}"
fi

mkdir -p "%{dup_state_dir}"
rpm -ql kmod-wanpipe-%{wanpipe_version}-%{release}.%{_arch} | grep '\.ko$' > "%{dup_state_dir}/rpm-kmod-wanpipe-modules"


%postun -n kmod-dahdi
modules=( $(cat "%{dup_state_dir}/rpm-kmod-dahdi-modules") )
rm -f "%{dup_state_dir}/rpm-kmod-dahdi-modules"
printf '%s\n' "${modules[@]}" | %{_sbindir}/weak-modules --remove-modules --no-initramfs

rmdir "%{dup_state_dir}" 2> /dev/null

exit 0


%postun -n kmod-wanpipe
modules=( $(cat "%{dup_state_dir}/rpm-kmod-wanpipe-modules") )
rm -f "%{dup_state_dir}/rpm-kmod-wanpipe-modules"
printf '%s\n' "${modules[@]}" | %{_sbindir}/weak-modules --remove-modules --no-initramfs

rmdir "%{dup_state_dir}" 2> /dev/null

exit 0


%files -n kmod-dahdi
%defattr(644,root,root,755)
/lib/modules/%{kmod_kernel_version}.%{_arch}/dahdi
%{_prefix}/lib/firmware/*
%{_prefix}/lib/firmware/.dahdi*
%{_datadir}/dahdi
%config /etc/depmod.d/kmod-dahdi.conf
%doc /usr/share/doc/kmod-dahdi-%{dahdi_version}/


%files -n kmod-wanpipe
%defattr(644,root,root,755)
/lib/modules/%{kmod_kernel_version}.%{_arch}/wanpipe
%config /etc/depmod.d/kmod-wanpipe.conf
%doc /usr/share/doc/kmod-wanpipe-%{wanpipe_version}/


%changelog
* Wed Jan 18 2023 Patrick Coakley <patrick.coakley@spearline.com> - 1.0-9
- Upgraded Kernel version to 4.18.0-425.10.1.el8_7 for SpearlineOS 8.7.4

* Tue Oct 25 2022 Patrick Coakley <patrick.coakley@spearline.com> - 1.0-8
- Rebuild for AlmaLinux 9
- Upgrade dahdi-linux to 3.2.0  

* Fri May 13 2022 Jonathan Dieter <jonathan.dieter@spearline.com> - 1.0-7
- Rebuild for AlmaLinux 8.6

* Tue Nov 16 2021 Jonathan Dieter <jonathan.dieter@spearline.com> - 1.0-6
- Rebuild for AlmaLinux 8.5
- Upgrade wanpipe to 7.0.34

* Wed Jun 30 2021 Jonathan Dieter <jonathan.dieter@spearline.com> - 1.0-5
- Move DAHDI firmware into kmod package

* Tue Jun 08 2021 Jonathan Dieter <jonathan.dieter@spearline.com> - 1.0-4
- Rebuild for AlmaLinux 8.4

* Mon Feb 22 2021 Jonathan Dieter <jonathan.dieter@spearline.com> - 1.0-3
- Remove dependencies on user-space packages since we're moving these kmods into OSTree host

* Fri Dec 11 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 1.0-2
- Rebuild for CentOS 8.3

* Fri Aug 28 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 1.0-1
- Initial build
