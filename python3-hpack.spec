#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (fixtures missing in sdist)

Summary:	HTTP/2 Header Encoding for Python 3
Summary(pl.UTF-8):	Kodowanie nagłówków HTTP/2 dla Pythona 3
Name:		python3-hpack
# keep in sync with python3-h2.spec
Version:	4.0.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/hpack/
Source0:	https://files.pythonhosted.org/packages/source/h/hpack/hpack-%{version}.tar.gz
# Source0-md5:	27e01514ef06dc9fa0798d3dcb7de47c
URL:		https://pypi.org/project/hpack/
BuildRequires:	python3-modules >= 1:3.6.1
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-hypothesis
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg >= 3.2.1
%endif
Requires:	python3-modules >= 1:3.6.1
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
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest test
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst CONTRIBUTORS.rst LICENSE README.rst
%{py3_sitescriptdir}/hpack
%{py3_sitescriptdir}/hpack-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_modules,_static,security,*.html,*.js}
%endif
