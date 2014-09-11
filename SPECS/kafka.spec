Summary:       Kafka is a distributed publish/subscribe messaging system
Name:          kafka
Version:       0.8.1.1
Release:       8

%define alternatives_ver 811%{release}
%define scala_ver 2.10.1

Group:         Applications/Internet
License:       Apache (v2)
Source0:       https://github.com/apache/kafka/archive/%{version}.zip
Source1:       kafka.init
URL:           http://kafka.apache.org
BuildRoot:     %{_tmppath}/%{name}-%{version}-root
Distribution:  Niels Basjes
Vendor:        Niels Basjes <kafka@basjes.nl>
Requires:      jdk >= 1.6
Requires(pre): shadow-utils
BuildRequires: shared-mime-info
BuildRequires: jdk >= 1.6

Patch0:        scala_gradle.patch
Patch1:        kafka_run_class_sh.patch
Patch2:        kafka_server_start_sh.patch

%description
It is designed to support the following

Persistent messaging with O(1) disk structures that provide constant time performance even with many TB of stored messages.
High-throughput: even with very modest hardware Kafka can support hundreds of thousands of messages per second.
Explicit support for partitioning messages over Kafka servers and distributing consumption over a cluster of consumer machines while maintaining per-partition ordering semantics.
Support for parallel data load into Hadoop.
Kafka is aimed at providing a publish-subscribe solution that can handle all activity stream data and processing on a consumer-scale web site. This kind of activity (page views, searches, and other user actions) are a key ingredient in many of the social feature on the modern web. This data is typically handled by "logging" and ad hoc log aggregation solutions due to the throughput requirements. This kind of ad hoc solution is a viable solution to providing logging data to an offline analysis system like Hadoop, but is very limiting for building real-time processing. Kafka aims to unify offline and online processing by providing a mechanism for parallel load into Hadoop as well as the ability to partition real-time consumption over a cluster of machines.

See our web site for more details on the project. (http://kafka.apache.org/)

%pre

# Create user and group
getent group kafka >/dev/null || groupadd -r kafka
getent passwd kafka >/dev/null || \
    useradd -r -g kafka -d /opt/kafka -s /bin/bash \
    -c "Kafka Account" kafka


exit 0

%post
alternatives --install /opt/kafka kafkahome  /opt/%{name}-%{version} %{alternatives_ver}

%preun
service kafka stop

%postun
alternatives --remove kafkahome  /opt/%{name}-%{version}

%prep

%setup -q

%patch0 -p0
%patch1 -p0
%patch2 -p0

%build
# Build package

./gradlew -PscalaVersion=%{scala_ver} releaseTarGz -x signArchives

%install

# Clean out any previous builds not on slash
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}/opt/%{name}-%{version}
%{__cp} -R * %{buildroot}/opt/%{name}-%{version}
%{__mkdir_p} %{buildroot}/var/log/kafka
%{__mkdir_p} %{buildroot}/etc/rc.d/init.d
%{__mkdir_p} %{buildroot}/etc/sysconfig
%{__mkdir_p} %{buildroot}/var/run/kafka
%{__chown} kafka:kafka %{buildroot}/var/run/kafka
install -m 755 %{S:1} %{buildroot}/etc/rc.d/init.d/kafka

echo -e "export PATH=${PATH}:/opt/kafka/bin\nexport SCALA_VERSION=%{scala_ver}" > %{buildroot}/etc/sysconfig/kafka

%files
%defattr(-,kafka,kafka)

%config /opt/%{name}-%{version}/config
/opt/%{name}-%{version}
/var/log/kafka
/etc/rc.d/init.d/kafka
/etc/sysconfig/kafka
/var/run/kafka

%clean
#used to cleanup things outside the build area and possibly inside.
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%changelog
* Wed Sep 10 2014 Marcin Stanislawski <marcin.stanislawski@gmail.com> - 0.8.1.1-8
- refactoring init.d script
- moving configuration from profile.d to sysconfig
- patch kafka startup scripts to provide pidfile
* Wed Aug 27 2014 Seweryn Ozog <seweryn.ozog@gmail.com> & Marcin Stanislawski <marcin.stanislawski@gmail.com> - 0.8.1.1-7
- Move everything to spec file
- Small refactoring
- Mock compatibility
* Mon Sep 16 2013 Niels Basjes <kafka@basjes.nl>
- Refactoring the scripting
* Fri Mar 15 2013 Mark Poole <mpoole@apache.org>
- First build
