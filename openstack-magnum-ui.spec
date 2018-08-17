%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library magnum-ui
%global module magnum_ui

%global common_desc \
OpenStack Magnum Horizon plugin

Name:       openstack-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Magnum UI Horizon plugin
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  git

Requires:   python2-pbr
Requires:   python2-babel
Requires:   python2-magnumclient >= 2.6.0
Requires:   openstack-dashboard >= 1:13.0.0
Requires:   python2-django >= 1.11
Requires:   python2-django-babel
Requires:   python2-django-compressor >= 2.0
Requires:   python2-django-pyscss >= 2.0.2

%description
%{common_desc}

%package -n python-%{library}-doc
Summary:    OpenStack example library documentation

BuildRequires: python2-sphinx
BuildRequires: python2-django
BuildRequires: python2-django-nose
BuildRequires: openstack-dashboard
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-sphinxcontrib-apidoc
BuildRequires: python2-magnumclient
BuildRequires: python2-mock
BuildRequires: python2-mox3
BuildRequires: openstack-macros

%description -n python-%{library}-doc
%{common_desc}

This package contains the documentation.

%prep
%autosetup -n %{library}-%{upstream_version} -S git
# Let's handle dependencies ourseleves
%py_req_cleanup


%build
%{__python2} setup.py build

# generate html docs
export PYTHONPATH=/usr/share/openstack-dashboard
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Move config to horizon
install -p -D -m 640 %{module}/enabled/_1370_project_container_infra_panel_group.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1370_project_container_infra_panel_group.py
install -p -D -m 640 %{module}/enabled/_1371_project_container_infra_clusters_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1371_project_container_infra_clusters_panel.py
install -p -D -m 640 %{module}/enabled/_1372_project_container_infra_cluster_templates_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1372_project_container_infra_cluster_templates_panel.py


%files
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_137*

%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst


%changelog
