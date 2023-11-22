%global distro  CyaraOS
# Previous release names:
# Coronea
# Poundlick
# Derrygool
# Russagh
# Gortnaclohy
# Tooreennasillane
# Lahernathee
%global release_name Mallavonea
%global major   9
%global minor   3
%global dist .el%{major}

Name:           cyaraos-release
Version:        %{major}.%{minor}
Release:        1%{?dist}
Summary:        %{distro} release files
License:        GPLv2
BuildArch:      noarch

Provides:       centos-release = %{version}-%{release}

# Required for a lorax run (to generate install media)
Provides:       centos-release-eula
Provides:       redhat-release-eula
Provides:       cyaraos-release = %{version}-%{release}

# required by epel-release
Provides:       redhat-release = %{version}-%{release}

# required by dnf
# https://github.com/rpm-software-management/dnf/blob/4.2.23/dnf/const.py.in#L26
Provides:       system-release = %{version}-%{release}
Provides:       system-release(releasever) = %{major}

# required by libdnf
# https://github.com/rpm-software-management/libdnf/blob/0.48.0/libdnf/module/ModulePackage.cpp#L472
Provides:       base-module(platform:el%{major})

Source200:      EULA
Source201:      LICENSE

Source300:      85-display-manager.preset
Source301:      90-default.preset
Source302:      90-default-user.preset
Source303:      99-default-disable.preset
Source304:      50-redhat.conf

Source400:      alsecureboot001.cer
# kernel signing certificate
Source401:      alsecureboot001.cer
# grub2 signing certificate
Source402:      alsecureboot001.cer
# Fwupd signing certificate
Source403:      alsecureboot001.cer
# UKI signing certificate
Source404:      alsecureboot001.cer

Source500:      almalinux-appstream.repo
Source501:      almalinux-baseos.repo
Source502:      almalinux-crb.repo
Source503:      almalinux-extras.repo
Source504:      almalinux-highavailability.repo
Source505:      almalinux-resilientstorage.repo
Source506:      almalinux-sap.repo
Source507:      almalinux-saphana.repo
Source508:      almalinux-plus.repo
# Only for x86_64
Source510:      almalinux-nfv.repo
Source511:      almalinux-rt.repo

Source600:      RPM-GPG-KEY-AlmaLinux-9

%package -n almalinux-sb-certs
Summary: %{distro} public secureboot certificates
Group: System Environment/Base
Provides: system-sb-certs = %{version}-%{release}
Provides: redhat-sb-certs = %{version}-%{release}

%package -n almalinux-repos
Summary:        %{distro} package repositories
Requires:       almalinux-release = %{version}-%{release}
Requires:       almalinux-gpg-keys = %{version}-%{release}

%package -n almalinux-gpg-keys
Summary:        %{distro} RPM keys


%description
%{distro} release files.

%description -n almalinux-sb-certs
%{distro} secureboot certificates

%description -n almalinux-repos
This package provides the package repository files for %{distro}.

%description -n almalinux-gpg-keys
This package provides the RPM signature keys for %{distro}.


%install
# copy license and contributors doc here for %%license and %%doc macros
mkdir -p ./docs
cp %{SOURCE201} ./docs

# create /etc/system-release and /etc/redhat-release
install -d -m 0755 %{buildroot}%{_sysconfdir}
echo "%{distro} release %{major}.%{minor}% (%{release_name})" > %{buildroot}%{_sysconfdir}/cyaraos-release
ln -s cyaraos-release %{buildroot}%{_sysconfdir}/system-release
ln -s cyaraos-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s cyaraos-release %{buildroot}%{_sysconfdir}/almalinux-release

# Create the os-release file
install -d -m 0755 %{buildroot}%{_prefix}/lib
cat > %{buildroot}%{_prefix}/lib/os-release << EOF
NAME="%{distro}"
VERSION="%{major}.%{minor} (%{release_name})"
ID="cyaraos"
ID_LIKE="rhel centos fedora"
VERSION_ID="%{major}.%{minor}"
PLATFORM_ID="platform:el%{major}"
PRETTY_NAME="%{distro} %{major}.%{minor}%{?beta: %{beta}} (%{release_name})"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:cyaraos:cyaraos:%{major}.%{minor}%{?tuned_profile}"
HOME_URL="https://www.cyara.com/"
BUG_REPORT_URL=""
EOF

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# write cpe to /etc/system/release-cpe
echo "cpe:/o:cyaraos:cyaraos:%{major}::baseos" > %{buildroot}%{_sysconfdir}/system-release-cpe

# create /etc/issue, /etc/issue.net and /etc/issue.d
echo '\S' > %{buildroot}%{_sysconfdir}/issue
echo 'Kernel \r on an \m' >> %{buildroot}%{_sysconfdir}/issue
cp %{buildroot}%{_sysconfdir}/issue{,.net}
echo >> %{buildroot}%{_sysconfdir}/issue
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

# set up the dist tag macros
mkdir -p %{buildroot}%{_rpmmacrodir}
cat > %{buildroot}%{_rpmmacrodir}/macros.dist << EOF
# dist macros.

%%__bootstrap ~bootstrap
%%almalinux_ver %{major}
%%almalinux %{major}
%%centos_ver %{major}
%%centos %{major}
%%rhel %{major}
%%dist %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}.el%{major}%%{?with_bootstrap:%{__bootstrap}}
%%el%{major} 1
%%dist_vendor         %{dist_vendor}
%%dist_name           %{dist_name}
%%dist_home_url       %{dist_home_url}
%%dist_bug_report_url %{dist_bug_report_url}
EOF

# use unbranded datadir
install -d -m 0755 %{buildroot}%{_datadir}/almalinux-release
ln -s almalinux-release %{buildroot}%{_datadir}/redhat-release
install -p -m 0644 %{SOURCE200} %{buildroot}%{_datadir}/almalinux-release/

# copy systemd presets
install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/user-preset
install -p -m 0644 %{SOURCE300} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -p -m 0644 %{SOURCE301} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -p -m 0644 %{SOURCE302} %{buildroot}%{_prefix}/lib/systemd/user-preset/

# installing the same file for both system and user presets to set the same behavior for both
install -p -m 0644 %{SOURCE303} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -p -m 0644 %{SOURCE303} %{buildroot}%{_prefix}/lib/systemd/user-preset/

# copy sysctl presets
mkdir -p %{buildroot}/%{_prefix}/lib/sysctl.d/
install -m 0644 %{SOURCE304} %{buildroot}/%{_prefix}/lib/sysctl.d/

# Create stub yum repos
mkdir %{buildroot}%{_sysconfdir}/yum.repos.d
touch %{buildroot}%{_sysconfdir}/yum.repos.d/redhat.repo

# Copy secureboot certificates
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/sb-certs/
install -d -m 0755 %{buildroot}%{_datadir}/pki/sb-certs/

# Install aarch64 certs
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-aarch64.cer
install -m 644 %{SOURCE401} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-aarch64.cer
install -m 644 %{SOURCE402} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-aarch64.cer
install -m 644 %{SOURCE403} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-aarch64.cer
install -m 644 %{SOURCE404} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-aarch64.cer

# Install x86_64 certs
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-x86_64.cer
install -m 644 %{SOURCE401} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-x86_64.cer
install -m 644 %{SOURCE402} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-x86_64.cer
install -m 644 %{SOURCE403} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-x86_64.cer
install -m 644 %{SOURCE404} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-x86_64.cer

# Install ppc64le certs
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-ppc64le.cer
install -m 644 %{SOURCE401} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-ppc64le.cer
install -m 644 %{SOURCE402} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-ppc64le.cer
install -m 644 %{SOURCE404} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-ppc64le.cer

# Install s390x certs
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-s390x.cer
install -m 644 %{SOURCE401} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-s390x.cer
install -m 644 %{SOURCE404} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-s390x.cer

	# Link x86_64 certs
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-grub2-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-fwupd-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-uki-virt-x86_64.cer

# Link aarch64 certs
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-grub2-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-fwupd-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-uki-virt-aarch64.cer

# Link ppc64le certs
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-ppc64le.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-ppc64le.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-ppc64le.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-grub2-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-ppc64le.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-uki-virt-ppc64le.cer

# Link s390x certs
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-s390x.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-s390x.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-s390x.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-s390x.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-s390x.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-uki-virt-s390x.cer

# copy yum repos
install -d -m 0755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -p -m 0644 %{SOURCE500} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE501} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE502} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE503} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE504} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE505} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE506} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE507} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE508} %{buildroot}%{_sysconfdir}/yum.repos.d/
# RT and NFV are only for x86_64
%ifarch x86_64
install -p -m 0644 %{SOURCE510} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE511} %{buildroot}%{_sysconfdir}/yum.repos.d/
%endif

# dnf variables
install -d -m 0755 %{buildroot}%{_sysconfdir}/dnf/vars
echo "%{major}-stream" > %{buildroot}%{_sysconfdir}/dnf/vars/stream

# copy GPG keys
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -p -m 0644 %{SOURCE600} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/


%files
%license docs/LICENSE
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/almalinux-release
%{_sysconfdir}/cyaraos-release
%config(noreplace) %{_sysconfdir}/os-release
%config %{_sysconfdir}/system-release-cpe
%config(noreplace) %{_sysconfdir}/issue
%config(noreplace) %{_sysconfdir}/issue.net
%dir %{_sysconfdir}/issue.d
%dir %{_sysconfdir}/yum.repos.d
%ghost %{_sysconfdir}/yum.repos.d/redhat.repo
%{_rpmmacrodir}/macros.dist
%{_datadir}/redhat-release
%{_datadir}/almalinux-release
%{_prefix}/lib/os-release
%{_prefix}/lib/systemd/system-preset/*
%{_prefix}/lib/systemd/user-preset/*
%{_prefix}/lib/sysctl.d/50-redhat.conf

%files -n almalinux-sb-certs
# Note to future packagers:
# resetting the symlinks in /etc/pki/sb-certs on upgrade is the intended behavior here
%dir %{_sysconfdir}/pki/sb-certs
%dir %{_datadir}/pki/sb-certs/
%{_sysconfdir}/pki/sb-certs/*.cer
%{_datadir}/pki/sb-certs/*.cer

%files -n almalinux-repos
%config(noreplace) %{_sysconfdir}/yum.repos.d/almalinux-appstream.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/almalinux-baseos.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/almalinux-crb.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/almalinux-extras.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/almalinux-highavailability.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/almalinux-resilientstorage.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/almalinux-sap.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/almalinux-saphana.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/almalinux-plus.repo
%ifarch x86_64
%config(noreplace) %{_sysconfdir}/yum.repos.d/almalinux-nfv.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/almalinux-rt.repo
%endif
%config(noreplace) %{_sysconfdir}/dnf/vars/stream

%files -n almalinux-gpg-keys
%{_sysconfdir}/pki/rpm-gpg


%changelog
* Fri Nov 24 2023 Patrick Coakley <patrick.coakley@cyara.com> - 9.3-1
- CyaraOS 9.3

* Mon June 12 2023 Patrick Coakley <patrick.coakley@cyara.com> - 9.2-2
- CyaraOS 9.2

* Tue May 02 2023 Andrew Lukoshko <alukoshko@almalinux.org> - 9.2-1
- 9.2 stable

* Mon May 01 2023 Patrick Coakley <patrick.coakley@spearline.com> - 9.1-1
- Changing SpearlineOS 9.1 to CyaraOS 9.1

* Tue Dec 20 2022 Patrick Coakley <patrick.coakley@spearline.com> - 9.1-1
- Creating fork for SpearlineOS 9.1

* Tue Nov 16 2021 Jonathan Dieter <jonathan.dieter@spearline.com> - 8.5-1
- Fork for SpearlineOS

* Fri Nov 12 2021 Andrew Lukoshko <alukoshko@almalinux.org> - 8.5-3
- Fix ResilientStorage repo

* Tue Nov 09 2021 Andrew Lukoshko <alukoshko@almalinux.org> - 8.5-2
- 8.5 stable release
- Add ResilientStorage repo
- Add Plus repo

* Thu Oct 07 2021 Andrew Lukoshko <alukoshko@almalinux.org> - 8.5-1
- 8.5 beta release

* Thu Jul 29 2021 Andrew Lukoshko <alukoshko@almalinux.org> - 8.4-3
- disable fastestmirror dnf plugin for all repos

* Thu May 20 2021 Andrew Lukoshko <alukoshko@almalinux.org> - 8.4-2
- 8.4 stable release
- Disable PowerTools repo by default and move it to separate file

* Fri Apr 16 2021 Andrew Lukoshko <alukoshko@almalinux.org> - 8.4-1
- 8.4 beta release

* Wed Mar 24 2021 Andrei Lukoshko <alukoshko@almalinux.org> - 8.3-4
- 8.3 stable release

* Wed Feb 10 2021 Andrei Lukoshko <alukoshko@cloudlinux.com> - 8.3-3
- Switch repos to mirrorlists and enable fastestmirror plugin
- Use full release version for ALMALINUX_MANTISBT_PROJECT_VERSION
- Add HighAvailability repo

* Wed Jan 27 2021 Anatholy Scryabin <ascryabin@cloudlinux.com> - 8.3-2
- Initial build for AlmaLinux
