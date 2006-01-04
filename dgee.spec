#
# TODO:
#  --without apache1 (default) should build mod_dgee.so for apache2 - it doesn't
#
# Conditional build:
%bcond_with	apache1
#
%define		apxs		/usr/sbin/apxs
%define		subver		2
%define		base_version	0.1.6
Summary:	The DotGNU Execution Environment Core
Summary(pl):	Podstawa ¶rodowiska wykonawczego DotGNU
Name:		dgee
Version:	%{base_version}_%{subver}
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.nfluid.com/download/src/%{name}-%{base_version}-%{subver}.tgz
# Source0-md5:	a2573a076832c4c7212479cabda15eff
Source1:	%{name}.init
Source2:	%{name}.logrotate
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-apache.patch
Patch2:		%{name}-dglib_fix_so.patch
Patch3:		%{name}-pythonvm.patch
Patch4:		%{name}-pic.patch
Patch5:		%{name}-nolibnsl.patch
URL:		http://www.dotgnu.org/dgee.html
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	gc-devel
BuildRequires:	goldwater-devel => 0.3.4
BuildRequires:	libffi-devel
BuildRequires:	phlib-devel => 1.20
BuildRequires:	pnet-compiler-csharp
BuildRequires:	pnet-devel => 0.6.0-2
BuildRequires:	pnetlib-base
Requires(post):	/sbin/ldconfig
Requires(post,preun):	%{apxs}
Requires(post,preun):	/sbin/chkconfig
Requires:	goldwater
Requires:	webserver = apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The core DotGNU Execution Environment that provides the functionality
of accepting, validating and satisfying web service requests.

%description -l pl
Ten pakiet zawiera podstawê ¶rodowiska wykonawczego DotGNU (DotGNU
Execution Environment) dostarczaj±c± funkcjonalno¶æ przyjmowania,
sprawdzania poprawno¶ci i wykonywania ¿±dañ us³ug WWW.

%prep
%setup -q -n %{name}-%{base_version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CFLAGS="%{rpmcflags} -I/usr/include/python2.4 -I/usr/include/python2.3"
export CFLAGS
%configure \
	cflags=our \
	--with-goldwater=%{_prefix} \
	--with-pnet=%{_prefix} \
	--with-repository=/var/lib/%{name} \
	--with-username=http \
	--with-usergroup=http \
	--with-python \
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

# Thise files should be installed by Makefile (I can't fix it):
install cslib/DotGNU/DGEE/DotGNU.DGEE.dll \
	$RPM_BUILD_ROOT%{_libdir}/%{name}
install cslib/System/Web/Services/System.Web.Services.dll \
	$RPM_BUILD_ROOT%{_libdir}/%{name}
install cslib/DotGNU/DGEE/Protocols/XmlRpc/XmlRpcService.exe \
	$RPM_BUILD_ROOT%{_libdir}/%{name}

install -d $RPM_BUILD_ROOT/var/lib/%{name}/{index,data}
install -d $RPM_BUILD_ROOT/var/log/%{name}
touch $RPM_BUILD_ROOT/var/log/%{name}/{%{name}.log,stdout,stderr}
install -d $RPM_BUILD_ROOT/var/log/archiv/%{name}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -d $RPM_BUILD_ROOT/etc/logrotate.d
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
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

if [ -f /var/lock/subsys/dgee ]; then
	/etc/rc.d/init.d/dgee restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/dgee start\" to start goltwater and dgee services."
fi
/sbin/chkconfig --add dgee

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
	if [ -f /var/lock/subsys/dgee ]; then
		/etc/rc.d/init.d/dgee stop 1>&2
	fi
	/sbin/chkconfig --del dgee
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BINARYINSTALL INSTALL QUICKSTART README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libdgee.so.*.*
%attr(755,root,root) %{_libdir}/libdgxml.so.*.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}*
%if %{with apache1}
%config %verify(not md5 mtime size) %{_sysconfdir}/httpd/mod_%{name}.conf
%{_libdir}/apache/mod_%{name}.so
%else
#%config %{_sysconfdir}/httpd/mod_%{name}.conf
#%{_libdir}/apache/mod_%{name}.so
%endif
%{_datadir}/%{name}
/var/lib/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(730,root,http) %dir /var/log/%{name}
%attr(660,root,http) /var/log/%{name}/*
%attr(750,root,root) %dir /var/log/archiv/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
