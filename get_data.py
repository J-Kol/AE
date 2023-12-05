# Jan Kolchuzhin
# 31.10.2023
# Wolfratshausen
# requires: SpotWave and the libaries

import time
import logging
from waveline import SpotWave
from waveline.spotwave import AERecord, TRRecord
from dataclasses import dataclass

def main():
    ports = SpotWave.discover()
    print(f"Discovered spotWave devices: {ports}")
    port = ports[0]

    # setup & start logging
    with SpotWave(port) as sw:
        print(sw.get_setup())
        sw.set_threshold(10e3)
        #sw.get_status
        #sw.set_datetime()
        sw.set_continuous_mode(False)
        #sw.set_cct(0)
        #sw.set_status_interval(0)
        sw.set_tr_enabled(False)
        sw.set_filter(highpass=500_000, lowpass=10_000, order=4)
        #sw.set_tr_decimation(1)  # 2 MHz
        #sw.set_ddt(10_000)  # 10 ms
        #sw.set_filter(None, None)  # deactivate IIR filter
        #sw.clear_data_log()
        #sw.set_logging_mode(True)
        #print(sw.get_status())
        sw.set_status_interval(1)
        sw.start_acquisition()
        print(sw.get_status())
        
        while True:
            time.sleep(5)
            records = sw.get_ae_data()
            print(f"{len(records)} new records")
            #sw.clear_data_log()
            #sw.stop_acquisition()
            #sw.set_logging_mode(True)
            #sw.start_acquisition()
            print(sw.get_status())
            with open("spotwave_records.txt","a") as f:
                for record in records:
                    print(f"Time: {record.time:.4f} s, Amplitude: {record.amplitude:.4f} V")
                    print(f"Time: {record.time:.4f} s, Amplitude: {record.amplitude:.4f} V", file=f)
                print("===================================", file=f)
                    

main()