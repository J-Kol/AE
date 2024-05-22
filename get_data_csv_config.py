import tomli
from pathlib import Path
import time
from waveline import SpotWave

csv_file = Path("records.csv")

def main():
    with open('config.toml', mode="rb") as f:
        config = tomli.load(f)
    ports = SpotWave.discover()
    print(f"Discovered spotWave devices: {ports}")
    port = ports[0]

    # setup & start logging using toml config
    with SpotWave(port) as sw:
        highpass_ = config["acq"]["filter"]["highpass"]
        lowpass_ = config["acq"]["filter"]["lowpass"]
        order_ = config["acq"]["filter"]["order"]
        sw.set_filter(highpass=highpass_, lowpass=lowpass_, order=order_)
        #print(sw.get_setup())
        sw.set_threshold(config["acq"]["threshold"])
        sw.set_ddt(config["acq"]["ddt"])
        #sw.set_filter(highpass=["acq"]["filter"]{highpass})
        sw.set_status_interval(config["acq"]["status_interval"])

        sw.set_continuous_mode(config["acq"]["continuous_mode"])
        sw.set_tr_enabled(config["acq"]["tr_enabled"])
        sw.set_tr_decimation(config["acq"]["set_tr_decimation"])
        sw.set_tr_enabled(config["acq"]["set_tr_enabled"])
        sw.set_tr_postduration(config["acq"]["set_tr_postduration"])
        sw.set_tr_pretrigger(config["acq"]["set_tr_pretrigger"])
        #print(config["acq"])
        sw.start_acquisition()
        #print(sw.get_status())

        #writes a Headzeile and overwrites an existing "records.csv"
        with open(csv_file, "w") as f:
            print("Time[s], Amplitude[v]", file=f)

        print("Start Recording")

        while True:
            time.sleep(config["acq"]["sleep_time"])
            records = sw.get_ae_data()
            print(f"{len(records)} new records")

            with open(csv_file, "a") as f:
                for record in records:
                    #formatted_time = format(record.time, '.2f')  # Adjust the number of decimal places as needed
                    print(f"{record.time} , {record.amplitude}", file=f)
                #print("===================================", file=f)
main()