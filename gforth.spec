%define name  gforth
%define release %mkrel 6
%define version 0.6.2

Name:		%name
Release:	%release
Version:	%version
License:	GPL
Group:		Development/Other
Summary:	GNU Forth
Url:		http://www.jwdt.com/~paysan/gforth.html
Source:		%name-%version.tar.bz2
Source16:	gnu-forth.16.png
Source32:	gnu-forth.32.png
Source48:	gnu-forth.48.png
BuildRoot:	%_tmppath/%name-%version-%release
BuildRequires:	emacs-bin

%description
Gforth is a fast and portable implementation of the ANS Forth language. 

%prep 

%setup -q

%build
# need to rebuild from these
#touch engine/prim.i engine/prim_lab.i

%configure2_5x CC="gcc -fno-reorder-blocks"

make

%install
rm -rf $RPM_BUILD_ROOT

%{__install} -d %{buildroot}/usr/share/emacs/site-lisp
#make install prefix=%{buildroot}%{_prefix} exec_prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} infodir=%{buildroot}%{_infodir}

%makeinstall

# icon section
install -D %SOURCE16 %buildroot/%_miconsdir/gnu-forth.png
install -D %SOURCE32 %buildroot/%_iconsdir/gnu-forth.png
install -D %SOURCE48 %buildroot/%_liconsdir/gnu-forth.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=GNU Forth
Exec=%{name} 
Icon=gnu-forth
Terminal=false
Type=Application
Categories=Development;Building;
EOF


%post
%if %mdkversion < 200900
%{update_menus}
%endif
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root, root)
%doc README BUGS NEWS
%_bindir/*
%_libdir/%name
%_datadir/%name
%_datadir/emacs/site-lisp/gforth.el
%_mandir/man1/*
%_infodir/*
%_iconsdir/*
%_liconsdir/*
%_miconsdir/*
%_datadir/applications/*
