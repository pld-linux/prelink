Summary:	Tool to optimize relocations in object files
Summary(pl):	Narzêdzie optymalizuj±ce relokacje w plikach obiektów
Name:		prelink
Version:	20040520
Release:	2
License:	GPL
Group:		Development/Tools
Source0:	ftp://people.redhat.com/jakub/prelink/%{name}-%{version}.tar.bz2
# Source0-md5:	581cdcac535e230b410dc1f253c40aad
Source1:	%{name}.conf
Source2:	ftp://people.redhat.com/jakub/prelink/prelink.pdf
# Source2-md5:	50946b654da9ccb26230cc1e00ccc53c
Patch0:		%{name}-Makefile.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glibc-devel >= 2.3
BuildRequires:	elfutils-devel
BuildRequires:	libselinux-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
Requires:	glibc >= 2.3.4-0.20040722
Conflicts:	paxtest
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program replaces relocations in object files with less expensive
ones. This allows faster run-time dynamic linking.

%description -l pl
Ten program zamienia relokacje w plikach obiektów na mniej wymagaj±ce.
Dziêki temu program jest szybciej konsolidowany w momencie
uruchomienia.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static=no
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/rpm}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} .

cat > $RPM_BUILD_ROOT/etc/rpm/macros.prelink <<"EOF"
# rpm-4.1 verifies prelinked libraries using a prelink undo helper.
#       Note: The 2nd token is used as argv[0] and "library" is a
#       placeholder that will be deleted and replaced with the appropriate
#       library file path.
%%__prelink_undo_cmd	/usr/sbin/prelink prelink -y library
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO prelink.pdf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%config(noreplace) %verify(not md5 size mtime) /etc/prelink.conf
/etc/rpm/macros.prelink
