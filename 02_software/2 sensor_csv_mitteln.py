import tomli
from pathlib import Path
import time
from waveline import SpotWave
import numpy as np

#csv_file = Path("records.csv")
HERE = Path(__file__).parent
CSV_DIR = HERE / "csv_data_2"
CSV_DIR.mkdir(exist_ok=True)

def main():
    with open(HERE / "config.toml", mode="rb") as f:
        config = tomli.load(f)
    ports = SpotWave.discover()
    print(f"Discovered spotWave devices: {ports}")
    port = ports[0]
    print(port)

    # setup & start logging using toml config
    with SpotWave(port) as sw:
        #sw.identify()
        highpass_ = config["acq"]["filter"]["highpass"]
        lowpass_ = config["acq"]["filter"]["lowpass"]
        order_ = config["acq"]["filter"]["order"]
        sw.set_filter(highpass=highpass_, lowpass=lowpass_, order=order_)
        sw.set_tr_decimation(1)
        sw.set_cct(-1)

        #print("Start Recording")
        samples = 1000
        a = 0
        averages = 100
        #print(sw.get_setup())
        while True:
            values_matrix = np.empty((samples, averages))
            for i in range(averages):
                record = sw.get_tr_snapshot(samples)
                values_matrix[:, i] = record.data
                time.sleep(0.01)                

            values_avg = np.mean(values_matrix, axis=1)
            print(values_avg.shape)

            times = np.arange(samples) / sw.CLOCK
            csv_data = np.stack((times, values_avg)).T
            np.savetxt(CSV_DIR / f"waveform_{a}.csv", csv_data, delimiter=",", header="Time[s], Amplitude[v]")

            time.sleep(0.1)
            a += 1
main()