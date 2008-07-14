#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_xhtml_neg
%define mod_conf B39_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	An XHTML content negotiation module for Apache
Name:		apache-%{mod_name}
Version:	1.0a
Release:	%mkrel 3
Group:		System/Servers
License:	Apache License
URL:		http://mod-xhtml-neg.sourceforge.net/
Source0:	http://dfn.dl.sourceforge.net/sourceforge/mod-xhtml-neg/%{mod_name}2-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This module provides content negotiation facilities for XHTML documents that
conform to Appendix C compatibility requirements of the XHTML 1.0
specification. This allows compatible browsers to view XHTML content as
XML-compliant documents, and older or less compatible clients to view XHTML
content as text/html documents.

%prep

%setup -q -n %{mod_name}-2.0

cp %{SOURCE1} %{mod_conf}

find -type f -exec dos2unix -U {} \;

%build

%{_sbindir}/apxs -c mod_xhtml_neg.c lookupa.c
        
%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README mod_xhtml_neg.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

