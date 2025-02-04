%{!?specfile: %global specfile spec file}
%global summary %{?longsum}%{!?longsum:A testing %{specfile}}

%global version_major 1
%global version_minor 0
%global version_patch 2
%global version_major_minor %{version_major}.%{version_minor}
%global version %{version_major_minor}.%{version_patch}

%global release 34
%global release_str %{release}%{?dist}

%global project rebase-helper
%global commit d70cb5a2f523db5b6088427563531f43b7703859

Summary: %{summary}
Name: test
Version: %{version}
Release: %{release_str}
License: GPL2+
Group: System Environment
URL: http://testing.org

# Note: non-current tarballs get moved to the history/ subdirectory,
# so look there if you fail to retrieve the version you want
Source: ftp://ftp.test.org/%{name}-%{version}.tar.xz
Source1: source-tests.sh
Source2 : ftp://test.com/test-source.sh
#Source3: source-tests.sh
Source4: file.txt.bz2
Source5: documentation.tar.xz
Source6: misc.zip
Source7: https://pypi.python.org/packages/source/p/positional/positional-1.1.0.tar.gz
Source8: https://github.com/%{project}/%{project}/archive/%{commit}/%{project}-%{commit}.tar.gz
Source9: https://test.com/#/1.0/%{name}-hardcoded-version-1.0.2.tar.gz
Patch1: test-testing.patch
Patch2: test-testing2.patch
Patch3: test-testing3.patch
Patch4: test-testing4.patch
Patch5: rebase-helper-results/rebased-sources/test-testing5.patch

BuildRequires: openssl-devel, pkgconfig, texinfo, gettext, autoconf

%description
Testing spec file

%package devel
Summary: A testing devel package

%description devel
Testing devel spec file

%prep
%setup -q -c -a 5
%patch1
%patch2 -p1
%patch3 -p1 -b .testing3
%patch4 -p0 -b .testing4
mkdir misc
tar -xf %{SOURCE6} -C misc

%build
autoreconf -vi # Unescaped macros %name %{name}

%configure
make TEST

%Install
make DESTDIR=$RPM_BUILD_ROOT install

%check
#to run make check use "--with check"
%if %{?_with_check:1}%{!?_with_check:0}
make check
%endif

%files
/usr/share/man/man1/*
/usr/bin/%{name}
%config(noreplace) /etc/test/test.conf

%files devel
%{_bindir}/test_example
%{_libdir}/my_test.so
/usr/share/test1.txt
/no/macros/here

%changelog
* Wed Apr 26 2017 Nikola Forró <nforro@redhat.com> - 1.0.2-34
- This is chnagelog entry with some indentional typos

* Wed Nov 12 2014 Tomas Hozza <thozza@redhat.com> 1.0.0-33
- Bump the release for testing purposes

* Tue Sep 24 2013 Petr Hracek <phracek@redhat.com> 1.0.0-1
- Initial version

