#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_xhtml_neg
%define mod_conf B39_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	An XHTML content negotiation module for Apache
Name:		apache-%{mod_name}
Version:	1.0a
Release:	10
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

%description
This module provides content negotiation facilities for XHTML documents that
conform to Appendix C compatibility requirements of the XHTML 1.0
specification. This allows compatible browsers to view XHTML content as
XML-compliant documents, and older or less compatible clients to view XHTML
content as text/html documents.

%prep

%setup -q -n %{mod_name}-2.0

cp %{SOURCE1} %{mod_conf}

find -type f -exec dos2unix {} \;

%build

%{_bindir}/apxs -c mod_xhtml_neg.c lookupa.c
        
%install

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

%files
%doc LICENSE README mod_xhtml_neg.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}



%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0a-9mdv2012.0
+ Revision: 773241
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0a-8
+ Revision: 678445
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0a-7mdv2011.0
+ Revision: 588091
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0a-6mdv2010.1
+ Revision: 516274
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0a-5mdv2010.0
+ Revision: 406685
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0a-4mdv2009.1
+ Revision: 326278
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0a-3mdv2009.0
+ Revision: 235133
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0a-2mdv2009.0
+ Revision: 215676
- fix rebuild

* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0a-1mdv2009.0
+ Revision: 208663
- import apache-mod_xhtml_neg


* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0a-1mdv2009.0
- initial Mandriva package
