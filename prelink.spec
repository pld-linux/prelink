Summary:	Tool to optimize relocations in object files
Summary(pl):	Narzêdzie optymalizuj±ce relokacje w plikach objektów
Name:		prelink
Version:	20021002
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	ftp://people.redhat.com/jakub/prelink/%{name}-%{version}.tar.bz2
BuildRequires:	glibc-devel >= 2.3
BuildRequires:	libelf-static
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
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/prelink.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/prelink.conf
