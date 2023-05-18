
# dataset_generator.py

import os
import pandas as pd
from pydub import AudioSegment
from distortions import (
    add_packet_loss,
    add_background_noise,
    add_white_noise,
    apply_lowpass_filter,
    apply_clipping,
    apply_codec
)


def write_conditions_to_excel(output_dir, num_files, codecs, packet_loss_rates, background_noise_levels, white_noise_levels, filter_cutoff_freqs, clipping_thresholds):
    """
    Write the conditions for the dataset to an Excel file.

    Args:
        output_dir (str): Directory to save the conditions file.
        num_files (int): Number of files to generate conditions for.
        codecs (list): List of codec names.
        packet_loss_rates (list): List of packet loss rates.
        background_noise_levels (list): List of background noise levels.
        white_noise_levels (list): List of white noise levels.
        filter_cutoff_freqs (list): List of filter cutoff frequencies.
        clipping_thresholds (list): List of clipping thresholds.

    Returns:
        None
    """
    conditions = []

    # Generate conditions for each file, codec, and distortion type
    for i in range(num_files):
        for codec in codecs:
            for loss_rate in packet_loss_rates:
                conditions.append({'file': f"distorted_{i}_loss_{loss_rate}_{codec}.wav",
                                   'codec': codec,
                                   'packet_loss_rate': loss_rate})
            
            for noise_level in background_noise_levels:
                conditions.append({'file': f"distorted_{i}_loss_noise_{noise_level}_{codec}.wav",
                                   'codec': codec,
                                   'background_noise_level': noise_level})
            
            for noise_level in white_noise_levels:
                conditions.append({'file': f"distorted_{i}_white_noise_{noise_level}_{codec}.wav",
                                   'codec': codec,
                                   'white_noise_level': noise_level})
            
            for cutoff_freq in filter_cutoff_freqs:
                conditions.append({'file': f"distorted_{i}_filter_{cutoff_freq}_{codec}.wav",
                                   'codec': codec,
                                   'filter_cutoff_freq': cutoff_freq})
            
            for threshold in clipping_thresholds:
                conditions.append({'file': f"distorted_{i}_clipping_{threshold}_{codec}.wav",
                                   'codec': codec,
                                   'clipping_threshold': threshold})

    # Create a DataFrame from the conditions and save to Excel
    conditions_df = pd.DataFrame(conditions)
    conditions_df.to_excel(os.path.join(output_dir, 'conditions.xlsx'), index=False)
    print("done")


def generate_dataset(clean_path, noise_path, output_dir, num_files):
    """
    Generate a speech quality dataset with different distortions.

    Args:
        clean_path (str): Path to the clean speech signal.
        noise_path (str): Path to the noise file.
        output_dir (str): Directory to save the generated distorted files.
        num_files (int): Number of files to generate.

    Returns:
        None
    """
    # Define the list of codecs and distortion parameters
    codecs = ['codec1', 'codec2', 'codec3', 'codec4', 'codec5', 'codec6']
    packet_loss_rates = [0.1, 0.2, 0.3]  # Example packet loss rates
    background_noise_levels = [0.01, 0.1, 0.15]  # Example background noise levels
    white_noise_levels = [0.1, 0.2, 0.3]  # Example white noise levels
    filter_cutoff_freqs = [3000, 5000, 8000] # Example filter cutoff frequencies
    clipping_thresholds = [0.5, 1.0, 1.5] # Example clipping thresholds


    # Write the conditions to an Excel file
    write_conditions_to_excel(output_dir, num_files, codecs, packet_loss_rates, background_noise_levels, white_noise_levels, filter_cutoff_freqs, clipping_thresholds)

    # Generate distorted files for each condition
    for i in range(num_files):
        # Load the clean speech signal
        clean_signal = AudioSegment.from_file(clean_path, format="wav")

        # Apply different distortions for each codec
        for codec in codecs:
            # Apply the codec distortion
            distorted_signal = apply_codec(AudioSegment(data=clean_signal.raw_data, sample_width=clean_signal.sample_width, frame_rate=clean_signal.frame_rate, channels=clean_signal.channels), codec)

            # Apply packet loss distortion
            for loss_rate in packet_loss_rates:
                distorted_signal_with_loss = add_packet_loss(AudioSegment(data=distorted_signal.raw_data, sample_width=distorted_signal.sample_width, frame_rate=distorted_signal.frame_rate, channels=distorted_signal.channels), loss_rate)
                output_path = os.path.join(output_dir, f"distorted_{i}_loss_{loss_rate}_{codec}.wav")
                distorted_signal_with_loss.export(output_path, format="wav")

            # Apply background noise distortion
            for noise_level in background_noise_levels:
                noise = AudioSegment.from_wav(noise_path)[:len(distorted_signal)]
                noise = noise - noise.dBFS + noise_level
                distorted_signal_with_noise = distorted_signal.overlay(noise)
                output_path = os.path.join(output_dir, f"distorted_{i}_loss_noise_{noise_level}_{codec}.wav")
                distorted_signal_with_noise.export(output_path, format="wav")

            # Apply white noise distortion
            for noise_level in white_noise_levels:
                distorted_signal_with_noise = add_white_noise(AudioSegment(data=distorted_signal.raw_data, sample_width=distorted_signal.sample_width, frame_rate=distorted_signal.frame_rate, channels=distorted_signal.channels), noise_level)
                output_path = os.path.join(output_dir, f"distorted_{i}_white_noise_{noise_level}_{codec}.wav")
                distorted_signal_with_noise.export(output_path, format="wav")

            # Apply lowpass filter distortion
            for cutoff_freq in filter_cutoff_freqs:
                filtered_signal = apply_lowpass_filter(AudioSegment(data=distorted_signal.raw_data, sample_width=distorted_signal.sample_width, frame_rate=distorted_signal.frame_rate, channels=distorted_signal.channels), cutoff_freq)
                output_path = os.path.join(output_dir, f"distorted_{i}_filter_{cutoff_freq}_{codec}.wav")
                filtered_signal.export(output_path, format="wav")

            # Apply clipping distortion
            for threshold in clipping_thresholds:
                clipping_signal = apply_clipping(AudioSegment(data=distorted_signal.raw_data, sample_width=distorted_signal.sample_width, frame_rate=distorted_signal.frame_rate, channels=distorted_signal.channels), threshold)
                output_path = os.path.join(output_dir, f"distorted_{i}_clipping_{threshold}_{codec}.wav")
                clipping_signal.export(output_path, format="wav")

