Summary:            Cloud storage sync tool
Name:               rclone
Version:            1.73.2
Release:            1%{?dist}
License:            MIT
URL:                https://github.com/rclone/rclone
Source:             %{name}-v%{version}.tar.gz
BuildRequires:      golang

%description
rclone is a command line program to sync files and directories to and from
many cloud storage providers.

%prep
%autosetup -n %{name}-%{version}

%build
export CGO_ENABLED=0
go build \
    -trimpath \
    -mod=vendor \
    -ldflags "-s -w -X github.com/rclone/rclone/fs.Version=%{version}" \
    -o %{name} \
    ./cmd/rclone

%install
install -Dpm0755 %{name} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
%{buildroot}%{_bindir}/%{name} genautocomplete bash > %{buildroot}%{_datadir}/bash-completion/completions/%{name}

mkdir -p %{buildroot}%{_datadir}/zsh/site-functions
%{buildroot}%{_bindir}/%{name} genautocomplete zsh > %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d
%{buildroot}%{_bindir}/%{name} genautocomplete fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish

%changelog
* Thu Mar 12 2026 Patrick Coakley <patrick.coakley@cyara.com> - 1.73.2-1
- Initial COPR package for AlmaLinux 8+
