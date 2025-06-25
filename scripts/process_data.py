import os
import json
import yaml
import numpy as np
import matplotlib.pyplot as plt
import SignalProcessingTools.time_signal as time_signal

from validators import json_validator, yaml_validator


COORD_REF = [0.75, 7.1, 30]
TOL = 1e-6


def main(folder_path: str):
    """
    Main function to process YAML and JSON files in the specified folder.
    It validates the YAML files, checks the corresponding JSON files,
    and generates plots based on the data.

    Parameters:
        folder_path (str): Path to the folder containing YAML files.
    """
    yaml_files = os.listdir(folder_path)
    yaml_files = [os.path.join(folder_path, file) for file in yaml_files if file.endswith('.yaml')]

    summary = {}

    for yaml_file in yaml_files:
        # validate YAML file
        if not yaml_validator(yaml_file):
            print(f"Validation failed for YAML file: {yaml_file}")
            raise ValueError(f"Invalid YAML file: {yaml_file}")

        with open(yaml_file, 'r') as f:
            meta = yaml.safe_load(f)

        # validate JSON files
        if not json_validator(os.path.join("data", meta["json-file"])):
            print(f"Validation failed for JSON file: {meta['json-file']}")
            raise ValueError(f"Invalid JSON file: {meta['json-file']}")

        with open(os.path.join("data", meta["json-file"]), "r") as f:
            data = json.load(f)

        # Plotting the data
        summary[";".join([meta["title"], meta["name"]])] = make_plot(data, meta)

    # edit the hugo content files
    edit_content_file(summary)


def edit_content_file(summary: dict):
    pass


def make_plot(data: dict, meta: dict) -> dict:
    """
    Create a plot from the data and metadata.

    Parameters:
        data (dict): The data dictionary containing the JSON results.
        meta (dict): The metadata dictionary.

    Returns:
        dict: A summary dictionary containing peak values and frequencies.
    """

    output_folder = "static/images"
    os.makedirs(output_folder, exist_ok=True)

    # define the node
    node = None
    for key in data.keys():
        if key.startswith("NODE_"):
            if np.linalg.norm(np.array(data[key]["COORDINATES"]) - np.array(COORD_REF)) < TOL:
                node = key

    if node is None:
        raise ValueError("The reference node was not found. Please use the reference mesh.")

    # process the time signal
    signal = time_signal.TimeSignalProcessing(data["TIME"],
                                              np.array(data[node]["VELOCITY_Y"])*1000)
    signal.fft()

    fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(10, 4))
    ax[0].plot(data["TIME"], np.array(data[node]["VELOCITY_Y"])*1000, label="VELOCITY Y", color="blue")
    ax[1].plot(signal.frequency, signal.amplitude, label="FFT Magnitude", color="blue")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Velocity Y (mm/s)")
    ax[1].set_xlabel("Frequency (Hz)")
    ax[1].set_ylabel("FFT Magnitude (mm/s/s)")
    ax[0].set_xlim(left=0)
    ax[1].set_xlim(0, 100)
    ax[1].set_ylim(bottom=0)
    ax[0].grid()
    ax[1].grid()
    ax[0].legend()
    ax[1].legend()
    plt.savefig(os.path.join(output_folder, f"{meta['title']}.png"))
    plt.close()

    # create the summary
    summary = {"peak_velocity_y": np.max(np.abs(np.array(data[node]["VELOCITY_Y"])*1000)),
               "peak_fft": np.max(signal.amplitude),
               "freq_peak_fft": signal.frequency[np.argmax(signal.amplitude)]}
    return summary


if __name__ == "__main__":
    main("./data")