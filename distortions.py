
# distortions.py

import random
import numpy as np
from pydub import AudioSegment
import subprocess


def add_packet_loss(signal, loss_rate):
    # Convert signal to numpy array
    samples = np.array(signal.get_array_of_samples())
    # Calculate number of samples to set to zero based on the loss rate
    num_loss_samples = int(loss_rate * len(samples))
    # Choose random indices to set to zero
    loss_indices = np.random.choice(len(samples), size=num_loss_samples, replace=False)
    # Set loss samples to zero
    samples[loss_indices] = 0
    # Convert modified samples back to AudioSegment
    modified_signal = signal._spawn(samples.astype(np.int16))
    return modified_signal


def add_background_noise(signal, noise_path, noise_level):
    # Load the noise signal
    noise = AudioSegment.from_wav(noise_path)[:len(signal)]
    # Adjust the noise level relative to the signal
    noise = noise - noise.dBFS + noise_level
    # Overlay the noise on the signal
    signal_with_noise = signal.overlay(noise)
    return signal_with_noise


def add_white_noise(signal, noise_level):
    # Create silent white noise with the same duration as the signal
    noise = AudioSegment.silent(duration=len(signal))
    # Adjust the noise level relative to the signal
    noise = noise - noise.dBFS + noise_level
    # Overlay the white noise on the signal
    signal_with_noise = signal.overlay(noise)
    return signal_with_noise


def apply_lowpass_filter(signal, cutoff_freq):
    # Apply a low-pass filter to the signal
    filtered_signal = signal.low_pass_filter(cutoff_freq)
    return filtered_signal


def apply_clipping(signal, threshold):
    # Apply clipping to the signal by setting samples above the threshold to the maximum level
    signal = signal.max_dBFS - threshold
    return signal


def apply_codec(signal, codec):
    if codec == 'amrnb':
        # Apply AMR-NB codec
        temp_path = "temp.amr"
        output_path = "output.wav"
        signal.export(temp_path, format='amr', codec='amr_nb')
        subprocess.call(["ffmpeg", "-i", temp_path, output_path])
        processed_signal = AudioSegment.from_file(output_path, format="wav")

    elif codec == 'amrwb':
        # Apply AMR-WB codec
        temp_path = "temp.awb"
        output_path = "output.wav"
        signal.export(temp_path, format='amr', codec='amr_wb')
        subprocess.call(["ffmpeg", "-i", temp_path, output_path])
        processed_signal = AudioSegment.from_file(output_path, format="wav")

    elif codec == 'evs':
        # Apply EVS codec
        temp_path = "temp.evrc"
        output_path = "output.wav"
        signal.export(temp_path, format='evrc')
        subprocess.call(["ffmpeg", "-i", temp_path, output_path])
        processed_signal = AudioSegment.from_file(output_path, format="wav")

    elif codec == 'opus':
        # Apply Opus codec
        temp_path = "temp.opus"
        output_path = "output.wav"
        signal.export(temp_path, format='opus', codec='libopus')
        subprocess.call(["ffmpeg", "-i", temp_path, output_path])
        processed_signal = AudioSegment.from_file(output_path, format="wav")

    elif codec == 'g711':
        # Apply G.711 codec
        temp_path = "temp.g711a"
        output_path = "output.wav"
        signal.export(temp_path, format='g711', codec='pcm_u8')
        subprocess.call(["ffmpeg", "-i", temp_path, output_path])
        processed_signal = AudioSegment.from_file(output_path, format="wav")

    elif codec == 'g722':
        # Apply G.722 codec
        temp_path = "temp.g722"
        output_path = "output.wav"
        signal.export(temp_path, format='g722')
        subprocess.call(["ffmpeg", "-i", temp_path, output_path])
        processed_signal = AudioSegment.from_file(output_path, format="wav")

    else:
        # No codec specified or unsupported codec
        processed_signal = signal

    return processed_signal
