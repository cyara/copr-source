# Define the kmod package name here.
%define kmod_name		hpsa

# If kmod_kernel_version isn't defined on the rpmbuild line, define it here.
%{!?kmod_kernel_version: %define kmod_kernel_version 4.18.0-553.el8_10}

%{!?dist: %define dist .el8}

Name:		kmod-%{kmod_name}
Version:	3.4.20
Release:	12%{?dist}
Summary:	%{kmod_name} kernel module(s)
Group:		System Environment/Kernel
License:	GPLv2
URL:		http://www.kernel.org/

# Sources
Source0:	%{kmod_name}-%{version}.tar.gz
Source5:	GPL-v2.0.txt

# Fix for the SB-signing issue caused by a bug in /usr/lib/rpm/brp-strip
# https://bugzilla.redhat.com/show_bug.cgi?id=1967291

%define __spec_install_post	/usr/lib/rpm/check-buildroot \
				/usr/lib/rpm/redhat/brp-ldconfig \
				/usr/lib/rpm/brp-compress \
				/usr/lib/rpm/brp-strip-comment-note /usr/bin/strip /usr/bin/objdump \
 				/usr/lib/rpm/brp-strip-static-archive /usr/bin/strip \
				/usr/lib/rpm/brp-python-bytecompile "" 1 \
				/usr/lib/rpm/brp-python-hardlink \
				PYTHON3="/usr/libexec/platform-python" /usr/lib/rpm/redhat/brp-mangle-shebangs

# Source code patches
Patch0: elrepo-hpsa-add-removed-devices-el9.patch

%define findpat %( echo "%""P" )
%define __find_requires /usr/lib/rpm/redhat/find-requires.ksyms
%define __find_provides /usr/lib/rpm/redhat/find-provides.ksyms %{kmod_name} %{?epoch:%{epoch}:}%{version}-%{release}
%define dup_state_dir %{_localstatedir}/lib/rpm-state/kmod-dups
%define kver_state_dir %{dup_state_dir}/kver
%define kver_state_file %{kver_state_dir}/%{kmod_kernel_version}.%{_arch}
%define dup_module_list %{dup_state_dir}/rpm-kmod-%{kmod_name}-modules
%define debug_package %{nil}

%global _use_internal_dependency_generator 0
%global kernel_source() %{_usrsrc}/kernels/%{kmod_kernel_version}.%{_arch}

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

ExclusiveArch:	x86_64

BuildRequires:	elfutils-libelf-devel
BuildRequires:	kernel-devel = %{kmod_kernel_version}
BuildRequires:	kernel-abi-whitelists
BuildRequires:	kernel-rpm-macros
BuildRequires:	redhat-rpm-config

Provides:	kernel-modules >= %{kmod_kernel_version}.%{_arch}
Provides:	kmod-%{kmod_name} = %{?epoch:%{epoch}:}%{version}-%{release}

Requires(post):	%{_sbindir}/weak-modules
Requires(postun):	%{_sbindir}/weak-modules
Requires:	kernel >= %{kmod_kernel_version}

%description
This package provides the %{kmod_name} kernel module(s).
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -n %{kmod_name}-%{version}
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

# Apply patch(es)
%patch0 -p1

%build
%{__make} -C %{kernel_source} %{?_smp_mflags} V=1 modules M=$PWD

whitelist="/lib/modules/kabi-current/kabi_whitelist_%{_target_cpu}"
for modules in $( find . -name "*.ko" -type f -printf "%{findpat}\n" | sed 's|\.ko$||' | sort -u ) ; do
	# update greylist
	nm -u ./$modules.ko | sed 's/.*U //' |  sed 's/^\.//' | sort -u | while read -r symbol; do
		grep -q "^\s*$symbol\$" $whitelist || echo "$symbol" >> ./greylist
	done
done
sort -u greylist | uniq > greylist.txt

%install
%{__install} -d %{buildroot}/lib/modules/%{kmod_kernel_version}.%{_arch}/extra/%{kmod_name}/
%{__install} %{kmod_name}.ko %{buildroot}/lib/modules/%{kmod_kernel_version}.%{_arch}/extra/%{kmod_name}/
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -m 0644 kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -d %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} -m 0644 %{SOURCE5} %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} -m 0644 greylist.txt %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/

# strip the modules(s)
find %{buildroot} -name \*.ko -type f | xargs --no-run-if-empty %{__strip} --strip-debug

# Sign the modules(s)
%if %{?_with_modsign:1}%{!?_with_modsign:0}
# If the module signing keys are not defined, define them here.
%{!?privkey: %define privkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.priv}
%{!?pubkey: %define pubkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.der}
for module in $(find %{buildroot} -type f -name \*.ko);
do %{_usrsrc}/kernels/%{kmod_kernel_version}.%{_arch}/scripts/sign-file \
sha256 %{privkey} %{pubkey} $module;
done
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
/lib/modules/%{kmod_kernel_version}.%{_arch}/
%config /etc/depmod.d/kmod-%{kmod_name}.conf
%doc /usr/share/doc/kmod-%{kmod_name}-%{version}/

%changelog
* Thu May 30 2024 Patrick Coakley <patrick.coakley@cyara.com> - 3.4.20-12
- Rebuilt for CyaraOS 8.10

* Thu May 23 2024 Akemi Yagi <toracat@elrepo.org> - 3.4.20-11
- Rebuilt for RHEL 8.10
- Source code from RHEL 8.10 GA kernel-4.18.0-553.el8_10

* Sun Nov 19 2023 Philip J Perry <phil@elrepo.org> - 3.4.20-10
- Reguilt against RHEL 8.9 kernel
- Source code from RHEL 8.9 GA kernel-4.18.0-513.5.1.el8_9

* Wed Aug 02 2023 Akemi Yagi <toracat@elrepo.org> - 3.4.20-9
- Rebuilt against RHEL 8.8 kernel 4.18.0-477.10.1.el8_8

* Mon Feb 13 2023 Akemi Yagi <toracat@elrepo.org> - 3.4.20-8
- Rebuilt against RHEL 8.7 kernel 4.18.0-425.10.1.el8_7

* Tue May 10 2022 Akemi Yagi <toracat@elrepo.org> - 3.4.20-7
- Rebuilt against RHEL 8.6 GA kernel 4.18.0-372.9.1.el8

* Fri Nov 12 2021 Akemi Yagi <toracat@elrepo.org> - 3.4.20-6
- Rebuilt against RHEL 8.5 kernel

* Tue May 18 2021 Philip J Perry <phil@elrepo.org> - 3.4.20-5
- Rebuilt against RHEL 8.4 kernel
- Fix updating of initramfs image
  [https://elrepo.org/bugs/view.php?id=1060]
- Revert addition of dracut conf file

* Mon Nov 09 2020 Akemi Yagi <toracat@elrepo.org> - 3.4.20-4
- Add dracut conf file to ensure module is in initramfs

* Tue Nov 03 2020 Akemi Yagi <toracat@elrepo.org> - 3.4.20-3
- Rebuilt against RHEL 8.3 kernel
- patch updated (v3)

* Mon Oct 26 2020 Akemi Yagi <toracat@elrepo.org> - 3.4.20-2
- Patch amended to include missing device IDs (v2)

* Sun Oct 25 2020 Akemi Yagi <toracat@elrepo.org> - 3.4.20-1
- Initial build for RHEL 8.2
