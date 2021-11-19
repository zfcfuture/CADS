#! /bin/bash
rm -rf ~/debugTool/snapshot/REF/*
rm -rf ~/debugTool/snapshot/DUT/*
rm -rf ~/debugTool/health/REF/*
rm -rf ~/debugTool/health/REF/*
rm -rf ~/debugTool/healthReport/*

touch ~/debugTool/snapshot/REF/regsnapshot_gem5.txt
touch ~/debugTool/snapshot/DUT/regsnapshot_haps.txt
touch ~/debugTool/snapshot/REF/memsnapshot_hexdump_gem5.txt
touch ~/debugTool/snapshot/DUT/memsnapshot_hexdump_haps.txt
touch ~/debugTool/health/REF/cpu_status_gem5.txt
touch ~/debugTool/health/DUT/cpu_status_haps.txt
touch ~/debugTool/healthReport/cpu_status_cmp_result.txt
