# Highly Performant I/O 
##  PyYYC Presentation - May 27, 2020

* `examples` directory contains code discussed in the slides.
* `echo_benchmark` directory contains similar code to the `examples` directory but modified as a simple/stupid echo server for benchmarking.


## Echo Benchmark
Run on a VM using Python 3.6.9 from 18.04.1 Ubuntu.

Load test run with [JMeter](https://jmeter.apache.org/) `JVM_ARGS="-Xms1024m -Xmx1024m -Dpropname=value" apache-jmeter-5.3/bin/jmeter -n -t Test\ TCP.jmx -l out.log`. I used 2 test plans:
1. 1000 threads each with a 2000 loop count on a 1 second ramp up period.
2. 100 threads each with a 20000 loop count on a 1 second ramp up period.

Are there better ways of doing this? Sure. Do I care for this purpose? Nope.

Rough CPU and memory use measured via `top`.


| Plan | Async/Await (Stream) | Async/Await (Protocol CB) | Sync Blocking | Sync Non-Blocking |
|------|----------------------|---------------------------|---------------|-------------------|
| 1    |  33307 in 00:00:10 = 3382.1/s Avg | 200000 in 00:00:27 = 7330.0/s Avg | 13223 in 00:00:08 = 1595.1/s Avg | 176183 in 00:00:20 = 8694.0/s Avg |
| 2    |  2000000 in 00:04:52 = 6846.1/s Avg | 2000000 in 00:03:30 = 9507.0/s Avg |  2000000 in 00:07:03 = 4724.9/s Avg | 2000000 in 00:02:36 = 12785.1/s Avg |


### Async Streamer Echo

#### Plan 1

~84% CPU 71MB Virtual 29MB Res & Shr

```
summary =  33307 in 00:00:10 = 3382.1/s Avg:   371 Min:     0 Max:  7271 Err:   846 (2.54%)
```

#### Plan 2

~88% to 94% CPU 68MB Virtual 27MB Res & Shr

```
summary + 150254 in 00:00:23 = 6614.5/s Avg:    14 Min:     0 Max:    45 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary + 206538 in 00:00:30 = 6885.3/s Avg:    14 Min:     1 Max:    32 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 356792 in 00:00:53 = 6768.6/s Avg:    14 Min:     0 Max:    45 Err:     0 (0.00%)
summary + 210303 in 00:00:30 = 7009.9/s Avg:    14 Min:     8 Max:    38 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 567095 in 00:01:23 = 6856.1/s Avg:    14 Min:     0 Max:    45 Err:     0 (0.00%)
summary + 208233 in 00:00:30 = 6940.2/s Avg:    14 Min:     7 Max:    34 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 775328 in 00:01:53 = 6878.5/s Avg:    14 Min:     0 Max:    45 Err:     0 (0.00%)
summary + 208752 in 00:00:30 = 6959.6/s Avg:    14 Min:     7 Max:    26 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 984080 in 00:02:23 = 6895.5/s Avg:    14 Min:     0 Max:    45 Err:     0 (0.00%)
summary + 204180 in 00:00:30 = 6806.0/s Avg:    14 Min:    10 Max:    35 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1188260 in 00:02:53 = 6880.0/s Avg:    14 Min:     0 Max:    45 Err:     0 (0.00%)
summary + 208306 in 00:00:30 = 6942.8/s Avg:    14 Min:    11 Max:    31 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1396566 in 00:03:23 = 6889.3/s Avg:    14 Min:     0 Max:    45 Err:     0 (0.00%)
summary + 198229 in 00:00:30 = 6608.3/s Avg:    15 Min:    11 Max:    36 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1594795 in 00:03:53 = 6853.1/s Avg:    14 Min:     0 Max:    45 Err:     0 (0.00%)
summary + 207265 in 00:00:30 = 6908.8/s Avg:    14 Min:    10 Max:    27 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1802060 in 00:04:23 = 6859.4/s Avg:    14 Min:     0 Max:    45 Err:     0 (0.00%)
summary + 197940 in 00:00:29 = 6726.9/s Avg:    14 Min:     0 Max:    30 Err:     0 (0.00%) Active: 0 Started: 100 Finished: 100
summary = 2000000 in 00:04:52 = 6846.1/s Avg:    14 Min:     0 Max:    45 Err:     0 (0.00%)
```

### Async Protocol/Callback Echo

#### Plan 1

81-89% CPU  70MB Virt 27MB Res + Shr

```
summary +     47 in 00:00:00 =  419.6/s Avg:    12 Min:     0 Max:    34 Err:     0 (0.00%) Active: 31 Started: 31 Finished: 0
summary + 199953 in 00:00:27 = 7358.5/s Avg:   109 Min:     0 Max:  7389 Err:     0 (0.00%) Active: 0 Started: 1000 Finished: 1000
summary = 200000 in 00:00:27 = 7330.0/s Avg:   109 Min:     0 Max:  7389 Err:     0 (0.00%)
```

#### Plan 2

~ 80-87% CPU  70MB Virtl 27MB Res + Shr

```
summary + 129099 in 00:00:15 = 8590.6/s Avg:    11 Min:     0 Max:    35 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary + 280818 in 00:00:30 = 9362.8/s Avg:    10 Min:     4 Max:    25 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 409917 in 00:00:45 = 9105.0/s Avg:    10 Min:     0 Max:    35 Err:     0 (0.00%)
summary + 284573 in 00:00:30 = 9485.1/s Avg:    10 Min:     0 Max:    28 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 694490 in 00:01:15 = 9257.0/s Avg:    10 Min:     0 Max:    35 Err:     0 (0.00%)
summary + 284658 in 00:00:30 = 9488.6/s Avg:    10 Min:     0 Max:    24 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 979148 in 00:01:45 = 9323.2/s Avg:    10 Min:     0 Max:    35 Err:     0 (0.00%)
summary + 295621 in 00:00:30 = 9853.7/s Avg:    10 Min:     1 Max:    36 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1274769 in 00:02:15 = 9441.1/s Avg:    10 Min:     0 Max:    36 Err:     0 (0.00%)
summary + 284285 in 00:00:30 = 9477.1/s Avg:    10 Min:     1 Max:    20 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1559054 in 00:02:45 = 9447.6/s Avg:    10 Min:     0 Max:    36 Err:     0 (0.00%)
summary + 287290 in 00:00:30 = 9576.0/s Avg:    10 Min:     0 Max:    23 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1846344 in 00:03:15 = 9467.4/s Avg:    10 Min:     0 Max:    36 Err:     0 (0.00%)
summary + 153656 in 00:00:15 = 10010.8/s Avg:     9 Min:     0 Max:    25 Err:     0 (0.00%) Active: 0 Started: 100 Finished: 100
summary = 2000000 in 00:03:30 = 9507.0/s Avg:    10 Min:     0 Max:    36 Err:     0 (0.00%)
```

### Sync Blocking Mutithreaded Echo

#### Plan 1

~40% CPU 2GB Virtual 22MB Res + Shr

```
summary +  11958 in 00:00:04 = 2776.4/s Avg:   506 Min:     0 Max:  3895 Err:    19 (0.16%) Active: 1266 Started: 4050 Finished: 2784
summary +   1265 in 00:00:04 =  317.6/s Avg:  3741 Min:  2896 Max:  7318 Err:     0 (0.00%) Active: 0 Started: 4050 Finished: 4050
summary =  13223 in 00:00:08 = 1595.1/s Avg:   815 Min:     0 Max:  7318 Err:    19 (0.14%)
```

#### Plan 2

~ 107 - 114% CPU  1.6GB Virtual with 16MB Res + Shr

```
summary +  23922 in 00:00:06 = 3779.1/s Avg:    24 Min:     0 Max:    69 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary + 144154 in 00:00:30 = 4805.1/s Avg:    20 Min:    14 Max:    78 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 168076 in 00:00:36 = 4626.4/s Avg:    21 Min:     0 Max:    78 Err:     0 (0.00%)
summary + 138682 in 00:00:30 = 4622.7/s Avg:    21 Min:    16 Max:   107 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 306758 in 00:01:06 = 4624.7/s Avg:    21 Min:     0 Max:   107 Err:     0 (0.00%)
summary + 138202 in 00:00:30 = 4606.3/s Avg:    21 Min:    15 Max:    86 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 444960 in 00:01:36 = 4619.0/s Avg:    21 Min:     0 Max:   107 Err:     0 (0.00%)
summary + 141127 in 00:00:30 = 4704.7/s Avg:    21 Min:    17 Max:    93 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 586087 in 00:02:06 = 4639.3/s Avg:    21 Min:     0 Max:   107 Err:     0 (0.00%)
summary + 137711 in 00:00:30 = 4589.9/s Avg:    21 Min:    16 Max:    87 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 723798 in 00:02:36 = 4629.8/s Avg:    21 Min:     0 Max:   107 Err:     0 (0.00%)
summary + 145363 in 00:00:30 = 4845.9/s Avg:    20 Min:    14 Max:    90 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 869161 in 00:03:06 = 4664.6/s Avg:    21 Min:     0 Max:   107 Err:     0 (0.00%)
summary + 140551 in 00:00:30 = 4684.6/s Avg:    21 Min:    13 Max:   134 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1009712 in 00:03:36 = 4667.4/s Avg:    21 Min:     0 Max:   134 Err:     0 (0.00%)
summary + 140592 in 00:00:30 = 4686.9/s Avg:    21 Min:    14 Max:    85 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1150304 in 00:04:06 = 4669.8/s Avg:    21 Min:     0 Max:   134 Err:     0 (0.00%)
summary + 140986 in 00:00:30 = 4699.5/s Avg:    21 Min:    16 Max:    79 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1291290 in 00:04:36 = 4673.0/s Avg:    21 Min:     0 Max:   134 Err:     0 (0.00%)
summary + 142580 in 00:00:30 = 4752.7/s Avg:    21 Min:    16 Max:    77 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1433870 in 00:05:06 = 4680.8/s Avg:    21 Min:     0 Max:   134 Err:     0 (0.00%)
summary + 149902 in 00:00:30 = 4996.2/s Avg:    19 Min:    14 Max:    75 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1583772 in 00:05:36 = 4708.9/s Avg:    21 Min:     0 Max:   134 Err:     0 (0.00%)
summary + 144108 in 00:00:30 = 4804.1/s Avg:    20 Min:    14 Max:    66 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1727880 in 00:06:06 = 4716.7/s Avg:    21 Min:     0 Max:   134 Err:     0 (0.00%)
summary + 147708 in 00:00:30 = 4923.6/s Avg:    20 Min:    14 Max:    66 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1875588 in 00:06:36 = 4732.4/s Avg:    21 Min:     0 Max:   134 Err:     0 (0.00%)
summary + 124412 in 00:00:27 = 4614.5/s Avg:    21 Min:     1 Max:    75 Err:     0 (0.00%) Active: 0 Started: 100 Finished: 100
summary = 2000000 in 00:07:03 = 4724.9/s Avg:    21 Min:     0 Max:   134 Err:     0 (0.00%)
```

### Sync Non-Blocking Echo

#### Plan 1

~ 87 - 94% CPU  37MB Virtual 15MB Res & Shr

```
summary +    857 in 00:00:00 = 3825.9/s Avg:     9 Min:     0 Max:    35 Err:     0 (0.00%) Active: 104 Started: 104 Finished: 0
summary + 175326 in 00:00:20 = 8748.4/s Avg:   167 Min:     0 Max: 16401 Err:   157 (0.09%) Active: 0 Started: 4129 Finished: 4129
summary = 176183 in 00:00:20 = 8694.0/s Avg:   166 Min:     0 Max: 16401 Err:   157 (0.09%)
```

#### Plan 2

~ 73 - 82% CPU  37MB Virtual  15MB Res & Shr

```
summary +      1 in 00:00:00 =   23.8/s Avg:     1 Min:     1 Max:     1 Err:     0 (0.00%) Active: 2 Started: 2 Finished: 0
summary + 338936 in 00:00:28 = 12296.3/s Avg:     7 Min:     0 Max:   120 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 338937 in 00:00:28 = 12277.7/s Avg:     7 Min:     0 Max:   120 Err:     0 (0.00%)
summary + 388696 in 00:00:30 = 12956.5/s Avg:     7 Min:     1 Max:    22 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 727633 in 00:00:58 = 12631.2/s Avg:     7 Min:     0 Max:   120 Err:     0 (0.00%)
summary + 392275 in 00:00:30 = 13075.8/s Avg:     7 Min:     0 Max:    31 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1119908 in 00:01:28 = 12783.5/s Avg:     7 Min:     0 Max:   120 Err:     0 (0.00%)
summary + 386697 in 00:00:30 = 12889.9/s Avg:     7 Min:     0 Max:    24 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1506605 in 00:01:58 = 12810.6/s Avg:     7 Min:     0 Max:   120 Err:     0 (0.00%)
summary + 378369 in 00:00:30 = 12612.3/s Avg:     7 Min:     2 Max:    39 Err:     0 (0.00%) Active: 100 Started: 100 Finished: 0
summary = 1884974 in 00:02:28 = 12770.3/s Avg:     7 Min:     0 Max:   120 Err:     0 (0.00%)
summary + 115026 in 00:00:09 = 13034.1/s Avg:     7 Min:     0 Max:    28 Err:     0 (0.00%) Active: 0 Started: 100 Finished: 100
summary = 2000000 in 00:02:36 = 12785.1/s Avg:     7 Min:     0 Max:   120 Err:     0 (0.00%)
```