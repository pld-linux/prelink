Summary:	Tool to optimize relocations in object files
Summary(pl):	Narzêdzie optymalizuj±ce relokacje w plikach objektów
Name:		prelink
Version:	20021002
Release:	3
License:	GPL
Group:		Development/Tools
Source0:	ftp://people.redhat.com/jakub/prelink/%{name}-%{version}.tar.bz2
BuildRequires:	glibc-devel >= 2.3
BuildRequires:	elfutils-static
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program replaces relocations in object files with less expensive
ones. This allows faster run-time dynamic linking.

%description -l pl
Ten program zamienia relokacje w plikach objektów na mniej wymagaj±ce.
Dziêki temu program jest szybciej linkowany w momencie uruchomienia.

%prep
%setup -q -n %{name}

%build
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/rpm}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/prelink.conf $RPM_BUILD_ROOT%{_sysconfdir}

cat > $RPM_BUILD_ROOT/etc/rpm/macros.prelink <<"EOF"
# rpm-4.1 verifies prelinked libraries using a prelink undo helper.
#       Note: The 2nd token is used as argv[0] and "library" is a
#       placeholder that will be deleted and replaced with the appropriate
#       library file path.
%%__prelink_undo_cmd     /usr/sbin/prelink prelink -y library
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/prelink.conf
/etc/rpm/macros.prelink
