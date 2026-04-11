%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)

%define libname %mklibname SonicDE
%define devname %mklibname SonicDE -d
#define git 20240222
%define gitbranch Plasma/6.6
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

Name: sonic-interface-libraries
Version: 6.6.4
Release: %{?git:0.%{git}.}1
URL: https://github.com/Sonic-DE/%name

# %if 0%{?git:1}
# Source0: https://invent.kde.org/plasma/libplasma/-/archive/%{gitbranch}/libplasma-%{gitbranchd}.tar.bz2#/libplasma-%{git}.tar.bz2
# %else
Source0: %url/archive/%version/%name-%version.tar.gz
# %endif

Summary: Foundational libraries, components, and tools of the SonicDE workspaces

License: CC0-1.0 LGPL-2.0+ LGPL-2.1 LGPL-3.0
Group: System/Libraries

BuildRequires: cmake(ECM)
BuildRequires: python
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6QmlTools)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6GuiTools)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: gettext
BuildRequires: doxygen
BuildRequires: cmake(Qt6ToolsTools)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6QuickControls2)
BuildRequires: cmake(KF6Kirigami2)

# pending rename
# BuildRequires: cmake(PlasmaActivities)
BuildRequires: %{_lib}SonicDEActivities-devel

BuildRequires: cmake(KF6Archive)
BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6ConfigWidgets)
BuildRequires: cmake(KF6CoreAddons)

# pending rewrite
# BuildRequires: cmake(KF6GlobalAccel)
BuildRequires: %{_lib}SonicDEKeybindDaemon-devel

BuildRequires: cmake(KF6GuiAddons)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6IconThemes)

# pending rewrite
# BuildRequires: cmake(KF6KIO)
# BuildRequires: cmake(KF6WindowSystem)
BuildRequires: %{_lib}SonicFrameworksIO-devel
BuildRequires: %{_lib}SonicFrameworksWindowSystem-devel

BuildRequires: cmake(KF6XmlGui)
BuildRequires: cmake(KF6Notifications)
BuildRequires: cmake(KF6Package)
BuildRequires: cmake(KF6KCMUtils)
BuildRequires: cmake(KF6Svg)

BuildSystem: cmake
BuildOption: -DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON
BuildOption: -DBUILD_QCH:BOOL=ON
Requires: %{libname} = %{EVRD}
Requires: sonic-framework-common = %{EVRD}

Conflicts:      libplasma
#patchlist

%description
%summary

%package -n %{libname}
Summary: Foundational libraries, components, and tools of the SonicDE workspaces
Group: System/Libraries
Requires: %{name} = %{EVRD}
Conflicts:       %{_lib}Plasma

%description -n %{libname}
%summary

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}
Conflicts:  %{_lib}Plasma-devel

%description -n %{devname}
%summary

%package -n sonic-framework-common
Summary: SonicDE Framework data files
Group: System/Libraries
Conflicts: plasma-framework-common

%description -n sonic-framework-common
%summary

%package doc
Summary: API documentation for %{name} in Qt Assistant format
Group: Development/C++

%description doc
%summary

%install -a
find %{buildroot}%{_datadir}/locale -name "*.js" |while read r; do
    L=$(echo $r |rev |cut -d/ -f4 |rev)
    echo "%%lang($L) %%{_datadir}/locale/$L/LC_SCRIPTS/libplasma6/$(basename $r)" >>%{name}.lang
done

%files -f %{name}.lang
%{_datadir}/qlogging-categories6/plasma-framework.categories
%{_datadir}/qlogging-categories6/plasma-framework.renamecategories

%files -n %{devname}
%{_includedir}/Plasma
%{_includedir}/PlasmaQuick
%{_libdir}/cmake/Plasma
%{_libdir}/cmake/PlasmaQuick
%{_datadir}/kdevappwizard/templates/*

%files -n %{libname}
%{_libdir}/libPlasma.so*
%{_libdir}/libPlasmaQuick.so*
# FIXME owning the whole /org namespace here
# may be a bit excessive, but there's probably
# no better place
%dir %{_qtdir}/qml/org
%{_qtdir}/qml/org/kde
%{_qtdir}/plugins/kf6/kirigami
%{_qtdir}/plugins/kf6/packagestructure

%files -n sonic-framework-common
%dir %{_datadir}/plasma
%{_datadir}/plasma/desktoptheme

%files doc
%{_qtdir}/doc/Plasma.*
