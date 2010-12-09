Name:		gforth
Version:	0.7.0
Release:	%mkrel 2
License:	GPLv3+
Group:		Development/Other
Summary:	GNU Forth
Url:		http://www.jwdt.com/~paysan/gforth.html
Source:		http://www.complang.tuwien.ac.at/forth/gforth/%{name}-%{version}.tar.gz
Source16:	gnu-forth.16.png
Source32:	gnu-forth.32.png
Source48:	gnu-forth.48.png
Patch0:		gforth-0.7.0-buildpath.patch
Patch1:		gforth-0.7.0-shebang.patch
BuildRoot:	%_tmppath/%name-%version-%release
BuildRequires:	emacs-bin

%description
Gforth is a fast and portable implementation of the ANS Forth language. 

%prep 
%setup -q
%patch0 -p1
%patch1 -p1

iconv -f latin1 -t utf8 AUTHORS > AUTHORS.new
mv -f AUTHORS.new AUTHORS

%build
%configure2_5x 
make

%install
rm -rf $RPM_BUILD_ROOT

%{__install} -d %{buildroot}/usr/share/emacs/site-lisp

%makeinstall_std

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
%doc README README.vmgen NEWS NEWS.vmgen AUTHORS BUGS

%_bindir/*
%_libdir/%name
%_datadir/%name
%_datadir/emacs/site-lisp/gforth.el
%_datadir/emacs/site-lisp/gforth.elc
%{_includedir}/%{name}/%{version}/*.h
%_mandir/man1/*
%_infodir/*
%_iconsdir/*
%_datadir/applications/*
