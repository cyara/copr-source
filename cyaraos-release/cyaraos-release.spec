%define debug_package %{nil}
%define product_family CyaraOS
%define variant_titlecase Server
%define variant_lowercase server
# Previous release names:
# Coronea
# Poundlick
# Derrygool
# Russagh
# Carrigfadda
# Gortnaclohy
# Tooreennasillane
#Derreendangan
%define release_name Coolnagarrane
%define contentdir almalinux
%define infra_var stock
%define base_release_version 8
%define full_release_version 8.10
%define dist_release_version 8
%define upstream_rel_long 8.10-0.2
%define upstream_rel 8.10
%define cyaraos_rel 1
%define dist .el%{dist_release_version}
%global eol_date 2029-06-01

# The anaconda scripts in %%{_libexecdir} can create false requirements
%global __requires_exclude_from %{_libexecdir}

Name:           cyaraos-release
Version:        %{upstream_rel}
Release:        %{cyaraos_rel}%{?dist}
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
BuildArch:      noarch
Provides:       cyaraos-release = %{version}-%{release}
Provides:       almalinux-release = %{version}-%{release}
Provides:       centos-release = %{version}-%{release}
Provides:       cyaraos-release(upstream) = %{upstream_rel}
Provides:       almalinux-release(upstream) = %{upstream_rel}
Provides:       centos-release(upstream) = %{upstream_rel}
Provides:       redhat-release = %{upstream_rel_long}
Provides:       system-release = %{upstream_rel_long}
Provides:       system-release(releasever) = %{base_release_version}
Provides:       base-module(platform:el%{base_release_version})

Provides:       almalinux-release-eula
Provides:       centos-release-eula
Provides:       redhat-release-eula

Source1:        85-display-manager.preset
Source2:        90-default.preset
Source3:        99-default-disable.preset
Source10:       RPM-GPG-KEY-AlmaLinux

##Source100:      rootfs-expand

Source200:      EULA
Source201:      GPL
##Source202:      Contributors

Source300:      almalinux.repo
Source301:      almalinux-ha.repo
Source302:      almalinux-powertools.repo
Source303:      almalinux-resilientstorage.repo
Source304:      almalinux-plus.repo
Source305:      almalinux-sap.repo
Source306:      almalinux-saphana.repo

# Only for x86_64
Source310:      almalinux-rt.repo
Source311:      almalinux-nfv.repo

%description
%{product_family} release files

%prep
echo OK

%build
echo OK

%install
rm -rf %{buildroot}

# create skeleton
mkdir -p %{buildroot}/etc
mkdir -p %{buildroot}%{_prefix}/lib

# create /etc/system-release and /etc/redhat-release
echo "%{product_family} release %{full_release_version} (%{release_name}) " > %{buildroot}/etc/cyaraos-release
echo "Derived from AlmaLinux which is derived from Red Hat Enterprise Linux %{upstream_rel} (Source)" > %{buildroot}/etc/cyaraos-release-upstream
ln -s cyaraos-release %{buildroot}/etc/almalinux-release
ln -s cyaraos-release %{buildroot}/etc/system-release
ln -s cyaraos-release %{buildroot}/etc/redhat-release
ln -s cyaraos-release %{buildroot}/etc/centos-release

# Create the os-release file
cat << EOF >>%{buildroot}%{_prefix}/lib/os-release
NAME="%{product_family}"
VERSION="%{full_release_version}"
ID="cyaraos"
ID_LIKE="rhel centos fedora"
VERSION_ID="%{full_release_version}"
PLATFORM_ID="platform:el%{base_release_version}"
PRETTY_NAME="%{product_family} %{full_release_version}%{?beta: %{beta}} (%{release_name})"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:cyaraos:cyaraos:%{full_release_version}%{?tuned_profile}"
HOME_URL="https://www.cyara.com/"
BUG_REPORT_URL=""
EOF

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# write cpe to /etc/system-release-cpe
echo "cpe:/o:cyaraos:cyaraos:%{full_release_version}" > %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
install -m 644 %{SOURCE10} %{buildroot}/etc/pki/rpm-gpg

# copy yum repos
mkdir -p -m 755 %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE300} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE301} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE302} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE303} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE304} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE305} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE306} %{buildroot}/etc/yum.repos.d

# RT and NFV are only for x86_64
%ifarch x86_64
install -m 644 %{SOURCE310} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE311} %{buildroot}/etc/yum.repos.d
%endif

mkdir -p -m 755 %{buildroot}/etc/dnf/vars
echo "%{infra_var}" > %{buildroot}/etc/dnf/vars/infra
echo "%{contentdir}" >%{buildroot}/etc/dnf/vars/contentdir
echo "%{base_release_version}-stream" > %{buildroot}/etc/dnf/vars/stream

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%almalinux_ver %{base_release_version}
%%almalinux %{base_release_version}
%%centos_ver %{base_release_version}
%%centos %{base_release_version}
%%rhel %{base_release_version}
%%dist .el%{base_release_version}
%%el%{base_release_version} 1
EOF

# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/almalinux-release
ln -s almalinux-release %{buildroot}/%{_datadir}/redhat-release
install -m 644 %{SOURCE200} %{buildroot}/%{_datadir}/almalinux-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/almalinux-release
ln -s almalinux-release %{buildroot}/%{_docdir}/redhat-release
install -m 644 %{SOURCE201} %{buildroot}/%{_docdir}/almalinux-release

# copy systemd presets
mkdir -p %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE3} %{buildroot}/%{_prefix}/lib/systemd/system-preset/


%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/redhat-release
/etc/system-release
/etc/centos-release
##/etc/centos-release-upstream
/etc/almalinux-release
/etc/cyaraos-release
/etc/cyaraos-release-upstream
/etc/dnf/vars/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-AlmaLinux
%config(noreplace) /etc/yum.repos.d/almalinux.repo
%config(noreplace) /etc/yum.repos.d/almalinux-ha.repo
%config(noreplace) /etc/yum.repos.d/almalinux-powertools.repo
%config(noreplace) /etc/yum.repos.d/almalinux-resilientstorage.repo
%config(noreplace) /etc/yum.repos.d/almalinux-plus.repo
%config(noreplace) /etc/yum.repos.d/almalinux-sap.repo
%config(noreplace) /etc/yum.repos.d/almalinux-saphana.repo
%ifarch x86_64
%config(noreplace) /etc/yum.repos.d/almalinux-rt.repo
%config(noreplace) /etc/yum.repos.d/almalinux-nfv.repo
%endif
%config(noreplace) /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
/etc/rpm/macros.dist
%{_docdir}/redhat-release
%{_docdir}/almalinux-release
%{_datadir}/redhat-release
%{_datadir}/almalinux-release
%{_prefix}/lib/os-release
%{_prefix}/lib/systemd/system-preset/*

%changelog
* Thu May 30 2024 Patrick Coakley <patrick.coakley@cyara.com> - 8.10-1
- Update to 8.10

* Fri Nov 24 2023 Patrick Coakley <patrick.coakley@cyara.com> - 8.9-1
- Update to 8.9

* Thu May 18 2023 Patrick Coakley <patrick.coakley@cyara.com> - 8.8-1
- Update to 8.8

* Wed Apr 05 2023 Jonathan Dieter <jonathan.dieter@cyara.com> - 8.7-2
- Rebadge to CyaraOS

* Mon Nov 21 2022 Jonathan Dieter <jonathan.dieter@spearline.com> - 8.7-1
- Update to 8.7

* Mon May 16 2022 Jonathan Dieter <jonathan.dieter@spearline.com> - 8.6-1
- Initial draft update to 8.6

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
