%global           pjsip_version   2.12.1

%global           optflags        %{optflags} -Werror-implicit-function-declaration -DLUA_COMPAT_MODULE
%ifarch s390 %{arm} aarch64 %{mips}
%global           ldflags         -Wl,--as-needed,--library-path=%{_libdir} %{__global_ldflags}
%else
%global           ldflags         -m%{__isa_bits} -Wl,--as-needed,--library-path=%{_libdir} %{__global_ldflags}
%endif

%global           astvarrundir     /var/run/asterisk
%global           tmpfilesd        1

%global           makeargs        DEBUG= OPTIMIZE= DESTDIR=%{buildroot} ASTVARRUNDIR=%{astvarrundir} ASTDATADIR=/var/lib/asterisk ASTVARLIBDIR=/var/lib/asterisk ASTDBDIR=%{_localstatedir}/spool/asterisk NOISY_BUILD=1

Summary:          The Open Source PBX
Name:             asterisk
Epoch:            2
Version:          20.9.3
Release:          1%{?dist}
License:          GPLv2
URL:              http://www.asterisk.org/

Source0:          http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-%{version}.tar.gz
Source1:          http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-%{version}.tar.gz.asc
Source2:          asterisk-logrotate
Source3:          menuselect.makedeps
Source4:          menuselect.makeopts
Source5:          asterisk.service
Source6:          asterisk-tmpfiles
# GPG keyring with Asterisk developer signatures
# Created by running:
#gpg2 --no-default-keyring --keyring ./asterisk-gpgkeys.gpg \
#--keyserver=hkp://pool.sks-keyservers.net --recv-keys \
#0x21A91EB1F012252993E9BF4A368AB332B59975F3 \
#0x80CEBC345EC9FF529B4B7B808438CBA18D0CAA72 \
#0xCDBEE4CC699E200EB4D46BB79E76E3A42341CE04 \
#0x639D932D5170532F8C200CCD9C59F000777DCC45 \
#0x551F29104B2106080C6C2851073B0C1FC9B2E352 \
#0x57E769BC37906C091E7F641F6CB44E557BD982D8 \
#0xF2FC93DB7587BD1FB49E045A5D984BE337191CE7
Source7:          asterisk-gpgkeys.gpg

# Now building Asterisk with bundled pjproject, because they apply custom patches to it
#Source8:          https://raw.githubusercontent.com/asterisk/third-party/master/pjproject/%{pjsip_version}/pjproject-%{pjsip_version}.tar.bz2
Source8:          https://github.com/asterisk/third-party/tree/master/pjproject/%{pjsip_version}/pjproject-%{pjsip_version}.tar.bz2

# Add asterisk-res_json
Source9:          https://github.com/felipem1210/asterisk-res_json/archive/asterisk-res_json-7081ef68a880eeb2b0a9c181d7fd72dd15ba7c65.tar.gz

# Asterisk now builds against a bundled copy of pjproject, as they apply some patches
# directly to pjproject before the build against it
Provides:         bundled(pjproject) = %{pjsip_version}

# Does not build on s390x: https://bugzilla.redhat.com/show_bug.cgi?id=1465162
#ExcludeArch:      s390x

BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    perl

# core build requirements
BuildRequires:    openssl-devel
BuildRequires:    newt-devel
BuildRequires:    ncurses-devel
BuildRequires:    libcap-devel
BuildRequires:    libsrtp-devel
BuildRequires:    perl-interpreter
BuildRequires:    perl-generators
BuildRequires:    popt-devel
BuildRequires:    systemd
BuildRequires:    xmlstarlet
BuildRequires:    kernel-headers
BuildRequires:    alsa-lib-devel
BuildRequires:    curl-devel
BuildRequires:    jansson-devel
BuildRequires:    libedit-devel
BuildRequires:    libstdc++-devel
BuildRequires:    libsrtp-devel
BuildRequires:    libtiff-devel
BuildRequires:    libtool-ltdl-devel
BuildRequires:    libuuid-devel
BuildRequires:    libxml2-devel
BuildRequires:    spandsp-devel
BuildRequires:    sqlite-devel
BuildRequires:    unixODBC-devel
BuildRequires:    dahdi-tools-devel
BuildRequires:    libpri-devel
BuildRequires:    openr2-devel
BuildRequires:    speex-devel
BuildRequires:    speexdsp-devel
BuildRequires:    opus-devel

BuildRequires:    systemd-rpm-macros

Requires(pre):    %{_sbindir}/useradd
Requires(pre):    %{_sbindir}/groupadd

Requires(post):   systemd-units
Requires(post):   systemd-sysv
Requires(preun):  systemd-units
Requires(postun): systemd-units

# chan_phone headers no longer in kernel headers
Obsoletes:        asterisk-phone < %{version}

%description
Asterisk is a complete PBX in software. It runs on Linux and provides
all of the features you would expect from a PBX and more. Asterisk
does voice over IP in three protocols, and can interoperate with
almost all standards-based telephony equipment using relatively
inexpensive hardware.

%package devel
Summary: Development files for Asterisk
Requires: asterisk = %{epoch}:%{version}-%{release}

%description devel
Development files for Asterisk.

%prep
gpgv2 --keyring %{SOURCE7} %{SOURCE1} %{SOURCE0}
%setup -q -n asterisk-%{version}

# copy the pjproject tarball to the cache/ directory
mkdir cache
cp %{SOURCE8} cache/
ls -altr cache/

cp %{S:3} menuselect.makedeps
cp %{S:4} menuselect.makeopts

# Fixup makefile so sound archives aren't downloaded/installed
%{__perl} -pi -e 's/^all:.*$/all:/' sounds/Makefile
%{__perl} -pi -e 's/^install:.*$/install:/' sounds/Makefile

# convert comments in one file to UTF-8
mv main/fskmodem.c main/fskmodem.c.old
iconv -f iso-8859-1 -t utf-8 -o main/fskmodem.c main/fskmodem.c.old
touch -r main/fskmodem.c.old main/fskmodem.c
rm main/fskmodem.c.old

chmod -x contrib/scripts/dbsep.cgi

tar -xvf %{SOURCE9}
mv ./asterisk-res_json* ./asterisk-res_json
./asterisk-res_json/install.sh

%build

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
export LDFLAGS="%{ldflags}"
export ASTCFLAGS=" "

sed -i '1s/env python/python3/' contrib/scripts/refcounter.py
sed -i '1s/env python/python3/' contrib/scripts/reflocks.py
sed -i '1s/env python/python3/' contrib/scripts/refstats.py

#aclocal -I autoconf --force
#autoconf --force
#autoheader --force
./bootstrap.sh

pushd menuselect
%configure --datadir=/var/lib
popd

%configure --with-libedit=yes --with-srtp --with-pjproject-bundled --with-externals-cache=%{_builddir}/asterisk-%{version}/cache LDFLAGS="%{ldflags}" --datadir=/var/lib

%make_build menuselect-tree NOISY_BUILD=1

%make_build %{makeargs}


%install
rm -rf %{buildroot}

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
export LDFLAGS="%{ldflags}"
export ASTCFLAGS="%{optflags}"

make install %{makeargs}
make samples %{makeargs}

install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/asterisk.service
rm -f %{buildroot}%{_sbindir}/safe_asterisk
install -D -p -m 0644 %{S:2} %{buildroot}%{_sysconfdir}/logrotate.d/asterisk


# create some directories that need to be packaged
mkdir -p %{buildroot}%{_datadir}/asterisk/moh
mkdir -p %{buildroot}%{_datadir}/asterisk/sounds
mkdir -p %{buildroot}%{_datadir}/asterisk/ast-db-manage
mkdir -p %{buildroot}%{_localstatedir}/lib/asterisk
mkdir -p %{buildroot}%{_localstatedir}/log/asterisk/cdr-custom
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/festival
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/monitor
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/outgoing
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/uploads

# We're not going to package any of the sample AGI scripts
rm -f %{buildroot}%{_datadir}/asterisk/agi-bin/*

# Don't package the sample voicemail user
rm -rf %{buildroot}%{_localstatedir}/spool/asterisk/voicemail/default

# Don't package example phone provision configs
rm -rf %{buildroot}%{_datadir}/asterisk/phoneprov/*

# these are compiled with -O0 and thus include unfortified code.
rm -rf %{buildroot}%{_sbindir}/hashtest
rm -rf %{buildroot}%{_sbindir}/hashtest2

#
rm -rf %{buildroot}%{_sysconfdir}/asterisk/app_skel.conf
rm -rf %{buildroot}%{_sysconfdir}/asterisk/config_test.conf
rm -rf %{buildroot}%{_sysconfdir}/asterisk/test_sorcery.conf

rm -rf %{buildroot}%{_libdir}/libasteriskssl.so
ln -s libasterisk.so.1 %{buildroot}%{_libdir}/libasteriskssl.so

# copy the alembic scripts
cp -rp contrib/ast-db-manage %{buildroot}%{_datadir}/asterisk/ast-db-manage

%if %{tmpfilesd}
install -D -p -m 0644 %{SOURCE6} %{buildroot}/usr/lib/tmpfiles.d/asterisk.conf
mkdir -p %{buildroot}%{astvarrundir}
%endif

rm -f %{buildroot}%{_sysconfdir}/asterisk/*_mysql.conf
rm -f %{buildroot}%{_sysconfdir}/asterisk/*_pgsql.conf
rm -f %{buildroot}%{_sysconfdir}/asterisk/misdn.conf
rm -f %{buildroot}%{_sysconfdir}/asterisk/res_snmp.conf
rm -f %{buildroot}%{_sysconfdir}/asterisk/res_ldap.conf
rm -f %{buildroot}%{_sysconfdir}/asterisk/res_corosync.conf
rm -f %{buildroot}%{_sysconfdir}/asterisk/phone.conf
rm -f %{buildroot}%{_sysconfdir}/asterisk/xmpp.conf
rm -f %{buildroot}%{_sysconfdir}/asterisk/motif.conf


%pre
%{_sbindir}/groupadd -r asterisk &>/dev/null || :
%{_sbindir}/useradd  -r -s /sbin/nologin -d /var/lib/asterisk -M \
                               -c 'Asterisk User' -g asterisk asterisk &>/dev/null || :

%post
%systemd_post asterisk.service


%preun
%systemd_preun asterisk.service


%postun
%systemd_postun apache-httpd.service


%files
%doc *.txt ChangeLog BUGS CREDITS configs
%license LICENSE

%doc doc/asterisk.sgml

%{_unitdir}/asterisk.service

%{_libdir}/libasteriskssl.so.1*
%{_libdir}/libasteriskpj.so.2*

%dir %{_libdir}/asterisk
%{_libdir}/asterisk/modules
%{_sbindir}/*

%{_mandir}/man8/*

%attr(0750,asterisk,asterisk) %dir %{_sysconfdir}/asterisk
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/*

%config(noreplace) %{_sysconfdir}/logrotate.d/asterisk

%{_datadir}/asterisk
%{_datadir}/dahdi/span_config.d/*

%{_localstatedir}/lib/asterisk

%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-csv
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-custom

%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk
%attr(0770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/monitor
%attr(0770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/outgoing
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/tmp
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/uploads
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/voicemail

%if %{tmpfilesd}
%attr(0644,root,root) /usr/lib/tmpfiles.d/asterisk.conf
%endif
%attr(0755,asterisk,asterisk) %dir %{astvarrundir}


%files devel
%dir %{_includedir}/asterisk
%dir %{_includedir}/asterisk/doxygen
%{_includedir}/asterisk.h
%{_includedir}/asterisk

%{_libdir}/libasteriskssl.so
%{_libdir}/libasteriskpj.so

%changelog
* Fri Oct 11 2024 Backend Team - 20.9.3
- Update asterisk to 20.9.3

* Tue Nov 1 2022 Patrick Coakley <patrick.coakley@spearline.com> - 16.29.0-2
- Update asterisk to 16.29.0
- Update pjproject to 2.12.1

* Tue Jan 25 2022 Dhaval Indrodiya <dhaval.indrodiya@spearline.com> - 16.23.0
- Update to asterisk 16.23.0

* Fri Feb 19 2021 Jonathan Dieter <jonathan.dieter@spearline.com> - 16.16.1-1
- Update to asterisk 16.16.1

* Fri Nov 20 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 16.12.0-4
- Enable http-websocket resource

* Tue Sep 15 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 16.12.0-3
- Fix Requires for devel package
- Add support for Opus

* Wed Sep 02 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 16.12.0-2
- Use /var/lib/asterisk rather than /usr/share/asterisk to match our current scripts

* Tue Aug 25 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 16.12.0-1
- Update to upstream 16.12.0 release for bug fixes
- Switch back to One Big Package (tm) to ease maintenance
- Use Spearline config

* Mon May 11 2020 Jared K. Smith <jsmith@fedoraproject.org> - 16.10.0-2
- app_page no longer depends on meetme
- fix usage of PJSIP_SC_NULL with older versions of pjproject
- stop building chan_misdn again

* Thu Apr 30 2020 Jared K. Smith <jsmith@fedoraproject.org> - 16.10.0-1
- Update to upstream 16.10.0 release for bug fixes
