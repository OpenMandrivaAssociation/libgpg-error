%define	version 1.4
%define release %mkrel 1

%define major 0
%define libname %mklibname gpg-error %{major}

Summary:	Library containing common error values for GnuPG components
Name:		libgpg-error
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://www.gnupg.org/

Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2.sig
Patch0:		libgpg-error-1.0-libdir.patch

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.


%package	-n %{libname}
Summary:	Library containing common error values for GnuPG components
Group:		System/Libraries
Provides:	%{name} = %{version}

%description	-n %{libname}
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package	-n %{libname}-devel
Summary:	Development related files of %{name}
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}

%description	-n %{libname}-devel
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
make check

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}


%files -n %{libname} -f %{name}.lang
%defattr(-,root,root)
%doc COPYING COPYING.LIB
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/*
%{_datadir}/aclocal/*.m4
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_includedir}/*
%{_datadir}/common-lisp/source/gpg-error



