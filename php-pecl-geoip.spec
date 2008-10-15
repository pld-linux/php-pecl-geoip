%define		_modname	geoip
%define		_status		status
Summary:	%{_modname} - Map IP address to geographic places
Summary(pl.UTF-8):	%{_modname} - odwzorowanie adresów IP w miejsca geograficzne
Name:		php-pecl-%{_modname}
Version:	1.0.3
Release:	1.1
License:	PHP 3.0.1
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	7c534b67f4eb0fe38f0f0f46a8b2ab52
URL:		http://pecl.php.net/package/geoip/
BuildRequires:	GeoIP-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This PHP extension allows you to find the location of an IP address -
City, State, Country, Longitude, Latitude, and other information as
all, such as ISP and connection type.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
To rozszerzenie pozwala na znalezienie miejsca, któremu odpowiada dany
adres IP - miasto, stan, kraj, szerokość i długość geograficzna czy
inne informacje, takie jak ISP czy typ połączenia.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

sed -i -e 's,GEOIP_DIR/lib,GEOIP_DIR/%{_lib},g' %{_modname}-%{version}/config.m4

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
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
%doc %{_modname}-%{version}/{README,ChangeLog}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
