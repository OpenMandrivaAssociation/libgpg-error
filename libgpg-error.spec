%define	major	0
%define	libname	%mklibname gpg-error %{major}
%define	devname	%mklibname gpg-error -d

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

%package -n	%{devname}
Summary:	Development related files of %{name}
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
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
%configure2_5x
%make

%check
make check

%install
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/gpg-error-config

%find_lang %{name}

%files common -f %{name}.lang

%files -n %{libname}
%{_libdir}/libgpg-error.so.%{major}*

%files -n %{devname}
%doc AUTHORS ChangeLog NEWS README
%{multiarch_bindir}/gpg-error-config
%{_bindir}/gpg-error
%{_bindir}/gpg-error-config
%{_datadir}/aclocal/gpg-error.m4
%{_libdir}/libgpg-error.so
%{_libdir}/pkgconfig/gpg-error.pc
%{_includedir}/gpg-error.h
%{_datadir}/common-lisp/source/gpg-error
