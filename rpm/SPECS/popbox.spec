Summary: Popbox module to manage node + Redis value server
Name: popbox
Version: 0.0.2
Release: 1
License: GNU
BuildRoot: %{_topdir}/BUILDROOT/
BuildArch: x86_64
Requires: nodejs >= 0.8
Group: Applications/Popbox
Vendor: Telefonica I+D
BuildRequires: npm

%description
Simple High-Performance High-Scalability Inbox Notification Service, 
require Redis 2.6 server, node 0.8 and npm only for installatión
%define _prefix_company pdi
%define _project_name popbox
%define _service_name %{_project_name}
%define _install_dir /opt
%define _srcdir %{_sourcedir}/../../
%define _project_install_dir %{_install_dir}/%{_prefix_company}-%{_project_name}
%define _logrotate_conf_dir %{_srcdir}/conf/log
%define _popbox_log_dir %{_localstatedir}/log/%{_prefix_company}-{_project_name}
%define _build_root_project %{buildroot}/%{_project_install_dir}

# -------------------------------------------------------------------------------------------- #
# prep section, setup macro:
# -------------------------------------------------------------------------------------------- #
%prep
rm -Rf $RPM_BUILD_ROOT && mkdir -p $RPM_BUILD_ROOT
[ -d %{_build_root_project} ] || mkdir -p %{_build_root_project}

cp -R %{_srcdir}/lib  %{_srcdir}/package.json %{_srcdir}/index.js \
      %{_srcdir}/bin %{_srcdir}/License.txt %{_build_root_project}
cp -R %{_sourcedir}/*  %{buildroot}

%build
cd %{_build_root_project}
npm install --production
rm package.json

# -------------------------------------------------------------------------------------------- #
# post-install section:
# -------------------------------------------------------------------------------------------- #
%post
echo "Configuring application:"
echo "Checking administration folders.."
[ -d $RPM_BUILD_ROOT%{_sysconfdir}/popbox ] || mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/popbox
[ -d $RPM_BUILD_ROOT%{_sysconfdir}/init.d ] || mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d
[ -d $RPM_BUILD_ROOT%{_popbox_log_dir} ] || mkdir -p $RPM_BUILD_ROOT%{_popbox_log_dir}

chkconfig --level 2345 %{_service_name} on
echo "Making links for logs and configuration files"
ln -fs %{_project_install_dir}/src/config.js $RPM_BUILD_ROOT%{_sysconfdir}/%{_project_name}/config.js
[ -e /usr/bin/node ] || ln -s /usr/bin/nodejs /usr/bin/node
echo "Done"

%preun
if [ $1 == 0 ]; then
echo "Removing application config files"
[ -f /etc/logrotate.d/popbox ] && rm -fv /etc/logrotate.d/popbox
[ -d /etc/popbox ] && rm -rfv /etc/popbox
[ -d %{_popbox_log_dir} ] && rm -rfv %{_popbox_log_dir}
[ -d %{_project_install_dir} ] && rm -rfv %{_project_install_dir}
chkconfig popbox off
echo "Done"
fi

%postun
%clean
rm -rf $RPM_BUILD_ROOT
%files
%defattr(755,root,root,755)
%config /etc/init.d/%{_service_name}
%config /etc/logrotate.d/%{_project_name}
%{_project_install_dir}
