temp_cnf = '''
[mysql]
default-character-set = utf8mb4
socket=/tmp/mysql{1}.sock

[mysqld]
# basic settings #
server_id={2}
port={1}
user=mysql
basedir={0}mysql{1}/service/
datadir={0}mysql{1}/data
socket=/tmp/mysql{1}.sock
log_error={0}mysql{1}/log/mysql.log
pid-file=/tmp/mysqld{1}.pid
log_bin={0}mysql{1}/binlog/mysql-bin
relay_log={0}mysql{1}/log/relay.log
pid-file=/tmp/mysqld{1}.pid
slow_query_log_file={0}mysql{1}/slowlog/slowlog
innodb_undo_directory={0}mysql{1}/undo
character_set_server = utf8mb4
collation-server=utf8mb4_general_ci
autocommit=1
symbolic-links=0
# //设置密码自动失效的时间，0为永不失效
max_allowed_packet = 67108864    
# //限制Server接受的数据包大小。有时候大的插入和更新会受此参数限制，导致大数据写入或者更新失败
# max_long_data_size = 67108864    
# //设定可以由mysql_stmt_send_long_data()这个C API函数所传送的参数值的最大长度，如果没有在mysqld启动时设定，其默认为max_allowed_packet变量的值
event_scheduler = 1    
# //事件调度器的总开关
# skip-grant-tables

# connection #
interactive_timeout = 1800   
# //MySQL服务器关闭交互式连接前等待的秒数
wait_timeout = 1800   
# //MySQL服务器关闭非交互连接之前等待的秒数
lock_wait_timeout = 1800
skip_name_resolve = 1
max_connections = 1024   
# //针对所有用户连接限制
max_user_connections = 256   
# //针对同一用户的连接限制
max_connect_errors = 1000000   
# //当错误连接数超过设定的值后,将无法正常连接

# table cache performance settings #
table_open_cache = 4096   
# //指定表高速缓存的大小。每当MySQL访问一个表时，如果在表缓冲区中还有空间，该表就被打开并放入其中，这样可以更快地访问表内容
table_definition_cache = 4096   
# //表定义信息缓存
table_open_cache_instances = 64   
# //指的是 MySQL 缓存 table 句柄的分区的个数，而每一个 cache_instance 可以包含不超过table_open_cache/table_open_cache_instances 的table_cache_element

# session memory settings #
read_buffer_size = 16M   
# //MySQL读入缓冲区的大小，将对表进行顺序扫描的请求将分配一个读入缓冲区，MySQL会为它分配一段内存缓冲区，read_buffer_size变量控制这一缓冲区的大小，如果对表的顺序扫描非常频繁，并你认为频繁扫描进行的太慢，可以通过增加该变量值以及内存缓冲区大小提高其性能，read_buffer_size变量控制这一提高表的顺序扫描的效率 数据文件顺序
read_rnd_buffer_size = 32M  
#  //
sort_buffer_size = 32M   
# //是MySQL的随机读缓冲区大小，当按任意顺序读取行时（列如按照排序顺序）将分配一个随机读取缓冲区，进行排序查询时，MySQL会首先扫描一遍该缓冲，以避免磁盘搜索，提高查询速度，如果需要大量数据可适当的调整该值，但MySQL会为每个客户连接分配该缓冲区所以尽量适当设置该值，以免内存开销过大。表的随机的顺序缓冲 提高读取的效率
tmp_table_size = 64M   
# //它规定了内部内存临时表的最大值，每个线程都要分配。（实际起限制作用的是tmp_table_size和max_heap_table_size的最小值。）如果内存临时表超出了限制，MySQL就会自动地把它转化为基于磁盘的MyISAM表，存储在指定的tmpdir目录下。优化查询语句的时候，要避免使用临时表，如果实在避免不了的话，要保证这些临时表是存在内存中的。如果需要的话并且你有很多group by语句，并且你有很多内存，增大tmp_table_size(和max_heap_table_size)的值。这个变量不适用与用户创建的内存表(memory table). 你可以比较内部基于磁盘的临时表的总数和创建在内存中的临时表的总数（Created_tmp_disk_tables和Created_tmp_tables），一般的比例关系是:Created_tmp_disk_tables/Created_tmp_tables<5%。max_heap_table_size这个变量定义了用户可以创建的内存表(memory table)的大小.这个值用来计算内存表的最大行数值。这个变量支持动态改变，即set @max_heap_table_size=#,但是对于已经存在的内存表就没有什么用了，除非这个表被重新创建(create table)或者修改(alter table)或者truncate table。服务重启也会设置已经存在的内存表为全局max_heap_table_size的值。这个变量和tmp_table_size一起限制了内部内存表的大小。
join_buffer_size = 128M   
# //用于表间关联缓存的大小
thread_cache_size = 64   
# //服务器线程缓存这个值表示可以重新利用保存在缓存中线程的数量,当断开连接时如果缓存中还有空间,那么客户端的线程将被放到缓存中,如果线程重新被请求，那么请求将从缓存中读取,如果缓存中是空的或者是新的请求，那么这个线程将被重新创建,如果有很多新的线程，增加这个值可以改善系统性能.通过比较 Connections 和 Threads_created 状态的变量，可以看到这个变量的作用.

# log settings #
slow_query_log = 1
long_query_time = 1

log_queries_not_using_indexes = 0 
#// 开启后，即使SQL效率很高，但是没有使用索引就记录慢SQL
log_slow_admin_statements = 1   
# //记录执行缓慢的管理SQL
log_slow_slave_statements = 0   
# //记录从库上执行的慢查询语句 
# log_throttle_queries_not_using_indexes = 10   
#  //每分钟允许记录到slow log的且未使用索引的SQL语句次数
expire_logs_days = 7
# min_examined_row_limit = 100   
#  //查询语句的执行行数检查返回少于该参数指定行的SQL不被记录到慢查询日志
# binlog-rows-query-log-events = 1   
#  //当binlog_fromat=row的时候记录的是event，如果想要在row模式的情况下也记录SQL语句
log-bin-trust-function-creators = 1  
#  //此参数仅在启用二进制日志时有效，用于控制创建存储函数时如果会导致不安全的事件记录二进制日志条件下是否禁止创建存储函数。默认值为0，表示除非用户除了CREATE ROUTING或ALTER ROUTINE权限外还有SUPER权限，否则将禁止创建或修改存储函数，同时，还要求在创建函数时必需为之使用DETERMINISTIC属性，再不然就是附带READS SQL DATA或NO SQL属性。设置其值为1时则不启用这些限制。作用范围为全局级别，可用于配置文件，属动态变量。
log-slave-updates = 1   
# //一般情况下slave不会把从master接收到的binlog记录写入自己的binlog，这个参数会使slave通过SQL线程把从master接受到的binlog写进自己的binlog，但是前提是slave一定要开启自己的binlog，此参数一般用于级联复制，例如需要A复制到B，B复制到C，那么B就要开启此参数。

# innodb settings #
innodb_page_size = 16384   
# //参数innodb_page_size可以设置Innodb数据页为8K,4K，默认为16K。这个参数在一开始初始化时就要加入my.cnf里，如果已经创建了表，再修改，启动MySQL会报错。
innodb_buffer_pool_size = 2G  
#  //参数表示缓冲池字节大小，InnoDB缓存表和索引数据的内存区域
innodb_buffer_pool_instances = 2   
# //默认值是1，表示InnoDB缓存池被划分到一个区域。适当地增加该参数（例如将该参数值设置为2），此时InnoDB被划分成为两个区域，可以提升InnoDB的并发性能。如果InnoDB缓存池被划分成多个区域，建议每个区域不小于1GB的空间
innodb_buffer_pool_load_at_startup = 1  
#  //在启动时把热数据加载到内存
innodb_buffer_pool_dump_at_shutdown = 1  
#  //在关闭时把热数据dump到本地磁盘
innodb_lru_scan_depth = 4096  
#  //控制LRU列表中可用页的数量,默认值为1024
innodb_lock_wait_timeout = 5  
#  //锁等待超时时间
innodb_io_capacity = 10000  
#  //参数可以动态调整刷新脏页的数量，这在一定程度上解决了这一问题。innodb_io_capacity参数默认是200，单位是页。该参数设置的大小取决于硬盘的IOPS，即每秒的输入输出量
innodb_io_capacity_max = 20000  
#  //该参数限制了每秒刷新的脏页上限，调大该值可以增加Page cleaner线程每秒的工作量
innodb_flush_method = O_DIRECT   
# //参考链接：http://www.cnblogs.com/simplelogic/p/5004786.html
# innodb_file_format = Barracuda
# innodb_file_format_max = Barracuda   
# //Innodb Plugin引擎开始引入多种格式的行存储机制，目前支持：Antelope、Barracuda两种。其中Barracuda兼容Antelope格式。另外，Innodb plugin还支持行数据压缩特性，不过前提是采用Barracuda行存储格式。表空间启用压缩的前提是innodb表空间文件存储格式修改成：Barracuda，需要修改2个选项：
# innodb_undo_logs = 128   
# //定义在一个事务中innodb使用的系统表空间中回滚段的个数。如果观察到同回滚日志有关的互斥争用，可以调整这个参数以优化性能。早期版本的命名为 innodb_rollback_segments，该变量可以动态调整，但是物理上的回滚段不会减少，只是会控制用到的回滚段的个数;默认为128个回滚段
innodb_undo_tablespaces = 3  
#  //用于设定创建的undo表空间的个数，在mysql_install_db时初始化后，就再也不能被改动了；默认值为0，表示不独立设置undo的tablespace，默认记录到ibdata中；否则，则在undo目录下创建这么多个undo文件，例如假定设置该值为4，那么就会创建命名为undo001~undo004的undo tablespace文件，每个文件的默认大小为10M。修改该值会导致Innodb无法完成初始化，数据库无法启动，但是另两个参数可以修改
innodb_flush_neighbors = 0   
# //默认值为 1. 在SSD存储上应设置为0(禁用) ,因为使用顺序IO没有任何性能收益. 在使用RAID的某些硬件上也应该禁用此设置,因为逻辑上连续的块在物理磁盘上并不能保证也是连续的
innodb_log_file_size = 200M  
#  //日志组的大小,默认为5M；如果对 Innodb 数据表有大量的写入操作，那么选择合适的 innodb_log_file_size值对提升MySQL性能很重要。然而设置太大了，就会增加恢复的时间，因此在MySQL崩溃或者突然断电等情况会令MySQL服务器花很长时间来恢复
innodb_log_files_in_group = 2  
#  //日志组的数量，默认为2
innodb_log_buffer_size = 16M  
#  //日志缓冲池的大小
innodb_purge_threads = 4  
#  //在innodb 1.2版本开始 innodb支持多个purge thread 这样做的目的是为了进一步加快undo页的回收这样也能更进一步利用磁盘的随机读取性能 用户可以设置4个purge thread

innodb_thread_concurrency = 64  
#  //参考：http://www.cnblogs.com/xinysu/p/6439715.html
innodb_print_all_deadlocks = 1  
#  //这样死锁相关信息会保存到MySQL 错误日志中
innodb_strict_mode = 1  
#  //开启强制检查模式，忽略警告信息，直接抛出错误信息
innodb_sort_buffer_size = 67108864   
# //加速ORDER BY 或者GROUP BY 操作
innodb_write_io_threads = 8
innodb_read_io_threads = 8  
#  //假如CPU是2颗8核的，那么可以设置：innodb_read_io_threads = 8，innodb_write_io_threads = 8。如果数据库的读操作比写操作多，那么可以设置：innodb_read_io_threads = 10，innodb_write_io_threads = 6
innodb_file_per_table = 1  
#  //独立表空间模式,每个数据库的每个表都会生成一个数据空间
innodb_stats_persistent_sample_pages = 64  
#  //控制收集统计信息时采样的page数量，默认是20。收集的page数量越多，每次收集统计信息的实际则越长，但是统计信息也相对比较准确
innodb_autoinc_lock_mode = 2  
#  //参考：http://blog.itpub.net/15498/viewspace-2141640/
innodb_online_alter_log_max_size = 1G  
#  //参考：http://blog.itpub.net/29773961/viewspace-2140971/
innodb_open_files = 4096   
# //作用：限制Innodb能打开的表的数据。分配原则：这个值默认是300。如果库里的表特别多的情况，可以适当增大为1000。innodb_open_files的大小对InnoDB效率的影响比较小。但是在InnoDBcrash的情况下，innodb_open_files设置过小会影响recovery的效率。所以用InnoDB的时候还是把innodb_open_files放大一些比较合适。
innodb_flush_log_at_trx_commit = 1   
# //如果innodb_flush_log_at_trx_commit设置为0，log buffer将每秒一次地写入log file中，并且log file的flush(刷到磁盘)操作同时进行.该模式下，在事务提交的时候，不会主动触发写入磁盘的操作。
# 如果innodb_flush_log_at_trx_commit设置为1，每次事务提交时MySQL都会把log buffer的数据写入log file，并且flush(刷到磁盘)中去.
# 如果innodb_flush_log_at_trx_commit设置为2，每次事务提交时MySQL都会把log buffer的数据写入log file.但是flush(刷到磁盘)操作并不会同时进行。该模式下,MySQL会每秒执行一次 flush(刷到磁盘)操作
# innodb_support_xa = 1  
#  //作用是分两类：第一，支持多实例分布式事务（外部xa事务），这个一般在分布式数据库环境中用得较多。第二，支持内部xa事务，说白了也就是说支持binlog与innodb redo log之间数据一致性

# replication settings #
master_info_repository = TABLE
relay_log_info_repository = TABLE   
# //在MySQL 5.6.2之前，slave记录的master信息以及slave应用binlog的信息存放在文件中，即master.info与relay-log.info。在5.6.2版本之后，允许记录到table中，参数设置如下：master-info-repository  = TABLE，relay-log-info-repository = TABLE，对应的表分别为mysql.slave_master_info与mysql.slave_relay_log_info，且这两个表均为innodb引擎表。
sync_binlog = 1  
#  //是MySQL 的二进制日志（binary log）同步到磁盘的频率。取值：0-N，sync_binlog=0，当事务提交之后，MySQL不做fsync之类的磁盘同步指令刷新binlog_cache中的信息到磁盘，而让Filesystem自行决定什么时候来做同步，或者cache满了之后才同步到磁盘。这个是性能最好的。sync_binlog=1，当每进行1次事务提交之后，MySQL将进行一次fsync之类的磁盘同步指令来将binlog_cache中的数据强制写入磁盘。sync_binlog=n，当每进行n次事务提交之后，MySQL将进行一次fsync之类的磁盘同步指令来将binlog_cache中的数据强制写入磁盘。
gtid_mode = on   
# //是否开启GTID功能
enforce_gtid_consistency = 1   
# //enforce_gtid_consistency 强制GTID一致性, 启用后，create table ... select ...命令无法再使用
log_slave_updates
binlog_format=MIXED
# binlog_rows_query_log_events = 1  
# #  //只作用于RBR格式,默认不启用 如果启用,会把用户写直的原生态DML操作记录到binlog中
relay_log_purge = 1
relay_log_recovery = 1  
#  //当slave从库宕机后，假如relay-log损坏了，导致一部分中继日志没有处理，则自动放弃所有未执行的relay-log，并且重新从master上获取日志，这样就保证了relay-log的完整性。默认情况下该功能是关闭的，将relay_log_recovery的值设置为 1时，可在slave从库上开启该功能，建议开启
# report-port = 3306
# report-host = 10.106.144.11
# slave_skip_errors = ddl_exist_errors
slave-rows-search-algorithms = 'INDEX_SCAN,HASH_SCAN'  
#  //可以部分解决无主键表导致的复制延迟问题



# perforamnce_schema settings
performance-schema-instrument='memory/%=COUNTED'
performance_schema_digests_size = 40000
performance_schema_max_table_instances = 40000
performance_schema_max_digest_length = 4096

[mysqld-5.6]
# metalock performance settings
metadata_locks_hash_instances = 64   
# //简单来说 MDL Lock 是 MySQL Server 层中的表锁，主要是为了控制 Server 层 DDL & DML 的并发而设计的， 但是 5.5 的设计中只有一把大锁，所以到5.6中添加了参数 metadata_locks_hash_instances 来控制分区的数量，进而实现大锁的拆分，虽然锁的拆分提高了并发的性能，但是仍然存在着不少的性能问题，所以在 5.7.4 中 MDL Lock 的实现方式采用了 lock free 算法，彻底的解决了 Server 层表锁的性能问题，而参数 metadata_locks_hash_instances 也将会在之后的某个版本中被删除掉
innodb_large_prefix = 1   
# //大家应该知道InnoDB单列索引长度不能超过767bytes，联合索引还有一个限制是长度不能超过3072。innodb_large_prefix 这个参数默认值是OFF，当改为ON时，允许列索引最大达到3072
# semi sync replication settings #
plugin_load = "rpl_semi_sync_master=semisync_master.so;rpl_semi_sync_slave=semisync_slave.so"
rpl_semi_sync_master_enabled = 1  
#  //控制在主库是否开启了半同步步复制模式，可以设置为ON,OFF ,默认是off 
rpl_semi_sync_master_timeout = 3000  
#  //控制主库等待备库反馈已提交事务在备库落地的时间，以毫秒为单位默认是10s 
rpl_semi_sync_slave_enabled = 1   
# //控制在从库是否开启了半同步步复制模式，可以设置为ON,OFF ,默认是off

[mysqld-5.7]
# semi sync replication settings #
plugin_load = "rpl_semi_sync_master=semisync_master.so;rpl_semi_sync_slave=semisync_slave.so"
rpl_semi_sync_master_enabled = 1  
#  //控制在主库是否开启了半同步步复制模式，可以设置为ON,OFF ,默认是off 
rpl_semi_sync_master_timeout = 3000  
#  //控制主库等待备库反馈已提交事务在备库落地的时间，以毫秒为单位默认是10s 
rpl_semi_sync_slave_enabled = 1   
# //控制在从库是否开启了半同步步复制模式，可以设置为ON,OFF ,默认是off
# new innodb settings #
innodb_large_prefix = 1   
# //大家应该知道InnoDB单列索引长度不能超过767bytes，联合索引还有一个限制是长度不能超过3072。innodb_large_prefix 这个参数默认值是OFF，当改为ON时，允许列索引最大达到3072
default_password_lifetime = 0    
performance_schema_max_sql_text_length = 4096
loose_innodb_numa_interleave = 1   
# //缓冲池内存的分配策略采用interleave的方式
innodb_buffer_pool_dump_pct = 40   
# //默认为关闭OFF。如果开启该参数，停止MySQL服务时，InnoDB将InnoDB缓冲池中的热数据的百分比保存到本地硬盘,5.7.6以前是100,5.7.7开始是25,也就是保存缓存中的25%热数据
innodb_page_cleaners = 16   
# //为了提升扩展性和刷脏效率，在5.7.4版本里引入了多个page cleaner线程。从而达到并行刷脏的效果。在该版本中，Page cleaner并未和buffer pool绑定，其模型为一个协调线程 + 多个工作线程，协调线程本身也是工作线程。因此如果innodb_page_cleaners设置为8，那么就是一个协调线程，加7个工作线程
innodb_undo_log_truncate = 1   
# //设置为ON即可开启undo表空间的自动truncate
innodb_max_undo_log_size = 2G   
# //undo表空间文件超过此值即标记为可收缩，默认1G，可在线修改
innodb_purge_rseg_truncate_frequency = 128  
#  //指定purge操作被唤起多少次之后才释放rollback segments。当undo表空间里面的rollback segments被释放时，undo表空间才会被truncate。由此可见，该参数越小，undo表空间被尝试truncate的频率越高。

# new replication settings #
slave-parallel-type = LOGICAL_CLOCK   
# //可以有两个值：DATABASE 默认值，基于库的并行复制方式；LOGICAL_CLOCK：基于组提交的并行复制方式
slave-parallel-workers = 8  
#  //在MySQL 5.7中，引入了基于组提交的并行复制（Enhanced Multi-threaded Slaves），设置参数slave_parallel_workers>0并且slave_parallel_type＝‘LOGICAL_CLOCK’，即可支持一个schema下，slave_parallel_workers个的worker线程并发执行relay log中主库提交的事务。其核心思想：一个组提交的事务都是可以并行回放（配合binary log group commit）
slave_preserve_commit_order = 1  
#  //mysql 5.7 后的MTS可以实现更小粒度的并行复制，但需要将slave_parallel_type设置为LOGICAL_CLOCK,但仅仅设置为LOGICAL_CLOCK也会存在问题，因为此时在slave上应用事务的顺序是无序的，和relay log中记录的事务顺序不一样，这样数据一致性是无法保证的，为了保证事务是按照relay log中记录的顺序来回放，就需要开启参数slave_preserve_commit_order
slave_transaction_retries = 128  
#  //如果SQL线程在执行事务时发生InnoDB死锁且等待超时后，slave重试的次数，默认为10，如果超过此次数，slave将会抛出error且终止replication；此值在“slave_parallel_workers”开启时无效，即为0，不重试。
# other change settings #
binlog_gtid_simple_recovery = 1  
#  //MySQL5.7.7之后默认on，这个参数控制了当mysql启动或重启时，mysql在搜寻GTIDs时是如何迭代使用binlog文件。该参数为真时，mysql-server只需打开最老的和最新的这2个binlog文件，gtid_purged参数的值和gtid_executed参数的值可以根据这些文件中的Previous_gtids_log_event或者Gtid_log_event计算得出。这确保了当mysql-server重启或清理binlog时，只需打开2个binlog文件。当这个参数设置为off，在mysql恢复期间，为了初始化gtid_executed，所有以最新文件开始的binlog都要被检查。并且为了初始化gtid_purged，所有的binlog都要被检查。这可能需要非常长的时间，建议开启。注意：MySQL5.6中，默认为off，调整这个选项设置也同样会提升性能，但是在一些特殊场景下，计算gtids值可能会出错。而保持这个选项值为off，能确保计算总是正确
log_timestamps = system   
# //该参数主要是控制 error log、genera log，等等记录日志的显示时间参数。在 5.7.2 之后改参数为默认 UTC 这样会导致日志中记录的时间比中国这边的慢，导致查看日志不方便。修改为 SYSTEM 就能解决问题
show_compatibility_56 = on  
#  //版本高的mysql中show_compatibility_56的默认值为OFF，不让用户访问GLOBAL_STATUS或者GLOBAL_VARIABLES等

# group replication settings
# plugin-load = "group_replication.so;validate_password.so;semisync_master.so;semisync_slave.so"
# transaction-write-set-extraction = XXHASH64    //server为每个事务收集write set并用XXHASH64哈唏算法编码这个set
# report_host = 127.0.0.1 # optional for group replication
# binlog_checksum = NONE # only for group replication
# loose_group_replication = FORCE_PLUS_PERMANENT
# loose_group_replication_group_name = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"    //表示plugin连接、创建的group的名称
# loose_group_replication_compression_threshold = 100    //将其设置为100表示对发送的网络消息（writeset）大于100字节的进行压缩，从而提升性能
# loose_group_replication_flow_control_mode = 0
# loose_group_replication_single_primary_mode = 0    //表示启动了Single-Primary模式，那么修改为OFF就意味着要启动Multi-Primary模式
# loose_group_replication_enforce_update_everywhere_checks = 1    //该参数设置为ON，则禁用了在多主模式下一些可能产生未知数据冲突的操作
# loose_group_replication_transaction_size_limit = 10485760
# loose_group_replication_unreachable_majority_timeout = 120
# loose_group_replication_start_on_boot = 0    //是否随着服务启动集群

[mysqld-8.0]
default_authentication_plugin = mysql_native_password
'''

