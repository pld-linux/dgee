%define		_rel	2
Summary:	The DotGNU Execution Environment Core
Name:		dgee
Version:	0.1.6
Release:	%{_rel}.0.0.1
Source0:	http://www.nfluid.com/download/src/%{name}-%{version}-%{_rel}.tgz
# Source0-md5:	a2573a076832c4c7212479cabda15eff
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-apache.patch
License:	GPL
Vendor:		DotGNU
Group:		Networking/Daemons
BuildRequires:	expat-devel
BuildRequires:	goldwater-devel => 0.3.4
BuildRequires:	phlib-devel => 1.20
BuildRequires:	pnet-devel => 0.6.0-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The core DotGNU Execution Environment that provides the functionality
of accepting, validating and satisfying web service requests.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-goldwater=%{_prefix} \
	--with-pnet=%{_prefix}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BINARYINSTALL INSTALL QUICKSTART README COPYING
%attr(755,root,root) %{_bindir}/*
%config %{_sysconfdir}/%{name}*
%config %{_sysconfdir}/httpd/mod_%{name}.conf
%{_libdir}/%{name}
%{_libdir}/libdgee.*
%{_libdir}/libdgxml.*
%{_libdir}/apache/mod_%{name}.so
%{_datadir}/%{name}

# Local variables:
# mode: rpm-spec
# end:
