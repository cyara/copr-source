%undefine _hardened_build
%define git_commit 9f92804a4e16642ab2f4ed74d9ff4839f5494701
%define git_short 9f92804a

Summary:	G.729 codec for Asterisk open source PBX
Name:		asterisk-g72x
Version:	0.1
Release:	0.2.git%{git_short}%{?dist}
License:	GPLv3
URL:		https://github.com/arkadijs/asterisk-g72x
Source0:	https://github.com/arkadijs/asterisk-g72x/archive/%{git_commit}/asterisk-g72x-%{git_short}.tar.gz
BuildRequires:	autoconf automake libtool
BuildRequires:	asterisk-devel bcg729-devel

%description
G.729 codec for Asterisk, using open source bcg729


%prep
%setup -q -n asterisk-g72x-%{git_commit}
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
* Tue Nov 24 2026 Telephony <telephony@spearline.com> - 0.1-0.2git
- Rebuild against Asterisk 24 headers

* Tue Sep 15 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 0.1-0.1git
- Initial release of GitHub version

