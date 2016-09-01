%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library magnum-ui
%global module magnum_ui

Name:       openstack-%{library}
Version:    1.0.0
Release:    1%{?dist}
Summary:    OpenStack Magnum UI Horizon plugin
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git

Requires:   python2-magnumclient >= 0.2.1
Requires:   openstack-dashboard >= 8.0.0

%description
OpenStack Magnum UI Horizon plugin

# Documentation package
%package -n python-%{library}-doc
Summary:    OpenStack example library documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n python-%{library}-doc
OpenStack Magnum UI Horizon plugin documentation

This package contains the documentation.

%prep
%autosetup -n %{library}-%{upstream_version} -S git
# Let's handle dependencies ourseleves
rm -f *requirements.txt


%build
%{__python2} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Move config to horizon
install -p -D -m 640 enabled/_50_project_containers_panelgroup.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_project_containers_panelgroup.py
install -p -D -m 640 enabled/_51_project_containers_bays_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_51_project_containers_bays_panel.py
install -p -D -m 640 enabled/_52_project_containers_baymodels_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_52_project_containers_baymodels_panel.py
install -p -D -m 640 enabled/_53_project_containers_containers_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_53_project_containers_containers_panel.py


%files
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_5*

%files -n python-%{library}-doc
%license LICENSE
%doc html README.rst


%changelog
* Wed Aug 31 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.0.0-1
- Upstream 1.0.0
