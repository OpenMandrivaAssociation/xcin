%define version 2.5.3
%define release 0.pre3.2mdk

%define chewing_version	0.0.5.1
%define canton_version	1.1

Summary:	X Input Method Server for Chinese
Name:		xcin
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Internationalization
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

#Source0:	ftp://xcin.linux.org.tw/pub/xcin/xcin/%name-%version.tar.bz2
Source0:	%{name}-2.5.3.pre3.tar.bz2
# http://hk.geocities.com/chandm9876/canton.htm
Source1:	canton-%{canton_version}.cin.bz2
# http://input.foruto.com/stroke5/
#Source2:	stroke5-%{stroke5_version}.cin.bz2
# http://chewing.good-man.org/
#Source3:	chewing-%{chewing_version}.tar.bz2

# Firefly patches
Patch0:  xcin-2.5.3.pre3-xcinrc.LINUX-20040105.patch.bz2
Patch1:  xcin-2.5.3.pre3-RootStyle-20040102.patch.bz2
Patch2:  xcin-2.5.3.pre3-OverTheSpot-20040102.patch.bz2
Patch3:  xcin-2.5.3.pre3-OnTheSpot-20040105.patch.bz2
Patch4:  xcin-2.5.3.pre3-bimsphone-20040102.patch.bz2
Patch5:  xcin-2.5.3-utf8-makefile-20031223.patch.bz2
Patch6:  xcin-2.5.3.pre3-cin2tab-20040102.patch.bz2
Patch7:  xcin-2.5.3-syscin_utf8.patch.bz2
Patch8:  xcin-2.5.3-cj5_utf8.patch.bz2
Patch9:  xcin-2.5.3-simplex5_utf8.patch.bz2

# Mandrake patches
Patch100:	xcin-2.5.3-extra-im.patch.bz2
Patch101:	xcin-2.5.3-xcinrc-mdk.patch.bz2

Requires:	locales-zh
Requires:	taipeifonts
BuildRequires:	XFree86-devel
BuildRequires:	db4-devel >= 4.1
BuildRequires:	libtabe-devel >= 0.2.4a
BuildRequires:	gettext

%description
Xcin is an X Input Method allowing to type in chinese in X applications that
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

find . -type d -name CVS | xargs -r rm -rf

bzcat %{SOURCE1} > cin/big5/canton.cin

#Install Chewing module
#pushd src/Cinput
#tar --bzip2 -xf %{SOURCE3}
#cd chewing
#./patch_chewing
#popd

%build
# Geoff -- don't use percent-configure because it breaks program.
CFLAGS="%optflags" CXXFLAGS="%optflags" ./configure \
	--build=%_target_platform \
	--prefix=%{_prefix}/X11R6 \
	--libdir=%{_prefix}/X11R6/%{_lib} \
	--with-xcin-dir=%{_prefix}/X11R6/%{_lib}/X11/xcin \
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

# remove unneeded files
rm -f %{buildroot}%{_prefix}/X11R6/lib/libxcin.{a,la}

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/* 
%dir %{_sysconfdir}/chinese/xcin
%config(noreplace) %{_sysconfdir}/chinese/xcin/*
%{_prefix}/X11R6/bin/*
%{_prefix}/X11R6/%{_lib}/X11/xcin
%{_prefix}/X11R6/%{_lib}/libxcin*
%{_prefix}/X11R6/man/man1/*

%clean
rm -rf %{buildroot}
