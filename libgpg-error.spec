%define	version 1.6
%define release %mkrel 2

%define major 0
%define libname %mklibname gpg-error %{major}
%define develname %mklibname gpg-error -d

Summary:	Library containing common error values for GnuPG components
Name:		libgpg-error
Version:	%{version}
Release:	%{release}
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gnupg.org/
Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Source1:	%{SOURCE0}.sig
Patch0:		libgpg-error-1.0-libdir.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-root

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package common
Summary:	Common files for libgpg-error
Group:		System/Libraries
Conflicts:	libgpg-error < 1.6-2

%description common
This package contains the common files that are used by the
libgpg-error library.

%package -n %{libname}
Summary:	Library containing common error values for GnuPG components
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Requires:	%{name}-common >= %{version}-%{release}

%description -n %{libname}
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package -n %{develname}
Summary:	Development related files of %{name}
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname gpg-error 0 -d
Provides:	%mklibname gpg-error 0 -d

%description -n %{develname}
%{name} is a library that defines common error values for all
GnuPG components.  Among these are GPG, GPGSM, GPGME, GPG-Agent,
libgcrypt, pinentry, SmartCard Daemon and possibly more in the future.

This package contains headers and other necessary files to develop 
or compile applications that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .libdir

%build
%configure2_5x
%make

%check
make check

%install
rm -rf %{buildroot}
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/gpg-error-config

%find_lang %{name}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files common -f %{name}.lang
%defattr(-,root,root)

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/*
%{multiarch_bindir}/gpg-error-config
%{_datadir}/aclocal/*.m4
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_includedir}/*
%{_datadir}/common-lisp/source/gpg-error
