%define name  gforth
%define release %mkrel 3
%define version 0.6.2


Name:		%name
Release:	%release
Version:	%version
License:	GPL
Group:		Development/Other
Summary:	GNU Forth
Url:		http://www.jwdt.com/~paysan/gforth.html
Source:		%name-%version.tar.bz2
Source16:	gnu-forth.16.png.bz2
Source32:	gnu-forth.32.png.bz2
Source48:	gnu-forth.48.png.bz2
BuildRoot:	%_tmppath/%name-%version-%release

%description
Gforth is a fast and portable implementation of the ANS Forth language. 

%prep 

%setup -q

%build
# need to rebuild from these
#touch engine/prim.i engine/prim_lab.i

%configure CC="gcc -fno-reorder-blocks"

make

%install
rm -rf $RPM_BUILD_ROOT

%{__install} -d %{buildroot}/usr/share/emacs/site-lisp
#make install prefix=%{buildroot}%{_prefix} exec_prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} infodir=%{buildroot}%{_infodir}

%makeinstall

# icon section
install -d %buildroot/%_miconsdir
install -d %buildroot/%_iconsdir
install -d %buildroot/%_liconsdir
bzcat %SOURCE16 > %buildroot/%_miconsdir/gnu-forth.png
bzcat %SOURCE32 > %buildroot/%_iconsdir/gnu-forth.png
bzcat %SOURCE48 > %buildroot/%_liconsdir/gnu-forth.png

# debian menu file
install -d %buildroot/%_menudir
cat << EOF > %buildroot/%_menudir/%name
?package(%name):command="%_bindir/%name" \
icon="gnu-forth.png"  needs="text" section="More Applications/Development/Interpreters" \
title="GNU Forth" longtitle="%summary - Shell" xdg="true"
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{Summary}
Exec=%{name} 
Icon="gnu-forth.png"
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Development-Interpreters;Development; 
EOF


%post
%{update_menus}

%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%postun
%{clean_menus}

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
%_menudir/*
%_datadir/applications/*
