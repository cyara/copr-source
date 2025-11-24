Summary:            SIP Messages flow viewer
Name:               sngrep
Version:            1.8.2
Release:            2%{?dist}
License:            GPLv3
Group:              Applications/Engineering
BuildRoot: 	        %{_tmppath}/%{name}-%{version}-%{release}-root
Source:             %{name}-%{version}.tar.gz
URL:                http://github.com/irontec/sngrep
BuildRequires: ncurses-devel
BuildRequires: make
BuildRequires: libpcap-devel
BuildRequires: pcre-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: openssl-devel
Requires: ncurses
Requires: libpcap
Requires: pcre

%description
sngrep displays SIP Messages grouped by Call-Id into flow
diagrams. It can be used as an offline PCAP viewer or online
capture using libpcap functions.

It supports SIP UDP, TCP and TLS transports (when each message is
delivered in one packet).

You can also create new PCAP files from captures or displayed dialogs.

%prep
%setup -q

%build
./bootstrap.sh
./configure --with-openssl --with-pcre --enable-unicode --enable-ipv6 --enable-eep --prefix=/usr --sysconfdir=/etc/ --mandir=/usr/share/man
make %{?_smp_mflags}

%install
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%files
%doc README TODO COPYING ChangeLog
%{_bindir}/*
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/*

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%changelog
* Wed Jul 23 2025 Patrick Coakley <patrick.coakley@cyara.com> - 1.8.2-2
- Bump to 1.8.2 and add openssl support

* Tue Sep 06 2022 Jonathan Dieter <jonathan.dieter@spearline.com> - 1.6.0-1
- Bump to 1.6.0

* Tue Feb 18 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 1.4.6-1
- Bump to 1.4.6
- Rebuild for EL8

* Tue Aug 23 2016 Ivan Alonso <kaian@irontec.com> - 1.4.0
- Version 1.4.0

* Tue Mar 15 2016 Ivan Alonso <kaian@irontec.com> - 1.3.0
- Version 1.3.0

* Thu Dec 10 2015 Ivan Alonso <kaian@irontec.com> - 1.2.0
- Version 1.2.0

* Wed Oct 28 2015 Ivan Alonso <kaian@irontec.com> - 1.1.0
- Version 1.1.0

* Tue Oct 06 2015 Ivan Alonso <kaian@irontec.com> - 1.0.0
- Version 1.0.0

* Mon Aug 31 2015 Ivan Alonso <kaian@irontec.com> - 0.4.2
- Version 0.4.2

* Tue Jul 07 2015 Ivan Alonso <kaian@irontec.com> - 0.4.1
- Version 0.4.1

* Mon Jun 29 2015 Ivan Alonso <kaian@irontec.com> - 0.4.0
- Version 0.4.0

* Tue Apr 14 2015 Ivan Alonso <kaian@irontec.com> - 0.3.1
- Version 0.3.1

* Wed Mar 04 2015 Ivan Alonso <kaian@irontec.com> - 0.3.0
- First RPM version of sngrep
