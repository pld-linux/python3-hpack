#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (fixtures missing in sdist)

Summary:	HTTP/2 Header Encoding for Python 3
Summary(pl.UTF-8):	Kodowanie nagłówków HTTP/2 dla Pythona 3
Name:		python3-hpack
# keep in sync with python3-h2.spec (<5 in h2 4.1)
Version:	4.1.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/hpack/
Source0:	https://files.pythonhosted.org/packages/source/h/hpack/hpack-%{version}.tar.gz
# Source0-md5:	16e7423c5b5078c1997fa3eedd2e5935
URL:		https://pypi.org/project/hpack/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-hypothesis >= 6.119.4
BuildRequires:	python3-pytest >= 8.3.3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg-3 >= 7.4.7
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module contains a pure-Python HTTP/2 header encoding (HPACK)
logic for use in Python programs that implement HTTP/2.

%description -l pl.UTF-8
Ten moduł zawiera czysto pythonową logikę kodowania nagłówków HTTP/2
(HPACK) dla programów, które implementują HTTP/2.

%package apidocs
Summary:	API documentation for Python hpack module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona hpack
Group:		Documentation

%description apidocs
API documentation for Python hpack module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona hpack.

%prep
%setup -q -n hpack-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst CONTRIBUTORS.rst LICENSE README.rst
%{py3_sitescriptdir}/hpack
%{py3_sitescriptdir}/hpack-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_modules,_static,security,*.html,*.js}
%endif
