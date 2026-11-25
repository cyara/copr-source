%undefine _hardened_build

Summary:	G.729 codec for Asterisk open source PBX
Name:		asterisk-g72x
Version:	1.4.5
Release:	1%{?dist}
License:	GPLv3
URL:		https://github.com/arkadijs/asterisk-g72x
Source0:	asterisk-g72x-1.4.5.tar.bz2
BuildRequires:	autoconf automake libtool
BuildRequires:	asterisk-devel bcg729-devel

%description
G.729 codec for Asterisk, using open source bcg729


%prep
%setup -q -n asterisk-g72x-1.4.5
rm ipp -rf


%build
./autogen.sh
%{configure} --with-asterisk --with-bcg729
%{__make}


%install
DESTDIR=%{buildroot} %{__make} install

# cleanup
rm -f %{buildroot}%{_libdir}/asterisk/modules/*.*a


%files
%attr(0755,root,root) %{_libdir}/asterisk/modules/*.so


%changelog
* Tue Nov 25 2026 Telephony <telephony@spearline.com> - 1.4.5-1
- Update asterisk-g72x to 1.4.5
- Use released tarball instead of git commit

* Tue Nov 24 2026 Telephony <telephony@spearline.com> - 0.1-0.2git
- Rebuild against Asterisk 24 headers

* Tue Sep 15 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 0.1-0.1git
- Initial release of GitHub version

