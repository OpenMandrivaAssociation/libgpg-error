%define major 0
%define libname %mklibname gpg-error %{major}
%define devname %mklibname gpg-error -d
%define staticname %mklibname gpg-error -d -s

# libgpg-error is used by libgcrypt, which in turn is used
# by gnutls and libxslt, which in turn are used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
%if %{with compat32}
%define lib32name libgpg-error%{major}
%define dev32name libgpg-error-devel
%define static32name libgpg-error-static-devel
%endif

Summary:	Library containing common error values for GnuPG components
Name:		libgpg-error
Version:	1.48
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnupg.org/
Source0:	https://www.gnupg.org/ftp/gcrypt/libgpg-error/libgpg-error-%{version}.tar.bz2
Source2:	%{name}.rpmlintrc
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(readline)
BuildRequires:	hostname
%if %{with compat32}
BuildRequires:	devel(libncursesw)
%endif

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package common
Summary:	Common files for libgpg-error
Group:		System/Libraries
Conflicts:	libgpg-error < 1.7

%description common
This package contains the common files that are used by the
libgpg-error library.

%package -n %{libname}
Summary:	Library containing common error values for GnuPG components
Group:		System/Libraries
Requires(meta):	%{name}-common

%description -n %{libname}
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package -n %{devname}
Summary:	Development related files of %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package contains headers and other necessary files to develop
or compile applications that use %{name}.

%package -n %{staticname}
Summary:	Library files needed for linking statically to %{name}
Group:		Development/C
Provides:	gpg-error-static-devel = %{EVRD}
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
Library files needed for linking statically to %{name}

%if %{with compat32}
%package -n %{lib32name}
Summary:	Library containing common error values for GnuPG components (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package -n %{dev32name}
Summary:	Development related files of %{name} (32-bit)
Group:		Development/Other
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
This package contains headers and other necessary files to develop
or compile applications that use %{name}.

%package -n %{static32name}
Summary:	Library files needed for linking statically to %{name} (32-bit)
Group:		Development/C
Requires:	%{dev32name} = %{EVRD}

%description -n %{static32name}
Library files needed for linking statically to %{name}
%endif

%prep
%autosetup -p1
%config_update

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32 --enable-static
cd ..
%endif
mkdir build
cd build
%configure \
	--enable-static \
	--enable-install-gpg-error-config

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%if ! %{cross_compiling}
%check
%if %{with compat32}
make check -C build32
%endif
make check -C build
%endif

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

%find_lang %{name}

%files common -f %{name}.lang
%{_bindir}/gpg-error
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/errorref.txt

%files -n %{libname}
%{_libdir}/libgpg-error.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS README
%{_bindir}/gpg-error-config
%{_bindir}/gpgrt-config
%{_bindir}/yat2m
%{_datadir}/aclocal/gpg-error.m4
%{_libdir}/libgpg-error.so
%{_libdir}/pkgconfig/gpg-error.pc
%{_includedir}/gpg-error.h
%{_includedir}/gpgrt.h
%{_datadir}/common-lisp/source/gpg-error
%{_datadir}/aclocal/gpgrt.m4
%doc %{_infodir}/gpgrt.info.*
%doc %{_mandir}/man1/gpgrt-config.1*
%doc %{_mandir}/man1/gpg-error-config.1*

%files -n %{staticname}
%{_libdir}/*.a

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/lib*.so.*

%files -n %{dev32name}
%{_prefix}/lib/lib*.so
%{_prefix}/lib/pkgconfig/*.pc

%files -n %{static32name}
%{_prefix}/lib/lib*.a
%endif
