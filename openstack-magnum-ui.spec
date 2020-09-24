%global milestone .0rc1
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library magnum-ui
%global module magnum_ui
%global with_doc 1

%global common_desc \
OpenStack Magnum Horizon plugin

Name:       openstack-%{library}
Version:    7.0.0
Release:    0.1%{?milestone}%{?dist}
Summary:    OpenStack Magnum UI Horizon plugin
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

#
# patches_base=7.0.0.0rc1
#

BuildArch:  noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python3-django
BuildRequires:  python3-django-nose
BuildRequires:  openstack-dashboard
BuildRequires:  python3-magnumclient
BuildRequires:  python3-heatclient
BuildRequires:  python3-mock
BuildRequires:  python3-mox3
BuildRequires:  python3-pytest
Requires:   python3-pbr
Requires:   python3-heatclient >= 1.18.0
Requires:   python3-magnumclient >= 2.15.0
Requires:   python3-django-babel
Requires:   python3-django-pyscss >= 2.0.2
Requires:   openstack-dashboard >= 1:17.1.0

%description
%{common_desc}

%if 0%{?with_doc}
%package -n python3-%{library}-doc
Summary:    OpenStack example library documentation
%{?python_provide:%python_provide python3-%{library}-doc}
BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme
BuildRequires: python3-sphinxcontrib-apidoc

%description -n python3-%{library}-doc
%{common_desc}

This package contains the documentation.
%endif

%prep
%autosetup -n %{library}-%{upstream_version} -S git
# Let's handle dependencies ourseleves
%py_req_cleanup


%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.:/usr/share/openstack-dashboard
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

# Move config to horizon
install -p -D -m 644 %{module}/enabled/_1370_project_container_infra_panel_group.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1370_project_container_infra_panel_group.py
install -p -D -m 644 %{module}/enabled/_1371_project_container_infra_clusters_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1371_project_container_infra_clusters_panel.py
install -p -D -m 644 %{module}/enabled/_1372_project_container_infra_cluster_templates_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1372_project_container_infra_cluster_templates_panel.py


%files
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_137*

%if 0%{?with_doc}
%files -n python3-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif


%changelog
* Thu Sep 24 2020 RDO <dev@lists.rdoproject.org> 7.0.0-0.1.0rc1
- Update to 7.0.0.0rc1

