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
%define _prefix_company pdi-
%define _project_name popbox 
%define _company_project_name %{_prefix_company}%{_project_name} 
%define _service_name %{_company_project_name}
%define _install_dir /opt
%define _srcdir %{_sourcedir}/../../
%define _project_install_dir %{_install_dir}/%{_company_project_name}
%define _logrotate_conf_dir %{_srcdir}/conf/log
%define _popbox_log_dir %{_localstatedir}/log/%{_company_project_name}
%define _build_root_project %{buildroot}/%{_project_install_dir}
%define _conf_dir /etc/%{_prefix_company}%{_project_name}
%define _log_dir /var/log/%{_prefix_company}%{_project_name}


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
# Only production modules
npm install --production
rm package.json

# -------------------------------------------------------------------------------------------- #
# post-install section:
# -------------------------------------------------------------------------------------------- #
%post
echo "Configuring application:"
rm -Rf /etc/initi.d/%{_service_name}
cd /etc/init.d

#Service 
echo "Creating %{_service_name} service:"
chkconfig --level 2345 %{_service_name} on

#Config 
rm -Rf %{_conf_dir} && mkdir -p %{_conf_dir}
cd %{_conf_dir}
ln -s %{_project_install_dir}/lib/baseConfig.js %{_project_name}_conf.js

#Logs
#TODO configuration logs
echo "Done"

%preun
if [ $1 == 0 ]; then
   echo "Removing application config files"
   [ -d /etc/%{_company_project_name} ] && rm -rfv /etc/%{_company_project_name}
   [ -d %{_popbox_log_dir} ] && rm -rfv %{_popbox_log_dir}
   [ -d %{_project_install_dir} ] && rm -rfv %{_project_install_dir}
   echo "Destroying %{_service_name} service:"
   chkconfig %{_service_name} off
   rm -Rf /etc/init.d/%{_service_name}
   echo "Done"
fi

%postun
%clean
rm -rf $RPM_BUILD_ROOT
%files
%defattr(755,root,root,755)
%config /etc/init.d/%{_service_name}
%config /etc/logrotate.d/%{_company_project_name}
%{_project_install_dir}
