%define major 0
%define libname %mklibname gpg-error %{major}
%define devname %mklibname gpg-error -d

%bcond_without uclibc

Summary:	Library containing common error values for GnuPG components
Name:		libgpg-error
Version:	1.19
Release:	3
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnupg.org/
Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
# comment out to workaround abf issue
#Source1:	%{SOURCE0}.sig
Source2:	%{name}.rpmlintrc
Patch0:		libgpg-error-1.16-libdir.patch
Patch1:		libgpg-error-1.19-pkgconfig.patch
BuildRequires:	gettext-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
BuildRequires:	uclibc-gettext-devel
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
Requires:	%{name}-common >= %{version}-%{release}

%description -n	%{libname}
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%if %{with uclibc}
%package -n	uclibc-%{libname}
Summary:	Library containing common error values for GnuPG components (uClibc build)
Group:		System/Libraries

%description -n	uclibc-%{libname}
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package -n	uclibc-%{devname}
Summary:	Development related files of %{name}
Group:		Development/Other
Provides:	uclibc-%{name}-devel = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}
Requires:	uclibc-%{libname} = %{version}-%{release}
Conflicts:	%{devname} < 1.19-2

%description -n	uclibc-%{devname}
This package contains headers and other necessary files to develop 
or compile applications that use %{name}.
%endif

%package -n	%{devname}
Summary:	Development related files of %{name}
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{devname}
This package contains headers and other necessary files to develop 
or compile applications that use %{name}.

%prep
%setup -q
%apply_patches

%build
#fix build with new automake
sed -i -e 's,AM_PROG_MKDIR_P,AC_PROG_MKDIR_P,g' configure.*
autoreconf -fi
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
%configure
%make
popd

%check
make -C system check

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
mkdir -p %{buildroot}%{uclibc_root}/%{_lib}
mv %{buildroot}%{uclibc_root}%{_libdir}/libgpg-error.so.%{major}* %{buildroot}%{uclibc_root}/%{_lib}
ln -srf %{buildroot}%{uclibc_root}/%{_lib}/libgpg-error.so.%{major}.*.* %{buildroot}%{uclibc_root}%{_libdir}/libgpg-error.so

rm -r %{buildroot}%{uclibc_root}%{_libdir}/pkgconfig
rm -r %{buildroot}%{uclibc_root}%{_bindir}
%endif

%makeinstall_std -C system

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libgpg-error.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libgpg-error.so.%{major}.*.* %{buildroot}%{_libdir}/libgpg-error.so

%multiarch_binaries %{buildroot}%{_bindir}/gpg-error-config

%find_lang %{name}

%files common -f %{name}.lang
%{_datadir}/info/gpgrt.info.*
%{_mandir}/man1/gpg-error-config.1.*

%files -n %{libname}
/%{_lib}/libgpg-error.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libgpg-error.so.%{major}*

%files -n uclibc-%{devname}
%{uclibc_root}%{_libdir}/libgpg-error.so
%endif

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

