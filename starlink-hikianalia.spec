# This is a thin RPM wrapper for the Starlink software. The software
# is a hideous monstrosity with a multitude of bundled libraires, tcl
# etc, so we're not going to try and build from source, or install in
# proper system directories. Just dump the lot into /opt and
# pray. This software is truly a testament for bad software
# engineering practices in academia. Because this software bundles its
# own hacked tcl/tk we can't reliably use environment modules to set
# this up either - once the module is loaded, the module command would
# then use the broken bundled tcl/tk when trying to unload, which
# breaks. What a total mess.

%define __arch_install_post %{nil}
%define __os_install_post %{nil}

# Disable automatic dependency and provides information
%define __find_provides %{nil} 
%define __find_requires %{nil} 
%define _use_internal_dependency_generator 0
Autoprov: 0
Autoreq: 0

%global debug_package %{nil}

Name:		starlink-hikianalia
Version:	1
Release:	1%{?dist}
Summary:	Software for astronomical data processing

Group:		Applications/Scientific
License:	GPLv3+
URL:		http://starlink.jach.hawaii.edu/starlink/WelcomePage
Source0:	http://ftp.jach.hawaii.edu/starlink/hikianalia/starlink-hikianalia-Linux-64bit.tar.gz

#BuildRequires:	
#Requires:	

%description
Software for astronomical data processing.

%prep
%setup -c -a0


%build
# Binary tarball - nothing to build


%install
rm -rf $RPM_BUILD_ROOT

pushd star-hikianalia/etc
sed -i -e '1iexport STARLINK_DIR=/opt/star-hikianalia' profile
sed -i -e '1isetenv STARLINK_DIR=/opt/star-hikianalia' login
sed -i -e '1isetenv STARLINK_DIR=/opt/star-hikianalia' cshrc
popd

mkdir -p $RPM_BUILD_ROOT/opt/
mv star-hikianalia $RPM_BUILD_ROOT/opt/

install -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/starlink-hikianalia.sh<<EOF
alias starlink-setup="source /opt/star-hikianalia/etc/profile"
EOF

cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/starlink-hikianalia.csh<<EOF
alias starlink-setup "source /opt/star-hikianalia/etc/login ; source /opt/star-hikianalia/etc/cshrc"
EOF



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/opt/star-hikianalia
%{_sysconfdir}/profile.d/*

%changelog
* Fri Dec 13 2013 Jonathan Underwood  <jonathan.underwood@gmail.com> - 1-1
- Inital package effort.

