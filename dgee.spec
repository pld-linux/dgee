%bcond_with	apache1

%define		_rel	2
Summary:	The DotGNU Execution Environment Core
Name:		dgee
Version:	0.1.6
Release:	%{_rel}.0.1.1
Source0:	http://www.nfluid.com/download/src/%{name}-%{version}-%{_rel}.tgz
# Source0-md5:	a2573a076832c4c7212479cabda15eff
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-apache.patch
License:	GPL
Vendor:		DotGNU
Group:		Networking/Daemons
Requires:	apache
Requires(post,preun):   %{apxs}
BuildRequires:	apache-devel
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
	--with-pnet=%{_prefix} \
%if %{with apache1}
	--with-apache=%{_prefix}
%else
	--without-apache \
	--with-apache2=%{_prefix}
%endif

%if %{with apache1}
%{__make} 
%else
%{__make} \
	APACHE=
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with apache1}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT 
%else
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	APACHE=
%endif

%post
%if %{with apache1}
if [ -f /etc/httpd/httpd.conf ] && \
    ! grep -q "^Include.*/mod_dgee.conf" /etc/httpd/httpd.conf; then
        echo "Include /etc/httpd/mod_dgee.conf" >> /etc/httpd/httpd.conf
fi
%endif

%{apxs} -e -a -n dgee %{_pkglibdir}/mod_dgee.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
        /etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
%if %{with apache1}
        umask 027
        grep -E -v "^Include.*/mod_dgee.conf" /etc/httpd/httpd.conf > \
                /etc/httpd/httpd.conf.tmp
        mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
%endif
        %{apxs} -e -A -n dgee %{_pkglibdir}/mod_dgee.so 1>&2
        if [ -f /var/lock/subsys/httpd ]; then
                /etc/rc.d/init.d/httpd restart 1>&2
        fi
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BINARYINSTALL INSTALL QUICKSTART README COPYING
%attr(755,root,root) %{_bindir}/*
%config %{_sysconfdir}/%{name}*
%{_libdir}/%{name}
%{_libdir}/libdgee.*
%{_libdir}/libdgxml.*
%if %{with apache1}
%config %{_sysconfdir}/httpd/mod_%{name}.conf
%{_libdir}/apache/mod_%{name}.so
%else
#%config %{_sysconfdir}/httpd/mod_%{name}.conf
#%{_libdir}/apache/mod_%{name}.so
%endif
%{_datadir}/%{name}

# Local variables:
# mode: rpm-spec
# end:
