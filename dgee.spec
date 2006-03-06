# TODO:
# - pnet incompatability, see -pnet.patch
#
# Conditional build:
%bcond_without	apache1		# disable building apache 1.3.x module
%bcond_without	apache2		# disable building apache 2.x module
%bcond_with	i_have_checked_this_patch_works_not_just_compiles
#
%define		apxs1		/usr/sbin/apxs1
%define		apxs2		/usr/sbin/apxs
%define		subver		2
%define		base_version	0.1.6
Summary:	The DotGNU Execution Environment Core
Summary(pl):	Podstawa ¶rodowiska wykonawczego DotGNU
Name:		dgee
Version:	%{base_version}_%{subver}
Release:	2.2
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.nfluid.com/download/src/%{name}-%{base_version}-%{subver}.tgz
# Source0-md5:	a2573a076832c4c7212479cabda15eff
Source1:	%{name}.init
Source2:	%{name}.logrotate
Source3:	%{name}-apache.conf
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-apache.patch
Patch2:		%{name}-dglib_fix_so.patch
Patch3:		%{name}-pythonvm.patch
Patch4:		%{name}-pic.patch
Patch5:		%{name}-nolibnsl.patch
Patch6:		%{name}-pnet.patch
URL:		http://www.dotgnu.org/dgee.html
%{?with_apache1:BuildRequires:	%{apxs1}}
%{?with_apache2:BuildRequires:	%{apxs2}}
%{?with_apache2:BuildRequires:	apache-devel}
%{?with_apache1:BuildRequires:	apache1-devel}
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	gc-devel
BuildRequires:	goldwater-devel >= 0.3.4
BuildRequires:	libffi-devel
BuildRequires:	phlib-devel >= 1.20
BuildRequires:	pnet-compiler-csharp
BuildRequires:	pnet-devel >= 0.6.0-2
BuildRequires:	pnetlib-base
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	rc-scripts
Requires:	goldwater
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The core DotGNU Execution Environment that provides the functionality
of accepting, validating and satisfying web service requests.

%description -l pl
Ten pakiet zawiera podstawê ¶rodowiska wykonawczego DotGNU (DotGNU
Execution Environment) dostarczaj±c± funkcjonalno¶æ przyjmowania,
sprawdzania poprawno¶ci i wykonywania ¿±dañ us³ug WWW.

%package -n apache1-mod_dgee
Summary:	DGEE DSO module for Apache 1.3.x
Summary(pl):	Modu³ DSO DGEE dla Apache'a 1.3.x
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	apache1(EAPI) >= 1.3.33-2
Requires:	apache1-mod_mime

%description -n apache1-mod_dgee
The DotGNU Execution Environment Core DSO module for Apache 1.3.x.

%description -n apache1-mod_dgee -l pl
Modu³ DSO podstawy ¶rodowiska wykonawczego DotGNU (DotGNU Execution
Environment) dla Apache'a 1.3.x.

%package -n apache-mod_dgee
Summary:	DGEE DSO module for Apache 2.x
Summary(pl):	Modu³ DSO DGEE dla Apache'a 2.x
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	apache(modules-api) = %{apache_modules_api}
Requires:	apache-mod_mime

%description -n apache-mod_dgee
The DotGNU Execution Environment Core DSO module for Apache 2.x.

%description -n apache-mod_dgee -l pl
Modu³ DSO podstawy ¶rodowiska wykonawczego DotGNU (DotGNU Execution
Environment) dla Apache'a 1.3.x.

%prep
%setup -q -n %{name}-%{base_version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%{?with_i_have_checked_this_patch_works_not_just_compiles:%patch6 -p1}

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CFLAGS="%{rpmcflags} -I/usr/include/python2.4"
export CFLAGS
%configure \
	cflags=our \
	--with-goldwater=%{_prefix} \
	--with-pnet=%{_prefix} \
	--with-repository=/var/lib/%{name} \
	--with-username=http \
	--with-usergroup=http \
	--with-python \
	%{?with_apache1:--with-apache=%{apxs1}} \
	%{?with_apache2:--with-apache2=%{apxs2}}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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

%if %{with apache1}
install -Dp %{SOURCE3} $RPM_BUILD_ROOT/etc/apache/conf.d/40_mod_dgee.conf
%endif
%if %{with apache2}
install -Dp %{SOURCE3} $RPM_BUILD_ROOT/etc/httpd/httpd.conf/40_mod_dgee.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add dgee
%service dgee restart "goltwater and dgee services"

%preun
if [ "$1" = "0" ]; then
	%service dgee stop
	/sbin/chkconfig --del dgee
fi

%postun	-p /sbin/ldconfig

%post -n apache1-mod_dgee
%service -q apache restart

%postun -n apache1-mod_dgee
if [ "$1" = 0 ]; then
	%service -q apache restart
fi

%post -n apache-mod_dgee
%service -q httpd restart

%postun -n apache-mod_dgee
if [ "$1" = 0 ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc BINARYINSTALL INSTALL QUICKSTART README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libdgee.so.*.*
%attr(755,root,root) %{_libdir}/libdgxml.so.*.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}*
%{_datadir}/%{name}
/var/lib/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(730,root,http) %dir /var/log/%{name}
%attr(660,root,http) /var/log/%{name}/*
%attr(750,root,root) %dir /var/log/archiv/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*

%if %{with apache1}
%files -n apache1-mod_dgee
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/apache/conf.d/*_mod_%{name}.conf
%attr(755,root,root) %{_libdir}/apache1/mod_%{name}.so
%endif

%if %{with apache2}
%files -n apache-mod_dgee
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/httpd/httpd.conf/*_mod_%{name}.conf
%attr(755,root,root) %{_libdir}/apache/mod_%{name}.so
%endif
