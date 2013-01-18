%define	major	0
%define	libname	%mklibname gpg-error %{major}
%define	devname	%mklibname gpg-error -d

%bcond_without	uclibc

Summary:	Library containing common error values for GnuPG components
Name:		libgpg-error
Version:	1.10
Release:	5
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gnupg.org/
Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
# comment out to workaround abf issue
#Source1:	%{SOURCE0}.sig
Patch0:		libgpg-error-1.9-libdir.patch
Patch1:		libgpg-error-1.10-pkgconfig.patch
BuildRequires:	gettext-devel
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
%configure2_5x
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

%files -n %{libname}
/%{_lib}/libgpg-error.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libgpg-error.so.%{major}*
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

%changelog
* Wed Dec 12 2012 Per Øyvind Karlesn <peroyvind@mandriva.org> 1.10-5
- rebuild on ABF

* Mon Oct 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.10-4
+ Revision: 820314
- drop bogus provides
- move library to /%%{_lib}
- do uclibc build
- make libgpg-common package noarch
- add pkgconfig support (P1, from OpenEmbedded)
- cleanups

* Fri Mar 16 2012 Oden Eriksson <oeriksson@mandriva.com> 1.10-3
+ Revision: 785355
- fix build
- nuke the libtool *.la file
- various fixes

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.10-2
+ Revision: 661451
- rebuild

* Mon Dec 06 2010 Funda Wang <fwang@mandriva.org> 1.10-1mdv2011.0
+ Revision: 611880
- new version 1.10

* Sun Aug 15 2010 Emmanuel Andry <eandry@mandriva.org> 1.9-1mdv2011.0
+ Revision: 570194
- New version 1.9
- rediff p0
- update files list

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7-2mdv2010.1
+ Revision: 520864
- rebuilt for 2010.1

* Wed Jan 07 2009 Emmanuel Andry <eandry@mandriva.org> 1.7-1mdv2009.1
+ Revision: 326808
- New version 1.7

* Wed Jun 18 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 1.6-4mdv2009.0
+ Revision: 224736
- Rebuild because of missing packages

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.6-3mdv2009.0
+ Revision: 222834
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jan 13 2008 Anssi Hannula <anssi@mandriva.org> 1.6-2mdv2008.1
+ Revision: 150903
- move locale files to new package libgpg-error-common

* Sat Jan 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.6-1mdv2008.1
+ Revision: 149222
- mark gpg-error-config as a multi arch binary
- new license policy
- new devel library policy
- add %%check section
- spec file clean
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Mon Nov 06 2006 Andreas Hasenack <andreas@mandriva.com> 1.4-1mdv2007.0
+ Revision: 77026
- updated to version 1.4
- added lisp files to devel package
- bunzipped patch
- Import libgpg-error

* Mon Jul 24 2006 Emmanuel Andry <eandry@mandriva.org> 1.3-1mdv2007.0
- New release 1.3

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.1-2mdk
- Rebuild

* Thu Aug 25 2005 Abel Cheung <deaddog@mandriva.org> 1.1-1mdk
- New release 1.1

* Fri Mar 11 2005 Stefan van der Eijk <stefan@eijk.nu> 1.0-4mdk
- reupload --> lost during ken crash

* Mon Feb 28 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0-3mdk
- drop lib64 patch in favor of total nuking of -L$(libdir) where
  libdir is a standard library search path (multiarch)

* Wed Feb 09 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0-2mdk
- lib64/multiarch fixes

* Fri Aug 20 2004 Abel Cheung <deaddog@deaddog.org> 1.0-1mdk
- New version
- Remove P0 (upstream)

* Fri May 21 2004 Abel Cheung <deaddog@deaddog.org> 0.7-2mdk
- Patch0: automake 1.8 compatibility

* Fri May 21 2004 Abel Cheung <deaddog@deaddog.org> 0.7-1mdk
- New version

* Mon Dec 08 2003 Abel Cheung <deaddog@deaddog.org> 0.6-1mdk
- 0.6
- Patch not needed
- Use tar.gz instead and include signature, to prove source legitimacy

