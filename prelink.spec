#
# Conditional build:
# _without_static	- build dynamically linked binary
#
Summary:	Tool to optimize relocations in object files
Summary(pl):	Narzêdzie optymalizuj±ce relokacje w plikach obiektów
Name:		prelink
Version:	20030808
Release:	2
License:	GPL
Group:		Development/Tools
#Source0:	ftp://people.redhat.com/jakub/prelink/%{name}-%{version}.tar.bz2
#Ripped from:	ftp://people.redhat.com/jakub/prelink/0.3.0-2/prelink-0.3.0-2.src.rpm
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	e4e6e568f4194e3a9cc7bf41984c6b4a
Patch0:		http://csociety-ftp.ecn.purdue.edu/pub/gentoo-portage/sys-devel/prelink/files/prelink-20030505-glibc231.patch
Source1:	%{name}.conf
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glibc-devel >= 2.3
%{!?_without_static:BuildRequires:	glibc-static >= 2.3}
BuildRequires:	elfutils-devel
%{!?_without_static:BuildRequires:	elfutils-static}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
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
%if 0%{!?_without_static:1}
rm -f missing
%{__libtoolize}
%{__aclocal} -I m4
%endif
%{__autoconf}
%{__autoheader}
%{!?_without_static:%{__automake}}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/rpm}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

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
%config(noreplace) %verify(not md5 size mtime) /etc/prelink.conf
/etc/rpm/macros.prelink
