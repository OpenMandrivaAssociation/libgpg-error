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

%global _disable_lto 1

Summary:	Library containing common error values for GnuPG components
Name:		libgpg-error
Version:	1.46
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
%configure --enable-static

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%check
%if %{with compat32}
make check -C build32
%endif
make check -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

%find_lang %{name}

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

%files common -f %{name}.lang
%{_datadir}/info/gpgrt.info.*

%files -n %{libname}
%{_libdir}/libgpg-error.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS README
%{_bindir}/gpg-error
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

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/lib*.so.*

%files -n %{dev32name}
%{_prefix}/lib/lib*.so
%{_prefix}/lib/pkgconfig/*.pc

%files -n %{static32name}
%{_prefix}/lib/lib*.a
%endif
