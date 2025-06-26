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
        summary[";".join([meta["title"], meta["name"]])] = process_plot_data(data, meta)

    # edit the hugo content files
    edit_content_file(summary)


def edit_content_file(summary: dict):
    """
    Edits the Hugo content files to include the summary of processed data.

    Parameters:
        summary (dict): A dictionary containing the summary of processed data.
    """

    pass


def process_plot_data(data: dict, meta: dict) -> dict:
    """
    Processes and creates a plot from the data and metadata.

    Parameters:
        data (dict): The data dictionary containing the JSON results.
        meta (dict): The metadata dictionary.

    Returns:
        dict: A summary dictionary containing peak values, frequencies, and plot location.
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
                                              np.array(data[node]["VELOCITY_Y"]))
    signal.fft(half_representation=True)
    signal.v_eff_SBR()

    fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(15, 4))
    ax[0].plot(data["TIME"], np.array(data[node]["VELOCITY_Y"])*1000, label=r"v$_{y}$", color="blue")
    ax[1].plot(data["TIME"], signal.v_eff, label=r"v$_{eff}$", color="orange")
    ax[2].plot(signal.frequency, signal.amplitude*1000, label=r"v$_{y}$", color="blue")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Velocity Y (mm/s)")
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("V_eff (mm/s)")
    ax[2].set_xlabel("Frequency (Hz)")
    ax[2].set_ylabel("FFT Magnitude (mm/s/s)")
    ax[0].set_xlim(left=0)
    ax[1].set_xlim(left=0)
    ax[2].set_xlim(0, 100)
    ax[1].set_ylim(bottom=0)
    ax[2].set_ylim(bottom=0)
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    ax[0].legend()
    ax[1].legend()
    ax[2].legend()
    plt.savefig(os.path.join(output_folder, f"{meta['title']}.png"))
    plt.close()

    # create the summary
    summary = {"peak_velocity_y": np.max(np.abs(np.array(data[node]["VELOCITY_Y"])*1000)),
               "peak_v_eff": np.max(signal.v_eff),
               "peak_fft": np.max(signal.amplitude)*1000,
               "freq_peak_fft": signal.frequency[np.argmax(signal.amplitude)],
               "plot_location": os.path.join(output_folder, f"{meta['title']}.png")}
    return summary


if __name__ == "__main__":
    main("./data")