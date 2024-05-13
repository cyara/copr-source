Summary: Sangoma WANPIPE package for Linux. This contains configuration/startup/debugging utilities for Linux.
Name: wanpipe
Version: 7.0.38
Release: 1%{?dist}
License: GPL
Url: www.sangoma.com
Source0: https://ftp.sangoma.com/linux/current_wanpipe/%{name}-%{version}.tgz


Requires: coreutils
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: make
BuildRequires: cmake
BuildRequires: libxml2-devel
BuildRequires: ncurses
BuildRequires: ncurses-devel
BuildRequires: bison
BuildRequires: bison-devel
BuildRequires: openr2-devel
BuildRequires: flex
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: patch
BuildRequires: perl
BuildRequires: wget
BuildRequires: dahdi-linux-devel
BuildRequires: libpri-devel

# Doesn't work for el9 
# On el8 it simply builds ncurses-devel so i think 
# libtermcap-devel is redundant 
# BuildRequires: libtermcap-devel

# Don't work for el9
%if 0%{?el8}
# flex-devel - Not included in RHEL9 CodeReady Repo 
# https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/package_manifest/repositories#CRB-modules
BuildRequires: flex-devel
%endif


%description
Linux Drivers for Sangoma AFT Series of cards and S Series of Cards.

This package contains configuration/startup/debugging utilities for Linux.


%package devel
Summary: Development libraries for wanpipe
Requires: wanpipe == %{version}-%{release}


%description devel
Linux Drivers for Sangoma AFT Series of cards and S Series of Cards.

This package contains the development libraries


%prep
%autosetup -p1
if [ "%{_libdir}" != "/usr/lib" ]; then
    sed -i 's@configure --prefix=$(LIBPREFIX)@configure --prefix=$(LIBPREFIX) --libdir=%{_libdir}@g' Makefile
    find ./ -iname Makefile -exec sed -i 's@/.lib/usr/lib@/.lib/usr/lib64@g' '{}' ';'
fi

%build
%{__make} all_util all_lib


%install
export QA_SKIP_BUILD_ROOT='true'

make INSTALLPREFIX=%{buildroot} LIBPREFIX=%{_libdir} install_etc install_util install_lib
install -m 0755 samples/wanrouter %{buildroot}%{_sbindir}/wanrouter
mkdir -p %{buildroot}%{_sysconfdir}/wanpipe
install -m 0644 samples/wanrouter.rc %{buildroot}%{_sysconfdir}/wanpipe/wanrouter.rc
mv %{buildroot}/usr/local/sbin/setup-sangoma %{buildroot}/usr/sbin/setup-sangoma
rm -rf %{buildroot}%{_libdir}/*.a %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}/var/tmp

# Clean up /etc
rm -rf %{buildroot}/etc/wanpipe/api
rm -rf %{buildroot}/etc/wanpipe/samples


%post
#update ldconfig
ldconfig


%files
%dir %{_sysconfdir}/wanpipe/
%config %{_sysconfdir}/wanpipe/lib
%config %{_sysconfdir}/wanpipe/util
%config %{_sysconfdir}/wanpipe/wancfg_zaptel
%config(noreplace) %{_sysconfdir}/wanpipe/wanrouter.rc
%{_libdir}/libsangoma.so.3*
%{_libdir}/libstelephony.so.1*
%{_sbindir}/setup-sangoma
%{_sbindir}/wan_aftup
%{_sbindir}/wan_ec_client
%{_sbindir}/wan_plxup
%{_sbindir}/wancfg
%{_sbindir}/wancfg_dahdi
%{_sbindir}/wancfg_data_api
%{_sbindir}/wancfg_fs
%{_sbindir}/wancfg_fs_legacy
%{_sbindir}/wancfg_ftdm
%{_sbindir}/wancfg_hp_tdmapi
%{_sbindir}/wancfg_legacy
%{_sbindir}/wancfg_openzap
%{_sbindir}/wancfg_smg
%{_sbindir}/wancfg_tdmapi
%{_sbindir}/wancfg_zaptel
%{_sbindir}/wanconfig
%{_sbindir}/wanpipe_lxdialog
%{_sbindir}/wanpipemon
%{_sbindir}/wanpipemon_legacy
%{_sbindir}/wanrouter
%{_sbindir}/wp_pppconfig
%{_sbindir}/wpbwm
%{_sysconfdir}/wanpipe/firmware
%{_sysconfdir}/wanpipe/wan_ec
%{_sysconfdir}/wanpipe/scripts


%files devel
%{_includedir}/libhpsangoma.h
%{_includedir}/libsangoma.h
%{_includedir}/libstelephony.h
%{_includedir}/wanec_api.h
%{_libdir}/libsangoma.so
%{_libdir}/libstelephony.so


%changelog
* Tue May 14 2024 Patrick Coakley <patrick.coakley@cyara.com> - 7.0.38-1
- Upgraded wanpipe to 7.0.38

* Fri Nov 24 2023 Jonathan Dieter <jonathan.dieter@cyara.com> - 7.0.36-2
- Disable utility and kernel version mismatch check

* Thu Nov 23 2023 Patrick Coakley <patrick.coackley@cyara.com> - 7.0.36-1
- Update to 7.0.36

* Mon Jan 23 2023 Patrick Coakley <patrick.coackley@cyara.com> - 7.0.34-1
- Update to 7.0.34

* Tue Jun 08 2021 Jonathan Dieter <jonathan.dieter@spearline.com> - 7.0.32-1
- Update to 7.0.32

* Wed Sep 02 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 7.0.27-2
- Add missing firmware and scripts

* Fri Aug 28 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 7.0.27-1
- Update to 7.0.27
- Add patch to build with latest CentOS 8 kernel
