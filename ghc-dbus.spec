%define		pkgname	dbus
Summary:	A Haskell binding to the dbus graphics library
Name:		ghc-%{pkgname}
Version:	0.10.4
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	37d7c18abd7a4b397265e90eed035e92
URL:		http://hackage.haskell.org/package/dbus/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-cereal < 0.4
BuildRequires:	ghc-cereal >= 0.3.4
BuildRequires:	ghc-libxml-sax >= 0.7
BuildRequires:	ghc-network >= 2.2.3
BuildRequires:	ghc-parsec < 3.2
BuildRequires:	ghc-parsec >= 2.0
BuildRequires:	ghc-random >= 1.0
BuildRequires:	ghc-text < 0.12
BuildRequires:	ghc-text >= 0.11.1.5
BuildRequires:	ghc-transformers < 0.4
BuildRequires:	ghc-transformers >= 0.2
BuildRequires:	ghc-vector < 0.11
BuildRequires:	ghc-vector >= 0.7
BuildRequires:	ghc-xml-types >= 0.3
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-cereal < 0.4
Requires:	ghc-cereal >= 0.3.4
Requires:	ghc-libxml-sax >= 0.7
Requires:	ghc-network >= 2.2.3
Requires:	ghc-parsec < 3.2
Requires:	ghc-parsec >= 2.0
Requires:	ghc-random >= 1.0
Requires:	ghc-text < 0.12
Requires:	ghc-text >= 0.11.1.5
Requires:	ghc-transformers < 0.4
Requires:	ghc-transformers >= 0.2
Requires:	ghc-vector < 0.11
Requires:	ghc-vector >= 0.7
Requires:	ghc-xml-types >= 0.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
A Haskell binding to the dbus graphics library.

%package doc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
