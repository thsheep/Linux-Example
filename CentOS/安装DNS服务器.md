安装DNS服务器

yum install -y bind bind-utils bind-libs

默认配置文件位置为：/etc/named.conf

备份配置文件
cp /etc/named.conf /etc/named.conf.backup

更改配置文件

//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//
// See the BIND Administrator's Reference Manual (ARM) for details about the
// configuration located in /usr/share/doc/bind-{version}/Bv9ARM.html

options {
	//监听所有网段
	listen-on port 53 { 0.0.0.0/0; };
	listen-on-v6 port 53 { ::1; };
	directory 	"/var/named";
	dump-file 	"/var/named/data/cache_dump.db";
	statistics-file "/var/named/data/named_stats.txt";
	memstatistics-file "/var/named/data/named_mem_stats.txt";
	//允许所有IP查询DNS记录
	allow-query     { any; };

	/* 
	 - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
	 - If you are building a RECURSIVE (caching) DNS server, you need to enable 
	   recursion. 
	 - If your recursive DNS server has a public IP address, you MUST enable access 
	   control to limit queries to your legitimate users. Failing to do so will
	   cause your server to become part of large scale DNS amplification 
	   attacks. Implementing BCP38 within your network would greatly
	   reduce such attack surface 
	*/
	recursion no;

	dnssec-enable no;
	dnssec-validation no;

	/* Path to ISC DLV key */
	bindkeys-file "/etc/named.iscdlv.key";

	managed-keys-directory "/var/named/dynamic";

	pid-file "/run/named/named.pid";
	session-keyfile "/run/named/session.key";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity info;
        };
};
//设置域名区域
zone "bicap.com" IN {
        type master;
        file "bicap.com.zone";
        allow-update { none; };
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";

配置域名详细解析
默认路径为：/var/named/


[root@localhost ~]# cat /var/named/
bicap.com.zone   data/            dynamic/         named.ca         named.empty      named.localhost  named.loopback   slaves/          
[root@localhost ~]# cat /var/named/bicap.com.zone 
$TTL 86400
@	IN SOA	 ns.bicap.com. 	root.bicap.com.(
					42
					1D	
					1H	
					1W	
					3H )	
	IN NS	ns.bicap.com.	
	IN MX 10	mail	
	IN A	10.10.1.222
ns	IN A	10.10.1.222
ag	IN A	10.10.1.98
app	IN A	10.10.1.61
sr	IN A	10.10.1.90
sr	IN A	10.10.1.92
sr	IN A	10.10.1.91



设置文件访问权限：
[root@localhost named]# chown root:named bicap.com.zone 
[root@localhost named]# ll
total 20
-rw-r-----. 1 root  named  272 May 27 00:20 bicap.com.zone
drwxrwx---. 2 named named   23 May 26 22:21 data
drwxrwx---. 2 named named   31 May 26 22:27 dynamic
-rw-r-----. 1 root  named 2076 Jan 28  2013 named.ca
-rw-r-----. 1 root  named  152 Dec 15  2009 named.empty
-rw-r-----. 1 root  named  152 Jun 21  2007 named.localhost
-rw-r-----. 1 root  named  168 Dec 15  2009 named.loopback
drwxrwx---. 2 named named    6 Apr 19 11:53 slaves

