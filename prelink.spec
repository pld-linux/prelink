#
# Conditional build:
%bcond_without	selinux		# SELinux support
%bcond_without	tests		# tests after build
#
Summary:	Tool to optimize relocations in object files
Summary(pl.UTF-8):	Narzędzie optymalizujące relokacje w plikach obiektów
Name:		prelink
Version:	20130503
Release:	1
License:	GPL v2+
Group:		Development/Tools
# backup:	http://distfiles.gentoo.org/distfiles/%{name}-%{version}.tar.bz2
Source0:	http://people.redhat.com/jakub/prelink/%{name}-%{version}.tar.bz2
# Source0-md5:	4cab1571718a9b25665bd025069a02c7
Source1:	%{name}.conf
Source2:	http://people.redhat.com/jakub/prelink/%{name}.pdf
# Source2-md5:	50946b654da9ccb26230cc1e00ccc53c
Source3:	%{name}.cron
Source4:	%{name}.sysconfig
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-fsync.patch
Patch2:		%{name}-init.patch
Patch3:		%{name}-md5sha.patch
Patch4:		%{name}-prelink.h.patch
Patch5:		%{name}-tests.patch
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake >= 1.4
BuildRequires:	elfutils-devel
BuildRequires:	glibc-devel >= 2.3
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
Requires:	glibc >= 2.3.4-0.20040722
Conflicts:	paxtest
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program replaces relocations in object files with less expensive
ones. This allows faster run-time dynamic linking.

%description -l pl.UTF-8
Ten program zamienia relokacje w plikach obiektów na mniej wymagające.
Dzięki temu program jest szybciej konsolidowany w momencie
uruchomienia.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static=no \
	%{!?with_selinux:ac_cv_lib_selinux_is_selinux_enabled=no} \

%{__make} \
	CLFAGS="%{rpmcflags} -D_LARGEFILE64_SOURCE"
%if %{with tests}
%{__make} -C testsuite check-harder
%{__make} -C testsuite check-cycle
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{sysconfig,rpm,cron.daily}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} .
cp -a %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.daily/prelink
cp -a %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/prelink

install -d $RPM_BUILD_ROOT/var/{lib/misc,log/prelink}
touch $RPM_BUILD_ROOT/var/lib/misc/prelink.full
touch $RPM_BUILD_ROOT/var/lib/misc/prelink.quick
touch $RPM_BUILD_ROOT/var/lib/misc/prelink.force
touch $RPM_BUILD_ROOT/var/log/prelink/prelink.log

cat > $RPM_BUILD_ROOT/etc/rpm/macros.prelink <<'EOF'
# rpm-4.1 verifies prelinked libraries using a prelink undo helper.
#       Note: The 2nd token is used as argv[0] and "library" is a
#       placeholder that will be deleted and replaced with the appropriate
#       library file path.
%%__prelink_undo_cmd %{_sbindir}/prelink prelink -y library
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 002
touch /var/lib/misc/prelink.force

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO prelink.pdf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/prelink.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/prelink
/etc/rpm/macros.prelink
%attr(755,root,root) /etc/cron.daily/prelink
%attr(755,root,root) %{_bindir}/execstack
%attr(755,root,root) %{_sbindir}/prelink
%{_mandir}/man8/execstack.8*
%{_mandir}/man8/prelink.8*
%verify(not md5 mtime size) %ghost %config(missingok,noreplace) /var/lib/misc/prelink.full
%verify(not md5 mtime size) %ghost %config(missingok,noreplace) /var/lib/misc/prelink.quick
%verify(not md5 mtime size) %ghost %config(missingok,noreplace) /var/lib/misc/prelink.force
%dir /var/log/prelink
%verify(not md5 mtime size) %ghost %config(missingok,noreplace) /var/log/prelink/prelink.log
