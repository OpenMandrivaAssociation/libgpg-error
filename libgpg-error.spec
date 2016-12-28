%define major 0
%define libname %mklibname gpg-error %{major}
%define devname %mklibname gpg-error -d
%define staticname %mklibname gpg-error -d -s

Summary:	Library containing common error values for GnuPG components
Name:		libgpg-error
Version:	1.26
Release:	1
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

%description -n	%{libname}
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package -n	%{devname}
Summary:	Development related files of %{name}
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{devname}
This package contains headers and other necessary files to develop 
or compile applications that use %{name}.

%package -n	%{staticname}
Summary:	Library files needed for linking statically to %name
Group:		Development/C
Provides:	gpg-error-static-devel = %{EVRD}
Provides:	libgpg-error-static-devel = %{EVRD}
Requires:	%devname = %EVRD

%description -n %{staticname}
Library files needed for linking statically to %name

%prep
%setup -q
%apply_patches

%build
#fix build with new automake
sed -i -e 's,AM_PROG_MKDIR_P,AC_PROG_MKDIR_P,g' configure.*
autoreconf -fi
CONFIGURE_TOP="$PWD"

mkdir -p system
pushd system
%configure --enable-static
%make
popd

%check
make -C system check

%install
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
%{_datadir}/%{name}/errorref.txt

%files -n %staticname
%_libdir/*.a
