#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	HTTP/2 Header Encoding for Python 2
Summary(pl.UTF-8):	Kodowanie nagłówków HTTP/2 dla Pythona 2
Name:		python-hpack
Version:	3.0.0
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/hpack/
Source0:	https://files.pythonhosted.org/packages/source/h/hpack/hpack-%{version}.tar.gz
# Source0-md5:	556b0ae66180f54c2ce8029a0952088b
URL:		https://pypi.org/project/hpack/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-hypothesis
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-hypothesis
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module contains a pure-Python HTTP/2 header encoding (HPACK)
logic for use in Python programs that implement HTTP/2.

%description -l pl.UTF-8
Ten moduł zawiera czysto pythonową logikę kodowania nagłówków HTTP/2
(HPACK) dla programów, które implementują HTTP/2.

%package -n python3-hpack
Summary:	HTTP/2 Header Encoding for Python 3
Summary(pl.UTF-8):	Kodowanie nagłówków HTTP/2 dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-hpack
This module contains a pure-Python HTTP/2 header encoding (HPACK)
logic for use in Python programs that implement HTTP/2.

%description -n python3-hpack -l pl.UTF-8
Ten moduł zawiera czysto pythonową logikę kodowania nagłówków HTTP/2
(HPACK) dla programów, które implementują HTTP/2.

%prep
%setup -q -n hpack-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
# test_hpack_integration.py requires test_fixtures not included in release tarball
%{__python} -m pytest test -k 'not TestHPACKDecoderIntegration'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pytest test -k 'not TestHPACKDecoderIntegration'
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS.rst HISTORY.rst LICENSE README.rst
%{py_sitescriptdir}/hpack
%{py_sitescriptdir}/hpack-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-hpack
%defattr(644,root,root,755)
%doc CONTRIBUTORS.rst HISTORY.rst LICENSE README.rst
%{py3_sitescriptdir}/hpack
%{py3_sitescriptdir}/hpack-%{version}-py*.egg-info
%endif
