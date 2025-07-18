%define		php_name	php%{?php_suffix}
%define		modname	geoip
%define		status		status
Summary:	%{modname} - Map IP address to geographic places
Summary(pl.UTF-8):	%{modname} - odwzorowanie adresów IP w miejsca geograficzne
Name:		%{php_name}-pecl-%{modname}
Version:	1.1.1
Release:	2
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	4f5f4b8a41a5802de6591c79b85cc838
Patch0:		find_libgeoip.patch
Patch1:         git.patch
URL:		http://pecl.php.net/package/geoip/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	GeoIP-devel >= 1.4.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Suggests:	GeoIP-db-City
Suggests:	GeoIP-db-Country
Suggests:	GeoIP-db-IPASNum
Provides:	php(geoip) = %{version}
Obsoletes:	php-pecl-geoip < 1.0.8-7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This PHP extension allows you to find the location of an IP address -
City, State, Country, Longitude, Latitude, and other information as
all, such as ISP and connection type.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
To rozszerzenie pozwala na znalezienie miejsca, któremu odpowiada dany
adres IP - miasto, stan, kraj, szerokość i długość geograficzna czy
inne informacje, takie jak ISP czy typ połączenia.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
%patch -P0 -p1
%patch -P1 -p1

sed -i -e 's,GEOIP_DIR/lib,GEOIP_DIR/%{_lib},g' config.m4

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
