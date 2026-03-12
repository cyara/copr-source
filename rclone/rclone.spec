Summary:            Cloud storage sync tool
Name:               rclone
Version:            1.73.2
Release:            1%{?dist}
License:            MIT
URL:                https://github.com/rclone/rclone
Source0:            %{url}/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:      golang >= 1.22
BuildRequires:      git-core

%description
rclone is a command line program to sync files and directories to and from
many cloud storage providers.

%prep
%autosetup -n %{name}-%{version}

%build
export CGO_ENABLED=0
build_target=.
if [ -d cmd/rclone ]; then
    build_target=./cmd/rclone
fi
go build \
    -trimpath \
    -mod=mod \
    -ldflags "-s -w -X github.com/rclone/rclone/fs.Version=%{version}" \
    -o %{name} \
    ${build_target}

%install
# 1. Install the main binary
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}

# 2. Define our target paths for completions
%define bash_comp %{buildroot}%{_datadir}/bash-completion/completions/%{name}
%define zsh_comp  %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
%define fish_comp %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish

# 3. Create directories
mkdir -p $(dirname %{bash_comp}) $(dirname %{zsh_comp}) $(dirname %{fish_comp})

# 4. Generate completions (Note: Passing the path as an argument prevents the /etc/ error)
%{buildroot}%{_bindir}/%{name} genautocomplete bash %{bash_comp}
%{buildroot}%{_bindir}/%{name} genautocomplete zsh %{zsh_comp}
%{buildroot}%{_bindir}/%{name} genautocomplete fish %{fish_comp}

# 5. Install the Man page (included in rclone source)
mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 0644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish

%changelog* Thu Mar 12 2026 Patrick Coakley <patrick.coakley@cyara.com> - 1.73.2-1
- Initial COPR package for AlmaLinux 8+
