Summary:	GNU Forth
Name:		gforth
Version:	0.7.3
Release:	1
License:	GPLv3+
Group:		Development/Other
Url:		https://www.jwdt.com/~paysan/gforth.html
Source0:	http://www.complang.tuwien.ac.at/forth/gforth/%{name}-%{version}.tar.gz
Source16:	gnu-forth.16.png
Source32:	gnu-forth.32.png
Source48:	gnu-forth.48.png
Source100:	%{name}.rpmlintrc
Patch0:		gforth-0.7.3-buildpath.patch
Patch1:		gforth-0.7.3-shebang.patch
# s390 build fix from Debian (http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=544827)
Patch2:		gforth-0.7.3-compile-fix.patch
# patches from fedora rawhide
Patch3:		gforth-0.7.3-broken-disassembler.patch
Patch4:		gforth-0.7.3-newline-null-local-array.patch
Patch5:		gforth-0.7.3-libtool-build.patch
Patch6:		gforth-0.7.3-compile.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	emacs

%description
Gforth is a fast and portable implementation of the ANS Forth language.

%files
%doc README README.vmgen NEWS NEWS.vmgen AUTHORS BUGS
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/emacs/site-lisp/gforth.el
%{_datadir}/emacs/site-lisp/gforth.elc
%{_includedir}/%{name}/%{version}/*.h
%{_mandir}/man1/*
%{_infodir}/*
%{_iconsdir}/*
%{_datadir}/applications/*.desktop

#----------------------------------------------------------------------------

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1 -b .compile-fix
%patch -P3 -p1 -b .broken-disassembler
%patch -P4 -p1 -b .newline-null-local-array
%patch -P5 -p1 -b .libtool-build
%patch -P6 -p1

iconv -f latin1 -t utf8 AUTHORS > AUTHORS.new
mv -f AUTHORS.new AUTHORS
touch -d 2008-10-01 prim prim.b engine/prim.i

find . -name "Makefile*" -o -name "*.m4" |xargs sed -i -e 's,configure.in,configure.ac,g'

%build
autoreconf -fi
%configure2_5x
make

%install
install -d %{buildroot}/usr/share/emacs/site-lisp

%makeinstall_std

# icon section
install -D %{SOURCE16} %{buildroot}%{_miconsdir}/gnu-forth.png
install -D %{SOURCE32} %{buildroot}%{_iconsdir}/gnu-forth.png
install -D %{SOURCE48} %{buildroot}%{_liconsdir}/gnu-forth.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=GNU Forth
Exec=%{name}
Icon=gnu-forth
Terminal=false
Type=Application
Categories=Development;Building;
EOF

