%define major 0
%define libname %mklibname %name %major
%define develname %mklibname %name -d
%define canton_version	1.1

Summary:	X Input Method Server for Chinese
Name:		xcin
Version:	2.5.3
Release:	6.pre3.7
License:	GPL
Group:		System/Internationalization
#Source0:	ftp://xcin.linux.org.tw/pub/xcin/xcin/%name-%version.tar.bz2
Source0:	%{name}-2.5.3.pre3.tar.bz2
# http://hk.geocities.com/chandm9876/canton.htm
Source1:	canton-%{canton_version}.cin.bz2
# Firefly patches
Patch0:  xcin-2.5.3.pre3-xcinrc.LINUX-20040105.patch
Patch1:  xcin-2.5.3.pre3-RootStyle-20040102.patch
Patch2:  xcin-2.5.3.pre3-OverTheSpot-20040102.patch
Patch3:  xcin-2.5.3.pre3-OnTheSpot-20040105.patch
Patch4:  xcin-2.5.3.pre3-bimsphone-20040102.patch
Patch5:  xcin-2.5.3-utf8-makefile-20031223.patch
Patch6:  xcin-2.5.3.pre3-cin2tab-20040102.patch
Patch7:  xcin-2.5.3-syscin_utf8.patch
Patch8:  xcin-2.5.3-cj5_utf8.patch
Patch9:  xcin-2.5.3-simplex5_utf8.patch
# Mandriva patches
Patch100:	xcin-2.5.3-extra-im.patch
Patch101:	xcin-2.5.3-xcinrc-mdk.patch
# From Fedora
Patch102:	xcin-2.5.3-no_rpath.patch
Requires:	locales-zh
Requires:	taipeifonts
Requires:	tabe
BuildRequires:	X11-devel
BuildRequires:	db-devel
BuildRequires:	tabe-devel
BuildRequires:	gettext
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Xcin is an X Input Method allowing to type in Chinese in X applications that
follow the XIM input method standard.

%package -n %libname
Group: System/Libraries
Summary: Shared libraries of xcin

%description -n %libname
Xcin is an X Input Method allowing to type in Chinese in X applications that
follow the XIM input method standard.

%package -n %develname
Group: Development/C
Summary: Development libraries of xcin
Requires: %libname = %version
Provides: lib%name-devel = %version-%release
Obsoletes: %{mklibname xcin 0 -d}

%description -n %develname
Xcin is an X Input Method allowing to type in Chinese in X applications that
follow the XIM input method standard.

%prep

%setup -q -n %{name}
%patch0 -p1
%patch1 -p1 -b .Rootstyle
%patch2 -p1 -b .OverTheSpot
%patch3 -p1 -b .OnTheSpot
%patch4 -p1 -b .bimsphone
%patch5 -p1 -b .utf8-makefile
%patch6 -p1 -b .cin2tab
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch100 -p1 -b .extra-im
%patch101 -p1 -b .mdk
%patch102 -p1 -b .rpath

find . -type d -name CVS | xargs -r rm -rf

bzcat %{SOURCE1} > cin/big5/canton.cin

#Install Chewing module
#pushd src/Cinput
#tar --bzip2 -xf %{SOURCE3}
#cd chewing
#./patch_chewing
#popd

%build
# From SUSE: re-generating configure fixes x86-64 build
mv script/configure.in .
# AdamW: Look for tabe .db files in /usr/share/tabe not /usr/lib/tabe
perl -pi -e 's,/lib/tabe,/share/tabe,g' configure.in
rm -f configure
autoreconf -i
# Geoff -- don't use percent-configure because it breaks program.
CFLAGS="%optflags" CXXFLAGS="%optflags" ./configure \
	--build=%_target_platform \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--with-xcin-dir=%{_prefix}/lib/xcin \
	--with-xcin-rcdir=%{_sysconfdir}/chinese/xcin \
	--with-dbinc=%{_includedir}/db4 \
	--with-locale-dir=%{_datadir}/locale \
	--with-extra-prefix=%{_prefix}

#Dadou - 2.5.2-6mdk - Don't use make macro. It breaks build.
make

%install
rm -rf %{buildroot}

export program_prefix=%{buildroot}
export xcin_rcp=%{buildroot}/%{_sysconfdir}/chinese/xcin
make -e install

%find_lang %{name}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/Bugs doc/CREDITS doc/Changes doc/Cin doc/En doc/FAQ doc/README doc/SETUP doc/Todo doc/Usage doc/UserGuide doc/internal doc/modules
%dir %{_sysconfdir}/chinese/xcin
%config(noreplace) %{_sysconfdir}/chinese/xcin/*
%{_bindir}/*
%{_prefix}/lib/%{name}
%{_mandir}/man1/*

%files -n %libname
%defattr(-,root,root)
%_libdir/lib*.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%_libdir/lib*.so
%attr(644,root,root) %_libdir/lib*a
