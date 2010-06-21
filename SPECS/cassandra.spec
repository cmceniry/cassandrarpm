Summary:	Cassandra Distributed Database
Name:		cassandra
Version:	0.6.2
Release:        1%{?dist}
License:	Apache Software License 2.0
Group:		Applications/Databases
Source:		http://www.apache.org/dist/cassandra/0.6.2/apache-cassandra-0.6.2-src.tar.gz
Source1:	cassandra.init
Source2:	cassandra.sysconfig
Source3:	cassandra.rc
Source4:	cassandra.logrotate
Source5:	storage-conf.xml
Source6:	log4j.properties
Source7:	log4j-tools.properties
Patch0:		commands.patch
Url:		http://cassandra.apache.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	ant
BuildRequires:	java

%description

The Apache Cassandra Project develops a highly scalable second-generation
distributed database, bringing together Dynamo's fully distributed design and
Bigtable's ColumnFamily-based data model.

%prep
%setup -q -n apache-cassandra-%{version}-src
%patch -p1

%build
ant jar javadoc

%clean 
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
install -m 0755 ${RPM_SOURCE_DIR}/cassandra.init ${RPM_BUILD_ROOT}/etc/rc.d/init.d/cassandra
mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
install -m 0755 ${RPM_SOURCE_DIR}/cassandra.logrotate ${RPM_BUILD_ROOT}/etc/logrotate.d/cassandra
mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig
install -m 0644 ${RPM_SOURCE_DIR}/cassandra.sysconfig ${RPM_BUILD_ROOT}/etc/sysconfig/cassandra
install -m 0755 -d ${RPM_BUILD_ROOT}/etc/cassandra
install -m 0644 ${RPM_SOURCE_DIR}/storage-conf.xml ${RPM_BUILD_ROOT}/etc/cassandra/storage-conf.xml
install -m 0644 ${RPM_SOURCE_DIR}/log4j.properties ${RPM_BUILD_ROOT}/etc/cassandra/log4j.properties
install -m 0644 ${RPM_SOURCE_DIR}/log4j-tools.properties ${RPM_BUILD_ROOT}/etc/cassandra/log4j-tools.properties

mkdir -p ${RPM_BUILD_ROOT}/usr/java
install -m 0755 -d ${RPM_BUILD_ROOT}/usr/java/cassandra-%{version}
install -m 0755 -d ${RPM_BUILD_ROOT}/usr/java/cassandra-%{version}/lib
for lib in antlr-3.1.3.jar \
  antlr-3.1.3.jar \
  avro-1.2.0-dev.jar \
  clhm-production.jar \
  commons-cli-1.1.jar \
  commons-codec-1.2.jar \
  commons-collections-3.2.1.jar \
  commons-lang-2.4.jar \
  google-collections-1.0.jar \
  hadoop-core-0.20.1.jar \
  high-scale-lib.jar \
  jackson-core-asl-1.4.0.jar \
  jackson-mapper-asl-1.4.0.jar \
  jline-0.9.94.jar \
  json-simple-1.1.jar \
  libthrift-r917130.jar \
  log4j-1.2.14.jar \
  slf4j-api-1.5.8.jar \
  slf4j-log4j12-1.5.8.jar; do
  install -m 0644 lib/${lib} ${RPM_BUILD_ROOT}/usr/java/cassandra-%{version}/lib/${lib}
done
install -m 0644 build/apache-cassandra-%{version}.jar \
  ${RPM_BUILD_ROOT}/usr/java/cassandra-%{version}/lib/apache-cassandra-%{version}.jar

install -m 0755 -d ${RPM_BUILD_ROOT}/usr/java/cassandra-%{version}/share
rsync -aHSP contrib/ ${RPM_BUILD_ROOT}/usr/java/cassandra-%{version}/share/contrib/
rsync -aHSP build/javadoc/ ${RPM_BUILD_ROOT}/usr/java/cassandra-%{version}/share/javadoc/
install -m 0644 ${RPM_SOURCE_DIR}/cassandra.rc ${RPM_BUILD_ROOT}/usr/java/cassandra-%{version}/share/cassandra.rc

install -m 0755 -d ${RPM_BUILD_ROOT}/usr/java/cassandra-%{version}/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
for bin in \
  cassandra-cli \
  json2sstable \
  nodeprobe \
  nodetool \
  sstable2json; do
  install -m 0755 bin/${bin} ${RPM_BUILD_ROOT}/usr/java/cassandra-%{version}/bin/${bin}
  ln -s /usr/java/cassandra/bin/${bin} ${RPM_BUILD_ROOT}/usr/bin/${bin}
done
install -m 0755 bin/cassandra ${RPM_BUILD_ROOT}/usr/java/cassandra-%{version}/bin/cassandra

mkdir -p ${RPM_BUILD_ROOT}/var/lib/cassandra
mkdir -p ${RPM_BUILD_ROOT}/var/log/cassandra

[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress

%files
%defattr(-,root,root)
%dir /etc/cassandra
%config(noreplace) /etc/cassandra/log4j.properties
%config(noreplace) /etc/cassandra/log4j-tools.properties
%config(noreplace) /etc/cassandra/storage-conf.xml
/etc/rc.d/init.d/cassandra
%config(noreplace) /etc/logrotate.d/cassandra
%config(noreplace) /etc/sysconfig/cassandra
/usr/bin/cassandra-cli
/usr/bin/json2sstable
/usr/bin/nodeprobe
/usr/bin/nodetool
/usr/bin/sstable2json
/usr/java/cassandra-%{version}
%dir %attr(0755, cassandra, cassandra) /var/lib/cassandra
%dir %attr(0755, cassandra, cassandra) /var/log/cassandra

%pre
/usr/sbin/groupadd -f -r cassandra
/usr/sbin/useradd -c "Cassandra" -m -r -d /var/lib/cassandra -s /sbin/nologin -g cassandra cassandra 2> /dev/null || :

%post
if [ $1 -eq 1 ]; then
  ln -s /usr/java/cassandra-%{version} /usr/java/cassandra
  /sbin/chkconfig --add cassandra
fi

%preun
if [ $1 -eq 0 ]; then
  service cassandra stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del cassandra
fi

%postun
if [ $1 -eq 0 ]; then
  rm /usr/java/cassandra >/dev/null 2>&1 || :
fi

%changelog
* Mon Jun 21 2010 Chris McEniry <cmceniry@corgalabs.com> - 0.6.2-1
- Initial spec file
