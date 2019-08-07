# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library magnum-ui
%global module magnum_ui
%global with_doc 1

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

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

Requires:   python%{pyver}-pbr
Requires:   python%{pyver}-babel
Requires:   python%{pyver}-magnumclient >= 2.11.0
Requires:   openstack-dashboard >= 1:15.0.0
Requires:   python%{pyver}-django >= 1.11
Requires:   python%{pyver}-django-babel
Requires:   python%{pyver}-django-compressor >= 2.0
Requires:   python%{pyver}-django-pyscss >= 2.0.2

%description
%{common_desc}

%if 0%{?with_doc}
%package -n python%{pyver}-%{library}-doc
Summary:    OpenStack example library documentation
%{?python_provide:%python_provide python%{pyver}-%{library}-doc}

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-django
BuildRequires: python%{pyver}-django-nose
BuildRequires: openstack-dashboard
BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-sphinxcontrib-apidoc
BuildRequires: python%{pyver}-magnumclient
BuildRequires: python%{pyver}-mock
BuildRequires: python%{pyver}-mox3

%description -n python%{pyver}-%{library}-doc
%{common_desc}

This package contains the documentation.
%endif

%prep
%autosetup -n %{library}-%{upstream_version} -S git
# Let's handle dependencies ourseleves
%py_req_cleanup


%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.:/usr/share/openstack-dashboard
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Move config to horizon
install -p -D -m 640 %{module}/enabled/_1370_project_container_infra_panel_group.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1370_project_container_infra_panel_group.py
install -p -D -m 640 %{module}/enabled/_1371_project_container_infra_clusters_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1371_project_container_infra_clusters_panel.py
install -p -D -m 640 %{module}/enabled/_1372_project_container_infra_cluster_templates_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1372_project_container_infra_cluster_templates_panel.py


%files
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_137*

%if 0%{?with_doc}
%files -n python%{pyver}-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif


%changelog
