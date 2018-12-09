%define major 0
%define libname %mklibname gpg-error %{major}
%define devname %mklibname gpg-error -d
%define staticname %mklibname gpg-error -d -s

Summary:	Library containing common error values for GnuPG components
Name:		libgpg-error
Version:	1.33
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnupg.org/
Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Source2:	%{name}.rpmlintrc
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(readline)
BuildRequires:	hostname

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package common
Summary:	Common files for libgpg-error
Group:		System/Libraries
BuildArch:	noarch
Conflicts:	libgpg-error < 1.7

%description common
This package contains the common files that are used by the
libgpg-error library.

%package -n %{libname}
Summary:	Library containing common error values for GnuPG components
Group:		System/Libraries

%description -n %{libname}
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package -n %{devname}
Summary:	Development related files of %{name}
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package contains headers and other necessary files to develop 
or compile applications that use %{name}.

%package -n %{staticname}
Summary:	Library files needed for linking statically to %{name}
Group:		Development/C
Provides:	gpg-error-static-devel = %{EVRD}
Provides:	libgpg-error-static-devel = %{EVRD}
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
Library files needed for linking statically to %{name}

%prep
%autosetup -p1

%build
%configure --enable-static
%make_build

%check
make check

%install
%make_install

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libgpg-error.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libgpg-error.so.%{major}.*.* %{buildroot}%{_libdir}/libgpg-error.so

%if %{mdvver} <= 3000000
%multiarch_binaries %{buildroot}%{_bindir}/gpg-error-config
%endif

%find_lang %{name}

%files common -f %{name}.lang
%{_datadir}/info/gpgrt.info.*

%files -n %{libname}
/%{_lib}/libgpg-error.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS README
%if %{mdvver} <= 3000000
%{multiarch_bindir}/gpg-error-config
%endif
%{_bindir}/gpg-error
%{_bindir}/gpg-error-config
%{_bindir}/gpgrt-config
%{_bindir}/yat2m
%{_datadir}/aclocal/gpg-error.m4
%{_libdir}/libgpg-error.so
%{_libdir}/pkgconfig/gpg-error.pc
%{_includedir}/gpg-error.h
%{_includedir}/gpgrt.h
%{_datadir}/common-lisp/source/gpg-error
%{_datadir}/%{name}/errorref.txt
%{_datadir}/aclocal/gpgrt.m4

%files -n %{staticname}
%{_libdir}/*.a
