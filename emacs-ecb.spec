%define tarname ecb
%define name	emacs-%{tarname}
%define version 2.40
%define release %mkrel 2

Summary:	Emacs Code Browser
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{tarname}-%{version}.tar.gz
License:	GPLv2+
Group:		Editors
Url:		http://ecb.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
Requires:	emacs >= 21.0
Requires:	emacs-cedet >= 1.0
BuildRequires:	emacs >= 21.0, emacs-cedet >= 1.0
BuildRequires:	texinfo

%description
ECB stands for "Emacs Code Browser". While Emacs already has good
editing support for many modes, its browsing support is somewhat
lacking. That's where ECB comes in: it displays a number of
informational windows that allow for easy source code navigation and
overview.

The informational windows can contain:

* A directory tree,
* a list of source files in the current directory,
* a list of functions/classes/methods/... in the current file, (ECB
  uses the Semantic Bovinator, or Imenu, or etags, for getting this
  list so all languages supported by any of these tools are
  automatically supported by ECB too)
* a history of recently visited files,
* the Speedbar, and
* output from compilation (the compilation window) and other modes
  like help, grep, etc., or whatever a user defines to be displayed in
  this window.

As an added bonus, ECB makes sure to keep these informational windows
visible, even when you use C-x 1 and similar commands.

It goes without saying that you can configure the layout, i.e., which
informational windows should be displayed where. ECB comes with a
number of ready-made window layouts to choose from.

%prep
%setup -q -n %{tarname}-%{version}

%build
%make all CEDET=/usr/share/emacs/site-lisp/cedet/ TEXI2DVI=/usr/bin/texi2dvi DVIPDFM=/usr/bin/dvipdfm EMACSINFOPATH=/usr/share/info/

%install
%__rm -rf %{buildroot}
%__mkdir -p %{buildroot}%{_infodir}
for info in info-help/*; do
    %__install -m 644 ${info} %{buildroot}%{_infodir}
done
%__mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp/ecb/
%__install -m 644 *.el* %{buildroot}/%{_datadir}/emacs/site-lisp/ecb
find ecb-images -exec %__install -m 644 -D {} %{buildroot}/%{_datadir}/emacs/site-lisp/ecb/{} \;

%__cat > %{tarname}.el << EOF
;; Make ECB available
(add-to-list 'load-path "/usr/share/emacs/site-lisp/ecb")
(require 'ecb-autoloads)
EOF
%__mkdir -p %{buildroot}%{_sysconfdir}/emacs/site-start.d/
%__install -m 644 %{tarname}.el %{buildroot}%{_sysconfdir}/emacs/site-start.d/

%clean
%__rm -rf %{buildroot}

%post
%_install_info ecb.info

%postun
%_remove_install_info ecb.info

%files
%defattr(-,root,root)
%doc NEWS README RELEASE_NOTES
%{_infodir}/*
%{_datadir}/emacs/site-lisp/%{tarname}
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/%{tarname}.*
