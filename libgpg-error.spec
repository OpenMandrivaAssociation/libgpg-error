%define	major	0
%define	libname	%mklibname gpg-error %{major}
%define	devname	%mklibname gpg-error -d

%bcond_without	uclibc

Summary:	Library containing common error values for GnuPG components
Name:		libgpg-error
Version:	1.10
Release:	3
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gnupg.org/
Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Source1:	%{SOURCE0}.sig
Patch0:		libgpg-error-1.9-libdir.patch
Patch1:		libgpg-error-1.10-pkgconfig.patch
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
%endif

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package	common
Summary:	Common files for libgpg-error
Group:		System/Libraries
BuildArch:	noarch
Conflicts:	libgpg-error < 1.7

%description	common
This package contains the common files that are used by the
libgpg-error library.

%package -n	%{libname}
Summary:	Library containing common error values for GnuPG components
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Requires:	%{name}-common >= %{version}-%{release}

%description -n	%{libname}
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package -n	uclibc-%{libname}
Summary:	Library containing common error values for GnuPG components (uClibc build)
Group:		System/Libraries

%description -n	uclibc-%{libname}
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package -n	%{devname}
Summary:	Development related files of %{name}
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{version}-%{release}
%endif
Obsoletes:	%mklibname gpg-error 0 -d

%description -n	%{devname}
%{name} is a library that defines common error values for all
GnuPG components.  Among these are GPG, GPGSM, GPGME, GPG-Agent,
libgcrypt, pinentry, SmartCard Daemon and possibly more in the future.

This package contains headers and other necessary files to develop 
or compile applications that use %{name}.

%prep
%setup -q
%patch0 -p0 -b .libdir~
%patch1 -p1 -b .pkgconf~
autoreconf -f

%build
CONFIGURE_TOP="$PWD"
%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure
%make
popd
%endif

mkdir -p system
pushd system
%configure2_5x
%make
popd

%check
make -C system check

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
rm -r %{buildroot}%{uclibc_root}%{_libdir}/pkgconfig
rm -r %{buildroot}%{uclibc_root}%{_bindir}
%endif

%makeinstall_std -C system

%multiarch_binaries %{buildroot}%{_bindir}/gpg-error-config

%find_lang %{name}

%files common -f %{name}.lang

%files -n %{libname}
%{_libdir}/libgpg-error.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/libgpg-error.so.%{major}*
%endif

%files -n %{devname}
%doc AUTHORS ChangeLog NEWS README
%{multiarch_bindir}/gpg-error-config
%{_bindir}/gpg-error
%{_bindir}/gpg-error-config
%{_datadir}/aclocal/gpg-error.m4
%{_libdir}/libgpg-error.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libgpg-error.so
%endif
%{_libdir}/pkgconfig/gpg-error.pc
%{_includedir}/gpg-error.h
%{_datadir}/common-lisp/source/gpg-error
