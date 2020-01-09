Name:           ksm_preload
Version:        0.10
Release:        3%{?dist}
Summary:        Library for enabling sharing memory pages between applications
License:        GPLv3
URL:            http://www.vleu.net/ksm_preload/

Source0:        https://github.com/unbrice/ksm_preload/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1:        LD_PRELOAD

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf automake libtool

Requires:       kernel >= 2.6.32

%global commit 346cb6db8e2ff4aba35917c3389d0ad2ed285c2f
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Patch0: ksm_preload-0.10-autoconf-ver.patch
Patch1: ksm_preload-0.10-mapstack.patch

%description
The %{name} package contains library ksm_preload which
enables legacy applications to leverage Linux's memory
deduplication.

%prep
%setup -qn %{name}-%{commit}
%patch0 -p1
%patch1 -p1

%build
autoreconf -vfi
%configure --disable-static
CFLAGS="%{optflags}" make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
libtool --finish %{buildroot}%{_libdir}/
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
install -D -p -m 0755 %{_builddir}/%{buildsubdir}/scripts/ksm-wrapper %{buildroot}%{_sbindir}/ksm-wrapper
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/openshift/env/LD_PRELOAD

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_libdir}/libksm_preload.so*
%{_sbindir}/ksm-wrapper
%{_sysconfdir}/openshift/env/LD_PRELOAD
%doc
%doc %{_defaultdocdir}/ksm_preload/README


%changelog
* Tue Nov 26 2013 Petr Holasek <pholasek@redhat.com> - 0.10-3
- Added mapstack define patch, so compilable also on s390 and ppc now

* Wed Oct 23 2013 Petr Holasek <pholasek@redhat.com> - 0.10-2
- Autotools build support added

* Fri Oct 11 2013 Petr Holasek <pholasek@redhat.com> - 0.10-1
- Initial version of ksm-preload package
