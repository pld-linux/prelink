#
# Conditional build:
# _without_static	- build dynamically linked binary

Summary:	Tool to optimize relocations in object files
Summary(pl):	Narz�dzie optymalizuj�ce relokacje w plikach objekt�w
Name:		prelink
Version:	20030522
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	ftp://people.redhat.com/jakub/prelink/%{name}-%{version}.tar.bz2
# Source0-md5:	07de27b8e677f787193592847296581f
Patch0:		http://csociety-ftp.ecn.purdue.edu/pub/gentoo-portage/sys-devel/prelink/files/prelink-20030505-glibc231.patch
BuildRequires:	glibc-devel >= 2.3
%{!?_without_static:BuildRequires:	glibc-static >= 2.3}
BuildRequires:	elfutils-static
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program replaces relocations in object files with less expensive
ones. This allows faster run-time dynamic linking.

%description -l pl
Ten program zamienia relokacje w plikach objekt�w na mniej wymagaj�ce.
Dzi�ki temu program jest szybciej linkowany w momencie uruchomienia.

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
